"""Official RTDB REST management + deny-all Rules verification. No secret-bearing errors."""
import hashlib,json,secrets
import httpx
from firebase_config import ManagerError,RULES,identity
PERMISSIONS=['firebasedatabase.instances.get','firebasedatabase.instances.list','firebasedatabase.instances.update']
ROLE_PERMISSIONS=PERMISSIONS+['firebasedatabase.instances.create','resourcemanager.projects.get','resourcemanager.projects.getIamPolicy','iam.roles.get']
def policy_fingerprint(policy):
    if not isinstance(policy,dict) or not isinstance(policy.get('bindings',[]),list) or any(not isinstance(b,dict) or not isinstance(b.get('members',[]),list) or not all(isinstance(m,str) for m in b.get('members',[])) for b in policy.get('bindings',[])):raise CloudError('invalid_iam_policy_response')
    normalized=dict(policy)
    normalized['bindings']=sorted([{**binding,'members':sorted(binding.get('members',[]))} for binding in policy.get('bindings',[])],key=lambda b:json.dumps(b,sort_keys=True))
    return hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class CloudError(ManagerError):
    def __init__(self,code,retry=False):super().__init__(code);self.retry=retry

class GoogleFirebase:
    def __init__(self,profile,client=None,credentials=None):
        self.p=profile;self.client=client or httpx.Client(timeout=8,follow_redirects=False)
        self.credentials=credentials
    def close(self):self.client.close()
    def headers(self):
        try:
            if self.credentials is None:
                import google.auth
                scopes=['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/firebase.database','https://www.googleapis.com/auth/userinfo.email']
                if self.p.get('credential_file'):self.credentials=google.auth.load_credentials_from_file(self.p['credential_file'],scopes=scopes)[0]
                else:self.credentials=google.auth.default(scopes=scopes)[0]
            if not self.credentials.valid:
                from google.auth.transport.requests import Request
                class BoundedRequest(Request):
                    def __call__(self,*args,**kwargs):
                        kwargs['timeout']=8
                        return super().__call__(*args,**kwargs)
                self.credentials.refresh(BoundedRequest())
            if getattr(self.credentials,'service_account_email',None)!=self.p['runtime_service_account']:raise CloudError('service_identity_mismatch')
            return {'Authorization':'Bearer '+self.credentials.token}
        except Exception:raise CloudError('cloud_credentials_unavailable') from None
    def call(self,method,url,body=None,auth=True,allow_missing=False):
        try:r=self.client.request(method,url,json=body,headers=self.headers() if auth else {},follow_redirects=False)
        except Exception:raise CloudError('cloud_timeout',True) from None
        if allow_missing and r.status_code==404:return None
        if not 200<=r.status_code<300:raise CloudError('cloud_http_'+str(r.status_code),r.status_code in (409,429,500,502,503,504))
        if len(r.content)>2_000_000:raise CloudError('cloud_response_limit')
        try:return r.json()
        except Exception:raise CloudError('invalid_cloud_response') from None
    def preflight(self,creating=False):
        p=self.p;project=p['project_id']
        actual=self.call('GET',f'https://cloudresourcemanager.googleapis.com/v1/projects/{project}')
        if actual.get('projectId')!=project or str(actual.get('projectNumber'))!=str(p['project_number']) or actual.get('lifecycleState')!='ACTIVE':raise CloudError('project_identity_mismatch')
        policy=self.call('POST',f'https://cloudresourcemanager.googleapis.com/v1/projects/{project}:getIamPolicy',{'options':{'requestedPolicyVersion':3}})
        fingerprint=policy_fingerprint(policy)
        if fingerprint!=p['iam_policy_sha256']:raise CloudError('iam_policy_changed_review_required')
        principal='serviceAccount:'+p['runtime_service_account']
        roles={b['role'] for b in policy.get('bindings',[]) if principal in b.get('members',[])}
        role='projects/'+project+'/roles/nemesisFirebaseManager'
        if roles!={role}:raise CloudError('runtime_role_review_required')
        definition=self.call('GET','https://iam.googleapis.com/v1/'+role)
        if definition.get('deleted') or set(definition.get('includedPermissions',[]))!=set(ROLE_PERMISSIONS):raise CloudError('runtime_role_not_least_privilege')
        required=PERMISSIONS+(['firebasedatabase.instances.create'] if creating else [])
        granted=self.call('POST',f'https://cloudresourcemanager.googleapis.com/v1/projects/{project}:testIamPermissions',{'permissions':required})
        if not set(required)<=set(granted.get('permissions',[])):raise CloudError('required_iam_permission_missing')
        if creating:
            if p.get('create_enabled') is not True or p.get('billing_acknowledged') is not True:raise CloudError('automatic_creation_disabled')
            billing=self.call('GET',f'https://cloudbilling.googleapis.com/v1/projects/{project}/billingInfo')
            if billing.get('billingEnabled') is not True:raise CloudError('billing_not_enabled')
    def instances(self):
        url=f'https://firebasedatabase.googleapis.com/v1beta/projects/{self.p["project_number"]}/locations/-/instances?pageSize=100';result=[]
        from urllib.parse import quote
        for _ in range(10):
            data=self.call('GET',url);result.extend(data.get('instances',[]))
            token=data.get('nextPageToken')
            if not token:return result
            url=f'https://firebasedatabase.googleapis.com/v1beta/projects/{self.p["project_number"]}/locations/-/instances?pageSize=100&pageToken='+quote(token,safe='')
        raise CloudError('inventory_page_limit')
    def get(self,resource):return self.call('GET','https://firebasedatabase.googleapis.com/v1beta/'+resource,allow_missing=True)
    def create(self,resource,known_resources=()):
        self.preflight(True)
        if len({r['name'] for r in self.instances()} | set(known_resources))>=self.p['max_instances']:raise CloudError('project_budget_instance_limit')
        parent,dbid=resource.rsplit('/instances/',1)
        url='https://firebasedatabase.googleapis.com/v1beta/'+parent+'/instances?databaseId='+dbid
        self.call('POST',url+'&validateOnly=true',{'type':'USER_DATABASE'})
        return self.call('POST',url,{'type':'USER_DATABASE'})
    def validate(self,url,apply_rules=False,require_empty=False):
        url,dbid,region=identity(url)
        if region!=self.p['region']:raise CloudError('project_region_mismatch')
        resource=f'projects/{self.p["project_number"]}/locations/{region}/instances/{dbid}'
        obj=self.get(resource)
        if not obj or obj.get('name')!=resource or obj.get('project')!='projects/'+str(self.p['project_number']) or obj.get('state')!='ACTIVE' or obj.get('databaseUrl','').rstrip('/')!=url:raise CloudError('database_identity_or_state_invalid')
        if apply_rules:self.call('PUT',url+'/.settings/rules.json',RULES)
        rules=self.call('GET',url+'/.settings/rules.json')
        if rules!=RULES:raise CloudError('deny_all_client_rules_required')
        # Backend identity connectivity (not sufficient by itself).
        self.call('GET',url+'/nemesis_manager_health.json')
        if require_empty and self.call('GET',url+'/.json?shallow=true') not in (None,{}):raise CloudError('nonempty_database_requires_manual_ownership_review')
        # Independent unprivileged REST checks. A null write targets a random nonexistent key.
        for method,path,body in [('GET','/.json',None),('PUT','/nemesis_denial_probe/'+secrets.token_hex(16)+'.json',None)]:
            try:r=self.client.request(method,url+path,**({'content':'null','headers':{'Content-Type':'application/json'}} if method=='PUT' else {}),follow_redirects=False,timeout=8)
            except Exception:raise CloudError('client_denial_probe_unavailable',True) from None
            if r.status_code not in (401,403):raise CloudError('unprivileged_client_not_denied')
        return {'resource':resource,'url':url,'region':region,'rules_hash':hashlib.sha256(json.dumps(RULES,sort_keys=True).encode()).hexdigest()}
    def preferences(self,url,value=None,write=False):
        return self.call('PUT' if write else 'GET',url+'/customer_preferences.json',value if write else None)
