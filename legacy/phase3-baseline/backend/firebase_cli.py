"""Root/operator-only Firebase inventory administration, no remote admin endpoints."""
import argparse,os,sys,json,re,time,sqlite3
from pathlib import Path
from urllib.parse import urlparse
from account_store import connect
from firebase_pool import init,allocate

def strict_url(s):
    u=urlparse(s)
    if u.scheme!='https' or u.port is not None or u.username or u.password or u.path not in ('','/') or u.query or u.fragment or not re.fullmatch(r'[a-z0-9-]+\.(?:firebaseio\.com|firebasedatabase\.app)',u.hostname or ''):
        raise ValueError('Expected exact HTTPS Realtime Database URL under firebaseio.com or firebasedatabase.app')
    return 'https://'+u.hostname

def run():
    p=argparse.ArgumentParser(description='NEMESIS Firebase pool operator CLI')
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('add');a.add_argument('label');a.add_argument('database_url');a.add_argument('credentials_file')
    sub.add_parser('list')
    sub.add_parser('allocate-all')
    sub.add_parser('requests')
    for action in ('approve','deny'):
        x=sub.add_parser(action);x.add_argument('login_id');x.add_argument('--actor',default='NemesisOwner')
    args=p.parse_args()
    init()
    if args.cmd=='add':
        if not re.fullmatch('[A-Za-z0-9_-]{2,48}',args.label):p.error('Invalid instance label')
        try:url=strict_url(args.database_url)
        except ValueError as e:p.error(str(e))
        f=Path(args.credentials_file)
        if not f.is_file() or not f.is_absolute() or not str(f).startswith('/etc/nemesis/firebase/') or f.is_symlink():p.error('Credentials must be a regular file inside /etc/nemesis/firebase/')
        if f.stat().st_mode & 0o007:p.error('Credentials must not be readable by others (use chmod 640 with root:nemesis or 600 with nemesis owner)')
        data=json.loads(f.read_text())
        if data.get('type')!='service_account' or not data.get('project_id') or not data.get('client_email') or not data.get('private_key'):p.error('Invalid Firebase service account JSON')
        with connect() as db:
            db.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',(args.label,url,str(f),int(time.time())))
        print('Instance added:',args.label,'(not yet connectivity verified)')
    elif args.cmd=='list':
        with connect() as db:
            rows=db.execute('''SELECT f.label,f.active,u.login_id FROM firebase_instances f LEFT JOIN users u ON u.id=f.assigned_user_id ORDER BY f.id''').fetchall()
        for label,active,user in rows:print(label,'active' if active else 'disabled','assigned:'+user if user else 'unassigned')
        print('TOTAL:',len(rows))
    elif args.cmd=='allocate-all':
        count=0
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            users=db.execute("SELECT id FROM users WHERE role='user' AND is_active=1 AND expires_at>? ORDER BY id",(int(time.time()),)).fetchall()
            for (uid,) in users:
                before=db.execute('SELECT id FROM firebase_instances WHERE assigned_user_id=?',(uid,)).fetchone()
                assigned=allocate(db,uid)
                if assigned and not before:count+=1
        print('New customer allocations:',count)
    elif args.cmd=='requests':
        with connect() as db:
            rows=db.execute('''SELECT u.login_id,r.state,f.label FROM firebase_link_requests r JOIN users u ON u.id=r.user_id LEFT JOIN firebase_instances f ON f.assigned_user_id=u.id ORDER BY r.requested_at DESC''').fetchall()
        for login,state,label in rows:print(login,state,label or 'unassigned')
        print('TOTAL:',len(rows))
    else:
        state='approved' if args.cmd=='approve' else 'denied'
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            actor=db.execute("SELECT id FROM users WHERE login_id=? AND role='owner' AND is_active=1",(args.actor,)).fetchone()
            customer=db.execute("SELECT id FROM users WHERE login_id=? AND role='user'",(args.login_id,)).fetchone()
            if not actor or not customer:raise SystemExit('Owner actor or customer not found')
            row=db.execute('SELECT state FROM firebase_link_requests WHERE user_id=?',(customer[0],)).fetchone()
            if not row or row[0]!='pending':raise SystemExit('No pending customer link request')
            if state=='approved':
                if not db.execute('SELECT 1 FROM firebase_instances WHERE assigned_user_id=? AND active=1',(customer[0],)).fetchone():raise SystemExit('No active assigned database')
            db.execute('UPDATE firebase_link_requests SET state=?,reviewed_at=?,reviewed_by=? WHERE user_id=?',(state,int(time.time()),actor[0],customer[0]))
            db.execute('INSERT INTO firebase_audit(user_id,action,actor_id,created_at) VALUES(?,?,?,?)',(customer[0],'link_'+state,actor[0],int(time.time())))
        print(args.login_id,'request',state)

if __name__=='__main__':
    try:run()
    except sqlite3.IntegrityError:raise SystemExit('Conflict: duplicate label, URL, or assignment')
