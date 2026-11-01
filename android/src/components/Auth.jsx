import React,{useEffect,useRef,useState} from 'react';
import {BrandLogo} from '../branding/BrandLogo.jsx';
import {Icon} from './Icon.jsx';

function Frame({children,otp=false,onBack,busy=false}){
 return <main className={'auth-page '+(otp?'is-otp':'is-login')}>
  <section className="auth-card">
   {otp&&<button type="button" className="back-control" onClick={onBack} disabled={busy}><Icon name="back" size={18}/>Back to login</button>}
   <BrandLogo/>{children}
  </section>
 </main>
}
export function Login({adapter,onChallenge,notice=''}){
 const [login,setLogin]=useState(''),[password,setPassword]=useState(''),[show,setShow]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState('');const lock=useRef(false);
 const submit=async e=>{e.preventDefault();if(lock.current||!adapter.ready)return;lock.current=true;setBusy(true);setError('');const submitted=password;setPassword('');try{onChallenge(await adapter.login(login.trim(),submitted))}catch(e){setError(e.message)}finally{lock.current=false;setBusy(false)}};
 return <Frame>
  <div className="auth-heading"><span className="auth-kicker">YOUR MANAGEMENT CONSOLE</span><h1>Welcome back</h1><p>Sign in to continue to your panel.</p></div>
  {notice&&<p className="notice" role="status">{notice}</p>}
  <form onSubmit={submit} className="polished-form" aria-busy={busy}>
   <label htmlFor="login">Login ID or username</label><div className="field-shell"><Icon name="user"/><input id="login" autoComplete="username" autoCapitalize="none" spellCheck="false" required value={login} onChange={e=>setLogin(e.target.value)} placeholder="Enter your login ID" disabled={busy}/></div>
   <label htmlFor="password">Password</label><div className="field-shell"><Icon name="lock"/><input id="password" type={show?'text':'password'} required autoComplete="current-password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" disabled={busy}/><button type="button" className="eye-button" aria-label={show?'Hide password':'Show password'} aria-pressed={show} onMouseDown={e=>e.preventDefault()} onClick={()=>setShow(!show)}><Icon name={show?'hide':'eye'}/></button></div>
   {error&&<p role="alert" className="error">{error}</p>}
   {!adapter.ready&&<div className="notice contract-notice" role="status">{adapter.configurationMessage}</div>}
   <button className="primary main-button" type="submit" disabled={busy||!adapter.ready}>{busy?'Validating…':'Sign in'}{!busy&&<Icon name="arrow" size={18}/>}</button>
   <div className="auth-step-note"><span className="step-point">1</span><span>Password</span><span className="step-line"/><span className="step-point next">2</span><span>Telegram OTP</span></div>
  </form>
  <p className="auth-footer"><Icon name="lock" size={12}/>Telegram verification follows your password.</p>
 </Frame>
}
export function OTP({adapter,challenge,onSession,onBack}){
 const [code,setCode]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false),[clock,setClock]=useState(Date.now());const lock=useRef(false),input=useRef(null);
 useEffect(()=>{if(!challenge.expiresAt)return;const t=setInterval(()=>setClock(Date.now()),1000);return()=>clearInterval(t)},[challenge.expiresAt]);
 const expired=Boolean(challenge.expiresAt&&clock>=challenge.expiresAt);
 const submit=async e=>{e.preventDefault();if(lock.current||expired||!/^\d{6}$/.test(code))return;lock.current=true;setBusy(true);setError('');const submitted=code;setCode('');try{onSession(await adapter.verify(challenge.id,submitted))}catch(e){setError(e.message);requestAnimationFrame(()=>input.current?.focus())}finally{lock.current=false;setBusy(false)}};
 return <Frame otp onBack={onBack} busy={busy}>
  <div className="auth-heading"><span className="auth-kicker">TWO-STEP VERIFICATION</span><h1>Check your Telegram</h1><p>Enter the six-digit code sent to your linked Telegram account.</p></div>
  <form onSubmit={submit} className="polished-form" aria-busy={busy}>
   <label htmlFor="otp">Six-digit OTP</label><div className="digit-entry" onClick={()=>input.current?.focus()}>
    <div className="digit-boxes" aria-hidden="true">{Array.from({length:6},(_,i)=><span key={i} className={(code[i]?'filled ':'')+(i===Math.min(code.length,5)?'current-digit':'')}>{code[i]||<i/>}</span>)}</div>
    <input ref={input} className="digit-input" id="otp" type="text" inputMode="numeric" autoComplete="one-time-code" pattern="[0-9]{6}" maxLength={6} required value={code} disabled={busy||expired} onChange={e=>setCode(e.target.value.replace(/\D/g,''))}/>
   </div>
   <div className="otp-assistance"><Icon name="telegram" size={17}/><p>Use the account already linked to Telegram.</p></div>
   {challenge.expiresAt&&<p className="subtle" aria-live="polite">{expired?'Code expired. Restart login to request another code.':'Valid until '+new Date(challenge.expiresAt).toLocaleTimeString()}</p>}
   {error&&<p role="alert" className="error">{error}</p>}
   <button className="primary main-button" disabled={busy||expired||code.length!==6}>{busy?'Verifying…':'Verify code'}{!busy&&<Icon name="arrow" size={18}/>}</button>
  </form>
  <button type="button" className="restart-link" disabled={busy} onClick={onBack}>Restart login / Request another code</button>
  <p className="auth-footer">Verification and request limits are handled by your account server.</p>
 </Frame>
}
