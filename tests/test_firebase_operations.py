import hashlib,json,time,importlib.util,sqlite3
from pathlib import Path
from types import SimpleNamespace
import pytest,httpx
from test_firebase_manager import env,db,verified,Cloud
from test_firebase_manager import reset_cloud
import account_store,firebase_config as cfg,firebase_jobs as jobs,firebase_manager_store as store
from firebase_cloud import GoogleFirebase,CloudError,PERMISSIONS,ROLE_PERMISSIONS
from firebase_worker import flush
from firebase_telegram import Manager


def test_official_google_creation_preflight_quota_validation_and_post(env):
    calls=[]
    def reply(req):
        calls.append((req.method,str(req.url)))
        if req.url.host=='cloudresourcemanager.googleapis.com' and req.method=='GET':return httpx.Response(200,json={'projectId':env['project_id'],'projectNumber':env['project_number'],'lifecycleState':'ACTIVE'})
        if req.url.host=='iam.googleapis.com':return httpx.Response(200,json={'includedPermissions':ROLE_PERMISSIONS})
        if req.url.path.endswith(':getIamPolicy'):return httpx.Response(200,json={'bindings':[{'role':'projects/nemesis-isolated/roles/nemesisFirebaseManager','members':['serviceAccount:'+env['runtime_service_account']]}]})
        if req.url.path.endswith(':testIamPermissions'):return httpx.Response(200,json={'permissions':PERMISSIONS+['firebasedatabase.instances.create']})
        if req.url.path.endswith('/billingInfo'):return httpx.Response(200,json={'billingEnabled':True})
        if req.method=='GET':return httpx.Response(200,json={'instances':[]})
        assert json.loads(req.content)=={'type':'USER_DATABASE'}
        return httpx.Response(200,json={'name':'projects/1234567890/locations/us-central1/instances/new-database','state':'ACTIVE'})
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(reply)),SimpleNamespace(service_account_email=env['runtime_service_account'],valid=True,token='synthetic'))
    assert provider.create('projects/1234567890/locations/us-central1/instances/new-database')['state']=='ACTIVE'
    assert any('validateOnly=true' in u for _,u in calls)
    assert any('databaseId=new-database' in u for _,u in calls)
    provider.close()

@pytest.mark.parametrize('failure',['billing','policy','permissions','budget','quota'])
def test_google_preflight_refuses_unready_projects(env,failure):
    def reply(req):
        if req.url.host=='cloudresourcemanager.googleapis.com' and req.method=='GET':return httpx.Response(200,json={'projectId':env['project_id'],'projectNumber':env['project_number'],'lifecycleState':'ACTIVE'})
        if req.url.host=='iam.googleapis.com':return httpx.Response(200,json={'includedPermissions':ROLE_PERMISSIONS})
        if req.url.path.endswith(':getIamPolicy'):return httpx.Response(200,json={'bindings':['changed']} if failure=='policy' else {'bindings':[{'role':'projects/nemesis-isolated/roles/nemesisFirebaseManager','members':['serviceAccount:'+env['runtime_service_account']]}]})
        if req.url.path.endswith(':testIamPermissions'):return httpx.Response(200,json={'permissions':[] if failure=='permissions' else PERMISSIONS+['firebasedatabase.instances.create']})
        if req.url.path.endswith('/billingInfo'):return httpx.Response(200,json={'billingEnabled':failure!='billing'})
        if req.method=='GET':return httpx.Response(200,json={'instances':[{'name':'resource-'+str(i)} for i in range(env['max_instances'])] if failure=='budget' else []})
        return httpx.Response(429,json={'error':'isolated quota failure'})
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(reply)),SimpleNamespace(service_account_email=env['runtime_service_account'],valid=True,token='synthetic'))
    with pytest.raises(cfg.ManagerError):provider.create('projects/1234567890/locations/us-central1/instances/new-database')
    provider.close()


def test_owner_notifications_approval_buttons_and_customer_notification(env):
    verified();from firebase_pool import get_or_assign,request_link
    get_or_assign(2);request_link(2)
    sent=[]
    def send(chat,text,keyboard):sent.append((chat,text,keyboard));return {'message_id':len(sent)}
    manager=Manager(send)
    for _ in range(5):flush(manager)
    pending=[s for s in sent if 'requests disclosure' in s[1]]
    assert len(pending)==1 and pending[0][0]==10001
    assert pending[0][2]['inline_keyboard'][0][0]['text']=='Approve'
    with account_store.connect() as c:rev=c.execute('SELECT revision FROM firebase_manager_request_versions WHERE user_id=2').fetchone()[0]
    store.decision(10001,2,rev,True)
    flush(manager)
    assert any(chat==10002 and 'approved' in text for chat,text,_ in sent)


