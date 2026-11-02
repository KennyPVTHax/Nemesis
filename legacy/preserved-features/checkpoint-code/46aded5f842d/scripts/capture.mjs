import {chromium} from 'playwright';import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';import http from 'node:http';
const output=path.resolve('../artifacts/ui-preview');const html=path.join(output,'NEMESIS-interactive-preview.html');
const server=http.createServer((req,res)=>{res.writeHead(200,{'Content-Type':'text/html'});res.end(fs.readFileSync(html))});await new Promise(r=>server.listen(4178,'127.0.0.1',r));const previewUrl='http://127.0.0.1:4178/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});const page=await browser.newPage({viewport:{width:393,height:852},deviceScaleFactor:2,reducedMotion:'reduce'});const errors=[],external=[],report=[];
page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(previewUrl))external.push(r.url())});
try{
 for(const screen of ['login','otp','monitoring','apk','future','settings']){
  await page.goto(previewUrl+'?raw=1&screen='+screen);await page.locator('.device-screen').waitFor();await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),screen+' overflow');
  await page.screenshot({animations:'disabled',path:path.join(output,screen+'.png')});report.push('Rendered '+screen);
 }
 await page.setViewportSize({width:1280,height:1100});await page.goto(previewUrl);await page.getByRole('heading',{name:'Welcome back'}).waitFor();await page.screenshot({animations:'disabled',path:path.join(output,'interactive-desktop.png'),fullPage:true});
 await page.getByRole('button',{name:'Show password'}).click();assert.equal(await page.locator('#preview-password').getAttribute('type'),'text');await page.getByRole('button',{name:'Hide password'}).click();
 await page.getByRole('navigation',{name:'Preview screens'}).getByRole('button',{name:'Telegram OTP'}).click();await page.getByRole('heading',{name:'Check your Telegram'}).waitFor();
 await page.getByRole('navigation',{name:'Preview screens'}).getByRole('button',{name:'Monitoring',exact:true}).click();assert.equal(await page.getByRole('navigation',{name:'Primary navigation'}).locator('button').count(),4);
 await page.getByRole('button',{name:'SMS',exact:true}).click();await page.getByRole('heading',{name:'SMS Searcher'}).waitFor();await page.screenshot({animations:'disabled',path:path.join(output,'sms-search.png')});await page.evaluate(()=>window.dispatchEvent(new Event('panel:back',{cancelable:true})));await page.getByRole('heading',{name:'SMS Searcher'}).waitFor({state:'hidden'});
 await page.getByRole('navigation',{name:'Primary navigation'}).getByRole('button',{name:'Settings',exact:true}).click();await page.getByLabel('Original theme').selectOption('nemesis-amethyst');assert.equal(await page.locator('html').getAttribute('data-theme'),'nemesis-amethyst');report.push('Preview navigation, show/hide password, original SMS modal/back and existing theme switching work');
 for(const width of [320,360,393,412])for(const screen of ['login','otp','monitoring','apk','future','settings']){await page.setViewportSize({width,height:800});await page.goto(previewUrl+'?raw=1&screen='+screen);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${screen} overflow at ${width}`)}
 report.push('No horizontal document overflow at 320/360/393/412px');
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);report.push('Offline standalone HTML renders without external network requests or runtime errors');
 const baseline=JSON.parse(fs.readFileSync(path.join(output,'APP_BEFORE.json')));for(const [name,digest] of Object.entries(baseline)){assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join('/workspace/android-app',name))).digest('hex'),digest,'App modified: '+name)}report.push('Current Android app files are unchanged');
 fs.writeFileSync(path.join(output,'PREVIEW_CHECKS.json'),JSON.stringify({passed:report,errors,external},null,2));console.log(report.join('\n'));
}finally{await browser.close();await new Promise(r=>server.close(r))}
