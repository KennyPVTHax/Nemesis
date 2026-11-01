import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {chromium} from 'playwright';
// Density conversion/packaging only. Preserve the generated source artwork unchanged.
const source=process.argv[2]||'public/nemesis-mark.png';
const out=path.resolve(process.env.ARTIFACT_DIR||'../artifacts/ui-refresh');
fs.mkdirSync(out,{recursive:true});
const raw=fs.readFileSync(source),base64=raw.toString('base64');
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const page=await browser.newPage();
async function render(size,type){
 const png=await page.evaluate(async({data,size,type})=>{
  const img=new Image();img.src='data:image/png;base64,'+data;await img.decode();
  const c=document.createElement('canvas');c.width=c.height=size;const ctx=c.getContext('2d');
  if(type!=='foreground'){ctx.beginPath();if(type==='round')ctx.arc(size/2,size/2,size/2,0,Math.PI*2);else ctx.roundRect(0,0,size,size,size*.22);ctx.clip();ctx.fillStyle='#0c020d';ctx.fillRect(0,0,size,size)}
  const side=type==='foreground'?size*66/108:size*.82;
  ctx.drawImage(img,(size-side)/2,(size-side)/2,side,side);
  return c.toDataURL('image/png').split(',')[1];
 },{data:base64,size,type});
 return Buffer.from(png,'base64');
}
try{
 for(const [density,factor] of [['mdpi',1],['hdpi',1.5],['xhdpi',2],['xxhdpi',3],['xxxhdpi',4]]){
  const dir='android/app/src/main/res/mipmap-'+density;fs.mkdirSync(dir,{recursive:true});
  for(const [name,type,dp] of [['ic_launcher','square',48],['ic_launcher_round','round',48],['ic_launcher_foreground','foreground',108]])fs.writeFileSync(path.join(dir,name+'.png'),await render(dp*factor,type));
 }
 for(const [name,type,size] of [['launcher-square','square',512],['launcher-round','round',512],['adaptive-foreground','foreground',432]])fs.writeFileSync(path.join(out,name+'.png'),await render(size,type));
 fs.writeFileSync('android/app/src/main/res/values/ic_launcher_background.xml','<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#0c020d</color></resources>\n');
 const metadata={source:'Owner-authorized generated crimson N monogram',image:'/nemesis-mark.png',aspectRatio:'1:1',pixelSize:1254,adaptiveSafeZoneDp:66,adaptiveViewportDp:108,background:'#0c020d',replacementInstalled:true,sha256:crypto.createHash('sha256').update(raw).digest('hex'),legacyOwnerArtwork:{image:'/nemesis-logo.jpg',sha256:'2662b265f5a176207968164694f3069e522792ba8acdb3567a1273bb9a74676d'}};
 fs.writeFileSync('src/branding/branding.json',JSON.stringify(metadata,null,2)+'\n');
 console.log('Packaged generated crimson monogram for web, launcher, adaptive icon and existing splash references.');
}finally{await browser.close()}