def test_gateway_uses_only_own_assignment_and_rechecks_authorization(env,monkeypatch):
    from firebase_pool import get_or_assign,request_link
    import firebase_gateway,auth_api,main
    from fastapi.testclient import TestClient
    verified();verified('SECOND_DB','https://isolated-two.firebaseio.com')
    get_or_assign(2);get_or_assign(3)
    for uid in (2,3):
        request_link(uid)
        with account_store.connect() as c:rev=c.execute('SELECT revision FROM firebase_manager_request_versions WHERE user_id=?',(uid,)).fetchone()[0]
        store.decision(10001,uid,rev,True)
    monkeypatch.setenv('NEMESIS_FIREBASE_GATEWAY_ENABLED','1')
    accessed=[]
    class Gateway(Cloud):
        def preferences(self,url,value=None,write=False):accessed.append(url);return {'theme':'test'}
    monkeypatch.setattr(firebase_gateway,'GoogleFirebase',Gateway)
    token='synthetic-session-'+__import__('secrets').token_urlsafe(24)
    with account_store.connect() as c:c.execute('INSERT INTO auth_sessions VALUES(?,?,?)',(auth_api.digest(token),3,int(time.time())+600))
    client=TestClient(main.app);headers={'Authorization':'Bearer '+token}
    assert client.get('/firebase/preferences').status_code==401
    assert client.get('/firebase/preferences',headers=headers).status_code==200
    assert accessed==['https://isolated-two.firebaseio.com']
    assert client.put('/firebase/preferences',headers=headers,json={'theme':'dark','locale':'en','database_url':'https://isolated-one.firebaseio.com'}).status_code==422
    with account_store.connect() as c:c.execute('UPDATE users SET expires_at=0 WHERE id=3')
    assert client.get('/firebase/preferences',headers=headers).status_code==401


def test_existing_bot_commands_and_403_handling_are_retained(env,monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN','synthetic-test-only')
    import telegram_bot
    messages=[]
    monkeypatch.setattr(telegram_bot,'send',lambda client,chat,text:messages.append(text))
    # Intercept raw manager calls; legacy command dispatch remains unchanged.
    monkeypatch.setattr(telegram_bot,'api',lambda *a,**k:{'message_id':1})
    names={'new_key':'/newkey','redeem':'/redeem INVALID','setid':'/setid ExampleID','registration_status':'/registration','registration_setup':'/setup','consume_code':'/link INVALID'}
    called=[]
    for name in names:
        monkeypatch.setattr(telegram_bot,name,lambda *a,n=name:(called.append(n) or 'invalid'))
    for command in ['/start','/help','/status',*names.values(),'/cancel']:
        telegram_bot.process(None,'NemesisAuthBot',{'update_id':len(messages)+100,'message':{'chat':{'id':10001,'type':'private'},'from':{'id':10001},'text':command}})
    assert set(called)==set(names)
    # Exercise actual delivery-error classifier after removing the intercept.
    original=__import__('importlib').reload(telegram_bot)
    class Client:
        def post(self,*args,**kwargs):return httpx.Response(403,json={'description':'bot was blocked by the user'})
    with pytest.raises(original.TelegramDeliveryForbidden,match='bot_blocked'):original.send(Client(),10001,'synthetic')


def test_copy_of_old_schema_migrates_without_account_or_assignment_changes(tmp_path,monkeypatch):
    import ast
    old=Path('legacy/phase3-baseline/backend/firebase_pool.py').read_text()
    tree=ast.parse(old);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='init')
    sql=next(x.value for x in ast.walk(fn) if isinstance(x,ast.Constant) and isinstance(x.value,str) and 'CREATE TABLE' in x.value)
    original=tmp_path/'old.sqlite3';copy=tmp_path/'copy.sqlite3'
    with sqlite3.connect(original) as c:
        c.executescript(account_store.SCHEMA);c.executescript(sql)
        c.execute("INSERT INTO users VALUES(1,'SyntheticOld','noncredential-test-marker',10002,'user',1,1,0)")
        c.execute("INSERT INTO firebase_instances VALUES(1,'OLD','https://old-instance.firebaseio.com','/isolated/path',1,1,1,1)")
    src=sqlite3.connect(original);dest=sqlite3.connect(copy);src.backup(dest);src.close();dest.close()
    monkeypatch.setattr(account_store,'DB_PATH',copy)
    from firebase_migration import migrate
    migrate();migrate()
    with sqlite3.connect(copy) as c,sqlite3.connect(original) as oldc:
        assert c.execute('SELECT * FROM users').fetchall()==oldc.execute('SELECT * FROM users').fetchall()
        assert c.execute('SELECT * FROM firebase_instances').fetchall()==oldc.execute('SELECT * FROM firebase_instances').fetchall()
        assert c.execute('SELECT user_id FROM firebase_assignment_ledger').fetchone()[0]==1
        assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'


