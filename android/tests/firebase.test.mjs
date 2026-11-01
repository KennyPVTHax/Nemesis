import test from 'node:test';import assert from 'node:assert/strict';import {randomBytes,randomUUID} from 'node:crypto';
import {ApiAuthAdapter} from '../src/auth/api-auth.mjs';
const response=(data,status=200)=>({ok:status>=200&&status<300,status,json:async()=>data});
async function signedIn(){
 const token=randomBytes(32).toString('hex'),challenge=randomUUID(),requests=[];let forbidden=false;
 const adapter=new ApiAuthAdapter({fetchImpl:async(u,o)=>{requests.push({u,o});if(u.endsWith('/auth/login'))return response({challenge_id:challenge,expires_in:300});if(u.endsWith('/auth/verify'))return response({access_token:token,token_type:'bearer',expires_in:28800});if(u.endsWith('/auth/me'))return response({login_id:'synthetic',role:'user',is_active:true,expires_at:null});if(u.endsWith('/firebase/capabilities'))return response({enabled:true,security_version:1,architecture:'backend-mediated'});if(u.endsWith('/firebase/status'))return response({assigned:true,status:'assigned',link_request:'pending'});if(u.endsWith('/firebase/request-link'))return response({status:'pending'});if(u.endsWith('/firebase/approved-link'))return forbidden?response({},403):response({database_url:'https://isolated-database.firebaseio.com'});throw Error('Unexpected route')}});
 const c=await adapter.login('synthetic',randomUUID());await adapter.verify(c.id,'000001');return {adapter,token,requests,forbid:()=>forbidden=true};
}
test('customer Firebase operations use existing bearer and exact GET/POST wire contracts',async()=>{
 const f=await signedIn();assert.equal((await f.adapter.firebase('capabilities')).enabled,true);assert.equal((await f.adapter.firebase('status')).assigned,true);assert.equal((await f.adapter.firebase('request')).status,'pending');assert.equal((await f.adapter.firebase('link')).database_url,'https://isolated-database.firebaseio.com');
 for(const {u,o} of f.requests.filter(x=>x.u.includes('/firebase/'))){assert.equal(o.headers.Authorization,'Bearer '+f.token);assert.equal(o.method,u.endsWith('/request-link')?'POST':'GET');assert.equal(o.body,undefined)}
});
test('approval denial and Firebase unavailability do not log the customer out',async()=>{
 const f=await signedIn();f.forbid();await assert.rejects(f.adapter.firebase('link'),{code:'forbidden'});assert.equal(f.adapter.session().login,'synthetic');const original=f.adapter.fetch;f.adapter.fetch=(u,o)=>u.includes('/firebase/')?response({},503):original(u,o);await assert.rejects(f.adapter.firebase('status'),{code:'server_unavailable'});assert.equal(f.adapter.session().login,'synthetic');
});
test('unknown Firebase operation and missing authentication are rejected before requests',async()=>{
 const a=new ApiAuthAdapter();await assert.rejects(a.firebase('admin'),{code:'rejected'});await assert.rejects(a.firebase('status'),{code:'unauthorized'});
});
