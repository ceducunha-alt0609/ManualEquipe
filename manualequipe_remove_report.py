from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for needle in ['Gerar relatório PDF','window.print()']:
    i=s.find(needle)
    assert i!=-1, needle
    a=max(0,i-900); b=min(len(s),i+1200)
    print('\n---',needle,'---\n')
    print(s[a:b])
