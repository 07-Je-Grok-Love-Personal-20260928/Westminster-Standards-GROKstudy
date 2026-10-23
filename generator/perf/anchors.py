from playwright.sync_api import sync_playwright
import sys
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18931/'
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
  for w in (1440,390):
    for h in ('memory.html#wlcmap','wcf.html#c20','wcf.html#c33','wlc.html#g98','wsc.html#q60','recite.html#r-wlc-150'):
      c=b.new_context(viewport={'width':w,'height':900});pg=c.new_page()
      pg.goto(base+h,wait_until='load');pg.wait_for_timeout(2500)
      r=pg.evaluate("(()=>{const t=document.getElementById(location.hash.slice(1));return [Math.round(t.getBoundingClientRect().top),t.tagName,document.querySelectorAll('.cv[style*=intrinsic]').length]})()")
      pg.evaluate("scrollBy(0,-3000)");pg.wait_for_timeout(600);pg.evaluate("scrollBy(0,3000)");pg.wait_for_timeout(600)
      r2=pg.evaluate("Math.round(document.getElementById(location.hash.slice(1)).getBoundingClientRect().top)")
      print(w,h,r,'after up/down',r2,flush=True);c.close()
  b.close()
