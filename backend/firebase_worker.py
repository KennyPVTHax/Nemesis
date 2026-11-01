"""Bounded background work and leased at-least-once notifications; no credentials in payloads."""
import json,time,threading
from account_store import connect
import firebase_config as cfg
from firebase_manager_store import transaction,owner
from firebase_jobs import tick

def flush(manager):
    if not cfg.enabled():return
    now=int(time.time())
    with transaction() as db:
        row=db.execute("SELECT id,kind,user_id,payload,attempts FROM firebase_manager_outbox WHERE (state='PENDING' OR (state='SENDING' AND lease_until<=?)) AND next_at<=? AND attempts<8 ORDER BY id LIMIT 1",(now,now)).fetchone()
        if not row:return
        oid,kind,uid,raw,attempts=row;payload=json.loads(raw)
        db.execute("UPDATE firebase_manager_outbox SET state='SENDING',lease_until=?,attempts=attempts+1 WHERE id=?",(now+90,oid))
    try:
        if kind.startswith('owner_'):
            with connect() as db:
                r=db.execute("SELECT telegram_chat_id FROM users WHERE role='owner' AND is_active=1 AND login_id='NemesisOwner' COLLATE NOCASE").fetchone()
            if not r or not r[0]:raise cfg.ManagerError('owner_not_linked')
            chat=r[0]
            if kind=='owner_request':
                with connect() as db:r=db.execute("SELECT u.login_id,r.state,v.revision FROM users u JOIN firebase_link_requests r ON r.user_id=u.id JOIN firebase_manager_request_versions v ON v.user_id=u.id WHERE u.id=?",(uid,)).fetchone()
                if r and r[1]=='pending' and r[2]==payload['revision']:
                    manager.message(chat,'Customer '+r[0]+' requests disclosure of their assigned database URL. Approval is not Firebase data authorization.',[(name,'decision_prompt',{'user_id':uid,'revision':r[2],'approve':yes}) for name,yes in [('Approve',True),('Deny',False)]])
            elif kind=='owner_low_pool':manager.message(chat,'Firebase available inventory is below the configured threshold. Open /firebase. No automatic provisioning was performed.')
            elif kind=='owner_job':
                with connect() as db:r=db.execute('SELECT kind,label,alias,state,diagnostic,result FROM firebase_manager_jobs WHERE id=?',(payload['job_id'],)).fetchone()
                if r and r[3]=='DONE':
                    result=json.loads(r[5])
                    text=r[1]+' | '+r[2]+' | '+result['region']+'\n'+result['url']+'\nConnectivity, project identity, exact deny-all Rules and unprivileged denial checks passed.'
                    if r[0]=='inspect':manager.confirm(chat,text+'\nConfirm registration as available?','register',{'job_id':payload['job_id'],'result_hash':__import__('hashlib').sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()})
                    else:
                        with connect() as db:state=db.execute('SELECT m.state FROM firebase_manager_jobs j JOIN firebase_manager_instances m ON m.instance_id=j.instance_id WHERE j.id=?',(payload['job_id'],)).fetchone()
                        manager.message(chat,text+'\nPool state: '+str(state[0] if state else 'not registered')+'. No reassignment or deletion occurred.')
                elif r:manager.message(chat,'Operation '+r[1]+' is '+r[3]+': '+str(r[4])+'. No database is reported ready.')
        else:
            with connect() as db:r=db.execute('SELECT telegram_chat_id FROM users WHERE id=?',(uid,)).fetchone()
            if r and r[0]:manager.send(r[0],('Firebase link request '+payload['state']+'. Check the authenticated app.' if kind=='customer_decision' else 'A dedicated Firebase database has been assigned. Check Firebase status in Settings.'),None)
        with transaction() as db:db.execute("UPDATE firebase_manager_outbox SET state='SENT',lease_until=0 WHERE id=?",(oid,))
    except Exception:
        with transaction() as db:db.execute("UPDATE firebase_manager_outbox SET state=?,next_at=?,lease_until=0 WHERE id=?",('FAILED' if attempts>=7 else 'PENDING',int(time.time())+min(900,15*2**attempts),oid))

def loop(manager,stop):
    while not stop.is_set():
        try:maintenance();tick();flush(manager)
        except Exception:pass # No provider/Telegram exceptions or payloads go into logs.
        stop.wait(2)


def maintenance():
    """Revalidate currently enabled verified resources; never enable ERROR/DISABLED resources."""
    if not cfg.enabled():return
    from firebase_manager_store import enqueue
    from firebase_jobs import enqueue_job
    with connect() as db:
        who=db.execute("SELECT telegram_chat_id FROM users WHERE role='owner' AND login_id='NemesisOwner' COLLATE NOCASE AND is_active=1").fetchone()
        row=db.execute("SELECT i.label,m.alias,i.database_url FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.active=1 AND m.state IN ('AVAILABLE','ASSIGNED') AND m.verified_at<? ORDER BY m.verified_at LIMIT 1",(int(time.time())-43200,)).fetchone()
    if who and who[0] and row:enqueue_job(who[0],'test',row[0],row[1],row[2])
    from firebase_manager_store import overview
    import os
    try:threshold=max(0,min(50,int(os.environ.get('NEMESIS_FIREBASE_MIN_AVAILABLE','3'))))
    except ValueError:threshold=3
    with transaction() as db:
        count=db.execute("SELECT COUNT(*) FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.active=1 AND i.assigned_user_id IS NULL AND m.state='AVAILABLE' AND m.verified_at>?",(int(time.time())-86400,)).fetchone()[0]
        if count<threshold:enqueue(db,'low-pool:'+str(int(time.time())//3600),'owner_low_pool')
