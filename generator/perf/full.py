import sys
from playwright.sync_api import sync_playwright
pg,w=sys.argv[1],int(sys.argv[2]); pal=sys.argv[3] if len(sys.argv)>3 else 'aurora'; mode=sys.argv[4] if len(sys.argv)>4 else 'light'
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':w,'height':900},device_scale_factor=1)
    c.add_init_script(f"localStorage.setItem('wsg_palette',JSON.stringify('{pal}'));localStorage.setItem('wsg_mode',JSON.stringify('{mode}'));localStorage.setItem('wsg_smooth','false')")
    x=c.new_page(); errs=[]; x.on('pageerror',lambda e:errs.append(str(e)))
    x.goto(f'http://127.0.0.1:18931/{pg}.html',wait_until='networkidle')
    h=x.evaluate('document.documentElement.scrollHeight')
    for y in range(0,h,600): x.evaluate(f'scrollTo(0,{y})'); x.wait_for_timeout(120)
    x.wait_for_timeout(3000); x.evaluate('scrollTo(0,0)'); x.wait_for_timeout(500)
    out=f'/workspace/shots/full-{pg}-{w}-{pal}-{mode}.png'
    x.screenshot(path=out,full_page=True); print(out,errs,h)
    b.close()
