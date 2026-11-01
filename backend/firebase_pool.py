"""Firebase instance inventory and isolation-aware allocation.
No Firebase credentials or URLs are ever returned by status or allocation.
A database URL is not a security boundary; Firebase Rules are required.
"""
import sqlite3
import time
from account_store import connect

def init():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS firebase_instances (
            id INTEGER PRIMARY KEY,
            label TEXT UNIQUE NOT NULL,
            database_url TEXT UNIQUE NOT NULL,
            credential_path TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            assigned_user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE RESTRICT,
            added_at INTEGER NOT NULL,
            assigned_at INTEGER
        );
        CREATE TABLE IF NOT EXISTS firebase_link_requests (
            user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            state TEXT NOT NULL CHECK(state IN ('pending','approved','denied')),
            requested_at INTEGER NOT NULL,
            reviewed_at INTEGER,
            reviewed_by INTEGER REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS firebase_audit (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            action TEXT NOT NULL,
            actor_id INTEGER,
            created_at INTEGER NOT NULL
        );
        ''')

    from firebase_migration import migrate
    migrate()

def eligible(db,user_id):
    r=db.execute('SELECT role,is_active,expires_at FROM users WHERE id=?',(user_id,)).fetchone()
    return bool(r and r[0]=='user' and r[1] and r[2] is not None and r[2]>int(time.time()))

def assignment(db,user_id):
    return db.execute('SELECT id,label FROM firebase_instances WHERE assigned_user_id=?',(user_id,)).fetchone()

def allocate(db,user_id):
    """Must be called in an IMMEDIATE transaction; no reallocation on renewal."""
    if not eligible(db,user_id):return None
    old=assignment(db,user_id)
    if old:return old
    if not eligible(db,user_id):return None
    candidate=db.execute("SELECT i.id,i.label FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.active=1 AND i.assigned_user_id IS NULL AND m.state='AVAILABLE' AND m.verified_at>? ORDER BY i.id LIMIT 1",(int(time.time())-86400,)).fetchone()
    if candidate:
        db.execute('UPDATE firebase_instances SET assigned_user_id=?,assigned_at=? WHERE id=? AND assigned_user_id IS NULL',(user_id,int(time.time()),candidate[0]))
        db.execute('INSERT INTO firebase_audit(user_id,action,created_at) VALUES(?,?,?)',(user_id,'assigned',int(time.time())))
        db.execute("UPDATE firebase_manager_instances SET state='ASSIGNED' WHERE instance_id=?",(candidate[0],))
        from firebase_manager_store import audit,enqueue
        audit(db,None,'assigned',candidate[0])
        enqueue(db,'assignment:'+str(user_id),'customer_assignment',user_id)
    from firebase_manager_store import enqueue
    import os
    try:threshold=max(0,min(50,int(os.environ.get('NEMESIS_FIREBASE_MIN_AVAILABLE','3'))))
    except ValueError:threshold=3
    available=db.execute("SELECT COUNT(*) FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.active=1 AND i.assigned_user_id IS NULL AND m.state='AVAILABLE' AND m.verified_at>?",(int(time.time())-86400,)).fetchone()[0]
    if available<threshold:enqueue(db,'low-pool:'+str(int(time.time())//3600),'owner_low_pool')
    return candidate

def get_or_assign(user_id):
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if not eligible(db,user_id):return None
        return allocate(db,user_id)

def summary(user_id):
    inst=get_or_assign(user_id)
    if not inst:return {'assigned':False,'status':'awaiting_available_database','link_request':'unavailable'}
    with connect() as db:
        r=db.execute('SELECT state FROM firebase_link_requests WHERE user_id=?',(user_id,)).fetchone()
        meta=db.execute('SELECT state FROM firebase_manager_instances WHERE instance_id=?',(inst[0],)).fetchone()
    return {'instance_state':meta[0] if meta else 'VALIDATING','assigned':True,'status':'assigned','instance_label':inst[1], 'link_request':r[0] if r else 'not_requested'}

def request_link(user_id):
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if not eligible(db,user_id):return 'not_eligible'
        inst=allocate(db,user_id)
        if not inst:return 'awaiting_available_database'
        from firebase_manager_store import verified,enqueue
        if not verified(db,inst[0]):return 'validation_required'
        old=db.execute('SELECT state FROM firebase_link_requests WHERE user_id=?',(user_id,)).fetchone()
        if old and old[0] in ('pending','approved'):return old[0]
        now=int(time.time())
        db.execute('INSERT INTO firebase_link_requests(user_id,state,requested_at,reviewed_at,reviewed_by) VALUES(?,\'pending\',?,NULL,NULL) ON CONFLICT(user_id) DO UPDATE SET state=\'pending\',requested_at=excluded.requested_at,reviewed_at=NULL,reviewed_by=NULL',(user_id,now))
        db.execute('INSERT INTO firebase_audit(user_id,action,created_at) VALUES(?,?,?)',(user_id,'link_requested',now))
        db.execute('INSERT INTO firebase_manager_request_versions VALUES(?,1) ON CONFLICT(user_id) DO UPDATE SET revision=revision+1',(user_id,))
        revision=db.execute('SELECT revision FROM firebase_manager_request_versions WHERE user_id=?',(user_id,)).fetchone()[0]
        enqueue(db,f'request:{user_id}:{revision}','owner_request',user_id,{'revision':revision})
        return 'pending'

def approved_url(user_id):
    """Called only for currently active authenticated customer; never a credential."""
    with connect() as db:
        if not eligible(db,user_id):return None
        from firebase_manager_store import verified
        inst=assignment(db,user_id)
        if not inst or not verified(db,inst[0]):return None
        r=db.execute('''SELECT i.database_url FROM firebase_instances i JOIN firebase_link_requests q ON q.user_id=i.assigned_user_id WHERE i.assigned_user_id=? AND q.state='approved' AND i.active=1''',(user_id,)).fetchone()
    return r[0] if r else None
