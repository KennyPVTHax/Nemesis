/** Offline development only. This module never opens a network connection.
 * Production must replace this adapter with server verification, not extend its trust.
 */
export const MOCK_CREDENTIALS = Object.freeze({login:'<REDACTED_DEVELOPMENT_LOGIN>',password:'<REDACTED_DEVELOPMENT_PASSWORD>'});
export class AuthError extends Error { constructor(code,message){super(message);this.code=code} }
export class MockAuthAdapter {
  #challenge=null; #session=null; #resends=0;
  constructor({now=()=>Date.now(),random=()=>crypto.getRandomValues(new Uint32Array(1))[0],id=()=>crypto.randomUUID()}={}){this.now=now;this.random=random;this.id=id}
  #code(){let n;do{n=this.random()}while(n>=4294800000);return String(100000+n%900000)}
  #newChallenge(login){const now=this.now();this.#challenge={id:this.id(),login,code:this.#code(),expiresAt:now+300000,resendAt:now+30000,attempts:0,used:false};return this.challenge()}
  challenge(){if(!this.#challenge)return null;const {code,attempts,...view}=this.#challenge;return {...view,attemptsRemaining:Math.max(0,3-attempts),developmentCode:code,mode:'offline-mock'}}
  async login(login,password){this.logout();if(login!==MOCK_CREDENTIALS.login||password!==MOCK_CREDENTIALS.password)throw new AuthError('credentials','Invalid development Login ID or password.');return this.#newChallenge(login)}
  async verify(id,code){const c=this.#challenge;if(!c||c.id!==id||c.used)throw new AuthError('invalid','This challenge is no longer valid. Start login again.');
    if(this.now()>=c.expiresAt)throw new AuthError('expired','Code expired. Request a new code.');
    if(c.attempts>=3)throw new AuthError('locked','Three incorrect attempts. Start login again.');
    if(!/^\d{6}$/.test(code)||code!==c.code){c.attempts++;throw new AuthError(c.attempts>=3?'locked':'incorrect',c.attempts>=3?'Three incorrect attempts. Start login again.':`Incorrect code. ${3-c.attempts} attempt(s) remaining.`)}
    c.used=true;this.#session=Object.freeze({id:this.id(),login:c.login,mode:'offline-mock',customerAccess:false,createdAt:this.now()});return this.#session;
  }
  async resend(id){const c=this.#challenge;if(!c||c.id!==id||c.used)throw new AuthError('invalid','Start login again.');if(c.attempts>=3)throw new AuthError('locked','Start login again after three incorrect attempts.');if(this.now()<c.resendAt)throw new AuthError('rate-limit','Please wait 30 seconds before requesting another code.');if(this.#resends>=3)throw new AuthError('rate-limit','Resend limit reached. Start login again.');this.#resends++;return this.#newChallenge(c.login)}
  session(){return this.#session}
  logout(){this.#challenge=null;this.#session=null;this.#resends=0}
}
