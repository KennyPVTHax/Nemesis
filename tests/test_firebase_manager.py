import concurrent.futures,hashlib,json,os,sqlite3,time
from pathlib import Path
from types import SimpleNamespace
import pytest,httpx
from test_backend import db
import account_store,firebase_pool as pool,firebase_config as cfg
import firebase_manager_store as store
import firebase_jobs as jobs
from firebase_cloud import GoogleFirebase,CloudError
from firebase_telegram import Manager,handle
from firebase_migration import migrate

@pytest.fixture
def env(db,monkeypatch):
    with account_store.connect() as c:c.execute("UPDATE users SET login_id='NemesisOwner' WHERE id=1")
    monkeypatch.setenv('NEMESIS_FIREBASE_MANAGER_ENABLED','1')
    policy={'bindings':[{'role':'projects/nemesis-isolated/roles/nemesisFirebaseManager','members':['serviceAccount:manager@nemesis-isolated.iam.gserviceaccount.com']}]}
    p={'runtime_service_account':'manager@nemesis-isolated.iam.gserviceaccount.com','project_id':'nemesis-isolated','project_number':'1234567890','region':'us-central1','max_instances':100,'create_enabled':True,'billing_acknowledged':True,'iam_reviewed_until':int(time.time())+86400,'iam_policy_sha256':hashlib.sha256(json.dumps(policy,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
    monkeypatch.setattr(cfg,'profiles',lambda:{'isolated':p})
    return p

def verified(label='DB_ONE',url='https://isolated-one.firebaseio.com'):
    with store.transaction() as c:
        c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',(label,url,'alias:isolated',int(time.time())))
        i=c.execute('SELECT last_insert_rowid()').fetchone()[0]
        _,dbid,region=cfg.identity(url)
        c.execute("INSERT INTO firebase_manager_instances VALUES(?,?,?,'AVAILABLE',?,NULL,'test-hash')",(i,'isolated',f'projects/1234567890/locations/{region}/instances/{dbid}',int(time.time())))
        return i

class Cloud:
    remote={};creates=0;fail=False;timeout_after_create=False
    def __init__(self,p):self.p=p
    def preflight(self,creating=False):
        if self.fail:raise CloudError('synthetic_cloud_failure')
    def get(self,r):return self.remote.get(r)
    def create(self,r,known_resources=()):
        type(self).creates+=1
        obj={'name':r,'state':'ACTIVE','databaseUrl':'https://'+r.split('/')[-1]+'.firebaseio.com'};self.remote[r]=obj
        if self.timeout_after_create:type(self).timeout_after_create=False;raise CloudError('cloud_timeout',True)
        return obj
    def validate(self,url,apply_rules=False,require_empty=False):
        u,d,r=cfg.identity(url)
        return {'url':u,'resource':f'projects/{self.p["project_number"]}/locations/{r}/instances/{d}','region':r,'rules_hash':'test-hash'}
    def close(self):pass

@pytest.fixture(autouse=True)
def reset_cloud():Cloud.remote={};Cloud.creates=0;Cloud.fail=False;Cloud.timeout_after_create=False

@pytest.mark.parametrize('url',['http://abc.firebaseio.com','https://abc.firebaseio.com.evil.invalid','https://user:pass@abc.firebaseio.com','https://abc.firebaseio.com:443','https://abc.firebaseio.com/x','https://abc.firebaseio.com?auth=bad','https://abc.unknown.firebasedatabase.app','https://127.0.0.1','https://abc.firebaseio.com#fragment'])
def test_invalid_urls(env,url):
    with pytest.raises(cfg.ManagerError):cfg.identity(url)

@pytest.mark.parametrize('url,region',[('https://database-one.firebaseio.com/','us-central1'),('https://database-one.europe-west1.firebasedatabase.app','europe-west1'),('https://database-one.asia-southeast1.firebasedatabase.app','asia-southeast1')])
def test_supported_urls(env,url,region):assert cfg.identity(url)[2]==region

def test_migration_retains_existing_assignment_and_is_idempotent(env):
    with account_store.connect() as c:
        c.execute('DROP TRIGGER firebase_assignment_insert')
        c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,assigned_user_id,added_at) VALUES(?,?,?,?,?)',('OLD_DB','https://old-database.firebaseio.com','/private/path',2,1))
    migrate();migrate()
    with account_store.connect() as c:
        assert c.execute("SELECT assigned_user_id FROM firebase_instances WHERE label='OLD_DB'").fetchone()[0]==2
        assert c.execute('SELECT COUNT(*) FROM firebase_assignment_ledger WHERE user_id=2').fetchone()[0]==1
        assert c.execute("SELECT state FROM firebase_manager_instances").fetchone()[0]=='VALIDATING'
    assert pool.approved_url(2) is None

def test_callback_private_owner_binding_replay_and_expiry(env):
    token=store.action(10001,'confirm',{'op':'disable','label':'test'})
    store.bind(10001,9,[token])
    with pytest.raises(cfg.ManagerError):store.consume(10002,9,token)
    with pytest.raises(cfg.ManagerError):store.consume(10001,10,token)
    assert store.consume(10001,9,token)[0]=='confirm'
    with pytest.raises(cfg.ManagerError):store.consume(10001,9,token)
    token=store.action(10001,'menu',{});store.bind(10001,9,[token])
    with account_store.connect() as c:c.execute('UPDATE firebase_manager_actions SET expires_at=0')
    with pytest.raises(cfg.ManagerError):store.consume(10001,9,token)

def test_concurrent_callback_single_consumer_and_owner_revocation(env):
    token=store.action(10001,'menu',{});store.bind(10001,9,[token])
    def call(_):
        try:store.consume(10001,9,token);return True
        except cfg.ManagerError:return False
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:assert sum(executor.map(call,range(8)))==1
    token=store.action(10001,'menu',{});store.bind(10001,10,[token])
    with account_store.connect() as c:c.execute('UPDATE users SET is_active=0 WHERE id=1')
    with pytest.raises(cfg.ManagerError):store.consume(10001,10,token)

def test_registration_validation_then_explicit_confirmation(env):
    job=jobs.enqueue_job(10001,'inspect','REGISTERED','isolated','https://registered-test.firebaseio.com')
    assert jobs.tick(Cloud)
    with account_store.connect() as c:assert c.execute('SELECT COUNT(*) FROM firebase_instances').fetchone()[0]==0
    iid=jobs.register(10001,job)
    with account_store.connect() as c:assert c.execute('SELECT state FROM firebase_manager_instances WHERE instance_id=?',(iid,)).fetchone()[0]=='AVAILABLE'
    with pytest.raises((cfg.ManagerError,sqlite3.IntegrityError)):jobs.register(10001,job)
    with pytest.raises(cfg.ManagerError):jobs.enqueue_job(10001,'inspect','OTHER','isolated','https://registered-test.firebaseio.com/')

def test_registration_rejects_profile_change_between_validation_and_confirmation(env):
    jid=jobs.enqueue_job(10001,'inspect','CHANGED','isolated','https://registered-test.firebaseio.com');jobs.tick(Cloud)
    env['project_number']='9999999999'
    with pytest.raises(cfg.ManagerError):jobs.register(10001,jid)

def test_create_is_persisted_retry_safe_and_does_not_duplicate(env):
    Cloud.timeout_after_create=True
    jid=jobs.enqueue_job(10001,'create','CREATED','isolated')
    jobs.tick(Cloud)
    with account_store.connect() as c:
        assert c.execute('SELECT state FROM firebase_manager_jobs').fetchone()[0]=='RETRY'
        c.execute('UPDATE firebase_manager_jobs SET next_at=0')
    jobs.tick(Cloud)
    assert Cloud.creates==1
    assert jobs.enqueue_job(10001,'create','CREATED','isolated')==jid
    with account_store.connect() as c:
        assert c.execute('SELECT COUNT(*) FROM firebase_instances').fetchone()[0]==1
        assert c.execute('SELECT state FROM firebase_manager_jobs').fetchone()[0]=='DONE'

def test_provision_failure_does_not_register_or_allocate(env):
    Cloud.fail=True;jobs.enqueue_job(10001,'create','FAIL_DB','isolated');jobs.tick(Cloud)
    assert pool.get_or_assign(2) is None
    with account_store.connect() as c:assert c.execute('SELECT state FROM firebase_manager_jobs').fetchone()[0]=='ERROR'

def test_creation_flag_is_fail_closed(env):
    env['create_enabled']=False
    with pytest.raises(cfg.ManagerError):jobs.enqueue_job(10001,'create','BLOCKED','isolated')

def test_allocations_are_dedicated_concurrent_and_permanent(env):
    one=verified();two=verified('DB_TWO','https://isolated-two.firebaseio.com')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:result=list(executor.map(lambda _:pool.get_or_assign(2),range(8)))
    assert all(r[0]==one for r in result)
    assert pool.get_or_assign(3)[0]==two
    with account_store.connect() as c:
        assert c.execute('SELECT COUNT(*) FROM firebase_assignment_ledger').fetchone()[0]==2
        with pytest.raises(sqlite3.IntegrityError):c.execute('UPDATE firebase_instances SET assigned_user_id=NULL WHERE id=?',(one,))
    with pytest.raises(cfg.ManagerError):store.manual_assign(10001,'DB_TWO','SyntheticCustomer')

def test_expiry_renewal_and_disable_do_not_release_assignment(env):
    iid=verified();pool.get_or_assign(2)
    with account_store.connect() as c:c.execute('UPDATE users SET expires_at=0 WHERE id=2')
    assert pool.get_or_assign(2) is None
    with account_store.connect() as c:c.execute('UPDATE users SET expires_at=? WHERE id=2',(int(time.time())+86400,))
    assert pool.get_or_assign(2)[0]==iid
    store.disable(10001,'DB_ONE');assert pool.get_or_assign(3) is None
    with account_store.connect() as c:assert c.execute('SELECT assigned_user_id FROM firebase_instances WHERE id=?',(iid,)).fetchone()[0]==2

def test_approval_revision_denial_and_customer_isolation(env):
    verified();pool.get_or_assign(2)
    assert pool.request_link(2)=='pending';assert pool.request_link(2)=='pending'
    assert pool.approved_url(2) is None
    with account_store.connect() as c:rev=c.execute('SELECT revision FROM firebase_manager_request_versions WHERE user_id=2').fetchone()[0]
    with pytest.raises(cfg.ManagerError):store.decision(10002,2,rev,True)
    store.decision(10001,2,rev,False);assert pool.approved_url(2) is None
    pool.request_link(2)
    with pytest.raises(cfg.ManagerError):store.decision(10001,2,rev,True)
    store.decision(10001,2,rev+1,True)
    assert pool.approved_url(2)=='https://isolated-one.firebaseio.com'
    assert pool.approved_url(3) is None
    store.disable(10001,'DB_ONE');assert pool.approved_url(2) is None

def test_unauthorized_forwarded_and_tampered_telegram_actions(env):
    sent=[];answers=[]
    def send(chat,text,keyboard):sent.append((chat,text,keyboard));return {'message_id':len(sent)}
    manager=Manager(send)
    def update(uid,text,**extra):return {'update_id':uid,'message':{'message_id':uid,'chat':{'id':uid,'type':'private'},'from':{'id':uid},'text':text,**extra}}
    handle(update(10002,'/firebase'),'NemesisAuthBot',manager,lambda *a:answers.append(a))
    assert not any('Total ' in x[1] for x in sent)
    handle(update(10001,'/firebase',forward_origin={'type':'user'}),'NemesisAuthBot',manager,lambda *a:None)
    assert not any('Total ' in x[1] for x in sent)
    handle(update(10001,'/firebase'),'NemesisAuthBot',manager,lambda *a:None)
    assert 'Total ' in sent[-1][1]
    assert sent[-1][2].get('inline_keyboard')
    callback={'callback_query':{'id':'synthetic','from':{'id':10002},'message':{'message_id':len(sent),'chat':{'id':10002,'type':'private'},'from':{'is_bot':True,'username':'NemesisAuthBot'}},'data':'nf:tampered'}}
    handle(callback,'NemesisAuthBot',manager,lambda *a:answers.append(a));assert answers

def test_owner_rate_limit_and_callback_cannot_be_reused_on_new_request(env):
    with store.transaction() as c:
        for _ in range(30):store.throttle(c,10001)
    with pytest.raises(cfg.ManagerError):
        with store.transaction() as c:store.throttle(c,10001)

def test_cloud_rest_identity_rules_and_unprivileged_denial(env):
    resource='projects/1234567890/locations/us-central1/instances/isolated-one'
    def respond(req):
        if req.url.host=='firebasedatabase.googleapis.com':return httpx.Response(200,json={'name':resource,'project':'projects/1234567890','state':'ACTIVE','databaseUrl':'https://isolated-one.firebaseio.com'})
        if req.headers.get('Authorization'):
            return httpx.Response(200,json=cfg.RULES) if req.url.path=='/.settings/rules.json' else httpx.Response(200,content='null')
        return httpx.Response(401,json={'error':'Permission denied'})
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(respond)),SimpleNamespace(service_account_email=env['runtime_service_account'],valid=True,token='synthetic-access'))
    assert provider.validate('https://isolated-one.firebaseio.com')['resource']==resource
    provider.close()

