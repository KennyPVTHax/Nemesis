#!/usr/bin/env python3
"""Verify packaged assets against dist and check for leaked original credentials.
Does not print credential values or contact any service.
"""
from pathlib import Path
import hashlib,json,re,sys,zipfile
root=Path(__file__).resolve().parents[1]
apk=Path(sys.argv[1]) if len(sys.argv)>1 else root/'android/app/build/outputs/apk/debug/app-debug.apk'
manifest=json.loads((root.parent/'docs/SOURCE_MANIFEST.json').read_text())
tokens=[]
for item in manifest.values():
    original=Path(item['path'])
    if original.exists() and original.suffix in ['.html','.bak']:
        match=re.search(r'const TELEGRAM_BOT_TOKEN\s*=\s*"([^"]+)"',original.read_text())
        if match: tokens.append(match[1].encode())
checks=[]
with zipfile.ZipFile(apk) as z:
    assert z.testzip() is None,'Invalid ZIP entry'
    for entry in z.infolist():
        content=z.read(entry)
        assert not any(token in content for token in tokens),'Original credential found in APK'
        assert not re.search(rb'\b\d{8,}:[A-Za-z0-9_-]{20,}',content),'Bot credential pattern found in APK'
        assert not re.search(rb'AIza[A-Za-z0-9_-]{30,}',content),'Unexpected Firebase key pattern found'
    checks.append('All APK entries scanned: no bot-token/Firebase-key patterns; exact original comparison only when inputs are mounted')
    for local in (root/'dist').rglob('*'):
        if local.is_file():
            name='assets/public/'+local.relative_to(root/'dist').as_posix()
            assert z.read(name)==local.read_bytes(),'Stale/missing web asset: '+name
    checks.append('Every packaged web asset matches final dist byte-for-byte')
    assert 'classes.dex' in z.namelist(),'Missing Android DEX'
    checks.append('Android DEX present; ZIP integrity valid')
    html=z.read('assets/public/index.html').decode()
    assert "connect-src https://nemesispanel.shop;" in html,'Incorrect API CSP'
    assert "frame-src 'none'" in html and "form-action 'none'" in html,'Missing CSP restrictions'
    settings=json.loads(z.read('assets/capacitor.config.json'))
    assert settings['server']['androidScheme']=='https' and settings['server']['cleartext'] is False
    assert settings['android']['allowMixedContent'] is False
    assert settings['android']['webContentsDebuggingEnabled'] is False
    assert settings['loggingBehavior'] == 'none','Native bridge logging must be disabled'
    assert settings.get('plugins',{}).get('CapacitorHttp',{}).get('enabled',False) is False,'Global fetch interception must remain disabled'
    assert 'assets/public/nemesis-mark.png' in z.namelist(),'Missing updated monogram'
    dex=b''.join(z.read(name) for name in z.namelist() if re.match(r'classes\d*\.dex$',name))
    assert b'SecureSessionPlugin' in dex and b'KeystoreSessionStore' in dex,'Missing Keystore-backed native implementation'
    for name in z.namelist():
        if name.startswith('assets/public/') and name.endswith(('.js','.json','.html')):
            data=z.read(name)
            assert not any(x in data for x in [b'MockAuthAdapter',b'developmentCode',b'LocalPreview!2026',b'test_bearer',b'test_profile',b'api.telegram.org',b'-----BEGIN PRIVATE KEY-----']),'Unexpected development/privileged code in packaged UI'
    checks.append('Strict API-only CSP, HTTPS-only native config, no credential logging/global fetch interception and no shipped synthetic auth fixture')
    checks.append('Updated monogram and Keystore-backed native classes are packaged; this does not prove device-level execution')
print(json.dumps({'apk':str(apk),'bytes':apk.stat().st_size,'sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'original_credentials_compared':len(tokens),'checks':checks},indent=2))
