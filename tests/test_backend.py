"""Isolated source tests: temporary SQLite only, no Telegram/Firebase network calls."""
import sys,time,secrets
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
import account_store,auth_api,registration_store,firebase_pool,telegram_link
from fastapi import HTTPException

@pytest.fixture
def db(tmp_path,monkeypatch):
    monkeypatch.setattr(account_store,'DB_PATH',tmp_path/'test.sqlite3')
    account_store.initialize();auth_api.init();registration_store.init();firebase_pool.init();telegram_link.initialize()
    now=int(time.time())
    with account_store.connect() as c:
        for name,role,chat,expiry in [('SyntheticOwner','owner',10001,None),('SyntheticCustomer','user',10002,now+86400),('SyntheticOther','user',10003,now+86400)]:
            c.execute('INSERT INTO users(login_id,password_hash,role,telegram_chat_id,expires_at,created_at) VALUES(?,?,?,?,?,?)',(name,account_store.HASHER.hash(secrets.token_urlsafe(24)),role,chat,expiry,now))
    return now

def challenge(db,uid=1):
    key=secrets.token_urlsafe(32);code=f'{secrets.randbelow(1000000):06d}'
    with account_store.connect() as c:c.execute('INSERT INTO auth_challenges VALUES(?,?,?,?,0,?)',(auth_api.digest(key),uid,auth_api.digest(key+':'+code),db+300,db))
    return key,code

def test_owner_session_otp_replay_logout(db):
    key,code=challenge(db);result=auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
    token=result['access_token'];user=auth_api.get_user(token)
    assert auth_api.me(user)['expires_at'] is None
    with pytest.raises(HTTPException):auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
    from fastapi.security import HTTPAuthorizationCredentials
    auth_api.logout(HTTPAuthorizationCredentials(scheme='Bearer',credentials=token))
    with pytest.raises(HTTPException):auth_api.get_user(token)

def test_customer_session_bounded_by_subscription(db):
    key,code=challenge(db,2);token=auth_api.verify(auth_api.Verify(challenge_id=key,code=code))['access_token']
    assert auth_api.me(auth_api.get_user(token))['role']=='user'
    with account_store.connect() as c:c.execute('UPDATE users SET expires_at=? WHERE id=2',(db-1,))
    with pytest.raises(HTTPException):auth_api.get_user(token)

@pytest.mark.xfail(strict=True,reason='Preserved source rolls back failed-OTP attempt increments on HTTPException; approval-required fix')
def test_three_wrong_attempts_are_persisted(db):
    key,code=challenge(db);wrong=f'{(int(code)+1)%1000000:06d}'
    for _ in range(3):
        with pytest.raises(HTTPException):auth_api.verify(auth_api.Verify(challenge_id=key,code=wrong))
    with account_store.connect() as c:assert c.execute('SELECT attempts FROM auth_challenges').fetchone()[0]==3

def test_firebase_approval_and_customer_isolation(db):
    with account_store.connect() as c:c.execute('INSERT INTO firebase_instances(label,database_url,credential_path,added_at) VALUES(?,?,?,?)',('synthetic','https://synthetic-test.firebaseio.com','/isolated/nonexistent.json',db))
    assert firebase_pool.summary(2)['assigned'] is True
    assert firebase_pool.summary(3)['assigned'] is False
    assert firebase_pool.approved_url(2) is None
    assert firebase_pool.request_link(2)=='pending'
    with account_store.connect() as c:c.execute("UPDATE firebase_link_requests SET state='approved' WHERE user_id=2")
    assert firebase_pool.approved_url(2)=='https://synthetic-test.firebaseio.com'
    assert firebase_pool.approved_url(3) is None

def test_registration_activation_and_key_single_use(db):
    key=registration_store.new_key(10001).splitlines()[-1]
    assert 'reserved' in registration_store.redeem(10004,key)
    assert 'reserved' in registration_store.setid(10004,'SyntheticNew')
    token=registration_store.setup(10004,'https://example.invalid').split('#')[-1]
    ok,_=registration_store.activate(token,secrets.token_urlsafe(24));assert ok
    assert not registration_store.activate(token,secrets.token_urlsafe(24))[0]

def test_source_syntax_and_checksum():
    import ast,hashlib
    root=Path(__file__).resolve().parents[1]
    for line in (root/'docs/BACKEND_EXPORT_SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split(maxsplit=1);p=root/name.lstrip('*');assert hashlib.sha256(p.read_bytes()).hexdigest()==digest;ast.parse(p.read_text())

def test_http_profile_and_firebase_authorization(db):
    from fastapi.testclient import TestClient
    import main
    client=TestClient(main.app)
    assert client.get('/auth/me').status_code==401
    assert client.get('/firebase/status').status_code==401
    key,code=challenge(db,2)
    result=client.post('/auth/verify',json={'challenge_id':key,'code':code})
    assert result.status_code==200
    headers={'Authorization':'Bearer '+result.json()['access_token']}
    assert client.get('/auth/me',headers=headers).json()['login_id']=='SyntheticCustomer'
    assert client.get('/firebase/approved-link',headers=headers).status_code==403
    assert client.post('/auth/logout',headers=headers).status_code==200
    assert client.get('/auth/me',headers=headers).status_code==401
