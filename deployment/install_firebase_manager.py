#!/usr/bin/env python3
"""Prepared source/dependency migration. No production action occurs on import."""
import argparse,fcntl,hashlib,json,os,shutil,sqlite3,subprocess,tempfile,time
from pathlib import Path
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/opt/nemesis');UNITS=('nemesis-api.service','nemesis-telegram.service')
class InstallError(RuntimeError):pass

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quiet(args,cwd=None):
    try:r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
    except Exception:raise InstallError('Local command failed or timed out; inspect privately.') from None
    if r.returncode:raise InstallError('Local command failed; inspect privately. No command output is published.')
    return r.stdout

def copy_atomic(source,target):
    target=Path(target);old=target.stat() if target.exists() else target.parent.stat()
    fd,name=tempfile.mkstemp(prefix='.firebase-install-',dir=target.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            os.fchown(f.fileno(),old.st_uid,old.st_gid);os.fchmod(f.fileno(),0o640)
            f.write(Path(source).read_bytes());f.flush();os.fsync(f.fileno())
        os.replace(name,target)
        fd=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
    finally:
        if os.path.exists(name):os.unlink(name)

class Installer:
    def __init__(self,base,source,manifest,backup_root,dropins,stop,restart,dependencies,migrate,health):
        self.base,self.source,self.backups=map(Path,(base,source,backup_root));self.manifest=manifest;self.dropins=dropins
        self.stop,self.restart,self.dependencies,self.migrate,self.health=stop,restart,dependencies,migrate,health
    def verify(self):
        for name,hashes in self.manifest.items():
            if Path(name).name!=name or not name.endswith(('.py','.txt')):raise InstallError('Invalid payload path.')
            candidate=self.source/name;target=self.base/'backend'/name
            if candidate.is_symlink() or digest(candidate)!=hashes['current']:raise InstallError('Candidate checksum mismatch.')
            if target.exists() and (target.is_symlink() or digest(target) not in {hashes['current'],hashes.get('original')}):raise InstallError('Production source drift; refuse overwrite.')
            if hashes.get('original') and not target.is_file():raise InstallError('Required baseline source is missing.')
        for p in [self.base/'backend',self.base/'.venv',self.base/'data/accounts.sqlite3']:
            if p.is_symlink() or p.resolve()!=p or not p.exists():raise InstallError('Unexpected production path.')
        if not self.health(False):raise InstallError('Existing API/bot health failed.')
    def apply(self,enabled=False):
        self.verify()
        marker=self.base/'data/firebase-manager-install.json'
        if marker.exists():
            saved=json.loads(marker.read_text())
            if saved.get('enabled')==enabled and all((self.base/'backend'/n).is_file() and digest(self.base/'backend'/n)==v['current'] for n,v in self.manifest.items()):
                if not self.health(True):raise InstallError('Installed source found but API/bot verification failed.')
                return Path(saved['backup'])
        self.backups.mkdir(parents=True,exist_ok=True,mode=0o700)
        backup=Path(tempfile.mkdtemp(prefix='firebase-manager-',dir=self.backups));backup.chmod(0o700)
        shutil.copytree(self.base/'backend',backup/'backend',symlinks=True)
        shutil.copytree(self.base/'.venv',backup/'venv',symlinks=True)
        saved={}
        for name,p in self.dropins.items():
            saved[name]=str(p);(backup/('dropin-'+name)).write_bytes(p.read_bytes() if p.exists() else b'')
        (backup/'metadata.json').write_text(json.dumps({'dropins':saved,'dropin_present':{name:p.exists() for name,p in self.dropins.items()},'files':self.manifest,'enabled':enabled}))
        try:self.stop()
        except Exception:
            self.restart();raise InstallError('Service stop failed; source unchanged and restart attempted.')
        try:
            src=sqlite3.connect('file:'+str(self.base/'data/accounts.sqlite3')+'?mode=ro',uri=True)
            dest=sqlite3.connect(backup/'accounts.sqlite3')
            try:src.backup(dest)
            finally:src.close();dest.close()
            (backup/'accounts.sqlite3').chmod(0o600)
            for name in self.manifest:copy_atomic(self.source/name,self.base/'backend'/name)
            self.dependencies();self.migrate()
            for p in self.dropins.values():
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text('[Service]\nEnvironment=NEMESIS_FIREBASE_MANAGER_ENABLED='+('1' if enabled else '0')+'\nEnvironment=NEMESIS_FIREBASE_GATEWAY_ENABLED=0\n')
            started=int(time.time());self.restart()
            if not self.health(True,started):raise InstallError('Post-install health failed.')
            marker.write_text(json.dumps({'backup':str(backup),'enabled':enabled}));marker.chmod(0o600)
            return backup
        except Exception:
            try:self.rollback(backup)
            except Exception:raise InstallError('Installation failed; automatic source/dependency recovery needs operator review. Protected backup: '+str(backup)) from None
            raise InstallError('Installation failed; previous source/dependencies restored. Database and additive tables retained. Backup: '+str(backup)) from None
    def rollback(self,backup):
        backup=Path(backup)
        if backup.is_symlink() or backup.resolve().parent!=self.backups.resolve() or not (backup/'metadata.json').is_file():raise InstallError('Invalid protected rollback directory.')
        metadata=json.loads((backup/'metadata.json').read_text())
        for name,hashes in metadata['files'].items():
            target=self.base/'backend'/name;old=backup/'backend'/name
            if target.exists() and digest(target) not in {hashes['current'],digest(old) if old.exists() else None}:raise InstallError('Source drift; refuse rollback overwrite.')
        unchanged=all((self.base/'backend'/name).exists()==(backup/'backend'/name).exists() and (not (backup/'backend'/name).exists() or digest(self.base/'backend'/name)==digest(backup/'backend'/name)) for name in metadata['files'])
        if unchanged and not (self.base/'data/firebase-manager-install.json').exists() and self.health(False):return
        self.stop()
        # Database is NEVER automatically restored: new registrations may have committed since restart.
        # Additive schema is compatible with the previous source and preserves permanent assignments.
        for name in metadata['files']:
            old=backup/'backend'/name;target=self.base/'backend'/name
            if old.exists():copy_atomic(old,target)
            elif target.exists():target.unlink()
        venv=self.base/'.venv'
        displaced=self.base/('.venv-firebase-failed-'+str(time.time_ns()))
        venv.rename(displaced)
        try:shutil.copytree(backup/'venv',venv,symlinks=True)
        except Exception:
            if venv.exists():shutil.rmtree(venv)
            displaced.rename(venv);raise
        shutil.rmtree(displaced)
        for name,p in self.dropins.items():
            data=(backup/('dropin-'+name)).read_bytes()
            if metadata['dropin_present'][name]:p.write_bytes(data)
            elif p.exists():p.unlink()
        marker=self.base/'data/firebase-manager-install.json'
        if marker.exists():marker.unlink()
        with sqlite3.connect(self.base/'data/accounts.sqlite3') as c:
            if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='firebase_manager_instances'").fetchone():
                c.execute("UPDATE firebase_instances SET active=0 WHERE id IN (SELECT instance_id FROM firebase_manager_instances WHERE state NOT IN ('AVAILABLE','ASSIGNED') OR verified_at IS NULL OR verified_at<=?)",(int(time.time())-86400,))
        self.restart()
        if not self.health(False):raise InstallError('Old source restored but service health requires private operator recovery.')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['check','apply','rollback'])
    parser.add_argument('--health-url',required=True);parser.add_argument('--enable-manager',action='store_true');parser.add_argument('--backup')
    args=parser.parse_args()
    from urllib.parse import urlsplit
    u=urlsplit(args.health_url)
    if u.scheme not in ('http','https') or u.hostname not in ('127.0.0.1','localhost','::1','nemesispanel.shop') or u.path!='/health' or u.username or u.password or u.query or u.fragment:raise InstallError('Use the verified API /health URL.')
    if u.hostname=='nemesispanel.shop' and u.scheme!='https':raise InstallError('Public health requires HTTPS.')
    if os.geteuid()!=0:raise InstallError('Root/operator approval required on the VPS.')
    for unit in UNITS:
        if quiet(['systemctl','show','-p','WorkingDirectory','--value',unit]).strip()!=b'/opt/nemesis/backend':raise InstallError('Verify unit working directories before installation.')
        command=quiet(['systemctl','show','-p','ExecStart','--value',unit])
        if b'/opt/nemesis/.venv/bin/' not in command or (b'main:app' not in command if unit==UNITS[0] else b'telegram_bot.py' not in command):raise InstallError('Unit executable does not match the reviewed configuration.')
    python=BASE/'.venv/bin/python'
    quiet([str(python),'-m','pip','check'])
    payload=json.loads((ROOT/'docs/phase3/BACKEND_PAYLOAD.json').read_text())
    def stop():
        for unit in reversed(UNITS):quiet(['systemctl','stop',unit])
    def restart():
        quiet(['systemctl','daemon-reload'])
        for unit in UNITS:quiet(['systemctl','restart',unit])
    def dependencies():
        quiet([str(python),'-m','pip','install','--disable-pip-version-check','--no-index','--find-links',str(BASE/'backups/firebase-manager/wheels'),'-r',str(ROOT/'deployment/requirements-firebase-manager.txt')])
        quiet([str(python),'-m','pip','check'])
        quiet([str(python),'-c','import google.auth,requests,fastapi,httpx,argon2,pydantic'])
        for name in payload:
            if name.endswith('.py'):quiet([str(python),'-c','import pathlib,sys;compile(pathlib.Path(sys.argv[1]).read_bytes(),"<reviewed-module>","exec")',str(BASE/'backend'/name)])
    def migrate():
        quiet([str(python),'-c','from firebase_pool import init;init()'],cwd=BASE/'backend')
        if args.enable_manager:quiet([str(python),'-c','from firebase_config import profiles;profiles()'],cwd=BASE/'backend')
    def health(new,started=0):
        for _ in range(20):
            try:
                for unit in UNITS:quiet(['systemctl','is-active','--quiet',unit])
                with urllib.request.urlopen(urllib.request.Request(args.health_url,headers={'Cache-Control':'no-store'}),timeout=3) as response:
                    data=json.loads(response.read(8192))
                if data.get('status')!='online' or data.get('service')!='NEMESIS Backend':raise ValueError()
                if new:
                    with sqlite3.connect('file:/opt/nemesis/data/accounts.sqlite3?mode=ro',uri=True) as c:
                        row=c.execute('SELECT last_poll FROM firebase_manager_health WHERE id=1').fetchone()
                        if not row or row[0]<max(started,int(time.time())-90):raise ValueError()
                return True
            except Exception:time.sleep(2)
        return False
    backups=BASE/'backups/firebase-manager';backups.mkdir(parents=True,exist_ok=True,mode=0o700)
    if backups.is_symlink() or backups.resolve()!=backups or backups.stat().st_uid!=0 or backups.stat().st_mode & 0o077:raise InstallError('Backup root must be root-owned mode 0700 without symlinks.')
    dropins={unit:Path('/etc/systemd/system')/(unit+'.d')/'firebase-manager.conf' for unit in UNITS}
    tool=Installer(BASE,ROOT/'backend',payload,backups,dropins,stop,restart,dependencies,migrate,health)
    with open(backups/'.installation.lock','w') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        if args.action=='check':tool.verify();print('Source/configuration/dependency baseline verified; no installation performed.')
        elif args.action=='apply':
            tool.verify()
            marker=BASE/'data/firebase-manager-install.json'
            already=marker.exists() and json.loads(marker.read_text()).get('enabled')==args.enable_manager and all((BASE/'backend'/n).exists() and digest(BASE/'backend'/n)==h['current'] for n,h in payload.items())
            if not already:
                quiet([str(python),'-m','pip','download','--only-binary=:all:','--dest',str(backups/'wheels'),'-r',str(ROOT/'deployment/requirements-firebase-manager.txt')])
            print('Installed; protected backup:',tool.apply(args.enable_manager))
        elif args.backup:tool.rollback(args.backup);print('Previous source/dependencies restored; SQLite accounts and additive schema retained.')
        else:raise InstallError('--backup is required for rollback.')

if __name__=='__main__':
    try:main()
    except Exception:
        import sys
        print('Firebase installation/recovery stopped. Inspect configuration and protected backups privately; no runtime details are printed.',file=sys.stderr);sys.exit(1)
