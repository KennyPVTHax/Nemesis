import hashlib,hmac,os,secrets,sqlite3,time
from fastapi import APIRouter,HTTPException,Request,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from argon2.exceptions import VerifyMismatchError,VerificationError
from account_store import connect,HASHER
import httpx

router=APIRouter(prefix='/auth',tags=['auth'])
security=HTTPBearer(auto_error=False)

def init():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS auth_challenges(id_hash TEXT PRIMARY KEY,user_id INTEGER NOT NULL,code_hash TEXT NOT NULL,expires_at INTEGER NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,created_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS auth_sessions(token_hash TEXT PRIMARY KEY,user_id INTEGER NOT NULL,expires_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS auth_throttle(key TEXT PRIMARY KEY,attempts INTEGER NOT NULL,window_start INTEGER NOT NULL);
        ''')

def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def deny(code=401,detail='Authentication failed'):raise HTTPException(code,detail)
def throttle(key,limit=5,window=900):
    now=int(time.time())
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row=db.execute('SELECT attempts,window_start FROM auth_throttle WHERE key=?',(key,)).fetchone()
        if row and now-row[1]<window:
            if row[0]>=limit:deny(429,'Too many attempts; try again later')
            db.execute('UPDATE auth_throttle SET attempts=attempts+1 WHERE key=?',(key,))
        else:db.execute('INSERT OR REPLACE INTO auth_throttle VALUES(?,?,?)',(key,1,now))

def eligible(row):
    return bool(row and row[4] and (row[3]=='owner' or (row[5] is not None and row[5]>int(time.time()))))

def get_user(token):
    with connect() as db:
        row=db.execute('''SELECT u.id,u.login_id,u.telegram_chat_id,u.role,u.is_active,u.expires_at FROM auth_sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?''',(digest(token),int(time.time()))).fetchone()
    if not eligible(row):deny()
    return row

def current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    if not credentials or credentials.scheme.lower()!='bearer':deny()
    return get_user(credentials.credentials)

class Login(BaseModel):
    login_id:str=Field(min_length=1,max_length=64)
    password:str=Field(min_length=1,max_length=256)
class Verify(BaseModel):
    challenge_id:str=Field(min_length=20,max_length=200)
    code:str=Field(pattern=r'^\d{6}$')

@router.post('/login')
def login(body:Login,request:Request):
    throttle('login:'+digest(body.login_id.casefold()))
    throttle('ip:'+digest(request.client.host if request.client else 'unknown'),20)
    with connect() as db:
        row=db.execute('SELECT id,login_id,telegram_chat_id,role,is_active,expires_at,password_hash FROM users WHERE login_id=?',(body.login_id,)).fetchone()
    try:valid=bool(row and HASHER.verify(row[6],body.password))
    except (VerifyMismatchError,VerificationError):valid=False
    if not valid or not eligible(row[:6]):deny()
    if not row[2]:deny(403,'Telegram not linked')
    challenge=secrets.token_urlsafe(32);code=f'{secrets.randbelow(1000000):06d}';now=int(time.time())
    with connect() as db:
        db.execute('DELETE FROM auth_challenges WHERE user_id=?',(row[0],))
        db.execute('INSERT INTO auth_challenges VALUES(?,?,?,?,0,?)',(digest(challenge),row[0],digest(challenge+':'+code),now+300,now))
    token=os.environ['TELEGRAM_BOT_TOKEN']
    try:
        with httpx.Client(timeout=15) as client:
            response=client.post(f'https://api.telegram.org/bot{token}/sendMessage',json={'chat_id':row[2],'text':'NEMESIS login OTP: '+code+'\nExpires in 5 minutes.'})
            response.raise_for_status()
            if not response.json().get('ok'):raise ValueError('Telegram delivery failed')
    except Exception:
        with connect() as db:db.execute('DELETE FROM auth_challenges WHERE id_hash=?',(digest(challenge),))
        deny(503,'OTP delivery unavailable')
    return {'challenge_id':challenge,'expires_in':300,'message':'OTP sent to linked Telegram'}

@router.post('/verify')
def verify(body:Verify):
    now=int(time.time());key=digest(body.challenge_id)
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row=db.execute('SELECT user_id,code_hash,expires_at,attempts FROM auth_challenges WHERE id_hash=?',(key,)).fetchone()
        if not row or row[2]<=now or row[3]>=3:deny()
        db.execute('UPDATE auth_challenges SET attempts=attempts+1 WHERE id_hash=?',(key,))
        if not hmac.compare_digest(row[1],digest(body.challenge_id+':'+body.code)):deny()
        user=db.execute('SELECT id,login_id,telegram_chat_id,role,is_active,expires_at FROM users WHERE id=?',(row[0],)).fetchone()
        if not eligible(user):deny()
        db.execute('DELETE FROM auth_challenges WHERE id_hash=?',(key,))
        token=secrets.token_urlsafe(32)
        db.execute('INSERT INTO auth_sessions VALUES(?,?,?)',(digest(token),row[0],min(now+28800,user[5]) if user[3]!='owner' else now+28800))
    return {'access_token':token,'token_type':'bearer','expires_in':28800}

@router.get('/me')
def me(user=Depends(current_user)):
    return {'login_id':user[1],'role':user[3],'is_active':bool(user[4]),'expires_at':user[5]}

@router.post('/logout')
def logout(credentials:HTTPAuthorizationCredentials=Depends(security)):
    if not credentials:deny()
    with connect() as db:db.execute('DELETE FROM auth_sessions WHERE token_hash=?',(digest(credentials.credentials),))
    return {'status':'logged_out'}
