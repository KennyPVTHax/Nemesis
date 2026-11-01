import React,{useState} from 'react';
export function FirebaseSettings({adapter,session}){
 const [status,setStatus]=useState(null),[busy,setBusy]=useState(false),[error,setError]=useState(''),[link,setLink]=useState(''),[available,setAvailable]=useState(false);
 const run=async operation=>{
  if(busy)return;setBusy(true);setError('');setLink('');
  try{const capabilities=await adapter.firebase('capabilities');setAvailable(capabilities.enabled);if(!capabilities.enabled){setStatus({status:'manager_not_enabled'});return}const data=await adapter.firebase(operation);if(operation==='link')setLink(data.database_url);else setStatus(operation==='request'?{...status,link_request:data.status,status:status?.status||data.status}:data)}catch(e){setError(e.message)}finally{setBusy(false)}
 };
 return <><p className="group-label">FIREBASE CONNECTION</p><section className="settings-group" style={{padding:14}}>
 <p className="subtle">{status?`${status.status}${status.instance_label?' · '+status.instance_label:''}${status.instance_state?' · '+status.instance_state:''}`:'Status has not been checked.'}</p>
 {status?.link_request&&<p className="subtle">Link request: {status.link_request}</p>}
 <button className="quiet refresh-account" disabled={busy} onClick={()=>run('status')}>{busy?'Checking…':'Check Firebase status'}</button>
 {session.role==='user'&&<button className="quiet refresh-account" disabled={busy||!available} onClick={()=>run('request')}>Request Firebase Link</button>}
 {status?.link_request==='approved'&&<button className="quiet refresh-account" disabled={busy} onClick={()=>run('link')}>View approved Firebase link</button>}
 {link&&<p style={{overflowWrap:'anywhere'}}>{link}</p>}{error&&<p className="error" role="alert">{error}</p>}
 </section></>;
}
