import React,{useState,useEffect} from 'react';
import {createRoot} from 'react-dom/client';
import '@fontsource/inter/latin-400.css';
import '@fontsource/inter/latin-500.css';
import '@fontsource/inter/latin-600.css';
import '@fontsource/inter/latin-700.css';
import '@fontsource/outfit/latin-400.css';
import '@fontsource/outfit/latin-600.css';
import '@fontsource/outfit/latin-700.css';
import '@fontsource/outfit/latin-800.css';
import '@fontsource/outfit/latin-900.css';
import '@fontsource/jetbrains-mono/latin-400.css';
import {OriginalDashboard,OriginalAccounts} from './vendor/OriginalUI.jsx';
import mark from './assets/nemesis-emblem.svg?url';
import './vendor/original.css';
import './proposal.css';
const icons={
 user:<><path d="M20 21v-2a7 7 0 0 0-14 0v2"/><circle cx="13" cy="7" r="4"/></>,
 lock:<><rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/></>,
 eye:<><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></>,
 hide:<><path d="m3 3 18 18M10.5 5.1A12 12 0 0 1 22 12a16 16 0 0 1-3 4M6 6c-2.5 1.8-4 6-4 6s3.5 7 10 7a12 12 0 0 0 4-1"/></>,
 arrow:<path d="M4 12h16m-6-6 6 6-6 6"/>,back:<path d="m14 6-6 6 6 6"/>,
 telegram:<><path d="m21 3-5 18-5-8-8-4 18-6Z"/><path d="m11 13 5-5"/></>,
 grid:<><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></>,
 box:<><path d="m12 2 9 5v10l-9 5-9-5V7l9-5Z"/><path d="m3 7 9 5 9-5m-9 5v10M7.5 4.5l9 5"/></>,
 diamond:<><path d="m12 3 9 9-9 9-9-9 9-9Z"/><path d="M12 8v8m-4-4h8"/></>,
 settings:<><path d="m9 3-1 3-3 1-2 3 2 2-1 3 2 3 3-1 2 3h3l1-3 3-1 2-3-2-2 1-3-2-3-3 1-2-3H9Z"/><circle cx="12" cy="12" r="3"/></>,
 shield:<><path d="M12 3 3 7v5c0 5 9 9 9 9s9-4 9-9V7l-9-4Z"/><path d="m8 12 3 3 5-6"/></>,
 chevron:<path d="m9 5 7 7-7 7"/>,clock:<><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
 devices:<><rect x="3" y="3" width="13" height="13" rx="3"/><path d="M8 21h8m-4-5v5"/><rect x="16" y="8" width="6" height="13" rx="2"/></>,
 logout:<><path d="M9 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h4m6-16 5 7-5 7M9 12h12"/></>,
 info:<><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10h.01"/></>,
};
function Icon({name,size=20,...rest}){return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>{icons[name]||icons.info}</svg>}
const tabs=[['apk','APK Management','box'],['monitoring','Monitoring','grid'],['future','Future','diamond'],['settings','Settings','settings']];
const screens=[['login','Login'],['otp','Telegram OTP'],['monitoring','Monitoring'],['apk','APK Management'],['future','Future'],['settings','Settings']];
const params=new URLSearchParams(location.search),raw=params.get('raw')==='1';
function App(){
 const [screen,setScreen]=useState(screens.some(([id])=>id===params.get('screen'))?params.get('screen'):'login'),[toast,setToast]=useState(''),[theme,setTheme]=useState('nemesis-crimson');
 useEffect(()=>{document.documentElement.dataset.theme=theme},[theme]);
 useEffect(()=>{if(!toast)return;const t=setTimeout(()=>setToast(''),3500);return()=>clearTimeout(t)},[toast]);
 const notify=()=>setToast('Design preview only. No request or account action was sent.');
 const go=id=>{setScreen(id);setToast('');document.querySelector('.screen-scroll')?.scrollTo(0,0)};
 return <div className={raw?'review raw':'review'}>{!raw&&<><header className="review-header"><a className="review-brand" href="#" onClick={e=>e.preventDefault()}>NEMESIS<span>UI PROPOSAL 01</span></a><div className="review-badge"><span/> Visual preview · App unchanged</div></header><div className="review-controls" role="navigation" aria-label="Preview screens">{screens.map(([id,label])=><button key={id} className={screen===id?'selected':''} onClick={()=>go(id)}>{label}</button>)}</div></>}
 <div className="review-stage"><div className="device"><div className="device-screen" onClickCapture={e=>{if(e.target.closest('a')){e.preventDefault();notify()}}} style={{'--owner-mark':`url("${mark}")`}}><StatusBar/><div className="screen-scroll" key={screen}>
 {(screen==='login'||screen==='otp')?<AuthPage otp={screen==='otp'} go={go} notify={notify}/>:<div className="application"><div className="panel-body">
 {screen==='monitoring'&&<div className="original-dashboard"><OriginalDashboard onLogout={notify}/></div>}
 {screen==='apk'&&<div className="original-apk"><div className="section-kicker"><span className="mini-tag">APK MANAGEMENT</span><span className="disconnected-dot">Not connected</span></div><OriginalAccounts/><div className="future-builder"><Icon name="box"/><div><h3>Future APK builder</h3><p>Reserved for a later phase.</p></div><span className="quiet-pill">Reserved</span></div></div>}
 {screen==='future'&&<Future/>}
 {screen==='settings'&&<Settings theme={theme} setTheme={setTheme} notify={notify}/>}
 </div></div>}
 </div>{!['login','otp'].includes(screen)&&<nav className="bottom-tabs" aria-label="Primary navigation">{tabs.map(([id,label,icon])=><button key={id} onClick={()=>go(id)} aria-current={id===screen?'page':undefined}><span className="tab-symbol"><Icon name={icon} size={22}/></span><span>{label}</span></button>)}</nav>}
 {toast&&<div role="status" className="preview-toast"><Icon name="info" size={16}/>{toast}</div>}<div className="gesture-space"><span/></div></div></div>
 {!raw&&<aside className="review-notes"><span className="note-index">01 / MOBILE UI POLISH</span><h1>Make the logo<br/>the focal point.</h1><p>Your actual emblem, cropped for smaller screens. The crimson palette, original dashboard and four main tabs stay.</p><div className="note-item"><span>01</span><div><h3>A compact brand mark</h3><p>The helmet stays legible, with a clean text wordmark underneath.</p></div></div><div className="note-item"><span>02</span><div><h3>More comfortable forms</h3><p>Clear labels, 52px touch targets and room for the keyboard.</p></div></div><div className="note-item"><span>03</span><div><h3>Consistent small details</h3><p>One icon style, more readable controls and balanced spacing.</p></div></div><p className="review-disclaimer">This is a design proposal. It uses no live API, accounts or monitoring data. Use the screen buttons above to review the layouts.</p></aside>}
 </div></div>
}
function StatusBar(){return <div className="status-bar" aria-hidden="true"><span>9:41</span><div><svg width="15" height="12" viewBox="0 0 15 12" fill="currentColor"><rect x="1" y="8" width="2" height="3" rx=".5"/><rect x="5" y="5" width="2" height="6" rx=".5"/><rect x="9" y="1" width="2" height="10" rx=".5"/></svg><svg width="17" height="12" viewBox="0 0 17 12" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M1 4c4-4 11-4 15 0M4 7c3-3 6-3 9 0m-6 3 1.5 1L10 10"/></svg><span className="battery-icon"/></div></div>}
function Brand(){return <div className="proposed-brand"><div className="brand-emblem"><img src={mark} alt="Owner-supplied NEMESIS helmet emblem"/></div><div className="brand-wordmark">NEMESIS <span>PANEL</span></div></div>}
function AuthPage({otp,go,notify}){
 const [show,setShow]=useState(false),[code,setCode]=useState('');
 return <section className={'auth-layout '+(otp?'is-otp':'is-login')}>
 <div className="ambient-orb one"/><div className="ambient-orb two"/>
 {otp&&<button className="back-control" onClick={()=>go('login')}><Icon name="back" size={18}/><span>Back to login</span></button>}
 <div className="auth-content"><Brand/>
 <div className="auth-heading"><span className="auth-kicker">{otp?'TWO-STEP VERIFICATION':'YOUR MANAGEMENT CONSOLE'}</span><h1>{otp?'Check your Telegram':'Welcome back'}</h1><p>{otp?'Enter the six-digit code sent to your linked Telegram account.':'Sign in to continue to your panel.'}</p></div>
 <form onSubmit={e=>{e.preventDefault();notify()}} className="polished-form">
 {otp?<><label htmlFor="preview-otp">Verification code</label><div className="digit-entry" onClick={()=>document.getElementById('preview-otp').focus()}><div className="digit-boxes" aria-hidden="true">{Array.from({length:6},(_,i)=><span key={i} className={code[i]?'filled':''}>{code[i]||<i/>}</span>)}</div><input id="preview-otp" aria-label="Six-digit verification code" className="digit-input" inputMode="numeric" maxLength={6} autoComplete="one-time-code" pattern="[0-9]{6}" required value={code} onChange={e=>setCode(e.target.value.replace(/\D/g,''))}/></div><div className="otp-assistance"><Icon name="telegram" size={16}/><p>Use the account already linked to Telegram.</p></div><button className="main-button" type="submit">Verify code<Icon name="arrow" size={18}/></button><button type="button" className="restart-link" onClick={()=>go('login')}>Restart login / Request another code</button></>:<><label htmlFor="preview-login">Login ID</label><div className="field-shell"><Icon name="user"/><input id="preview-login" autoComplete="off" autoCapitalize="none" placeholder="Enter your login ID" required/></div><label htmlFor="preview-password">Password</label><div className="field-shell"><Icon name="lock"/><input id="preview-password" type={show?'text':'password'} autoComplete="off" placeholder="Enter your password" required/><button type="button" className="eye-button" aria-label={show?'Hide password':'Show password'} onClick={()=>setShow(!show)}><Icon name={show?'hide':'eye'}/></button></div><button className="main-button" type="submit">Sign in<Icon name="arrow" size={18}/></button><div className="auth-step-note"><span className="step-point">1</span><span>Password</span><span className="step-line"/><span className="step-point future">2</span><span>Telegram OTP</span></div></>}
 </form><div className="auth-footer"><Icon name="lock" size={12}/><span>{otp?'Verification is handled by your account server.':'Telegram verification follows your password.'}</span></div>
 </div><div className="auth-bottom-brand">NEMESIS PANEL<span>DEVICE MANAGEMENT CONSOLE</span></div>
 </section>
}
function Header({title,description}){return <div className="simple-header"><div><p className="section-eyebrow">NEMESIS PANEL</p><h1>{title}</h1>{description&&<p className="section-description">{description}</p>}</div><div className="small-emblem"><img src={mark} alt=""/></div></div>}
function Future(){return <div className="utility-page"><Header title="Future feature"/><div className="reserved-card"><div className="reserved-icon"><Icon name="diamond" size={34}/></div><span className="mini-tag">TAB 03</span><h2>Room for what's next.</h2><p>This space is reserved for the functionality you specify later.</p><span className="quiet-pill">Reserved</span></div></div>}
function Settings({theme,setTheme,notify}){return <div className="utility-page settings-proposal"><Header title="Settings" description="Your account and preferences."/><div className="account-summary"><div className="account-avatar"><Icon name="user" size={23}/></div><div><h2>Account information</h2><p>Details appear after sign-in.</p></div><Icon name="chevron" size={17}/></div><p className="group-label">ACCOUNT & SECURITY</p><div className="settings-group">{[['lock','Change password',''],['clock','Login activity',''],['devices','Active sessions',''],['telegram','Telegram connection','Not loaded'],['shield','Two-step verification','Not loaded']].map(([icon,title,value])=><button key={title} onClick={notify} className="setting-control"><span className="setting-icon"><Icon name={icon} size={19}/></span><span>{title}</span>{value&&<small>{value}</small>}<Icon name="chevron" size={15}/></button>)}</div><p className="group-label">APPEARANCE</p><div className="settings-group theme-row"><div><h3>Original theme</h3><p>The existing NEMESIS palette.</p></div><label className="sr-label" htmlFor="proposal-theme">Original theme</label><select id="proposal-theme" value={theme} onChange={e=>setTheme(e.target.value)}><option value="nemesis-crimson">Crimson</option><option value="nemesis-amethyst">Amethyst</option><option value="nemesis-emerald">Emerald</option><option value="nemesis-gold">Gold</option></select></div><p className="group-label">APPLICATION</p><button className="app-info-row" onClick={notify}><Icon name="info" size={19}/><span>Application information</span><Icon name="chevron" size={15}/></button><button className="logout-control" onClick={notify}><Icon name="logout" size={18}/>Logout</button></div>}
createRoot(document.getElementById('root')).render(<App/>);
