from pathlib import Path
import re
from collections import Counter
s=Path('index.html').read_text(encoding='utf-8')
lines=s.splitlines()
terms=['localStorage','sessionStorage','indexedDB','seed','demo','backup','restore','import','export','supabase','firebase','serviceWorker.register','caches.delete','localStorage.clear','removeItem(','setItem(','toISOString().split','innerHTML','fetch(','reset','delete','excluir','senha','password']
out=[f'LINES={len(lines)} BYTES={len(s.encode())}\n']
for t in terms:
 hits=[i for i,l in enumerate(lines,1) if t.lower() in l.lower()]
 out.append(f'\n{t}: {len(hits)}\n')
 for i in hits[:35]: out.append(f'{i}: {lines[i-1][:320]}\n')
names=re.findall(r'(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(',s)
out.append('\nDUP_FUNCTIONS\n')
for n,c in Counter(names).items():
 if c>1: out.append(f'{n}: {c}\n')
ids=re.findall(r'\bid=["\']([^"\']+)["\']',s)
out.append('\nDUP_IDS\n')
for n,c in Counter(ids).items():
 if c>1: out.append(f'{n}: {c}\n')
Path('manualequipe_audit_report.txt').write_text(''.join(out),encoding='utf-8')
