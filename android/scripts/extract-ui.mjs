import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {parse} from 'acorn';
import * as walk from 'acorn-walk';
const manifest=JSON.parse(fs.readFileSync('../docs/SOURCE_MANIFEST.json','utf8'));
const file=process.argv[2] || manifest['4-index.html'].path;
const html=fs.readFileSync(file,'utf8');
if(crypto.createHash('sha256').update(html).digest('hex')!==manifest['4-index.html'].sha256) throw Error('Authoritative source hash mismatch');
const scripts=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const js=scripts.find(s=>s.includes('function p1('));
const ast=parse(js,{ecmaVersion:'latest'}), functions=new Map(), declarations=new Map(), icons=[];
walk.simple(ast,{FunctionDeclaration(n){functions.set(n.id.name,n)},VariableDeclarator(n){if(n.id.type==='Identifier')declarations.set(n.id.name,n.init)}});
function literal(n){
 if(n.type==='Literal')return n.value;
 if(n.type==='ArrayExpression')return n.elements.map(literal);
 if(n.type==='ObjectExpression')return Object.fromEntries(n.properties.map(p=>[p.key.name||p.key.value,literal(p.value)]));
 throw Error('Unexpected nonliteral icon definition');
}
for(const [name,n] of declarations){if(n?.type==='CallExpression'&&n.callee.name==='Qt'&&n.arguments[0]?.type==='Literal'){
 icons.push(`export const ${name}=icon(${JSON.stringify(n.arguments[0].value)},${JSON.stringify(literal(declarations.get(n.arguments[1].name)))});`)
}}
fs.writeFileSync('src/generated/icons.js',`// Original Lucide SVG path arrays extracted from supplied index. See provenance.json.\nimport React from 'react';\nfunction icon(name,paths){return function OriginalIcon({size=24,strokeWidth=2,...props}){return React.createElement('svg',{xmlns:'http://www.w3.org/2000/svg',width:size,height:size,viewBox:'0 0 24 24',fill:'none',stroke:'currentColor',strokeWidth,strokeLinecap:'round',strokeLinejoin:'round',...props},paths.map(([tag,attrs],i)=>React.createElement(tag,{...attrs,key:i})))}}\n`+icons.join('\n'));
const css=[...html.matchAll(/<style([^>]*)>([\s\S]*?)<\/style>/g)].filter(m=>!m[2].includes('Anti-Inspection')).map(m=>m[2]).join('\n');
fs.writeFileSync('src/generated/original.css','/* Verbatim style blocks from authoritative index; anti-inspection style omitted in separate wrapper. */\n'+css);
function render(name){const n=functions.get(name); const ret=n.body.body.find(n=>n.type==='ReturnStatement');let code=js.slice(ret.start,ret.end);const edits=[];walk.simple(ret,{Property(p){if(p.key.name==='onClick'&&['ArrowFunctionExpression','FunctionExpression'].includes(p.value.type)&&/fetch\(|btoa\(|navigator\.clipboard/.test(js.slice(p.value.start,p.value.end))){edits.push({start:p.value.start-ret.start,end:p.value.end-ret.start,text:name==='s1'?'blocked':'I'})}}});for(const e of edits.sort((a,b)=>b.start-a.start)){code=code.slice(0,e.start)+e.text+code.slice(e.end)}return code}
const accountState=js.slice(functions.get('s1').body.body[0].start,functions.get('s1').body.body[0].end);
let accounts=render('s1');
// The original inline bulk-connect handler calls yn and nh. Both are isolated blockers here.
// Keep input values transient; never persist credentials or connect to customer data.
accounts=accounts.replace('NEMESIS · High Security Console · All connections logged','Development preview · No connections or uploads are made');
const accountCode=`export function OriginalAccounts(){\n${accountState}\nconst blocked=()=>T('Unavailable in this offline development build. Do not enter production secrets.');\nconst at=blocked,c=blocked,I=blocked,Z=blocked,openMerged=blocked,toggleSel=blocked;\nconst yn=async()=>{throw new Error('Live Firebase access is unavailable in offline development mode')},nh=()=>{},A=blocked;\nconst it=e=>{e.target.value='';H('APK inspection is awaiting a secure integration. No file has been read or uploaded.')};\nconst bt=e=>{e.preventDefault();H('APK inspection is awaiting a secure integration. No file has been read or uploaded.')};\nconst y=()=>{nt(null);H('');ot('')};\n${accounts}\n}`;
let dashboard=render('p1');
// Truthful transport states replace original live-only messages in this disconnected wrapper.
const replacements={
 'children: "Connected"':'children: "Offline preview"',
 'children: "Waiting for devices to register…"':'children: "No customer data is loaded in development mode."',
 'children: "Auto-refreshing every 15s"':'children: "Live connection awaiting approved backend"',
 '`${d.length} / ${d.length} devices · ${totalSms} SMS · 4:24`':'`${d.length} devices · ${totalSms} SMS · Offline preview`',
 '`100% ${d.length}/${d.length} devices · ${totalSms} SMS · 4:24`':'`No live connection · ${totalSms} SMS`',
 'children: "You can search while loading"':'children: "No customer messages loaded"'
};
for(const [from,to] of Object.entries(replacements)){if(!dashboard.includes(from))throw Error('Source status text changed: '+from);dashboard=dashboard.replace(from,to)}
const dashboardCode=`export function OriginalDashboard({onLogout:b}){\nconst Ac=[],d=[],f=false,h=false,x=null,it=0,bt=0,y=0,_=0,mt=[],sv=new Set();\nconst [w,C]=jt.useState('all'),[v,E]=jt.useState('new'),[g,z]=jt.useState(''),[N,k]=jt.useState(''),[M,H]=jt.useState('');\nconst [smsSearch,setSmsSearch]=jt.useState(false),[smsResults,setSmsResults]=jt.useState([]),[smsSearchQuery,setSmsSearchQuery]=jt.useState('');\nconst smsSearchResults=smsResults;\nconst X='—',Z=b,xt=k,I=()=>H('Refresh unavailable: no authenticated backend is connected.'),q=I,T=I,Sv=I;\nReact.useEffect(()=>{const close=e=>{if(e.key==='Escape')setSmsSearch(false)};window.addEventListener('keydown',close);return()=>window.removeEventListener('keydown',close)},[]);\nReact.useEffect(()=>{const close=e=>{if(smsSearch){e.preventDefault();setSmsSearch(false)}};window.addEventListener('panel:back',close);return()=>window.removeEventListener('panel:back',close)},[smsSearch]);\n${dashboard}\n}`;
const small=['h1','m1'].map(n=>js.slice(functions.get(n).start,functions.get(n).end)).join('\n');
fs.writeFileSync('src/generated/OriginalUI.jsx',`// Derived render expressions only. Original business logic is not bundled.\nimport React from 'react';\nimport * as r from 'react/jsx-runtime';\nimport * as jt from 'react';\nimport {${icons.map(s=>s.match(/export const ([\w$]+)/)[1]).join(',')}} from './icons.js';\nfunction NotIntegrated(){return r.jsx('p',{className:'integration-note',children:'This feature requires an approved authenticated backend.'})} const Zu=NotIntegrated,f1=NotIntegrated,d1=NotIntegrated;\n${small}\n${accountCode}\n${dashboardCode}\n`);
fs.writeFileSync('src/generated/provenance.json',JSON.stringify({source:'4-index.html',sha256:manifest['4-index.html'].sha256,extracted:['style blocks (excluding anti-inspection CSS)','Lucide SVG path arrays','s1 return expression and local state declaration','p1 return expression','h1 error and m1 skeleton renderers'],wrapperChanges:['Disconnected state and events; no original network handlers','Live-only status labels made explicitly offline; hardcoded 4:24 time removed','smsSearchResults compatibility binding (original undefined variable)','Escape and Android back close SMS search'],icons:icons.length},null,2)+'\n');
console.log('Extracted original CSS, icons and two React UI render expressions without original network/credential handlers.');