@pytest.mark.parametrize('defect',['wrong_project','public_rules','public_write','missing_instance'])
def test_cloud_checks_fail_closed(env,defect):
    resource='projects/1234567890/locations/us-central1/instances/isolated-one'
    def respond(req):
        if req.url.host=='firebasedatabase.googleapis.com':return httpx.Response(404 if defect=='missing_instance' else 200,json={'name':resource,'project':'projects/wrong' if defect=='wrong_project' else 'projects/1234567890','state':'ACTIVE','databaseUrl':'https://isolated-one.firebaseio.com'})
        if req.headers.get('Authorization'):return httpx.Response(200,json={'rules':{'.read':True}} if defect=='public_rules' else cfg.RULES)
        return httpx.Response(200 if defect=='public_write' and req.method=='PUT' else 401,json=None)
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(respond)),SimpleNamespace(service_account_email=env['runtime_service_account'],valid=True,token='synthetic'))
    with pytest.raises(cfg.ManagerError):provider.validate('https://isolated-one.firebaseio.com')
    provider.close()


def test_inspect_confirmation_cannot_register_a_different_revalidated_result(env):
    jid=jobs.enqueue_job(10001,'inspect','VERSIONED','isolated','https://version-one.firebaseio.com');jobs.tick(Cloud)
    with account_store.connect() as c:result=json.loads(c.execute('SELECT result FROM firebase_manager_jobs WHERE id=?',(jid,)).fetchone()[0])
    old_hash=hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()
    jobs.enqueue_job(10001,'inspect','VERSIONED','isolated','https://version-two.firebaseio.com');jobs.tick(Cloud)
    with pytest.raises(cfg.ManagerError):jobs.register(10001,jid,old_hash)


def test_disable_revalidates_affected_customer_at_confirmation(env):
    verified()
    from firebase_pool import get_or_assign
    get_or_assign(2)
    with pytest.raises(cfg.ManagerError):store.disable(10001,'DB_ONE',None)
    store.disable(10001,'DB_ONE','SyntheticCustomer')


def test_fifty_customers_receive_fifty_independent_instances(env):
    ids=[]
    with account_store.connect() as c:
        for i in range(50):
            c.execute("INSERT INTO users(login_id,password_hash,telegram_chat_id,role,is_active,created_at,expires_at) VALUES(?,?,?,'user',1,?,?)",('SyntheticLoad'+str(i),'noncredential-test-marker',20000+i,int(time.time()),int(time.time())+86400))
            ids.append(c.execute('SELECT last_insert_rowid()').fetchone()[0])
    for i in range(50):verified('LOAD_'+str(i),'https://load-database-'+str(i)+'.firebaseio.com')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:assigned=list(executor.map(pool.get_or_assign,ids))
    assert len({r[0] for r in assigned})==50
    with account_store.connect() as c:assert c.execute('SELECT COUNT(*) FROM firebase_assignment_ledger').fetchone()[0]==50
