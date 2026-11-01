import test from 'node:test';
import assert from 'node:assert/strict';
import {randomBytes} from 'node:crypto';
import {createAuthTransport} from '../src/auth/https-transport.mjs';
const base='https://nemesispanel.shop';
test('native transport sends only fixed HTTPS auth routes with JSON, redirect rejection and timeouts',async()=>{
 const sent=[],token=randomBytes(32).toString('hex');
 const transport=createAuthTransport({isNative:()=>true,nativeRequest:async o=>{sent.push(o);return {status:200,url:o.url,data:{fixture:'ok'}}},webFetch:()=>{throw Error('Wrong transport')}});
 const r=await transport(base+'/auth/verify',{method:'POST',headers:{Accept:'application/json','Content-Type':'application/json'},body:JSON.stringify({challenge_id:'synthetic-challenge',code:'012345'})});
 assert.equal(r.ok,true);assert.deepEqual(await r.json(),{fixture:'ok'});assert.deepEqual(sent[0].data,{challenge_id:'synthetic-challenge',code:'012345'});assert.equal(sent[0].disableRedirects,true);assert.equal(sent[0].connectTimeout,15000);assert.equal(sent[0].readTimeout,15000);
 await transport(base+'/auth/me',{method:'GET',headers:{Authorization:'Bearer '+token}});assert.equal(sent[1].data,undefined);assert.equal(sent[1].headers.Authorization,'Bearer '+token);
});
test('transport rejects alternate origins, query strings, paths, methods and headers before networking',async()=>{
 let sent=false;const transport=createAuthTransport({isNative:()=>true,nativeRequest:async()=>{sent=true},webFetch:async()=>{sent=true}});
 for(const url of ['http://nemesispanel.shop/auth/me','https://other.invalid/auth/me',base+'/auth/me?token=secret',base+'/auth/me#fragment',base+'/data',base+'/auth/me/'])await assert.rejects(transport(url,{method:'GET'}));
 await assert.rejects(transport(base+'/auth/me',{method:'POST'}));await assert.rejects(transport(base+'/auth/me',{method:'GET',headers:{Cookie:'fixture'}}));assert.equal(sent,false);
});
test('browser transport keeps normal fetch semantics, strict request options and cancellation',async()=>{
 const controller=new AbortController(),options={method:'GET',headers:{Accept:'application/json'},credentials:'omit',redirect:'error',cache:'no-store',signal:controller.signal};let received;
 const expected={ok:true,status:200};const transport=createAuthTransport({isNative:()=>false,nativeRequest:()=>{throw Error('Wrong transport')},webFetch:async(u,o)=>{received={u,o};return expected}});
 assert.equal(await transport(base+'/auth/me',options),expected);assert.equal(received.o,options);assert.equal(received.u,base+'/auth/me');controller.abort();await assert.rejects(transport(base+'/auth/me',options),{name:'AbortError'});
});
test('native cancellation ignores delayed response, and cancellation before dispatch sends nothing',async()=>{
 let resolve;const controller=new AbortController();const transport=createAuthTransport({isNative:()=>true,nativeRequest:()=>new Promise(r=>resolve=r)});
 const pending=transport(base+'/auth/me',{method:'GET',signal:controller.signal});await Promise.resolve();controller.abort();await assert.rejects(pending,{name:'AbortError'});resolve({url:base+'/auth/me',status:200,data:{fixture:'late'}});
 let sent=false;const c=new AbortController(),t=createAuthTransport({isNative:()=>true,nativeRequest:async()=>{sent=true}});const p=t(base+'/auth/me',{method:'GET',signal:c.signal});c.abort();await assert.rejects(p,{name:'AbortError'});assert.equal(sent,false);
});
test('native transport rejects changed response URL and retains error statuses for adapter handling',async()=>{
 const t=createAuthTransport({isNative:()=>true,nativeRequest:async o=>({url:o.url,status:401,data:'{}'})});const r=await t(base+'/auth/me',{method:'GET'});assert.equal(r.ok,false);assert.equal(r.status,401);assert.deepEqual(await r.json(),{});
 const u=createAuthTransport({isNative:()=>true,nativeRequest:async()=>({url:'https://other.invalid/auth/me',status:200,data:{}})});await assert.rejects(u(base+'/auth/me',{method:'GET'}));
});
