from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
needles=['Gerar relatório PDF','Gerar relatorio PDF','gerar relatório','gerar relatorio','window.print()']
for n in needles:
 print(n, s.lower().count(n.lower()))
# remove button/link containing Gerar relatório PDF (or unaccented), then remove a dedicated print handler if left behind
import re
patterns=[
 r'\s*<button\b[^>]*>[^<]*(?:Gerar relat[oó]rio PDF)[^<]*</button>\s*',
 r'\s*<a\b[^>]*>[^<]*(?:Gerar relat[oó]rio PDF)[^<]*</a>\s*'
]
removed=0
for pat in patterns:
 s,n=re.subn(pat,'\n',s,flags=re.I)
 removed+=n
assert removed==1, f'expected one report control, removed={removed}'
# Remove simple named function whose only meaningful action is window.print, if present.
s,n=re.subn(r'\n\s*function\s+[A-Za-z_$][\w$]*\s*\([^)]*\)\s*\{\s*window\.print\(\);?\s*\}\s*','\n',s,count=1,flags=re.S)
p.write_text(s,encoding='utf-8')
print('removed control',removed,'simple print functions',n)
