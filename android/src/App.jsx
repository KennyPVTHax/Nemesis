import React,{useState,useEffect,useRef} from 'react';
import {Capacitor} from '@capacitor/core';
import {App as NativeApp} from '@capacitor/app';
import {ApiAuthAdapter} from './auth/api-auth.mjs';
import {authTransport} from './auth/capacitor-transport.mjs';
import {secureSessionVault} from './auth/secure-session.mjs';
import {BrandLogo} from './branding/BrandLogo.jsx';
import {Keyboard} from '@capacitor/keyboard';
import {Login,OTP} from './components/Auth.jsx';
import {OriginalAccounts,OriginalDashboard} from './generated/OriginalUI.jsx';
import {Icon} from './components/Icon.jsx';
import {Settings} from './components/Settings.jsx';
import {Future} from './components/Pages.jsx';
const tabs=[['apk','APK Management','box'],['monitoring','Monitoring','grid'],['future','Future','diamond'],['settings','Settings','settings']];
export default function App({authAdapter}){
 const [adapter]=useState(()=>authAdapter||new ApiAuthAdapter({fetchImpl:authTransport,vault:secureSessionVault})),[restoring,setRestoring]=useState(true),[challenge,setChallenge]=useState(null),[session,setSession]=useState(null),[tab,setTab]=useState('monitoring'),[exitPrompt,setExitPrompt]=useState(false),[notice,setNotice]=useState(''),[theme,setTheme]=useState(()=>localStorage.getItem('nemesis_theme')||'nemesis-crimson');
 const reset=()=>{setSession(null);setChallenge(null);setTab('monitoring');setExitPrompt(false)};
 const logout=async()=>{setNotice('');reset();const result=await adapter.logout();if(!result.localCleared)setNotice('Saved credentials could not be removed. Close the app and clear its storage before signing in again.');else if(!result.serverRevoked)setNotice('Local credentials cleared. If the server was unreachable, review and revoke the session when connectivity returns.')};
 const restart=()=>{adapter.cancel();reset();setNotice('')};
 useEffect(()=>{adapter.onInvalidSession=()=>{adapter.cancel();reset();setNotice('Your server session was rejected or expired. Please sign in again.')};return()=>{adapter.onInvalidSession=()=>{}}},[adapter]);
 useEffect(()=>{let active=true;adapter.restore().then(value=>{if(active&&value)setSession(value)}).catch(e=>{if(active)setNotice(e.message)}).finally(()=>{if(active)setRestoring(false)});return()=>{active=false}},[adapter]);
 useEffect(()=>{if(!session)return;const expiry=Math.min(...[session.expiresAt,session.accountExpiresAt].filter(v=>typeof v==='number'));if(!Number.isFinite(expiry))return;const timer=setTimeout(()=>{adapter.logout();reset();setNotice('Your session or account has expired. Please sign in again.')},Math.max(0,Math.min(2147483647,expiry-Date.now())));return()=>clearTimeout(timer)},[adapter,session]);
 const transition=callback=>value=>{document.activeElement?.blur();if(Capacitor.isNativePlatform())Keyboard.hide().catch(()=>{});callback(value)};

 const current=useRef();current.current={session,challenge,tab,logout,restart};
 useEffect(()=>{document.documentElement.dataset.theme=theme;localStorage.setItem('nemesis_theme',theme)},[theme]);
 useEffect(()=>{const handler=()=>{const focused=document.activeElement;if(focused&&['INPUT','TEXTAREA','SELECT'].includes(focused.tagName)){focused.blur();if(Capacitor.isNativePlatform())Keyboard.hide().catch(()=>{});return}const e=new Event('panel:back',{cancelable:true});window.dispatchEvent(e);if(e.defaultPrevented)return;const c=current.current;if(c.challenge&&!c.session){c.restart();return}if(c.session&&c.tab!=='monitoring'){setTab('monitoring');return}if(Capacitor.isNativePlatform())setExitPrompt(true)};
 let handle;let disposed=false;
 if(Capacitor.isNativePlatform())NativeApp.addListener('backButton',handler).then(h=>{if(disposed)h.remove();else handle=h});
 const esc=e=>{if(e.key==='Escape')handler()};window.addEventListener('keydown',esc);
 const resume=()=>{if(document.visibilityState==='visible'&&adapter.session())adapter.profile().then(setSession).catch(()=>{})};document.addEventListener('visibilitychange',resume);
 return()=>{disposed=true;handle?.remove();window.removeEventListener('keydown',esc);document.removeEventListener('visibilitychange',resume)}},[adapter]);
 return <><div id="universe-bg" aria-hidden="true"><span className="u-blob"/><span className="u-blob"/><span className="u-blob"/><span className="u-fog"/>{Array.from({length:40},(_,i)=><span key={i} className="u-star" style={{left:`${(i*37)%100}%`,top:`${(i*19)%100}%`,width:2,height:2,animationDelay:`${i%3}s`}}/>)}</div>{restoring?<main className="auth-page"><section className="auth-card restore-session"><BrandLogo/><p role="status">Checking your saved session…</p></section></main>:!session?(challenge?<OTP adapter={adapter} challenge={challenge} onSession={transition(setSession)} onBack={restart}/>:<Login adapter={adapter} onChallenge={transition(setChallenge)} notice={notice}/>):<div className="app-shell"><div className="development-banner">Account connected · Device services not connected</div><div className="tab-content">{tab==='apk'&&<div className="original-apk"><div className="integration-note">Original APK and Firebase interface. Connections, extraction and uploads await secure backend integration. Do not enter production secrets.</div><OriginalAccounts/><section className="reserve card"><h2>Future APK builder</h2><p>Reserved for a later phase. No packer or repacking is included.</p></section></div>}{tab==='monitoring'&&<div className="original-dashboard"><OriginalDashboard onLogout={logout}/></div>}{tab==='future'&&<Future/>}{tab==='settings'&&<Settings adapter={adapter} session={session} setSession={setSession} theme={theme} setTheme={setTheme} logout={logout}/>}</div><nav className="primary-tabs" aria-label="Primary navigation">{tabs.map(([key,name,icon])=><button key={key} aria-current={tab===key?'page':undefined} onClick={()=>{setTab(key);setExitPrompt(false)}}><span className="tab-symbol"><Icon name={icon} size={22}/></span><span>{name}</span></button>)}</nav></div>}{exitPrompt&&<div className="modal-shade"><section className="card exit-dialog" role="dialog" aria-modal="true" aria-label="Close application"><h2>Close application?</h2><p>Local credentials will be cleared.</p><button className="primary" onClick={()=>{logout().finally(()=>NativeApp.exitApp())}}>Close app</button><button className="quiet full" onClick={()=>setExitPrompt(false)}>Stay here</button></section></div>}</>
}
