import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {chromium} from 'playwright';
// Deterministic Android asset conversion of the actual supplied artwork; no generated replacement.
const source=process.argv[2]||'public/nemesis-logo.jpg';
const raw=fs.readFileSync(source),base64=raw.toString('base64');
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});const page=await browser.newPage();
const sizes=[['mdpi',1],['hdpi',1.5],['xhdpi',2],['xxhdpi',3],['xxxhdpi',4]];
async function render(size,type){const png=await page.evaluate(async({data,size,type})=>{const img=new Image();img.src='data:image/jpeg;base64,'+data;await img.decode();const c=document.createElement('canvas');c.width=c.height=size;const ctx=c.getContext('2d');if(type!=='foreground'){
 ctx.beginPath();if(type==='round')ctx.arc(size/2,size/2,size/2,0,Math.PI*2);else ctx.roundRect(0,0,size,size,size*.22);ctx.clip();ctx.fillStyle='#080e15';ctx.fillRect(0,0,size,size)}
 const side=type==='foreground'?size*66/108:size*.8;const h=side*425/505;ctx.drawImage(img,390,55,505,425,(size-side)/2,(size-h)/2,side,h);return c.toDataURL('image/png').split(',')[1]}, {data:base64,size,type});return Buffer.from(png,'base64')}
for(const [density,factor] of sizes){const dir=`android/app/src/main/res/mipmap-${density}`;fs.writeFileSync(`${dir}/ic_launcher.png`,await render(48*factor,'square'));fs.writeFileSync(`${dir}/ic_launcher_round.png`,await render(48*factor,'round'));fs.writeFileSync(`${dir}/ic_launcher_foreground.png`,await render(108*factor,'foreground'))}
fs.writeFileSync('../artifacts/phase2/launcher-square.png',await render(512,'square'));fs.writeFileSync('../artifacts/phase2/launcher-round.png',await render(512,'round'));fs.writeFileSync('../artifacts/phase2/adaptive-foreground.png',await render(432,'foreground'));
const colorFile='android/app/src/main/res/values/ic_launcher_background.xml';fs.writeFileSync(colorFile,'<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#080e15</color></resources>\n');
const metadata=JSON.parse(fs.readFileSync('src/branding/branding.json'));metadata.sha256=crypto.createHash('sha256').update(raw).digest('hex');fs.writeFileSync('src/branding/branding.json',JSON.stringify(metadata,null,2)+'\n');
await browser.close();console.log('Applied the supplied JPG unchanged to web branding and cropped its emblem for density-correct launcher/adaptive assets.');
