"""Server-side aliases only. No credentials are accepted over Telegram or returned to clients."""
import json,os,re,time,stat
from pathlib import Path
from urllib.parse import urlsplit
REGIONS=('us-central1','europe-west1','asia-southeast1')
RULES={'rules':{'.read':False,'.write':False}}
class ManagerError(RuntimeError):pass

def enabled():return os.environ.get('NEMESIS_FIREBASE_MANAGER_ENABLED')=='1'
def profiles():
    path=Path(os.environ.get('NEMESIS_FIREBASE_PROFILES','/etc/nemesis/firebase-manager.json'))
    if not path.is_absolute() or path.is_symlink() or path.stat().st_mode & 0o007:raise ManagerError('profile_configuration_unavailable')
    data=json.loads(path.read_text())
    if not isinstance(data,dict) or len(data)>20:raise ManagerError('invalid_profiles')
    for alias,p in data.items():
        if not re.fullmatch(r'[A-Za-z0-9_-]{2,40}',alias) or not re.fullmatch(r'[a-z][a-z0-9-]{4,28}[a-z0-9]',p['project_id']) or not re.fullmatch(r'[0-9]{5,20}',str(p['project_number'])) or p['region'] not in REGIONS:raise ManagerError('invalid_profiles')
        if not re.fullmatch(r'[A-Za-z0-9._-]+@[a-z0-9-]+\.iam\.gserviceaccount\.com',p.get('runtime_service_account','')):raise ManagerError('runtime_service_identity_required')
        if not isinstance(p.get('create_enabled',False),bool) or not isinstance(p.get('billing_acknowledged',False),bool):raise ManagerError('invalid_creation_flags')
        if isinstance(p['max_instances'],bool) or not isinstance(p['max_instances'],int):raise ManagerError('invalid_budget_limit')
        if not 1<=int(p['max_instances'])<=1000:raise ManagerError('invalid_budget_limit')
        if not re.fullmatch('[a-f0-9]{64}',p.get('iam_policy_sha256','')) or p.get('iam_reviewed_until',0)<=time.time():raise ManagerError('iam_review_required')
        if p.get('credential_file'):
            f=Path(p['credential_file'])
            if not f.is_absolute() or not str(f).startswith('/etc/nemesis/firebase/') or f.is_symlink() or f.stat().st_mode & 0o007:raise ManagerError('unsafe_credential_file')
    return data

def profile(alias):
    p=profiles().get(alias)
    if not p:raise ManagerError('unknown_project_alias')
    return p

def identity(url):
    if not isinstance(url,str) or len(url)>250:raise ManagerError('invalid_database_url')
    u=urlsplit(url)
    if u.scheme!='https' or u.username or u.password or u.port is not None or u.path not in ('','/') or u.query or u.fragment:raise ManagerError('invalid_database_url')
    host=u.hostname or ''
    m=re.fullmatch(r'([a-z][a-z0-9-]{2,61}[a-z0-9])(?:\.([a-z0-9-]+))?\.(firebaseio\.com|firebasedatabase\.app)',host)
    if not m:raise ManagerError('invalid_database_url')
    db,region,suffix=m.groups()
    if suffix=='firebaseio.com' and region is None:region='us-central1'
    elif suffix!='firebasedatabase.app' or region not in REGIONS or region=='us-central1':raise ManagerError('unsupported_database_location')
    return 'https://'+host,db,region

def label(value):
    if not isinstance(value,str) or not re.fullmatch('[A-Za-z0-9_-]{2,48}',value):raise ManagerError('invalid_label')
    return value
