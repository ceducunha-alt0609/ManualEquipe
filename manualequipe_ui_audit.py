from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
lines=s.splitlines()
out=[]
out.append(f'index bytes={len(s.encode())} lines={len(lines)}\n')
# embedded data URIs
uris=list(re.finditer(r'data:[^\"\']+',s))
out.append(f'data_uris={len(uris)} total_chars={sum(len(m.group(0)) for m in uris)}\n')
for m in uris[:10]: out.append(f'data_uri_start={m.start()} chars={len(m.group(0))} prefix={m.group(0)[:80]}\n')
# duplicated key head declarations
for token in ['<meta name="theme-color"','<meta name="mobile-web-app-capable"','<meta name="apple-mobile-web-app-capable"','<meta name="apple-mobile-web-app-status-bar-style"','<meta name="apple-mobile-web-app-title"','<meta name="application-name"','rel="manifest"','apple-touch-startup-image']:
 out.append(f'{token}: {s.count(token)}\n')
# class/id references useful for nav/install
for token in ['nav-pdf-wrap','btn-pdf','btn-install','installPWA','@media (max-width:720px)','@media(max-width:720px)','!important']:
 out.append(f'{token}: {s.count(token)}\n')
# rough CSS selector duplicates for simple selectors
css='\n'.join(re.findall(r'<style[^>]*>(.*?)</style>',s,flags=re.S|re.I))
sel=[]
for raw in re.findall(r'([^{}]+)\{',css):
 t=' '.join(raw.strip().split())
 if len(t)<120 and not t.startswith('@') and not t.startswith('from') and not t.startswith('to') and '%' not in t:
  sel.append(t)
from collections import Counter
out.append('\nDUP_SELECTORS\n')
for k,v in Counter(sel).most_common():
 if v>1: out.append(f'{v} x {k}\n')
# links/files referenced locally
refs=sorted(set(re.findall(r'(?:href|src)=["\'](?!data:|https?:|#)([^"\']+)',s)))
out.append('\nLOCAL_REFS\n')
for r in refs: out.append(r+'\n')
for mf in ['manifest.json','manifest.webmanifest']:
 if Path(mf).exists(): out.append(f'\n--- {mf} ---\n'+Path(mf).read_text(encoding='utf-8')[:5000]+'\n')
Path('manualequipe_ui_audit_report.txt').write_text(''.join(out),encoding='utf-8')
