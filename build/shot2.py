import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for n,w,sel,act in [('history',1280,'#map',''),('history',390,'#map',''),('recite',390,'#rbar',"document.getElementById('rMode').value='cloze';document.getElementById('rMode').dispatchEvent(new Event('input'))"),('memory',390,'#flash',''),('wcf',1280,'#c7',''),('compare',390,'#matrix','')]:
            ctx=await b.new_context(viewport={'width':w,'height':900})
            pg=await ctx.new_page()
            errs=[];pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.goto(f'http://localhost:18931/{n}.html',wait_until='networkidle')
            await pg.wait_for_timeout(1200)
            if act: await pg.evaluate(act); await pg.wait_for_timeout(500)
            await pg.evaluate(f"document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));document.querySelector('{sel}').scrollIntoView()")
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f'/workspace/shots/v-{n}-{w}.png')
            print(n,w,errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
