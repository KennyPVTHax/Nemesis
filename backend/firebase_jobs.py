"""Persisted bounded jobs; external calls run outside SQLite transactions."""
import hashlib,json,time,secrets
from account_store import connect
import firebase_config as cfg
from firebase_cloud import GoogleFirebase,CloudError
from firebase_manager_store import transaction,owner,audit,enqueue

def enqueue_job(chat,kind,label,alias,url=None):
    if not cfg.enabled():raise cfg.ManagerError('firebase_manager_disabled')
    p=cfg.profile(alias);cfg.label(label)
    if kind not in ('inspect','create','test','enable'):raise cfg.ManagerError('invalid_job_kind')
    if kind=='create' and p.get('create_enabled') is not True:raise cfg.ManagerError('automatic_creation_disabled')
    resource=None
    if kind=='create':
        dbid='nemesis-'+hashlib.sha256((str(p['project_number'])+':'+label).encode()).hexdigest()[:24]
        resource=f'projects/{p["project_number"]}/locations/{p["region"]}/instances/{dbid}'
    elif url:url=cfg.identity(url)[0]
    with transaction() as db:
        actor=owner(db,chat)
        old=db.execute('SELECT id,state FROM firebase_manager_jobs WHERE kind=? AND alias=? AND label=?',(kind,alias,label)).fetchone()
        if old:
            if old[1]=='ERROR':
                db.execute("UPDATE firebase_manager_jobs SET state='PENDING',attempts=0,next_at=0 WHERE id=?",(old[0],));audit(db,actor,'job_retry',old[0])
            elif old[1]=='DONE' and kind in ('test','enable','inspect'):
                db.execute("UPDATE firebase_manager_jobs SET state='PENDING',attempts=0,next_at=0,url=?,result=NULL WHERE id=?",(url,old[0]))
            return old[0]
        if kind in ('create','inspect') and db.execute("SELECT 1 FROM firebase_manager_jobs WHERE kind IN ('create','inspect') AND label=?",(label,)).fetchone():raise cfg.ManagerError('label_reserved_by_existing_operation')
        if kind in ('create','inspect') and db.execute("SELECT 1 FROM firebase_instances WHERE label=? OR lower(rtrim(database_url,'/'))=?",(label,url or '')).fetchone():raise cfg.ManagerError('duplicate_instance_label_or_url')
        jid=secrets.token_hex(12)
        db.execute('INSERT INTO firebase_manager_jobs(id,kind,label,alias,project_number,url,resource,actor_chat,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(jid,kind,label,alias,str(p['project_number']),url,resource,chat,int(time.time())))
        audit(db,actor,'job_queued',jid)
        return jid

def register(chat,job_id,expected_result=None):
    with transaction() as db:
        actor=owner(db,chat)
        row=db.execute("SELECT label,alias,result FROM firebase_manager_jobs WHERE id=? AND kind='inspect' AND state='DONE' AND actor_chat=?",(job_id,chat)).fetchone()
        if not row:raise cfg.ManagerError('validation_not_ready')
        result=json.loads(row[2])
        if expected_result is not None and hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()!=expected_result:raise cfg.ManagerError('validation_changed_reconfirm_required')
        p=cfg.profile(row[1])
        if result.get('profile_hash')!=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest():raise cfg.ManagerError('project_profile_changed_retest_required')
        if db.execute("SELECT 1 FROM firebase_instances WHERE label=? OR lower(rtrim(database_url,'/'))=?",(row[0],result['url'])).fetchone():raise cfg.ManagerError('duplicate_instance_label_or_url')
        if result['verified_at']<=time.time()-180:raise cfg.ManagerError('validation_expired_retest_required')
        db.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',(row[0],result['url'],'alias:'+row[1],int(time.time())))
        iid=db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.execute("INSERT INTO firebase_manager_instances VALUES(?,?,?,'AVAILABLE',?,NULL,?)",(iid,row[1],result['resource'],result['verified_at'],result['rules_hash']))
        audit(db,actor,'registered',iid)
        return iid

def tick(provider_factory=GoogleFirebase):
    if not cfg.enabled():return False
    now=int(time.time())
    with transaction() as db:
        exhausted=db.execute("SELECT id FROM firebase_manager_jobs WHERE attempts>=6 AND lease_until<=? AND state IN ('RUNNING','PROVISIONING','VALIDATING','RETRY')",(now,)).fetchall()
        for item in exhausted:
            db.execute("UPDATE firebase_manager_jobs SET state='ERROR',diagnostic='retry_limit_reached' WHERE id=?",item)
            enqueue(db,'exhausted:'+item[0],'owner_job',payload={'job_id':item[0]})
        lock=db.execute('SELECT lease_until FROM firebase_manager_cloud_lock WHERE id=1').fetchone()
        if lock and lock[0]>now:return False
        r=db.execute("SELECT id,kind,label,alias,url,resource,actor_chat,attempts,phase,project_number FROM firebase_manager_jobs WHERE (state IN ('PENDING','RETRY') OR (state IN ('RUNNING','PROVISIONING','VALIDATING') AND lease_until<=?)) AND next_at<=? AND attempts<6 ORDER BY created_at LIMIT 1",(now,now)).fetchone()
        if not r:return False
        jid,kind,label,alias,url,resource,chat,attempts,phase,job_project=r
        try:owner(db,chat)
        except cfg.ManagerError:
            db.execute("UPDATE firebase_manager_jobs SET state='ERROR',diagnostic='owner_authorization_required' WHERE id=?",(jid,));return True
        db.execute('INSERT OR REPLACE INTO firebase_manager_cloud_lock VALUES(1,?,?)',(jid,now+300))
        db.execute("UPDATE firebase_manager_jobs SET state='RUNNING',attempts=attempts+1,lease_until=? WHERE id=?",(now+300,jid))
    provider=None
    try:
        p=cfg.profile(alias)
        if str(p['project_number'])!=job_project or (resource and not resource.startswith(f'projects/{job_project}/locations/{p["region"]}/instances/')):raise cfg.ManagerError('project_profile_changed_operation_blocked')
        provider=provider_factory(p);provider.preflight(kind=='create')
        if kind=='create':
            obj=provider.get(resource)
            if obj is None:
                if phase=='INIT':
                    with transaction() as db:owner(db,chat);db.execute("UPDATE firebase_manager_jobs SET phase='REQUESTED',state='PROVISIONING' WHERE id=?",(jid,))
                with connect() as db:
                    known=[r[0] for r in db.execute('SELECT resource FROM firebase_manager_instances WHERE resource LIKE ?',('projects/'+str(p['project_number'])+'/%',)).fetchall()]
                    known.extend(r[0] for r in db.execute("SELECT resource FROM firebase_manager_jobs WHERE project_number=? AND phase='REQUESTED' AND resource IS NOT NULL AND resource<>?",(str(p['project_number']),resource)).fetchall())
                obj=provider.create(resource,known_resources=known)
            elif phase=='INIT':raise CloudError('resource_exists_before_creation')
            if obj.get('state')!='ACTIVE':raise CloudError('provisioning_not_active',True)
            url=obj.get('databaseUrl')
        with transaction() as db:db.execute("UPDATE firebase_manager_jobs SET state='VALIDATING' WHERE id=?",(jid,))
        canonical=cfg.identity(url)[0]
        with connect() as db:
            if db.execute("SELECT COUNT(*) FROM firebase_instances WHERE lower(rtrim(database_url,'/'))=?",(canonical,)).fetchone()[0]>1:raise cfg.ManagerError('duplicate_database_identity_manual_review')
        with connect() as db:existing=db.execute("SELECT assigned_user_id FROM firebase_instances WHERE label=? AND lower(rtrim(database_url,'/'))=?",(label,canonical)).fetchone()
        require_empty=kind in ('create','inspect') or not existing or existing[0] is None
        result=provider.validate(url,apply_rules=kind=='create',require_empty=require_empty)
        result['verified_at']=int(time.time())
        result['profile_hash']=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
        if cfg.profile(alias)!=p:raise cfg.ManagerError('project_profile_changed_retest_required')
        with transaction() as db:
            actor=owner(db,chat)
            if kind=='create':
                existing=db.execute('SELECT id FROM firebase_instances WHERE database_url=?',(result['url'],)).fetchone()
                if existing:iid=existing[0]
                else:
                    db.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',(label,result['url'],'alias:'+alias,int(time.time())))
                    iid=db.execute('SELECT last_insert_rowid()').fetchone()[0]
                db.execute("INSERT INTO firebase_manager_instances VALUES(?,?,?,'AVAILABLE',?,NULL,?) ON CONFLICT(instance_id) DO UPDATE SET verified_at=excluded.verified_at,rules_hash=excluded.rules_hash,diagnostic=NULL",(iid,alias,result['resource'],result['verified_at'],result['rules_hash']))
            elif kind in ('test','enable'):
                instance=db.execute("SELECT id,assigned_user_id,active FROM firebase_instances WHERE label=? AND lower(rtrim(database_url,'/'))=?",(label,result['url'])).fetchone()
                if not instance:raise cfg.ManagerError('unknown_instance')
                iid=instance[0]
                active=1 if kind=='enable' else instance[2]
                state=('ASSIGNED' if instance[1] is not None else 'AVAILABLE') if active else 'DISABLED'
                db.execute('UPDATE firebase_instances SET active=? WHERE id=?',(active,iid))
                db.execute('UPDATE firebase_manager_instances SET alias=?,resource=?,state=?,verified_at=?,rules_hash=?,diagnostic=NULL WHERE instance_id=?',(alias,result['resource'],state,result['verified_at'],result['rules_hash'],iid))
            else:iid=None
            db.execute("UPDATE firebase_manager_jobs SET state='DONE',result=?,instance_id=?,diagnostic=NULL,lease_until=0 WHERE id=?",(json.dumps(result),iid,jid))
            audit(db,actor,'job_validated',jid);enqueue(db,'job:'+jid+':'+str(attempts),'owner_job',payload={'job_id':jid})
    except Exception as error:
        code=str(error) if isinstance(error,cfg.ManagerError) else 'administrative_operation_failed'
        # Only known short diagnostic codes, never provider exception payloads/URLs/tokens.
        import re
        if not re.fullmatch('[a-z0-9_]{1,80}',code):code='administrative_operation_failed'
        retry=isinstance(error,CloudError) and error.retry and attempts<5
        with transaction() as db:
            db.execute('UPDATE firebase_manager_jobs SET state=?,diagnostic=?,next_at=?,lease_until=0 WHERE id=?',('RETRY' if retry else 'ERROR',code,int(time.time())+min(900,30*2**attempts),jid))
            if kind in ('test','enable'):
                db.execute("UPDATE firebase_manager_instances SET state='ERROR',diagnostic=?,verified_at=NULL WHERE instance_id IN (SELECT id FROM firebase_instances WHERE label=?)",(code,label))
            audit(db,None,'job_error',jid)
            if not retry:enqueue(db,'joberror:'+jid+':'+str(attempts),'owner_job',payload={'job_id':jid})
    finally:
        with transaction() as db:db.execute('DELETE FROM firebase_manager_cloud_lock WHERE job_id=?',(jid,))
        if provider:provider.close()
    return True
