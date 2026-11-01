"""Audit indexed filenames/content and original-source checksums without printing values."""
import hashlib,json,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
patterns=[rb'\b[0-9]{8,}:[A-Za-z0-9_-]{25,}',rb'AIza[A-Za-z0-9_-]{30,}',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'(?m)^-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\s*$',rb'\$argon2id\$v=\d+\$m=\d+,t=\d+,p=\d+\$[A-Za-z0-9+/]{12,}\$[A-Za-z0-9+/]{20,}']
for name in filter(None,files):
    p=Path(name)
    assert not {'node_modules','.gradle','dist','build'}.intersection(p.parts),name
    assert p.suffix not in {'.db','.sqlite3','.sqlite','.jks','.keystore','.apk','.log','.pem','.p12'},name
    assert p.name!='.env' and (not p.name.startswith('.env.') or p.name=='.env.example'),name
    content=subprocess.check_output(['git','show',':'+name],cwd=root)
    assert not any(re.search(pattern,content) for pattern in patterns),'Potential secret in '+name
manifest=json.loads((root/'docs/IMPORT_MANIFEST.json').read_text())
for row in manifest:
    if row['public_path']:
        assert row['public_path'] in files,row['public_path']
        assert hashlib.sha256((root/row['public_path']).read_bytes()).hexdigest()==row['sha256'],row['public_path']
print(json.dumps({'indexed_files':len([x for x in files if x]),'verified_imported_source_files':sum(bool(x['public_path']) for x in manifest),'high_confidence_secret_findings':0}))
