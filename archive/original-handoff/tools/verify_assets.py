#!/usr/bin/env python3
# Usage: python tools/verify_assets.py
from pathlib import Path
import hashlib, json
from PIL import Image
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'data'/'manifest.json').read_text(encoding='utf8'))
assert len(manifest['files'])==manifest['asset_count']
problems=[]
for a in manifest['files']:
    p=root/a['path']
    if not p.is_file(): problems.append(a['id']+': missing'); continue
    with Image.open(p) as im:
        sz=[im.width,im.height]
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if sz!=a['size_px']: problems.append(a['id']+': dimension differs')
    if h!=a['sha256']: problems.append(a['id']+': hash differs')
print('Images:',len(manifest['files']))
print('Verification:', 'PASS' if not problems else 'FAIL')
for p in problems: print(' -',p)
