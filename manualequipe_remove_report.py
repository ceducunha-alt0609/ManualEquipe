from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''      <button class="btn-pdf" onclick="window.print()">\n        <svg width="13" height="13" viewBox="0 0 20 20" fill="currentColor"><path d="M3 17h14v2H3v-2zm7-3l-5-5 1.4-1.4L9 10.2V2h2v8.2l2.6-2.6L15 9l-5 5z"/></svg>\n        Gerar relatório PDF\n      </button>\n'''
assert s.count(old)==1, f'report button anchor count={s.count(old)}'
s=s.replace(old,'',1)
assert 'Gerar relatório PDF' not in s
assert 'window.print()' not in s
s=s.replace("navigator.serviceWorker.register('./sw.js?v=13'", "navigator.serviceWorker.register('./sw.js?v=14'", 1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
assert "manual-equipe-pwa-v13-audit-integrity" in t
t=t.replace("manual-equipe-pwa-v13-audit-integrity","manual-equipe-pwa-v14-clean-nav",1)
sw.write_text(t,encoding='utf-8')