spec=importlib.util.spec_from_file_location('firebase_install',Path(__file__).resolve().parents[1]/'deployment/install_firebase_manager.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

@pytest.fixture
def install(tmp_path):
    base=tmp_path/'production';source=tmp_path/'candidate';backups=tmp_path/'backups'
    (base/'backend').mkdir(parents=True);(base/'.venv').mkdir();(base/'data').mkdir();source.mkdir()
    (base/'backend/main.py').write_text('# baseline\n');(source/'main.py').write_text('# patched\n');(base/'.venv/state').write_text('baseline dependencies')
    with sqlite3.connect(base/'data/accounts.sqlite3') as c:c.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY)');c.execute('INSERT INTO customers VALUES(1)')
    manifest={'main.py':{'original':hashlib.sha256(b'# baseline\n').hexdigest(),'current':hashlib.sha256(b'# patched\n').hexdigest()}}
    events=[]
    def dependencies():(base/'.venv/state').write_text('patched dependencies')
    def migrate():
        with sqlite3.connect(base/'data/accounts.sqlite3') as c:c.execute('CREATE TABLE IF NOT EXISTS additive_schema(id INTEGER)')
    tool=module.Installer(base,source,manifest,backups,{'api':tmp_path/'unit.d/manager.conf'},lambda:events.append('stop'),lambda:events.append('restart'),dependencies,migrate,lambda *a:True)
    return tool,events

def test_install_and_rollback_are_idempotent_and_preserve_database(install):
    tool,events=install;backup=tool.apply(True);count=len(events);assert tool.apply(True)==backup;assert len(events)==count
    with sqlite3.connect(tool.base/'data/accounts.sqlite3') as c:c.execute('INSERT INTO customers VALUES(2)')
    tool.rollback(backup)
    assert (tool.base/'backend/main.py').read_text()=='# baseline\n'
    assert (tool.base/'.venv/state').read_text()=='baseline dependencies'
    with sqlite3.connect(tool.base/'data/accounts.sqlite3') as c:assert c.execute('SELECT COUNT(*) FROM customers').fetchone()[0]==2
    count=len(events);tool.rollback(backup);assert len(events)==count


def test_failed_post_install_health_rolls_back_source_and_venv(install):
    tool,_=install;tool.health=lambda new,*args:not new
    with pytest.raises(module.InstallError):tool.apply()
    assert (tool.base/'backend/main.py').read_text()=='# baseline\n'
    assert (tool.base/'.venv/state').read_text()=='baseline dependencies'


def test_install_refuses_unknown_source_drift(install):
    tool,events=install;(tool.base/'backend/main.py').write_text('# unknown\n')
    with pytest.raises(module.InstallError):tool.apply()
    assert events==[]


def test_capabilities_are_authenticated_and_activation_is_explicit(env,monkeypatch):
    import auth_api,main,secrets
    from fastapi.testclient import TestClient
    token=secrets.token_urlsafe(32)
    with account_store.connect() as c:c.execute('INSERT INTO auth_sessions VALUES(?,?,?)',(auth_api.digest(token),2,int(time.time())+600))
    client=TestClient(main.app)
    assert client.get('/firebase/capabilities').status_code==401
    headers={'Authorization':'Bearer '+token}
    assert client.get('/firebase/capabilities',headers=headers).json()['enabled'] is True
    monkeypatch.delenv('NEMESIS_FIREBASE_MANAGER_ENABLED')
    assert client.get('/firebase/capabilities',headers=headers).json()['enabled'] is False


def test_crashed_final_attempt_becomes_error_instead_of_stuck_running(env):
    jid=jobs.enqueue_job(10001,'create','EXHAUSTED','isolated')
    with account_store.connect() as c:c.execute("UPDATE firebase_manager_jobs SET state='RUNNING',attempts=6,lease_until=0 WHERE id=?",(jid,))
    jobs.tick(Cloud)
    with account_store.connect() as c:assert c.execute('SELECT state FROM firebase_manager_jobs WHERE id=?',(jid,)).fetchone()[0]=='ERROR'


@pytest.mark.parametrize('bad_role',['editor','extra_permission'])
def test_broad_iam_grants_are_rejected_even_with_matching_review_hash(env,bad_role):
    policy={'bindings':[{'role':'roles/editor' if bad_role=='editor' else 'projects/nemesis-isolated/roles/nemesisFirebaseManager','members':['serviceAccount:'+env['runtime_service_account']]}]}
    env['iam_policy_sha256']=hashlib.sha256(json.dumps(policy,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    def reply(req):
        if req.url.host=='iam.googleapis.com':return httpx.Response(200,json={'includedPermissions':ROLE_PERMISSIONS+['firebasedatabase.instances.delete']})
        if req.url.path.endswith(':getIamPolicy'):return httpx.Response(200,json=policy)
        return httpx.Response(200,json={'projectId':env['project_id'],'projectNumber':env['project_number'],'lifecycleState':'ACTIVE'})
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(reply)),SimpleNamespace(valid=True,token='synthetic',service_account_email=env['runtime_service_account']))
    with pytest.raises(cfg.ManagerError):provider.preflight()
    provider.close()


