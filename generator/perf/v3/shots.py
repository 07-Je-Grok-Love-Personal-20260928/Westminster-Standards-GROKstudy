from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for pal,md,w in (('parchment','dark',1440),('parchment','light',390),('ocean','light',1440)):
        ctx=b.new_context(viewport={'width':w,'height':900 if w>500 else 844})
        ctx.add_init_script(f"localStorage.setItem('wsg_palette',JSON.stringify('{pal}'));localStorage.setItem('wsg_mode',JSON.stringify('{md}'))")
        x=ctx.new_page();x.goto('http://127.0.0.1:18931/atlas.html',wait_until='load');x.wait_for_timeout(1500)
        x.screenshot(path=f'/workspace/perf/v3/s_atlas_{pal}_{md}_{w}.png')
        x.evaluate("document.getElementById('confchart').scrollIntoView()");x.wait_for_timeout(1500);x.screenshot(path=f'/workspace/perf/v3/s_conf_{pal}_{md}_{w}.png')
        x.goto('http://127.0.0.1:18931/history.html',wait_until='load');x.wait_for_timeout(800)
        x.evaluate("document.getElementById('mb-overview').scrollIntoView()");x.wait_for_timeout(2500);x.screenshot(path=f'/workspace/perf/v3/s_hist_{pal}_{md}_{w}.png')
        x.goto('http://127.0.0.1:18931/wcf.html#c11',wait_until='load');x.wait_for_timeout(2500);x.screenshot(path=f'/workspace/perf/v3/s_wcf_{pal}_{md}_{w}.png')
        ctx.close()
    b.close()
