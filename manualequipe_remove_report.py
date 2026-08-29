from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
pat=r'\s*<button\s+class="btn-pdf"\s+onclick="window\.print\(\)"\s*>.*?Gerar relatório PDF.*?</button>\s*'
s,n=re.subn(pat,'\n',s,count=1,flags=re.S)
assert n==1, f'report button removals={n}'
assert 'Gerar relatório PDF' not in s
assert 'window.print()' not in s
assert "navigator.serviceWorker.register('./sw.js?v=13'" in s
s=s.replace("navigator.serviceWorker.register('./sw.js?v=13'", "navigator.serviceWorker.register('./sw.js?v=14'", 1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
assert "manual-equipe-pwa-v13-audit-integrity" in t
t=t.replace("manual-equipe-pwa-v13-audit-integrity","manual-equipe-pwa-v14-clean-nav",1)
sw.write_text(t,encoding='utf-8')
