import {LIVE_AUTH_CONTRACT} from './api-contract.mjs';
export const API_ORIGIN='https://nemesispanel.shop';
export class AuthError extends Error{constructor(code,message,status=null){super(message);this.code=code;this.status=status}}
const plain=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
function at(data,path){if(path==='$')return data;if(typeof path!=='string'||!path)return undefined;return path.split('.').reduce((value,key)=>plain(value)&&Object.hasOwn(value,key)?value[key]:undefined,data)}
function time(value,format){
 if(format==='iso8601'&&typeof value==='string'){const t=Date.parse(value);if(Number.isFinite(t))return t}
 if(['unix-seconds','unix-ms'].includes(format)&&Number.isFinite(value)&&value>0)return value*(format==='unix-seconds'?1000:1);
 throw new AuthError('unexpected_response','The server returned invalid expiration metadata. Please contact support.');
}
function ttl(value){if(!Number.isInteger(value)||value<1||value>2147483)throw new AuthError('unexpected_response','The server returned invalid session duration metadata.');return Date.now()+value*1000}
const validToken=value=>typeof value==='string'&&value.length>=16&&value.length<=16384&&!/\s/.test(value);
const errors=status=>status===429?['rate_limited','Too many attempts. Please wait before trying again.']:status===410?['expired','The code has expired. Restart login to request another code.']:status===423?['locked','This challenge is locked. Restart login and follow the server instructions.']:status===422?['validation','Check your login details or enter exactly six digits, then try again.']:status===401?['unauthorized','Sign-in was rejected or the session has expired. Please sign in again.']:status===403?['forbidden','This account or request is not permitted. Contact your account administrator.']:status>=500?['server_unavailable','The authentication service is unavailable. Please try again later.']:['rejected','The server rejected this request. Check your details or restart login.'];

