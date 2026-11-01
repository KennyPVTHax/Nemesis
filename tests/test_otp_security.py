"""Synthetic challenges and temporary SQLite only; no production credentials or network."""
from concurrent.futures import ThreadPoolExecutor
import threading
import sqlite3
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from test_backend import db, challenge
import auth_api, account_store


def wrong(code):
    return f'{(int(code)+1)%1000000:06d}'


def denied(key, code):
    with pytest.raises(HTTPException) as error:
        auth_api.verify(auth_api.Verify(challenge_id=key, code=code))
    assert error.value.status_code == 401
    assert error.value.detail == 'Authentication failed'


def counts(key):
    # New connection observes committed state, not the verifying connection's cache.
    with account_store.connect() as conn:
        row=conn.execute('SELECT attempts FROM auth_challenges WHERE id_hash=?',(auth_api.digest(key),)).fetchone()
        sessions=conn.execute('SELECT COUNT(*) FROM auth_sessions').fetchone()[0]
    return row[0] if row else None, sessions


def test_one_failure_is_durable_and_correct_code_still_works(db):
    key,code=challenge(db)
    denied(key,wrong(code))
    assert counts(key)==(1,0)
    result=auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
    assert set(result)=={'access_token','token_type','expires_in'}
    assert result['token_type']=='bearer' and result['expires_in']==28800
    assert counts(key)==(None,1)


def test_lockout_rejects_correct_code_and_additional_guesses(db):
    key,code=challenge(db)
    for expected in range(1,4):
        denied(key,wrong(code));assert counts(key)==(expected,0)
    denied(key,code);denied(key,wrong(code))
    assert counts(key)==(3,0)


def test_expired_challenge_rejects_correct_and_wrong_codes(db):
    key,code=challenge(db)
    with account_store.connect() as conn:conn.execute('UPDATE auth_challenges SET expires_at=?',(db-1,))
    denied(key,code);denied(key,wrong(code))
    assert counts(key)==(0,0)


def test_expiry_boundary_is_exclusive(db,monkeypatch):
    key,code=challenge(db)
    monkeypatch.setattr(auth_api,'time',SimpleNamespace(time=lambda:db+300))
    denied(key,code)
    assert counts(key)==(0,0)


def test_expiry_is_checked_after_writer_lock_wait(db,monkeypatch):
    key,code=challenge(db)
    now=[db+299];waiting=threading.Event();original=account_store.connect
    monkeypatch.setattr(auth_api,'time',SimpleNamespace(time=lambda:now[0]))
    class WaitingConnection:
        def __init__(self):self.conn=original()
        def __enter__(self):self.conn.__enter__();return self
        def __exit__(self,*args):
            try:return self.conn.__exit__(*args)
            finally:self.conn.close()
        def execute(self,sql,*args):
            if sql=='BEGIN IMMEDIATE':waiting.set()
            return self.conn.execute(sql,*args)
    monkeypatch.setattr(auth_api,'connect',WaitingConnection)
    holder=original();holder.execute('BEGIN IMMEDIATE')
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future=pool.submit(denied,key,code)
            try:
                assert waiting.wait(5)
                now[0]=db+301
            finally:holder.commit()
            future.result(timeout=5)
    finally:holder.close()
    assert counts(key)==(0,0)


def race(key, codes):
    barrier=threading.Barrier(len(codes))
    def submit(code):
        barrier.wait(timeout=5)
        try:
            auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
            return 200
        except HTTPException as error:return error.status_code
    with ThreadPoolExecutor(max_workers=len(codes)) as pool:
        return list(pool.map(submit,codes))


def test_concurrent_wrong_submissions_cannot_exceed_three_failures(db):
    key,code=challenge(db)
    assert race(key,[wrong(code)]*8)==[401]*8
    assert counts(key)==(3,0)
    denied(key,code)


def test_concurrent_correct_submissions_create_exactly_one_session(db):
    key,code=challenge(db)
    statuses=race(key,[code]*8)
    assert statuses.count(200)==1 and statuses.count(401)==7
    assert counts(key)==(None,1)
    denied(key,code)
    assert counts(key)==(None,1)


def test_mixed_race_at_last_attempt_is_serialized(db):
    key,code=challenge(db)
    denied(key,wrong(code));denied(key,wrong(code))
    statuses=race(key,[wrong(code)]*5+[code])
    assert statuses.count(200) in (0,1)
    assert counts(key)==((None,1) if 200 in statuses else (3,0))
    denied(key,code)


