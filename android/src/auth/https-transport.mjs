import {API_ORIGIN} from './api-auth.mjs';
const methods=new Map([['/auth/login','POST'],['/auth/verify','POST'],['/auth/me','GET'],['/auth/logout','POST'],['/firebase/status','GET'],['/firebase/capabilities','GET'],['/firebase/request-link','POST'],['/firebase/approved-link','GET']]);
function validate(url,options){
 const u=new URL(url);
 if(u.origin!==API_ORIGIN||u.username||u.password||u.search||u.hash||methods.get(u.pathname)!==options.method)throw new Error('Unsupported authentication destination.');
 if(Object.keys(options.headers||{}).some(k=>!['accept','content-type','authorization'].includes(k.toLowerCase())))throw new Error('Unsupported authentication headers.');
 if(options.body!==undefined&&(typeof options.body!=='string'||options.body.length>32768))throw new Error('Invalid authentication request.');
 return u.href;
}
function abortError(){return new DOMException('Authentication request cancelled.','AbortError')}
/** Uses Android's standard HTTPS transport only for fixed customer API routes.
 * No fetch patch, redirect, proxy, TLS override, URL selector or token persistence.
 * Native HTTP cannot be physically aborted; a late result is discarded on abort.
 */
export function createAuthTransport({isNative,nativeRequest,webFetch}){
 return async(url,options={})=>{
  const target=validate(url,options);
  if(options.signal?.aborted)throw abortError();
  if(!isNative())return webFetch(target,options);
  const request={url:target,method:options.method,headers:{...options.headers,'Cache-Control':'no-store'},responseType:'json',disableRedirects:true,connectTimeout:15000,readTimeout:15000};
  if(options.body!==undefined)request.data=JSON.parse(options.body);
  let onAbort;
  const aborted=new Promise((_,reject)=>{onAbort=()=>reject(abortError());options.signal?.addEventListener('abort',onAbort,{once:true})});
  try{
   const r=await Promise.race([Promise.resolve().then(()=>{if(options.signal?.aborted)throw abortError();return nativeRequest(request)}),aborted]);
   if(options.signal?.aborted)throw abortError();
   if(r.url&&r.url!==target)throw new Error('Authentication redirects are not accepted.');
   if(!Number.isInteger(r.status)||r.status<100||r.status>599)throw new Error('Invalid HTTPS response.');
   return {status:r.status,ok:r.status>=200&&r.status<300,json:async()=>{if(typeof r.data==='string')return JSON.parse(r.data);return r.data}};
  }finally{options.signal?.removeEventListener('abort',onAbort)}
 };
}
