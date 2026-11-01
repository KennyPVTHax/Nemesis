"""Additive v1 migration. Old accounts/auth tables and assignment values are untouched."""
import time
from account_store import connect
SCHEMA='''
CREATE TABLE IF NOT EXISTS firebase_manager_schema(version INTEGER PRIMARY KEY, applied_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_instances(
 instance_id INTEGER PRIMARY KEY REFERENCES firebase_instances(id), alias TEXT, resource TEXT UNIQUE,
 state TEXT NOT NULL CHECK(state IN ('PROVISIONING','VALIDATING','AVAILABLE','ASSIGNED','DISABLED','ERROR')),
 verified_at INTEGER, diagnostic TEXT, rules_hash TEXT);
CREATE TABLE IF NOT EXISTS firebase_assignment_ledger(
 instance_id INTEGER PRIMARY KEY REFERENCES firebase_instances(id),user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),assigned_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_audit(id INTEGER PRIMARY KEY,actor_id INTEGER,action TEXT NOT NULL,subject TEXT NOT NULL,created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_actions(hash TEXT PRIMARY KEY,chat_id INTEGER NOT NULL,message_id INTEGER,action TEXT NOT NULL,payload TEXT NOT NULL,expires_at INTEGER NOT NULL,used INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS firebase_manager_wizards(chat_id INTEGER PRIMARY KEY,stage TEXT NOT NULL,payload TEXT NOT NULL,expires_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_throttle(chat_id INTEGER PRIMARY KEY,window INTEGER NOT NULL,count INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_cloud_lock(id INTEGER PRIMARY KEY CHECK(id=1),job_id TEXT,lease_until INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_health(id INTEGER PRIMARY KEY CHECK(id=1),last_poll INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_seen(update_id INTEGER PRIMARY KEY,created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_jobs(id TEXT PRIMARY KEY,kind TEXT NOT NULL,label TEXT NOT NULL,alias TEXT NOT NULL,project_number TEXT NOT NULL,url TEXT,resource TEXT UNIQUE,actor_chat INTEGER NOT NULL,phase TEXT NOT NULL DEFAULT 'INIT',state TEXT NOT NULL DEFAULT 'PENDING',attempts INTEGER NOT NULL DEFAULT 0,lease_until INTEGER NOT NULL DEFAULT 0,next_at INTEGER NOT NULL DEFAULT 0,diagnostic TEXT,instance_id INTEGER,result TEXT,created_at INTEGER NOT NULL,UNIQUE(kind,alias,label));
CREATE TABLE IF NOT EXISTS firebase_manager_request_versions(user_id INTEGER PRIMARY KEY,revision INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS firebase_manager_outbox(id INTEGER PRIMARY KEY,event_key TEXT UNIQUE NOT NULL,kind TEXT NOT NULL,user_id INTEGER,payload TEXT NOT NULL DEFAULT '{}',state TEXT NOT NULL DEFAULT 'PENDING',attempts INTEGER NOT NULL DEFAULT 0,next_at INTEGER NOT NULL DEFAULT 0,lease_until INTEGER NOT NULL DEFAULT 0);
CREATE TRIGGER IF NOT EXISTS firebase_assignment_no_reuse BEFORE UPDATE OF assigned_user_id ON firebase_instances
 WHEN OLD.assigned_user_id IS NOT NULL AND NEW.assigned_user_id IS NOT OLD.assigned_user_id BEGIN SELECT RAISE(ABORT,'Assignment is permanent'); END;
CREATE TRIGGER IF NOT EXISTS firebase_assignment_record AFTER UPDATE OF assigned_user_id ON firebase_instances
 WHEN NEW.assigned_user_id IS NOT NULL AND OLD.assigned_user_id IS NULL BEGIN
 INSERT INTO firebase_assignment_ledger VALUES(NEW.id,NEW.assigned_user_id,COALESCE(NEW.assigned_at,0)); END;
CREATE TRIGGER IF NOT EXISTS firebase_assignment_insert AFTER INSERT ON firebase_instances WHEN NEW.assigned_user_id IS NOT NULL BEGIN
 INSERT INTO firebase_assignment_ledger VALUES(NEW.id,NEW.assigned_user_id,COALESCE(NEW.assigned_at,0)); END;
CREATE TRIGGER IF NOT EXISTS firebase_assignment_no_delete BEFORE DELETE ON firebase_instances WHEN OLD.assigned_user_id IS NOT NULL BEGIN SELECT RAISE(ABORT,'Assigned database cannot be deleted'); END;
CREATE TRIGGER IF NOT EXISTS firebase_ledger_no_update BEFORE UPDATE ON firebase_assignment_ledger BEGIN SELECT RAISE(ABORT,'Immutable assignment ledger'); END;
CREATE TRIGGER IF NOT EXISTS firebase_ledger_no_delete BEFORE DELETE ON firebase_assignment_ledger BEGIN SELECT RAISE(ABORT,'Immutable assignment ledger'); END;
'''

def migrate():
    # executescript commits implicitly: an explicit transaction in the script makes DDL/data atomic.
    with connect() as db:
        try:
            db.executescript('BEGIN IMMEDIATE;'+SCHEMA)
            db.execute("INSERT OR IGNORE INTO firebase_manager_instances(instance_id,state,diagnostic) SELECT id,CASE WHEN active=0 THEN 'DISABLED' ELSE 'VALIDATING' END,'import_requires_verification' FROM firebase_instances")
            db.execute('INSERT OR IGNORE INTO firebase_assignment_ledger SELECT id,assigned_user_id,COALESCE(assigned_at,0) FROM firebase_instances WHERE assigned_user_id IS NOT NULL')
            db.execute('INSERT OR IGNORE INTO firebase_manager_request_versions SELECT user_id,1 FROM firebase_link_requests')
            db.execute('INSERT OR IGNORE INTO firebase_manager_schema VALUES(1,?)',(int(time.time()),))
            db.commit()
        except Exception:db.rollback();raise