/** Exact confirmed API contract. Native persistence is supplied only by Android Keystore. */
export class ApiAuthAdapter{
 #token=null;#session=null;#challenge=null;#pending=null;#epoch=0;#expiresAt=null;#vault;
 constructor({fetchImpl=(...args)=>fetch(...args),contract=LIVE_AUTH_CONTRACT,timeoutMs=15000,onInvalidSession=()=>{},vault=null}={}){
  this.fetch=fetchImpl;this.contract=contract;this.timeout=timeoutMs;this.onInvalidSession=onInvalidSession;this.#vault=vault;
 }
 get ready(){const c=this.contract;return c.confirmed===true&&['tokenPath','profilePath','idPath','loginPath','rolePath'].every(k=>typeof c[k]==='string'&&c[k].length>0)}
 get configurationMessage(){return 'Sign-in setup is incomplete. Please contact the application owner. No development account is enabled.'}
 session(){return this.#session}
 #clear(){this.#token=null;this.#session=null;this.#challenge=null;this.#expiresAt=null}
 async #eraseSaved(){if(this.#vault)try{await this.#vault.clear()}catch{throw new AuthError('secure_storage','Unable to remove the saved session. Close the app and clear its storage before signing in again.')}}
 async #request(path,body,{token=null,signal,method=body===undefined?'GET':'POST',invalidateForbidden=true}={}){
  let response;const epoch=this.#epoch;
  try{response=await this.fetch(API_ORIGIN+path,{method,headers:{Accept:'application/json',...(body!==undefined?{'Content-Type':'application/json'}:{}),...(token?{Authorization:'Bearer '+token}:{})},...(body===undefined?{}:{body:JSON.stringify(body)}),credentials:'omit',redirect:'error',cache:'no-store',referrerPolicy:'no-referrer',signal})}
  catch{throw new AuthError(signal?.aborted?'cancelled':'network',signal?.aborted?'Request cancelled or timed out. Try again.':'Cannot reach the authentication service. Check your connection and try again.')}
  if(!response.ok){
   if(token&&token===this.#token&&epoch===this.#epoch&&(response.status===401||(response.status===403&&invalidateForbidden))){
    this.#clear();try{await this.#eraseSaved()}finally{this.onInvalidSession()}
   }
   throw new AuthError(...errors(response.status),response.status);
  }
  if(path==='/auth/logout')return null;
  let data;try{data=await response.json()}catch{throw new AuthError('unexpected_response','The authentication service returned an unexpected response. Please contact support.')}
  if(!plain(data))throw new AuthError('unexpected_response','The authentication service returned an unexpected response. Please contact support.');
  return data;
 }
 async #operation(fn){
  if(this.#pending)throw new AuthError('busy','A request is already in progress.');
  const controller=new AbortController(),epoch=this.#epoch;this.#pending=controller;
  const timer=setTimeout(()=>controller.abort(),this.timeout);
  try{return await fn(controller.signal,()=>{if(this.#epoch!==epoch||controller.signal.aborted)throw new AuthError('cancelled','Request cancelled. Please sign in again.')},()=>this.#epoch===epoch)}
  finally{clearTimeout(timer);if(this.#pending===controller)this.#pending=null}
 }
 async #revoke(token){
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),5000);
  try{await this.#request('/auth/logout',undefined,{token,signal:controller.signal,method:'POST'});return true}catch{return false}finally{clearTimeout(timer)}
 }
 #profile(data,sessionExpiry){
  const c=this.contract,p=at(data,c.profilePath);
  if(!plain(p))throw new AuthError('unexpected_response','The server profile does not match the confirmed contract.');
  const id=at(p,c.idPath),login=at(p,c.loginPath),role=at(p,c.rolePath);
  if(!['string','number'].includes(typeof id)||!String(id)||typeof login!=='string'||!login||typeof role!=='string'||!role||login.length>200||role.length>64)
   throw new AuthError('unexpected_response','The server profile is missing required identity or role fields.');
  const result={id:String(id),login,role};
  if(c.activePath){
   const active=at(p,c.activePath);
   if(typeof active!=='boolean')throw new AuthError('unexpected_response','The server profile is missing the account status.');
   if(!active)throw new AuthError('inactive','This account is inactive. Contact your account administrator.');
   result.active=active;
  }
  if(c.accountExpiryPath){
   const expiry=at(p,c.accountExpiryPath);
   result.accountExpiresAt=expiry===null?null:time(expiry,c.accountExpiryFormat);
   if(result.accountExpiresAt!==null&&result.accountExpiresAt<=Date.now())throw new AuthError('account_expired','Your account has expired. Contact your account administrator.');
  }
  const expiry=c.sessionExpiryPath?time(at(data,c.sessionExpiryPath),c.sessionExpiryFormat):sessionExpiry;
  if(expiry){if(expiry<=Date.now())throw new AuthError('expired','The server session has expired. Sign in again.');result.expiresAt=expiry}
  return Object.freeze(result);
 }
 async login(login,password){
  if(!this.ready)throw new AuthError('contract_pending',this.configurationMessage);
  return this.#operation(async(signal,check)=>{
   this.#clear();
   if(this.#vault){await this.#eraseSaved();check()}
   const d=await this.#request('/auth/login',{login_id:login,password},{signal});check();
   if(typeof d.challenge_id!=='string'||d.challenge_id.length<1||d.challenge_id.length>2048)throw new AuthError('unexpected_response','The server did not provide a valid login challenge.');
   const c={id:d.challenge_id};
   if(this.contract.challengeTtlPath)c.expiresAt=ttl(at(d,this.contract.challengeTtlPath));
   else if(this.contract.challengeExpiryPath)c.expiresAt=time(at(d,this.contract.challengeExpiryPath),this.contract.challengeExpiryFormat);
   this.#challenge=c;return {...c};
  });
 }
 async verify(id,code){
  if(!this.ready)throw new AuthError('contract_pending',this.configurationMessage);
  if(!this.#challenge||id!==this.#challenge.id)throw new AuthError('stale_challenge','This challenge is no longer current. Restart login.');
  if(this.#challenge.expiresAt&&this.#challenge.expiresAt<=Date.now())throw new AuthError('expired','The code has expired. Restart login to request another code.');
  if(!/^\d{6}$/.test(code))throw new AuthError('invalid_code','Enter exactly six digits.');
  return this.#operation(async(signal,check,current)=>{
   // OTP rejection preserves the challenge so the server can enforce its attempt limit.
   const d=await this.#request('/auth/verify',{challenge_id:id,code},{signal});check();
   const token=at(d,this.contract.tokenPath);
   if(!validToken(token)){this.#clear();throw new AuthError('unexpected_response','The server token response does not match the confirmed contract. No local session was kept.')}
   try{
    if(this.contract.tokenTypePath&&at(d,this.contract.tokenTypePath)!=='bearer')throw new AuthError('unexpected_response','The server returned an unsupported token type.');
    const expiresAt=this.contract.tokenTtlPath?ttl(at(d,this.contract.tokenTtlPath)):null;
    const raw=await this.#request('/auth/me',undefined,{token,signal});check();
    const profile=this.#profile(raw,expiresAt);
    if(this.#vault){
     if(!expiresAt)throw new AuthError('secure_storage','A verified session expiry is required for secure storage.');
     try{await this.#vault.set({version:1,token,expiresAt})}catch{throw new AuthError('secure_storage','Unable to save the session securely. Sign-in was cancelled.')}
     check();
    }
    this.#token=token;this.#expiresAt=expiresAt;this.#session=profile;this.#challenge=null;return profile;
   }catch(error){
    if(current()){this.#clear();try{await this.#eraseSaved()}catch{}}
    await this.#revoke(token);throw error;
   }
  });
 }
 async firebase(operation){
  const paths={capabilities:['/firebase/capabilities','GET'],status:['/firebase/status','GET'],request:['/firebase/request-link','POST'],link:['/firebase/approved-link','GET']};
  if(!Object.hasOwn(paths,operation))throw new AuthError('rejected','Unsupported Firebase action.');
  return this.#operation(async(signal,check)=>{
   if(!this.#token)throw new AuthError('unauthorized','Sign in again.');
   const [path,method]=paths[operation];
   const data=await this.#request(path,undefined,{token:this.#token,signal,method,invalidateForbidden:false});check();
   if(operation==='capabilities'){if(typeof data.enabled!=='boolean'||data.security_version!==1)throw new AuthError('unexpected_response','Firebase service setup is incomplete.');return data}
   if(operation==='link'){
    let url;try{url=new URL(data.database_url)}catch{throw new AuthError('unexpected_response','The service returned an invalid database link.')}
    if(url.protocol!=='https:'||url.username||url.password||url.port||url.search||url.hash||!/^[-a-z0-9]+(?:\.[-a-z0-9]+)?\.(firebaseio\.com|firebasedatabase\.app)$/.test(url.hostname)||!['','/'].includes(url.pathname))throw new AuthError('unexpected_response','The service returned an invalid database link.');
   }else if(typeof data.status!=='string'||data.status.length>80)throw new AuthError('unexpected_response','The service returned an invalid Firebase status.');
   return data;
  });
 }
 async restore(){
  if(!this.ready||!this.#vault)return null;
  return this.#operation(async(signal,check,current)=>{
   let saved;
   try{saved=await this.#vault.get()}catch{throw new AuthError('secure_storage','Saved sign-in is unavailable. Please sign in again.')}
   check();if(saved===null)return null;
   if(!plain(saved)||saved.version!==1||!validToken(saved.token)||!Number.isFinite(saved.expiresAt)||saved.expiresAt<=Date.now()){await this.#eraseSaved();return null}
   try{
    const raw=await this.#request('/auth/me',undefined,{token:saved.token,signal});check();
    const profile=this.#profile(raw,saved.expiresAt);
    this.#token=saved.token;this.#expiresAt=saved.expiresAt;this.#session=profile;return profile;
   }catch(error){
    if(current()){this.#clear();try{await this.#eraseSaved()}catch{}}
    throw error;
   }
  });
 }
 async profile(){
  return this.#operation(async(signal,check)=>{
   if(!this.#token)throw new AuthError('unauthorized','Sign in again.');
   try{
    const raw=await this.#request('/auth/me',undefined,{token:this.#token,signal});check();
    const profile=this.#profile(raw,this.#expiresAt);this.#session=profile;return profile;
   }catch(error){
    try{check()}catch{throw error}
    if(['unexpected_response','expired','account_expired','inactive'].includes(error.code)){const token=this.#token;this.#clear();try{await this.#eraseSaved()}finally{this.onInvalidSession()}if(token)await this.#revoke(token)}
    throw error;
   }
  });
 }
 cancel(){this.#epoch++;this.#pending?.abort();this.#pending=null;this.#clear()}
 async logout(){
  const token=this.#token;this.cancel();
  let localCleared=true;try{await this.#eraseSaved()}catch{localCleared=false}
  return {localCleared,serverRevoked:token?await this.#revoke(token):false};
 }
}
