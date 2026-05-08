Correção Android PWA v8

Esta versão usa uma configuração conservadora para Chrome Android:
- registro antecipado do service worker no <head>
- manifest.json com start_url ./index.html?source=pwa
- scope ./
- service worker v8 com offline real
- página diagnostico-pwa.html para testar no celular

Suba TODOS os arquivos na mesma pasta do GitHub Pages.
Depois abra /diagnostico-pwa.html no celular para confirmar se tudo está OK.
