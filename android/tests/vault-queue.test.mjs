import test from 'node:test';
import assert from 'node:assert/strict';
import {randomBytes} from 'node:crypto';
import {createSecureVault} from '../src/auth/vault-queue.mjs';
test('logout deletion follows a delayed native write; later restore cannot recover that token',async()=>{
 let saved=null,release;const events=[],token=randomBytes(32).toString('hex');
 const vault=createSecureVault({write:async data=>{events.push('write:start');await new Promise(r=>release=r);saved=data;events.push('write:end')},clear:async()=>{events.push('clear');saved=null},read:async()=>({session:saved})});
 const writing=vault.set({token,expiresAt:Date.now()+60000});await Promise.resolve();const clearing=vault.clear(),reading=vault.get();assert.deepEqual(events,['write:start']);release();await writing;await clearing;assert.equal(await reading,null);assert.deepEqual(events,['write:start','write:end','clear']);
});
test('a failed native write does not prevent logout deletion or subsequent reads',async()=>{
 let cleared=false;const vault=createSecureVault({write:async()=>{throw Error('fixture failure')},clear:async()=>{cleared=true},read:async()=>({session:null})});
 await assert.rejects(vault.set({token:randomBytes(32).toString('hex'),expiresAt:Date.now()+60000}));await vault.clear();assert.equal(cleared,true);assert.equal(await vault.get(),null);
});
