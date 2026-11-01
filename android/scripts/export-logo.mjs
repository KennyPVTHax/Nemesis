import {chromium} from 'playwright';import fs from 'node:fs';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox'],headless:true});const page=await browser.newPage({viewport:{width:800,height:800},deviceScaleFactor:1});
await page.goto('http://127.0.0.1:4173');await page.locator('#login').fill('developer');await page.locator('#password').fill('LocalPreview!2026');await page.getByRole('button',{name:'Login',exact:true}).click();await page.locator('#otp').fill(await page.getByTestId('development-code').innerText());await page.getByRole('button',{name:'Verify code'}).click();await page.getByRole('button',{name:'APK Management',exact:true}).click();const logo=page.locator('.nemesis-splash-logo-circle');await logo.waitFor();
await page.evaluate(()=>{document.querySelector('.nemesis-splash-logo-circle').style.cssText='transform-origin:top left;position:fixed;top:0;left:0;margin:0;z-index:1000';document.querySelectorAll('*').forEach(e=>e.style.animation='none')});
async function render(size){await logo.evaluate((e,size)=>{e.style.transform='none';const w=e.getBoundingClientRect().width;e.style.transform=`scale(${size/w})`},size);return logo.screenshot()}
for(const [density,multiplier] of [['mdpi',1],['hdpi',1.5],['xhdpi',2],['xxhdpi',3],['xxxhdpi',4]]){
 const dir=`android/app/src/main/res/mipmap-${density}`;const png=await render(48*multiplier);
 for(const name of ['ic_launcher.png','ic_launcher_round.png'])fs.writeFileSync(`${dir}/${name}`,png);
 fs.writeFileSync(`${dir}/ic_launcher_foreground.png`,await render(108*multiplier));
}
await browser.close();console.log('Rendered original website logo at correct launcher and adaptive-icon Android densities.');