@pytest.mark.parametrize('change',["is_active=0","expires_at=0"])
def test_ineligible_customer_cannot_create_session(db,change):
    key,code=challenge(db,2)
    with account_store.connect() as conn:conn.execute('UPDATE users SET '+change+' WHERE id=2')
    denied(key,code)
    assert counts(key)==(0,0)


def test_session_insert_failure_rolls_back_challenge_consumption(db):
    key,code=challenge(db)
    with account_store.connect() as conn:
        conn.execute("CREATE TRIGGER reject_session BEFORE INSERT ON auth_sessions BEGIN SELECT RAISE(ABORT,'synthetic insert failure'); END")
    with pytest.raises(sqlite3.IntegrityError):auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
    assert counts(key)==(0,0)
    with account_store.connect() as conn:conn.execute('DROP TRIGGER reject_session')
    auth_api.verify(auth_api.Verify(challenge_id=key,code=code))
    assert counts(key)==(None,1)


def test_unknown_challenge_discloses_no_state(db):
    import secrets
    key=secrets.token_urlsafe(32)
    denied(key,'000000')
    assert counts(key)==(None,0)


def test_android_wire_contract_full_login_without_external_delivery(db,monkeypatch):
    import secrets
    from fastapi.testclient import TestClient
    import main
    password=secrets.token_urlsafe(24);delivery={}
    with account_store.connect() as conn:
        conn.execute('UPDATE users SET password_hash=?,expires_at=? WHERE id=2',(account_store.HASHER.hash(password),db+3600))
    client=TestClient(main.app)
    class DeliveryClient:
        def __init__(self,**kwargs):pass
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def post(self,url,json):
            assert url.endswith('/sendMessage')
            delivery['code']=json['text'].splitlines()[0].rsplit(' ',1)[1]
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:{'ok':True})
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN','synthetic-'+secrets.token_urlsafe(24))
    monkeypatch.setattr(auth_api.httpx,'Client',DeliveryClient)
    login=client.post('/auth/login',json={'login_id':'SyntheticCustomer','password':password})
    assert login.status_code==200
    data=login.json();assert set(data)=={'challenge_id','expires_in','message'}
    assert data['expires_in']==300
    key=data['challenge_id']
    with account_store.connect() as conn:
        expiry,created=conn.execute('SELECT expires_at,created_at FROM auth_challenges WHERE id_hash=?',(auth_api.digest(key),)).fetchone()
        assert expiry-created==300
    malformed=client.post('/auth/verify',json={'challenge_id':key,'code':'bad'})
    assert malformed.status_code==422 and counts(key)==(0,0)
    failed=client.post('/auth/verify',json={'challenge_id':key,'code':wrong(delivery['code'])})
    assert failed.status_code==401 and failed.json()=={'detail':'Authentication failed'}
    assert counts(key)==(1,0)
    verified=client.post('/auth/verify',json={'challenge_id':key,'code':delivery['code']})
    assert verified.status_code==200
    result=verified.json();assert set(result)=={'access_token','token_type','expires_in'}
    assert result['token_type']=='bearer' and result['expires_in']==28800
    headers={'Authorization':'Bearer '+result['access_token']}
    profile=client.get('/auth/me',headers=headers)
    assert profile.json()=={'login_id':'SyntheticCustomer','role':'user','is_active':True,'expires_at':db+3600}
    with account_store.connect() as conn:
        assert conn.execute('SELECT expires_at FROM auth_sessions').fetchone()[0]==db+3600
    assert client.post('/auth/verify',json={'challenge_id':key,'code':delivery['code']}).status_code==401
    assert client.post('/auth/logout',headers=headers).json()=={'status':'logged_out'}
    assert client.get('/auth/me',headers=headers).status_code==401


def test_failed_commit_never_returns_authentication_denial(db,monkeypatch):
    key,code=challenge(db);original=account_store.connect
    class FailedCommit:
        def __init__(self):self.conn=original()
        def __enter__(self):self.conn.__enter__();return self.conn
        def __exit__(self,*args):
            self.conn.rollback();self.conn.close()
            raise sqlite3.OperationalError('Synthetic commit failure')
    monkeypatch.setattr(auth_api,'connect',FailedCommit)
    with pytest.raises(sqlite3.OperationalError):auth_api.verify(auth_api.Verify(challenge_id=key,code=wrong(code)))
    assert counts(key)==(0,0)
    monkeypatch.setattr(auth_api,'connect',original)
    denied(key,wrong(code));assert counts(key)==(1,0)
