// Real local emulator REST clients. The owner token is used ONLY to install test Rules.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createMockUserToken} from '@firebase/util';
const base='http://127.0.0.1:9005';
const rule=fs.readFileSync(new URL('database.rules.json',import.meta.url),'utf8');
async function install(body){
 const r=await fetch(base+'/.settings/rules.json?ns=demo-nemesis',{method:'PUT',headers:{Authorization:'Bearer owner','Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(5000)});
 assert.equal(r.status,200);
}
// Prove mock JWTs are interpreted as Firebase users, not merely rejected as invalid.
let controls=0;
try{
 await install({rules:{'.read':"auth != null && auth.uid === 'customer-a'",'.write':false}});
 for(const uid of ['customer-a','customer-b',null]){
  const auth=uid?'&auth='+encodeURIComponent(createMockUserToken({sub:uid,user_id:uid},'demo-nemesis')):'';
  const r=await fetch(base+'/customer_preferences.json?ns=demo-nemesis'+auth,{signal:AbortSignal.timeout(5000)});
  assert.equal(r.status,uid==='customer-a'?200:401);controls++;
 }
}finally{await install(JSON.parse(rule))}
let passed=0;
for(const uid of [null,'customer-a','customer-b']){
 const auth=uid?'&auth='+encodeURIComponent(createMockUserToken({sub:uid,user_id:uid},'demo-nemesis')):'';
 for(const method of ['GET','PUT']){
  const r=await fetch(base+'/customer_preferences.json?ns=demo-nemesis'+auth,{method,headers:{'Content-Type':'application/json'},...(method==='PUT'?{body:JSON.stringify({theme:'test'})}:{}),signal:AbortSignal.timeout(5000)});
  assert.ok([401,403].includes(r.status),'Unprivileged client '+String(uid)+' '+method+' must be denied; HTTP '+r.status);passed++;
 }
}
console.log(JSON.stringify({passed,authentication_controls_passed:controls,failed:0,scope:'Real RTDB emulator REST denial for anonymous and two Firebase mock-user tokens; no live cloud'}));
