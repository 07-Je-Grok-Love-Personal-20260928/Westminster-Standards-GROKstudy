import sys
from playwright.sync_api import sync_playwright
# usage: shot.py page width [palette] [mode] [scrollY|#id] [fullpage]
pg,w=sys.argv[1],int(sys.argv[2]); pal=sys.argv[3] if len(sys.argv)>3 else 'aurora'; mode=sys.argv[4] if len(sys.argv)>4 else 'light'; pos=sys.argv[5] if len(sys.argv)>5 else '0'
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':w,'height':900 if w>500 else 844},device_scale_factor=1)
    c.add_init_script(f"localStorage.setItem('wsg_palette',JSON.stringify('{pal}'));localStorage.setItem('wsg_mode',JSON.stringify('{mode}'));localStorage.setItem('wsg_smooth','false')")
    x=c.new_page(); errs=[]; x.on('pageerror',lambda e:errs.append(str(e))); x.on('console',lambda m: m.type=='error' and errs.append(m.text))
    x.goto(f'http://127.0.0.1:18931/{pg}.html',wait_until='networkidle'); x.wait_for_timeout(800)
    if pos.startswith('#'): x.evaluate(f"window.__goTo(document.getElementById('{pos[1:]}'),false)")
    else: x.evaluate(f'scrollTo(0,{pos})')
    x.wait_for_timeout(2500)
    out=f'/workspace/shots/v2-{pg}-{w}-{pal}-{mode}-{pos.strip("#")}.png'
    x.screenshot(path=out); print(out, errs)
    b.close()
