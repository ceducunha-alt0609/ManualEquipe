from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Persist read progress locally instead of losing it on every reload/PWA restart.
old="""const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.section');
const readState = {};
"""
new="""const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.section');
const READ_STATE_KEY = 'manualequipe.readState';
let readState = {};
try {
  const savedReadState = JSON.parse(localStorage.getItem(READ_STATE_KEY) || '{}');
  if(savedReadState && typeof savedReadState === 'object' && !Array.isArray(savedReadState)) readState = savedReadState;
} catch(e) {}
"""
assert old in s, 'read state anchor not found'
s=s.replace(old,new,1)

old_click="""    updateProgress();
  });
});

updateProgress();
"""
new_click="""    try { localStorage.setItem(READ_STATE_KEY, JSON.stringify(readState)); } catch(e) {}
    updateProgress();
  });
});

document.querySelectorAll('.btn-read').forEach(btn => {
  const key = btn.getAttribute('data-key');
  if(!readState[key]) return;
  btn.textContent = '✓ Lida';
  btn.classList.add('done');
  const navItem = document.querySelector('[data-section="' + key + '"]');
  navItem && navItem.classList.add('read-done');
});
updateProgress();
"""
assert old_click in s, 'read click anchor not found'
s=s.replace(old_click,new_click,1)

# Keep a single service-worker registration path. Enhance the diagnostic registration
# with waiting-worker activation and remove the second registration function/call.
old_top="""      navigator.serviceWorker.register('./sw.js?v=11', { scope: './' })
        .then(function(reg){ window.__PWA_DIAG__.swRegistered = true; window.__PWA_DIAG__.scope = reg.scope; return navigator.serviceWorker.ready; })
        .then(function(){ window.__PWA_DIAG__.swReady = true; })
"""
new_top="""      navigator.serviceWorker.register('./sw.js?v=13', { scope: './' })
        .then(function(reg){
          window.__PWA_DIAG__.swRegistered = true;
          window.__PWA_DIAG__.scope = reg.scope;
          if(reg.waiting) reg.waiting.postMessage({type:'SKIP_WAITING'});
          return navigator.serviceWorker.ready;
        })
        .then(function(){ window.__PWA_DIAG__.swReady = true; })
"""
assert old_top in s, 'top sw anchor not found'
s=s.replace(old_top,new_top,1)

pattern=re.compile(r"\n  async function registerServiceWorker\(\)\{.*?\n  \}\n",re.S)
s,n=pattern.subn('\n',s,count=1)
assert n==1, 'duplicate sw function not found'
s=s.replace('\n  registerServiceWorker();\n})();','\n})();',1)

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
t=t.replace("const CACHE_NAME = 'manual-equipe-pwa-v12-icon-final';","const CACHE_NAME = 'manual-equipe-pwa-v13-audit-integrity';",1)
old="keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))"
new="keys.filter((key) => key.startsWith('manual-equipe-pwa-') && key !== CACHE_NAME).map((key) => caches.delete(key))"
assert old in t, 'cache cleanup anchor not found'
t=t.replace(old,new,1)
sw.write_text(t,encoding='utf-8')

s=p.read_text(encoding='utf-8')
assert "READ_STATE_KEY = 'manualequipe.readState'" in s
assert s.count('serviceWorker.register(')==1
assert "./sw.js?v=13" in s
