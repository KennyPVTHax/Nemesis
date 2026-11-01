import React,{useState} from 'react';
import {Icon} from './Icon.jsx';
import {FirebaseSettings} from './FirebaseSettings.jsx';
import {PageHeader} from './Pages.jsx';
const themes=[['nemesis-crimson','Crimson'],['nemesis-amethyst','Amethyst'],['nemesis-emerald','Emerald'],['nemesis-gold','Gold']];
export function Settings({adapter,session,setSession,theme,setTheme,logout}){
 const [error,setError]=useState(''),[loading,setLoading]=useState(false);
 const refresh=async()=>{if(loading)return;setLoading(true);setError('');try{setSession(await adapter.profile())}catch(e){setError(e.message)}finally{setLoading(false)}};
 const rows=[
  ['lock','Change password','Unavailable — a password-change endpoint has not been supplied.'],
  ['clock','Login activity history','Unavailable — no account-history endpoint has been supplied.'],
  ['devices','Active sessions','This Android session is saved with Keystore-backed encryption. A server session-list endpoint has not been supplied.'],
  ['telegram','Telegram account connection','Login codes are sent by your account server to its previously linked Telegram account. Connection details are not returned by the confirmed API contract.'],
  ['shield','Two-step verification','Telegram verification is part of this sign-in flow. An account security-settings endpoint has not been supplied.'],
 ];
 return <main className="page utility-page settings settings-proposal">
  <PageHeader title="Settings" description="Your account and preferences."/>
  <section className="account-summary"><div className="account-avatar"><Icon name="user" size={23}/></div><div><h2>Account information</h2><p>{session.login}</p></div></section>
  <section className="account-details"><dl><dt>Login ID</dt><dd>{session.login}</dd><dt>Role</dt><dd>{session.role}</dd>{session.active!==undefined&&<><dt>Account status</dt><dd>{session.active?'Active':'Inactive'}</dd></>}{session.accountExpiresAt!==undefined&&<><dt>Account expiry</dt><dd>{session.accountExpiresAt===null?'No configured expiry':new Date(session.accountExpiresAt).toLocaleString()}</dd></>}<dt>Session expiry</dt><dd>{session.expiresAt?new Date(session.expiresAt).toLocaleString():'Not provided by the account server'}</dd></dl><button className="quiet refresh-account" disabled={loading} onClick={refresh}>{loading?'Checking…':'Refresh account'}</button>{error&&<p role="alert" className="error">{error}</p>}</section>
  <p className="group-label">ACCOUNT & SECURITY</p><section className="settings-group">{rows.map(([icon,title,value])=><details className="security-detail" key={title}><summary className="setting-control"><span className="setting-icon"><Icon name={icon} size={19}/></span><span>{title}</span><Icon name="chevron" size={15}/></summary><p>{value}</p></details>)}</section>
  <FirebaseSettings adapter={adapter} session={session}/>
  <p className="group-label">APPEARANCE</p><section className="settings-group theme-row"><div><h3>Original theme</h3><p>The existing NEMESIS palette.</p></div><label className="sr-label" htmlFor="theme">Original website theme</label><select id="theme" value={theme} onChange={e=>setTheme(e.target.value)}>{themes.map(([v,l])=><option key={v} value={v}>{l}</option>)}</select></section>
  <p className="group-label">APPLICATION</p><details className="application-detail"><summary className="app-info-row"><Icon name="info" size={19}/><span>Application information</span><Icon name="chevron" size={15}/></summary><div><p>NEMESIS Panel Development · 0.3.0</p><p>Device services remain disconnected in this build. No child-device collector is included.</p></div></details>
  <button className="logout-control" onClick={logout}><Icon name="logout" size={18}/>Logout</button>
 </main>
}
