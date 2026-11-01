#!/usr/bin/env python3
"""Operator-only profile bootstrap. No private keys or Cloud policy bodies are printed."""
import argparse,hashlib,json,os,time,grp,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from firebase_cloud import GoogleFirebase,policy_fingerprint
from firebase_config import REGIONS

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['fingerprint','write'])
    p.add_argument('--alias',required=True);p.add_argument('--project-id',required=True);p.add_argument('--project-number',required=True)
    p.add_argument('--region',choices=REGIONS,required=True);p.add_argument('--max-instances',type=int,default=20)
    p.add_argument('--runtime-service-account',required=True);p.add_argument('--credential-file');p.add_argument('--iam-policy-sha256');p.add_argument('--enable-create',action='store_true')
    p.add_argument('--billing-acknowledged',action='store_true');p.add_argument('--group',default='nemesis')
    a=p.parse_args()
    import re
    if not re.fullmatch('[A-Za-z0-9_-]{2,40}',a.alias) or not re.fullmatch('[a-z][a-z0-9-]{4,28}[a-z0-9]',a.project_id) or not re.fullmatch('[0-9]{5,20}',a.project_number) or not 1<=a.max_instances<=1000:raise ValueError()
    profile={'runtime_service_account':a.runtime_service_account,'project_id':a.project_id,'project_number':a.project_number,'region':a.region,'max_instances':a.max_instances,'create_enabled':a.enable_create,'billing_acknowledged':a.billing_acknowledged,'iam_reviewed_until':int(time.time())+365*86400}
    if a.credential_file:
        f=Path(a.credential_file)
        if f.is_symlink() or not f.is_absolute() or not str(f).startswith('/etc/nemesis/firebase/') or f.stat().st_mode & 0o007:raise ValueError()
        profile['credential_file']=str(f)
    if a.action=='fingerprint':
        provider=GoogleFirebase(profile)
        try:policy=provider.call('POST','https://cloudresourcemanager.googleapis.com/v1/projects/'+a.project_id+':getIamPolicy',{'options':{'requestedPolicyVersion':3}})
        finally:provider.close()
        print(policy_fingerprint(policy));return
    if os.geteuid()!=0 or not re.fullmatch('[a-f0-9]{64}',a.iam_policy_sha256 or ''):raise ValueError()
    if a.enable_create and not a.billing_acknowledged:raise ValueError()
    profile['iam_policy_sha256']=a.iam_policy_sha256
    path=Path('/etc/nemesis/firebase-manager.json')
    if path.is_symlink() or path.parent.resolve()!=path.parent:raise ValueError()
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.loads(path.read_text()) if path.exists() else {}
    data[a.alias]=profile
    # All aliases for one project must share its operator-approved cap.
    for item in data.values():
        if str(item['project_number'])==a.project_number and item['max_instances']!=a.max_instances:raise ValueError()
    fd,name=tempfile.mkstemp(dir=path.parent,prefix='.firebase-profiles-')
    try:
        with os.fdopen(fd,'w') as f:
            os.fchown(f.fileno(),0,grp.getgrnam(a.group).gr_gid);os.fchmod(f.fileno(),0o640)
            json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
    print('Authorized project alias saved; no instance was created. IAM inheritance must have been reviewed by the operator.')

if __name__=='__main__':
    try:main()
    except Exception:print('Bootstrap failed; inspect project permissions/profile values privately. No credential values are printed.',file=sys.stderr);sys.exit(1)
