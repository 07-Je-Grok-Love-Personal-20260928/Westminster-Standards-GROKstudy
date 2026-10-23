import sys,json
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18931/'
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in (1440,390):
        ctx=b.new_context(viewport={'width':w,'height':900 if w>500 else 844},device_scale_factor=1)
        x=ctx.new_page();errs=[]
        x.on('pageerror',lambda e:errs.append(str(e)[:200]));x.on('console',lambda m:m.type=='error' and errs.append(m.text[:200]))
        x.goto(base+'atlas.html',wait_until='load')
        x.wait_for_timeout(800)
        for mid in ('reform','brit','london','global','geo'):
            x.evaluate(f"document.getElementById('mb-{mid}').scrollIntoView()");x.wait_for_timeout(2600)
            x.locator(f'#mb-{mid} .cmap').screenshot(path=f'/workspace/perf/v3/{mid}_{w}.png')
        # click a pin & live map
        x.evaluate("document.getElementById('mb-brit').scrollIntoView()")
        x.locator('#mb-brit .pin').nth(2).click();x.wait_for_timeout(300)
        info=x.locator('#mb-brit .minfo').inner_text()
        x.locator('#mb-brit .mtabs [data-v=l]').click();x.wait_for_timeout(9000)
        st=x.evaluate("document.getElementById('mb-brit').dataset.tiles")
        x.locator('#mb-brit .mv-l').screenshot(path=f'/workspace/perf/v3/brit_live_{w}.png')
        out[w]=dict(errs=errs,info=info[:80],tiles=st,log=x.evaluate('window.__tileLog'))
        x.evaluate("scrollTo(0,0)");x.wait_for_timeout(400)
        x.screenshot(path=f'/workspace/perf/v3/atlas_top_{w}.png')
        x.hover('.fab-main') if w>500 else x.click('.fab-main');x.wait_for_timeout(500)
        x.screenshot(path=f'/workspace/perf/v3/fab_{w}.png',clip={'x':w-200,'y':(900 if w>500 else 844)-360,'width':200,'height':360})
        ctx.close()
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
