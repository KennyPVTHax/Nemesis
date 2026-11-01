// Real local emulator REST clients. The owner token is used ONLY to install test Rules.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createMockUserToken} from '@firebase/util';
const base='http://127.0.0.1:9005';
const rule=fs.readFileSync(new URL('database.rules.json',import.meta.url),'utf8');
const installed=await fetch(base+'/.settings/rules.json?ns=demo-nemesis',{method:'PUT',headers:{Authorization:'Bearer owner','Content-Type':'application/json'},body:rule,signal:AbortSignal.timeout(5000)});
assert.equal(installed.status,200);
let passed=0;
for(const uid of [null,'customer-a','customer-b']){
 const auth=uid?'&auth='+encodeURIComponent(createMockUserToken({sub:uid,user_id:uid},'demo-nemesis')):'';
 for(const method of ['GET','PUT']){
  const r=await fetch(base+'/customer_preferences.json?ns=demo-nemesis'+auth,{method,headers:{'Content-Type':'application/json'},...(method==='PUT'?{body:JSON.stringify({theme:'test'})}:{}),signal:AbortSignal.timeout(5000)});
  assert.ok([401,403].includes(r.status),'Unprivileged client '+String(uid)+' '+method+' must be denied; HTTP '+r.status);passed++;
 }
}
console.log(JSON.stringify({passed,failed:0,scope:'Real RTDB emulator REST denial for anonymous and two Firebase mock-user tokens; no live cloud'}));
