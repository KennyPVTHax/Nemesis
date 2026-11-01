import hashlib,json,secrets,time,sqlite3
from contextlib import contextmanager
from account_store import connect
from firebase_config import ManagerError

@contextmanager
def transaction():
    with connect() as db:
        db.execute('BEGIN IMMEDIATE');yield db

def owner(db,chat):
    row=db.execute("SELECT id FROM users WHERE telegram_chat_id=? AND role='owner' AND is_active=1 AND login_id='NemesisOwner' COLLATE NOCASE",(chat,)).fetchone()
    if not row:raise ManagerError('owner_authorization_required')
    return row[0]

def audit(db,actor,action,subject):db.execute('INSERT INTO firebase_manager_audit(actor_id,action,subject,created_at) VALUES(?,?,?,?)',(actor,action,str(subject)[:100],int(time.time())))
def enqueue(db,key,kind,user_id=None,payload=None):db.execute('INSERT OR IGNORE INTO firebase_manager_outbox(event_key,kind,user_id,payload) VALUES(?,?,?,?)',(key,kind,user_id,json.dumps(payload or {})))
def verified(db,i):
    r=db.execute("SELECT 1 FROM firebase_manager_instances m JOIN firebase_instances i ON i.id=m.instance_id WHERE i.id=? AND i.active=1 AND m.state IN ('AVAILABLE','ASSIGNED') AND m.verified_at>?",(i,int(time.time())-86400)).fetchone()
    return bool(r)

def throttle(db,chat):
    now=int(time.time())//60
    db.execute('INSERT INTO firebase_manager_throttle VALUES(?,?,1) ON CONFLICT(chat_id) DO UPDATE SET count=CASE WHEN window=excluded.window THEN count+1 ELSE 1 END,window=excluded.window',(chat,now))
    if db.execute('SELECT count FROM firebase_manager_throttle WHERE chat_id=?',(chat,)).fetchone()[0]>30:raise ManagerError('administrative_rate_limit')

def seen(update):
    with transaction() as db:
        db.execute('DELETE FROM firebase_manager_seen WHERE created_at<?',(int(time.time())-14*86400,))
        return db.execute('INSERT OR IGNORE INTO firebase_manager_seen VALUES(?,?)',(update,int(time.time()))).rowcount==1

