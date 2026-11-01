import test from 'node:test';
import assert from 'node:assert/strict';
import {randomBytes,randomInt,randomUUID} from 'node:crypto';
import {ApiAuthAdapter} from '../src/auth/api-auth.mjs';
import {LIVE_AUTH_CONTRACT} from '../src/auth/api-contract.mjs';
// Exact owner-confirmed wire schema with isolated synthetic identities/secrets only.
const response=(data,status=200)=>({ok:status>=200&&status<300,status,json:async()=>data});
function fixture({role='user',expiry=null,active=true}={}){
 const token=randomBytes(32).toString('hex'),id=randomUUID(),password=randomUUID(),code=String(randomInt(100000,1000000)),login='synthetic-'+randomUUID();
 const requests=[],events=[];let saved=null,meStatus=200,writeFails=false,tokenType='bearer',challengeTtl=300,tokenTtl=28800;
 const vault={get:async()=>saved,set:async value=>{events.push('vault:set');if(writeFails)throw Error('fixture');saved={...value}},clear:async()=>{events.push('vault:clear');saved=null}};
 const fetchImpl=async(url,options)=>{requests.push({url,options});events.push(new URL(url).pathname);
  if(url.endsWith('/auth/login'))return response({challenge_id:id,expires_in:challengeTtl,message:'OTP sent to linked Telegram'});
  if(url.endsWith('/auth/verify'))return response({access_token:token,token_type:tokenType,expires_in:tokenTtl});
  if(url.endsWith('/auth/me'))return meStatus===200?response({login_id:login,role,is_active:active,expires_at:expiry}):response({},meStatus);
  if(url.endsWith('/auth/logout'))return response({status:'logged_out'});
  throw Error('Unexpected fixture route');
 };
 const make=()=>new ApiAuthAdapter({fetchImpl,vault});
 return {adapter:make(),make,vault,events,requests,token,id,password,code,login,saved:()=>saved,setSaved:value=>saved=value,setMeStatus:value=>meStatus=value,setWriteFails:value=>writeFails=value,setType:value=>tokenType=value,setChallengeTtl:value=>challengeTtl=value,setTokenTtl:value=>tokenTtl=value};
}
async function signIn(f){const c=await f.adapter.login(f.login,f.password);return f.adapter.verify(c.id,f.code)}
test('confirmed production schema enables login; owner null account expiry is distinct from eight-hour session',async()=>{
 const f=fixture({role:'owner'}),before=Date.now();assert.equal(LIVE_AUTH_CONTRACT.confirmed,true);assert.equal(f.adapter.ready,true);
 const challenge=await f.adapter.login(f.login,f.password);assert.equal(challenge.id,f.id);assert.ok(challenge.expiresAt>=before+300000&&challenge.expiresAt<=Date.now()+300000);
 assert.equal(f.adapter.session(),null);assert.equal(f.saved(),null);
 const profile=await f.adapter.verify(challenge.id,f.code);assert.equal(profile.login,f.login);assert.equal(profile.role,'owner');assert.equal(profile.active,true);assert.equal(profile.accountExpiresAt,null);assert.ok(profile.expiresAt>=before+28800000&&profile.expiresAt<=Date.now()+28800000);
 assert.ok(f.events.indexOf('/auth/me')<f.events.indexOf('vault:set'));assert.equal(f.saved().token,f.token);assert.equal(f.saved().version,1);assert.equal(JSON.stringify(profile).includes(f.token),false);assert.equal(JSON.stringify(f.adapter).includes(f.token),false);
});
test('customer account expiry uses UNIX seconds independently of the token lifetime',async()=>{
 const expiry=Math.floor(Date.now()/1000)+86400,f=fixture({expiry});const p=await signIn(f);assert.equal(p.role,'user');assert.equal(p.accountExpiresAt,expiry*1000);assert.ok(p.expiresAt<p.accountExpiresAt);
});
for(const [description,options,code] of [['inactive',{active:false},'inactive'],['expired',{expiry:Math.floor(Date.now()/1000)-60},'account_expired'],['missing status',{active:undefined},'unexpected_response'],['invalid expiry',{expiry:'not-a-timestamp'},'unexpected_response']])test('production profile rejects '+description+' account before secure persistence',async()=>{
 const f=fixture(options);if(description==='missing status'){
  const original=f.adapter.fetch;f.adapter.fetch=async(u,o)=>u.endsWith('/auth/me')?response({login_id:f.login,role:'user',expires_at:null}):original(u,o);
 }
 await assert.rejects(signIn(f),{code});assert.equal(f.adapter.session(),null);assert.equal(f.saved(),null);assert.ok(f.requests.some(r=>r.url.endsWith('/auth/logout')));
});
test('Keystore-backed restore validates the bearer with /auth/me before exposing account UI',async()=>{
 const f=fixture();await signIn(f);const restored=f.make();assert.equal(restored.session(),null);const count=f.requests.length;const profile=await restored.restore();assert.equal(profile.login,f.login);assert.equal(f.requests[count].options.headers.Authorization,'Bearer '+f.token);assert.ok(f.requests[count].url.endsWith('/auth/me'));assert.equal(f.requests.length,count+1);
});
test('revoked saved session and expired local envelope are erased and cannot restore identity',async()=>{
 const f=fixture();await signIn(f);f.setMeStatus(401);await assert.rejects(f.make().restore(),{code:'unauthorized'});assert.equal(f.saved(),null);
 f.setSaved({version:1,token:f.token,expiresAt:Date.now()-1});const count=f.requests.length;assert.equal(await f.make().restore(),null);assert.equal(f.saved(),null);assert.equal(f.requests.length,count);
});
test('secure persistence failure cancels login and revokes the newly issued bearer',async()=>{
 const f=fixture();f.setWriteFails(true);await assert.rejects(signIn(f),{code:'secure_storage'});assert.equal(f.adapter.session(),null);assert.equal(f.saved(),null);assert.ok(f.requests.some(r=>r.url.endsWith('/auth/logout')));
});
test('logout erases saved credentials and uses the real bearer endpoint with no invented request body',async()=>{
 const f=fixture();await signIn(f);const result=await f.adapter.logout();assert.equal(result.localCleared,true);assert.equal(result.serverRevoked,true);assert.equal(f.saved(),null);assert.equal(f.adapter.session(),null);const last=f.requests.at(-1);assert.equal(last.options.method,'POST');assert.equal(last.options.headers.Authorization,'Bearer '+f.token);assert.equal(last.options.body,undefined);
});
test('wrong token type or invalid TTL metadata fail closed without persisted access',async()=>{
 const f=fixture();f.setType('unexpected');await assert.rejects(signIn(f),{code:'unexpected_response'});assert.equal(f.saved(),null);
 const g=fixture();g.setTokenTtl(-1);await assert.rejects(signIn(g),{code:'unexpected_response'});assert.equal(g.saved(),null);
 const h=fixture();h.setChallengeTtl('300');await assert.rejects(h.adapter.login(h.login,h.password),{code:'unexpected_response'});assert.equal(h.saved(),null);
});
test('profile rejection removes the saved envelope and notifies the app before another restore',async()=>{
 const f=fixture();await signIn(f);let invalid=false;f.adapter.onInvalidSession=()=>invalid=true;f.setMeStatus(403);await assert.rejects(f.adapter.profile(),{code:'forbidden'});assert.equal(f.saved(),null);assert.equal(f.adapter.session(),null);assert.equal(invalid,true);
});
