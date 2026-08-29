from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Keep the canonical PWA metadata at the top of <head>. In the later PWA block,
# retain only build/tile/startup-image metadata that is not duplicated.
dup='''  <meta name="theme-color" content="#221e1a"/>\n  <meta name="pwa-build" content="v13-mobile-scroll-bar-fix"/>\n  <meta name="mobile-web-app-capable" content="yes"/>\n  <meta name="apple-mobile-web-app-capable" content="yes"/>\n  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>\n  <meta name="apple-mobile-web-app-title" content="Manual Equipe"/>\n  <meta name="application-name" content="Manual Equipe"/>\n'''
replacement='''  <meta name="pwa-build" content="v14-clean-nav"/>\n'''
assert s.count(dup)==1, f'duplicate PWA metadata block count={s.count(dup)}'
s=s.replace(dup,replacement,1)
# Confirm only one copy remains for canonical metadata.
for name in ['theme-color','mobile-web-app-capable','apple-mobile-web-app-capable','apple-mobile-web-app-status-bar-style','apple-mobile-web-app-title','application-name']:
    assert s.count(f'name="{name}"')==1, (name,s.count(f'name="{name}"'))
p.write_text(s,encoding='utf-8')

for mf in ['manifest.json','manifest.webmanifest']:
    q=Path(mf)
    t=q.read_text(encoding='utf-8')
    assert 'source=pwa-v12' in t, f'{mf}: expected old start_url marker'
    t=t.replace('source=pwa-v12','source=pwa-v14',1)
    q.write_text(t,encoding='utf-8')
