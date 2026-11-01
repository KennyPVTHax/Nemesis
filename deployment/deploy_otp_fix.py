#!/usr/bin/env python3
"""Reviewed source replacement only. Never runs automatically; no secrets are read or logged."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import time
import urllib.request
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
TARGET=Path('/opt/nemesis/backend/auth_api.py')
BACKUPS=Path('/opt/nemesis/backups/otp-attempt-rollback')

class DeploymentError(RuntimeError):
    pass

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def atomic_replace(target,data):
    previous=target.stat()
    fd,name=tempfile.mkstemp(prefix='.auth_api.otp-',dir=target.parent)
    try:
        with os.fdopen(fd,'wb') as output:
            os.fchown(output.fileno(),previous.st_uid,previous.st_gid)
            os.fchmod(output.fileno(),stat.S_IMODE(previous.st_mode))
            output.write(data);output.flush();os.fsync(output.fileno())
        os.replace(name,target);sync_dir(target.parent)
    finally:
        if os.path.exists(name):os.unlink(name)

class Deployment:
    """Dependencies injected for isolated tests; CLI always uses the exact production paths."""
    def __init__(self,target,backups,candidate,original_sha,patched_sha,preflight,restart,healthy):
        self.target,self.backups,self.candidate=map(Path,(target,backups,candidate))
        self.original_sha,self.patched_sha=original_sha,patched_sha
        self.preflight,self.restart,self.healthy=preflight,restart,healthy
    def inspect(self):
        if self.target.is_symlink() or not self.target.is_file() or self.target.resolve()!=self.target:
            raise DeploymentError('Target must be the regular file at the reviewed path.')
        if self.target.stat().st_mode & 0o022:
            raise DeploymentError('Refusing group/world-writable production source.')
        self.payload=self.candidate.read_bytes()
        if self.candidate.is_symlink() or hashlib.sha256(self.payload).hexdigest()!=self.patched_sha:
            raise DeploymentError('Candidate does not match the reviewed patch checksum.')
        current=digest(self.target)
        if current not in (self.original_sha,self.patched_sha):
            raise DeploymentError('Source drift: refusing to overwrite an unknown production revision.')
        self.preflight()
        if digest(self.candidate)!=self.patched_sha:
            raise DeploymentError('Candidate changed during preflight; target unchanged.')
        return current
    def backup(self):
        fd,name=tempfile.mkstemp(prefix='auth_api.',suffix='.py',dir=self.backups)
        with os.fdopen(fd,'wb') as output:
            os.fchmod(output.fileno(),0o600)
            output.write(self.target.read_bytes());output.flush();os.fsync(output.fileno())
        sync_dir(self.backups)
        path=Path(name)
        if digest(path)!=self.original_sha:raise DeploymentError('Backup checksum failed; target unchanged.')
        return path
    def apply(self):
        current=self.inspect()
        if not self.healthy():raise DeploymentError('Predeployment API health check failed; target unchanged.')
        if current==self.patched_sha:return 'Already patched; health verified; no restart or new backup.'
        backup=self.backup()
        if digest(self.target)!=self.original_sha:raise DeploymentError('Source changed during preparation; target unchanged by this operation.')
        try:
            atomic_replace(self.target,self.payload)
            if digest(self.target)!=self.patched_sha:raise DeploymentError('Installed checksum mismatch.')
            self.restart()
            if not self.healthy():raise DeploymentError('Postdeployment health failed.')
        except Exception:
            current=digest(self.target)
            if current==self.original_sha:
                raise DeploymentError('Patch failed before source replacement; original source retained.') from None
            if current!=self.patched_sha:
                raise DeploymentError('Patch failed with unexpected source drift; refusing automatic overwrite. Manual recovery required.') from None
            try:
                atomic_replace(self.target,backup.read_bytes())
                self.restart()
                if not self.healthy():raise DeploymentError('Rollback health failed.')
            except Exception:
                raise DeploymentError('Patch failed; rollback needs manual recovery using the verified backup: '+str(backup)) from None
            raise DeploymentError('Patch failed; original source restored, API restarted and rollback health verified. Backup: '+str(backup)) from None
        return 'Patch installed; API restarted and health verified. Backup: '+str(backup)
    def rollback(self,backup):
        current=self.inspect()
        backup=Path(backup)
        if backup.is_symlink() or not backup.is_file() or backup.resolve().parent!=self.backups or digest(backup)!=self.original_sha:
            raise DeploymentError('Rollback requires a verified original backup from the protected backup directory.')
        if current==self.original_sha:
            if not self.healthy():raise DeploymentError('Original source is installed but API health failed; manual service recovery required.')
            return 'Original source already installed; health verified; no restart.'
        if digest(self.target)!=self.patched_sha:raise DeploymentError('Source changed; refusing rollback overwrite.')
        atomic_replace(self.target,backup.read_bytes())
        if digest(self.target)!=self.original_sha:raise DeploymentError('Rollback checksum failed; manual recovery required.')
        self.restart()
        if not self.healthy():raise DeploymentError('Original source restored but API health failed; manual service recovery required.')
        return 'Original source restored; API restarted and health verified.'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def run_quiet(args,timeout=45):
    try:
        result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=False)
    except (OSError,subprocess.TimeoutExpired):raise DeploymentError('Required local command failed or timed out.') from None
    if result.returncode:raise DeploymentError('Required local command failed; inspect it privately on the server.')
    return result.stdout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['check','apply','rollback'])
    parser.add_argument('--service',required=True,help='Verified existing API systemd .service unit; never guessed')
    parser.add_argument('--python',required=True,help='Absolute Python executable used by that API service')
    parser.add_argument('--health-url',required=True,help='Verified loopback API /health endpoint')
    parser.add_argument('--backup',help='Exact protected backup path, required for rollback')
    args=parser.parse_args()
    if os.geteuid()!=0:raise DeploymentError('Run this reviewed deployment tool as root on the VPS only after approval.')
    if not re.fullmatch(r'[A-Za-z0-9_.@:-]+\.service',args.service):raise DeploymentError('Invalid API service unit.')
    python=Path(args.python)
    if not python.is_absolute() or not python.is_file() or not os.access(python,os.X_OK):raise DeploymentError('Provide the verified API Python executable.')
    url=urlsplit(args.health_url)
    if url.scheme not in ('http','https') or url.hostname not in ('127.0.0.1','localhost','::1') or url.path!='/health' or url.username or url.password or url.query or url.fragment:
        raise DeploymentError('Health URL must be a credential-free, direct loopback /health endpoint.')
    if args.action=='rollback' and not args.backup:raise DeploymentError('--backup is required for rollback.')
    metadata=json.loads((ROOT/'docs/security/OTP_SOURCE_CHECKSUMS.json').read_text())
    candidate=ROOT/'backend/auth_api.py'
    def preflight():
        # Never import main/account_store/auth_api or read production environment/data.
        if run_quiet(['systemctl','show','--property=LoadState','--value',args.service]).strip()!=b'loaded':
            raise DeploymentError('The specified API unit is not loaded.')
        run_quiet([str(python),'-c','import fastapi,pydantic,argon2,httpx,sqlite3; c=sqlite3.connect(":memory:"); c.execute("BEGIN IMMEDIATE"); c.rollback(); c.close()'])
        run_quiet([str(python),'-m','pip','check'])
        run_quiet([str(python),'-c','import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_bytes(),"<reviewed-auth-api>","exec")',str(candidate)])
    def restart():run_quiet(['systemctl','restart',args.service])
    def healthy():
        opener=urllib.request.build_opener(NoRedirect())
        for _ in range(15):
            try:
                run_quiet(['systemctl','is-active','--quiet',args.service],timeout=5)
                request=urllib.request.Request(args.health_url,headers={'Accept':'application/json','Cache-Control':'no-store'})
                with opener.open(request,timeout=2) as response:
                    if response.status==200:
                        data=json.loads(response.read(8192))
                        if data.get('status')=='online' and data.get('service')=='NEMESIS Backend':return True
            except Exception:pass
            time.sleep(1)
        return False
    # No file writes for 'check'. apply/rollback serialize using a root-private lock.
    deployment=Deployment(TARGET,BACKUPS,candidate,metadata['original_sha256'],metadata['patched_sha256'],preflight,restart,healthy)
    if args.action=='check':
        deployment.inspect()
        if not healthy():raise DeploymentError('Predeployment health check failed.')
        print('Source, dependencies, syntax, loaded API unit and current health verified. No deployment performed.')
        return
    BACKUPS.mkdir(parents=True,exist_ok=True,mode=0o700)
    if BACKUPS.is_symlink() or BACKUPS.resolve()!=BACKUPS or BACKUPS.stat().st_uid!=0 or stat.S_IMODE(BACKUPS.stat().st_mode)!=0o700:
        raise DeploymentError('Backup directory must be a root-owned, non-symlink directory with mode 0700.')
    lock=os.open(BACKUPS/'.deployment.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    with os.fdopen(lock,'w') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        print(deployment.apply() if args.action=='apply' else deployment.rollback(args.backup))

if __name__=='__main__':
    try:main()
    except (DeploymentError,OSError,ValueError,KeyError) as error:
        # Avoid tracebacks, environment, request details or secret-bearing command output.
        import sys
        print(str(error) if isinstance(error,DeploymentError) else 'Deployment prerequisite or filesystem error; inspect privately on the VPS.',file=sys.stderr)
        sys.exit(1)
