import asyncio,sys
from playwright.async_api import async_playwright
B='http://localhost:18931/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    pg=await b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    for u in ['index','wcf','wlc','wsc','recite','creeds','history','atlas','compare','memory','sources']:
      await pg.goto(B+u+'.html',wait_until='load');await pg.wait_for_timeout(600)
      n=await pg.evaluate("document.getElementsByTagName('*').length")
      print(u,n,errs);errs.clear()
    for u,i in [('wcf.html#c11','c11'),('wlc.html#q123','q123'),('wsc.html#q80','q80'),('recite.html#r-wlc-40','r-wlc-40'),('creeds.html#ld20','ld20')]:
      await pg.goto(B+u,wait_until='load');await pg.wait_for_timeout(1500)
      r=await pg.evaluate(f"(()=>{{const e=document.getElementById('{i}');if(!e)return 'MISSING';const r=e.getBoundingClientRect();return [Math.round(r.top),scrollY]}})()")
      print(u,r,errs);errs.clear()
    await pg.goto(B+'wcf.html');await pg.wait_for_timeout(500)
    await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)");await pg.wait_for_timeout(1500)
    print('wcf after bottom',await pg.evaluate("[document.getElementsByTagName('*').length,document.querySelectorAll('.lz').length,document.querySelectorAll('.lz template').length]"))
    await pg.goto(B+'recite.html');await pg.wait_for_timeout(500)
    await pg.select_option('#rMode','cloze') if await pg.query_selector('#rMode') else None
    await pg.evaluate("window.scrollTo(0,6000)");await pg.wait_for_timeout(1200)
    print('cloze',await pg.evaluate("[document.querySelectorAll('.ansbody').length,document.querySelectorAll('.ansbody .cz, .ansbody [class*=cz]').length]"),errs)
    await b.close()
asyncio.run(main())
