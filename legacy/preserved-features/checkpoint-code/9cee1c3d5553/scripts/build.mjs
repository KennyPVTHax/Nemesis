import {build} from 'vite';import fs from 'node:fs';import path from 'node:path';
await build({configFile:false,logLevel:'warn',build:{target:'es2020',assetsInlineLimit:20000000,cssCodeSplit:false,rollupOptions:{output:{inlineDynamicImports:true}}}});
const dir=path.resolve('dist');let html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
html=html.replace(/<script type="module" crossorigin src="([^"]+)"><\/script>/g,(_,url)=>'<script type="module">'+fs.readFileSync(path.join(dir,url.replace(/^\//,'')),'utf8').replace(/<\/script/gi,'<\\/script')+'</script>');
html=html.replace(/<link rel="stylesheet" crossorigin href="([^"]+)">/g,(_,url)=>'<style>'+fs.readFileSync(path.join(dir,url.replace(/^\//,'')),'utf8')+'</style>');
const csp="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; object-src 'none'; form-action 'none'; base-uri 'none'";
html=html.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+csp+'">');
fs.mkdirSync('../artifacts/ui-preview',{recursive:true});fs.writeFileSync('../artifacts/ui-preview/NEMESIS-interactive-preview.html',html);console.log('Built a standalone offline UI proposal. App and APK unchanged.');
