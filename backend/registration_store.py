import hashlib,hmac,secrets,time,sqlite3
from account_store import connect,HASHER

def hashval(v):return hashlib.sha256(v.encode()).hexdigest()
def init():
    with connect() as db:db.executescript('''
    CREATE TABLE IF NOT EXISTS redeem_keys(key_hash TEXT PRIMARY KEY,created_at INTEGER NOT NULL,expires_at INTEGER NOT NULL,redeemed_at INTEGER,redeemed_by TEXT);
    CREATE TABLE IF NOT EXISTS registrations(chat_id INTEGER PRIMARY KEY,key_hash TEXT NOT NULL,login_id TEXT COLLATE NOCASE,created_at INTEGER NOT NULL,expires_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS signup_tokens(token_hash TEXT PRIMARY KEY,chat_id INTEGER NOT NULL,expires_at INTEGER NOT NULL,issued_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS registration_throttle(chat_id INTEGER PRIMARY KEY,attempts INTEGER NOT NULL,window_start INTEGER NOT NULL);
    ''')

def new_key(chat_id):
    with connect() as db:
        if not db.execute("SELECT 1 FROM users WHERE role='owner' AND telegram_chat_id=? AND is_active=1",(chat_id,)).fetchone():return 'Owner only.'
        key='NM-'+secrets.token_urlsafe(24);now=int(time.time())
        db.execute('INSERT INTO redeem_keys(key_hash,created_at,expires_at) VALUES(?,?,?)',(hashval(key),now,now+30*86400))
    return 'New 30-day access key (one use; expires in 30 days):\n'+key

def redeem(chat_id,key):
    now=int(time.time())
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        throttle=db.execute('SELECT attempts,window_start FROM registration_throttle WHERE chat_id=?',(chat_id,)).fetchone()
        if throttle and now-throttle[1]<900:
            if throttle[0]>=5:return 'Too many attempts. Try again later.'
            db.execute('UPDATE registration_throttle SET attempts=attempts+1 WHERE chat_id=?',(chat_id,))
        else:db.execute('INSERT OR REPLACE INTO registration_throttle VALUES(?,?,?)',(chat_id,1,now))
        row=db.execute('SELECT expires_at,redeemed_at FROM redeem_keys WHERE key_hash=?',(hashval(key),)).fetchone()
        if not row or row[1] is not None or row[0]<=now:return 'Invalid or expired key.'
        existing=db.execute('SELECT login_id,expires_at FROM users WHERE telegram_chat_id=? AND role=\'user\'',(chat_id,)).fetchone()
        if existing:
            new_exp=max(now,existing[1] or now)+30*86400
            db.execute('UPDATE users SET expires_at=?,is_active=1 WHERE telegram_chat_id=?',(new_exp,chat_id))
            db.execute('UPDATE redeem_keys SET redeemed_at=?,redeemed_by=? WHERE key_hash=?',(now,existing[0],hashval(key)))
            return 'Renewal successful: 30 days added.'
        db.execute('INSERT OR REPLACE INTO registrations(chat_id,key_hash,login_id,created_at,expires_at) VALUES(?,?,NULL,?,?)',(chat_id,hashval(key),now,now+86400))
    return 'Key reserved. Choose your login ID with /setid NAME.'

def setid(chat_id,name):
    import re
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{2,31}',name):return 'Login ID must be 3–32 letters, digits or underscores; start with a letter.'
    now=int(time.time())
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        r=db.execute('SELECT key_hash,expires_at FROM registrations WHERE chat_id=?',(chat_id,)).fetchone()
        if not r or r[1]<=now:return 'First use /redeem KEY.'
        if db.execute('SELECT 1 FROM users WHERE login_id=?',(name,)).fetchone() or db.execute('SELECT 1 FROM registrations WHERE login_id=? AND chat_id<>? AND expires_at>?',(name,chat_id,now)).fetchone():return 'Login ID unavailable.'
        db.execute('UPDATE registrations SET login_id=? WHERE chat_id=?',(name,chat_id))
    return 'Login ID reserved: '+name+'\nUse /setup to receive your password setup link.'

def status(chat_id):
    with connect() as db:
        u=db.execute('SELECT login_id,expires_at FROM users WHERE telegram_chat_id=?',(chat_id,)).fetchone()
        r=db.execute('SELECT login_id,expires_at FROM registrations WHERE chat_id=?',(chat_id,)).fetchone()
    if u:return 'Account active: '+u[0]+'\nExpires (UTC epoch): '+str(u[1])
    if r:return 'Registration pending: '+str(r[0] or 'Login ID not chosen')
    return 'No pending registration. Use /redeem KEY.'

def setup(chat_id,base_url):
    now=int(time.time())
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row=db.execute('SELECT r.login_id,r.expires_at,k.expires_at,k.redeemed_at FROM registrations r JOIN redeem_keys k ON k.key_hash=r.key_hash WHERE r.chat_id=?',(chat_id,)).fetchone()
        if not row or not row[0] or row[1]<=now or row[2]<=now or row[3] is not None:return 'Complete /redeem and /setid first.'
        last=db.execute('SELECT issued_at FROM signup_tokens WHERE chat_id=? ORDER BY issued_at DESC LIMIT 1',(chat_id,)).fetchone()
        if last and now-last[0]<60:return 'Please wait 60 seconds before requesting another link.'
        db.execute('DELETE FROM signup_tokens WHERE chat_id=?',(chat_id,))
        token=secrets.token_urlsafe(32)
        db.execute('INSERT INTO signup_tokens VALUES(?,?,?,?)',(hashval(token),chat_id,now+600,now))
    return 'Private password setup link (10 minutes):\n'+base_url+'/register/#'+token

def activate(token,password):
    if len(password)<12 or len(password)>256:return False,'Password must be 12–256 characters.'
    if len(token)!=43:return False,'Invalid or expired link.'
    hashed=HASHER.hash(password);now=int(time.time())
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        t=db.execute('SELECT chat_id,expires_at FROM signup_tokens WHERE token_hash=?',(hashval(token),)).fetchone()
        if not t or t[1]<=now:return False,'Invalid or expired link.'
        r=db.execute('SELECT key_hash,login_id,expires_at FROM registrations WHERE chat_id=?',(t[0],)).fetchone()
        if not r or not r[1] or r[2]<=now:return False,'Registration expired.'
        k=db.execute('SELECT expires_at,redeemed_at FROM redeem_keys WHERE key_hash=?',(r[0],)).fetchone()
        if not k or k[0]<=now or k[1] is not None:return False,'Key expired or already used.'
        if db.execute('SELECT 1 FROM users WHERE login_id=? OR telegram_chat_id=?',(r[1],t[0])).fetchone():return False,'Account already exists.'
        db.execute('INSERT INTO users(login_id,password_hash,telegram_chat_id,role,is_active,created_at,expires_at) VALUES(?,?,?,\'user\',1,?,?)',(r[1],hashed,t[0],now,now+30*86400))
        from firebase_pool import allocate
        new_user_id=db.execute('SELECT id FROM users WHERE login_id=?',(r[1],)).fetchone()[0]
        allocate(db,new_user_id)
        db.execute('UPDATE redeem_keys SET redeemed_at=?,redeemed_by=? WHERE key_hash=?',(now,r[1],r[0]))
        db.execute('DELETE FROM registrations WHERE chat_id=?',(t[0],))
        db.execute('DELETE FROM signup_tokens WHERE chat_id=?',(t[0],))
    return True,'Account activated. You may now log in.'
