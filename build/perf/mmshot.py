from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
  for pal,m,w,page,i in [('aurora','light',1440,'index',2),('ocean','dark',1440,'index',2),('ocean','dark',1440,'index',3),('crimson','dark',390,'compare',0),('jade','light',390,'index',1),('sunset','dark',768,'wlc',0)]:
    c=b.new_context(viewport={'width':w,'height':900})
    c.add_init_script(f"localStorage.setItem('wsg_palette','\"{pal}\"');localStorage.setItem('wsg_mode','\"{m}\"')")
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(f'http://127.0.0.1:18931/{page}.html',wait_until='load')
    el=pg.locator('.mermaid').nth(i);el.scroll_into_view_if_needed();pg.wait_for_timeout(500)
    el.screenshot(path=f'/workspace/shots/mm-{page}{i}-{pal}-{m}-{w}.png');print(pal,m,w,page,errs)
    c.close()
  b.close()