def test_unprivileged_identity_cannot_be_substituted(env):
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200,json={}))),SimpleNamespace(valid=True,token='synthetic',service_account_email='other@nemesis-isolated.iam.gserviceaccount.com'))
    with pytest.raises(cfg.ManagerError):provider.headers()
    provider.close()


def test_rollback_does_not_reenable_unverified_instances_in_legacy_allocator(install):
    tool,_=install
    with sqlite3.connect(tool.base/'data/accounts.sqlite3') as c:
        c.execute('CREATE TABLE firebase_instances(id INTEGER PRIMARY KEY,active INTEGER)')
        c.execute('CREATE TABLE firebase_manager_instances(instance_id INTEGER,state TEXT,verified_at INTEGER)')
        c.executemany('INSERT INTO firebase_instances VALUES(?,1)',[(1,),(2,)])
        c.execute("INSERT INTO firebase_manager_instances VALUES(1,'VALIDATING',NULL)")
        c.execute("INSERT INTO firebase_manager_instances VALUES(2,'AVAILABLE',?)",(int(time.time()),))
    backup=tool.apply();tool.rollback(backup)
    with sqlite3.connect(tool.base/'data/accounts.sqlite3') as c:assert c.execute('SELECT active FROM firebase_instances ORDER BY id').fetchall()==[(0,),(1,)]


def test_legacy_trailing_slash_url_can_be_verified_without_rewriting_original(env):
    with account_store.connect() as c:c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',('TRAILING','https://legacy-instance.firebaseio.com/','/isolated/path',1))
    from firebase_migration import migrate
    migrate();jobs.enqueue_job(10001,'test','TRAILING','isolated','https://legacy-instance.firebaseio.com/');jobs.tick(Cloud)
    with account_store.connect() as c:
        assert c.execute('SELECT database_url FROM firebase_instances').fetchone()[0].endswith('/')
        assert c.execute('SELECT state FROM firebase_manager_instances').fetchone()[0]=='AVAILABLE'


def test_legacy_duplicate_identity_is_not_silently_verified(env):
    with account_store.connect() as c:
        c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',('DUP_A','https://legacy-instance.firebaseio.com','/isolated/path',1))
        c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',('DUP_B','https://legacy-instance.firebaseio.com/','/isolated/path',1))
    from firebase_migration import migrate
    migrate();jobs.enqueue_job(10001,'test','DUP_A','isolated','https://legacy-instance.firebaseio.com');jobs.tick(Cloud)
    with account_store.connect() as c:
        assert c.execute('SELECT diagnostic FROM firebase_manager_jobs').fetchone()[0]=='duplicate_database_identity_manual_review'
        assert c.execute("SELECT COUNT(*) FROM firebase_manager_instances WHERE state='AVAILABLE'").fetchone()[0]==0


def test_nonempty_unassigned_database_is_not_recycled(env):
    resource='projects/1234567890/locations/us-central1/instances/isolated-one'
    def reply(req):
        if req.url.host=='firebasedatabase.googleapis.com':return httpx.Response(200,json={'name':resource,'project':'projects/1234567890','state':'ACTIVE','databaseUrl':'https://isolated-one.firebaseio.com'})
        if req.url.path=='/.settings/rules.json':return httpx.Response(200,json=cfg.RULES)
        if req.url.query:return httpx.Response(200,json={'old_customer_data':True})
        return httpx.Response(200,content='null')
    provider=GoogleFirebase(env,httpx.Client(transport=httpx.MockTransport(reply)),SimpleNamespace(service_account_email=env['runtime_service_account'],valid=True,token='synthetic'))
    with pytest.raises(CloudError,match='nonempty_database'):provider.validate('https://isolated-one.firebaseio.com',require_empty=True)
    provider.close()


@pytest.mark.parametrize('flag',['false','0'])
def test_creation_flags_must_be_true_booleans(env,flag):
    env['create_enabled']=flag
    with pytest.raises(cfg.ManagerError):jobs.enqueue_job(10001,'create','FLAG_CLOSED','isolated')


def test_queued_job_cannot_create_in_old_project_after_alias_rebinding(env):
    jobs.enqueue_job(10001,'create','REBIND_GUARD','isolated')
    env['project_number']='9999999999'
    jobs.tick(Cloud)
    assert Cloud.creates==0
    with account_store.connect() as c:assert c.execute('SELECT diagnostic FROM firebase_manager_jobs').fetchone()[0]=='project_profile_changed_operation_blocked'
