/** Serialize native persistence so logout always follows an in-flight write. */
export function createSecureVault(plugin){
 let queue=Promise.resolve();
 const ordered=fn=>{const result=queue.then(fn,fn);queue=result.catch(()=>{});return result};
 return {
  get:()=>ordered(async()=>{const result=await plugin.read();return result.session??null}),
  set:value=>ordered(()=>plugin.write({token:value.token,expiresAt:value.expiresAt})),
  clear:()=>ordered(()=>plugin.clear()),
 };
}