def action(chat,kind,payload):
    token=secrets.token_urlsafe(24)
    with transaction() as db:
        owner(db,chat)
        db.execute('DELETE FROM firebase_manager_actions WHERE expires_at<?',(int(time.time())-86400,))
        db.execute('INSERT INTO firebase_manager_actions(hash,chat_id,action,payload,expires_at) VALUES(?,?,?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),chat,kind,json.dumps(payload),int(time.time())+180))
    return 'nf:'+token

def bind(chat,message_id,tokens):
    with transaction() as db:
        owner(db,chat)
        for token in tokens:db.execute('UPDATE firebase_manager_actions SET message_id=? WHERE hash=? AND chat_id=?',(message_id,hashlib.sha256(token[3:].encode()).hexdigest(),chat))

def consume(chat,message_id,token):
    if not isinstance(token,str) or not token.startswith('nf:') or len(token)>64:raise ManagerError('invalid_callback')
    with transaction() as db:
        owner(db,chat);throttle(db,chat)
        key=hashlib.sha256(token[3:].encode()).hexdigest()
        r=db.execute('SELECT action,payload FROM firebase_manager_actions WHERE hash=? AND chat_id=? AND message_id=? AND used=0 AND expires_at>?',(key,chat,message_id,int(time.time()))).fetchone()
        if not r:raise ManagerError('expired_or_consumed_callback')
        db.execute('UPDATE firebase_manager_actions SET used=1 WHERE hash=?',(key,))
        return r[0],json.loads(r[1])

def wizard(chat,stage,payload):
    with transaction() as db:
        owner(db,chat)
        db.execute('INSERT OR REPLACE INTO firebase_manager_wizards VALUES(?,?,?,?)',(chat,stage,json.dumps(payload),int(time.time())+600))

def take_wizard(chat):
    with transaction() as db:
        owner(db,chat)
        r=db.execute('SELECT stage,payload FROM firebase_manager_wizards WHERE chat_id=? AND expires_at>?',(chat,int(time.time()))).fetchone()
        return (r[0],json.loads(r[1])) if r else None

def clear_wizard(chat):
    with transaction() as db:owner(db,chat);db.execute('DELETE FROM firebase_manager_wizards WHERE chat_id=?',(chat,))

def overview():
    with connect() as db:
        total=db.execute('SELECT COUNT(*) FROM firebase_instances').fetchone()[0]
        available=db.execute("SELECT COUNT(*) FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.active=1 AND i.assigned_user_id IS NULL AND m.state='AVAILABLE' AND m.verified_at>?",(int(time.time())-86400,)).fetchone()[0]
        assigned=db.execute('SELECT COUNT(*) FROM firebase_instances WHERE assigned_user_id IS NOT NULL').fetchone()[0]
        disabled=db.execute('SELECT COUNT(*) FROM firebase_instances WHERE active=0').fetchone()[0]
        pending=db.execute("SELECT COUNT(*) FROM firebase_link_requests WHERE state='pending'").fetchone()[0]
        waiting=db.execute("SELECT COUNT(*) FROM firebase_manager_instances WHERE state IN ('VALIDATING','PROVISIONING','ERROR') OR verified_at IS NULL OR verified_at<=?",(int(time.time())-86400,)).fetchone()[0]
    return f'Total {total} | Available {available} | Assigned {assigned}\nDisabled {disabled} | Pending requests {pending} | Awaiting verification {waiting}'

def rows(section,page=0):
    with connect() as db:
        if section=='requests':return db.execute("SELECT u.login_id,r.user_id,v.revision FROM firebase_link_requests r JOIN users u ON u.id=r.user_id JOIN firebase_manager_request_versions v ON v.user_id=r.user_id WHERE r.state='pending' ORDER BY r.requested_at LIMIT 8 OFFSET ?",(page*8,)).fetchall()
        if section=='audit':return db.execute('SELECT action,subject,created_at FROM firebase_manager_audit ORDER BY id DESC LIMIT 8 OFFSET ?',(page*8,)).fetchall()
        if section=='jobs':return db.execute('SELECT label,state,COALESCE(diagnostic,phase) FROM firebase_manager_jobs ORDER BY created_at DESC LIMIT 8 OFFSET ?',(page*8,)).fetchall()
        query="SELECT i.label,COALESCE(u.login_id,'unassigned'),m.state FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id LEFT JOIN users u ON u.id=i.assigned_user_id"
        if section=='assignments':query+=' WHERE i.assigned_user_id IS NOT NULL'
        return db.execute(query+' ORDER BY i.id LIMIT 8 OFFSET ?',(page*8,)).fetchall()

def decision(chat,user_id,revision,approve):
    from firebase_pool import eligible
    with transaction() as db:
        actor=owner(db,chat)
        r=db.execute("SELECT r.state,v.revision,i.id FROM firebase_link_requests r JOIN firebase_manager_request_versions v ON v.user_id=r.user_id JOIN firebase_instances i ON i.assigned_user_id=r.user_id WHERE r.user_id=?",(user_id,)).fetchone()
        if not r or r[0]!='pending' or r[1]!=revision:raise ManagerError('request_no_longer_pending')
        if approve and (not eligible(db,user_id) or not verified(db,r[2])):raise ManagerError('customer_or_instance_not_eligible')
        state='approved' if approve else 'denied'
        db.execute('UPDATE firebase_link_requests SET state=?,reviewed_at=?,reviewed_by=? WHERE user_id=?',(state,int(time.time()),actor,user_id))
        audit(db,actor,'link_'+state,user_id)
        enqueue(db,f'decision:{user_id}:{revision}', 'customer_decision',user_id,{'state':state})
        return state

def disable(chat,label,expected_customer=...):
    with transaction() as db:
        actor=owner(db,chat);r=db.execute('SELECT id FROM firebase_instances WHERE label=?',(label,)).fetchone()
        if not r:raise ManagerError('unknown_instance')
        current=db.execute('SELECT u.login_id FROM firebase_instances i LEFT JOIN users u ON u.id=i.assigned_user_id WHERE i.id=?',r).fetchone()[0]
        if expected_customer is not ... and current!=expected_customer:raise ManagerError('assignment_changed_reconfirm_required')
        db.execute('UPDATE firebase_instances SET active=0 WHERE id=?',r)
        db.execute("UPDATE firebase_manager_instances SET state='DISABLED' WHERE instance_id=?",r)
        audit(db,actor,'disabled',r[0])

def manual_assign(chat,label,login):
    from firebase_pool import eligible
    with transaction() as db:
        actor=owner(db,chat)
        u=db.execute('SELECT id FROM users WHERE login_id=?',(login,)).fetchone()
        i=db.execute('SELECT id,assigned_user_id FROM firebase_instances WHERE label=?',(label,)).fetchone()
        if not u or not i or not eligible(db,u[0]) or not verified(db,i[0]):raise ManagerError('assignment_not_eligible')
        old=db.execute('SELECT id FROM firebase_instances WHERE assigned_user_id=?',(u[0],)).fetchone()
        if old:
            if old[0]==i[0]:return 'Assignment already recorded.'
            raise ManagerError('customer_already_assigned')
        if i[1] is not None:raise ManagerError('instance_already_assigned')
        db.execute('UPDATE firebase_instances SET assigned_user_id=?,assigned_at=? WHERE id=?',(u[0],int(time.time()),i[0]))
        db.execute("UPDATE firebase_manager_instances SET state='ASSIGNED' WHERE instance_id=?",(i[0],));audit(db,actor,'assigned',i[0])
        return 'Dedicated assignment recorded.'
