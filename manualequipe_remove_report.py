from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
needle='Gerar relatório PDF'
i=s.find(needle)
assert i!=-1, 'report label not found'
start=s.rfind('<button',0,i)
end=s.find('</button>',i)
assert start!=-1 and end!=-1, (start,end)
end += len('</button>')
block=s[start:end]
assert 'window.print()' in block and needle in block
s=s[:start]+s[end:]
assert needle not in s
assert 'window.print()' not in s
assert "navigator.serviceWorker.register('./sw.js?v=13'" in s
s=s.replace("navigator.serviceWorker.register('./sw.js?v=13'", "navigator.serviceWorker.register('./sw.js?v=14'", 1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
assert "manual-equipe-pwa-v13-audit-integrity" in t
t=t.replace("manual-equipe-pwa-v13-audit-integrity","manual-equipe-pwa-v14-clean-nav",1)
sw.write_text(t,encoding='utf-8')
