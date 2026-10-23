import asyncio, json, sys
from playwright.async_api import async_playwright
PAGES=sys.argv[1].split(',') if len(sys.argv)>1 else ['index','history','wcf','wlc','wsc','compare','recite','memory','creeds','sources']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        res={}
        for name,vp in [('mobile',{'width':390,'height':844}),('tablet',{'width':820,'height':1180}),('desktop',{'width':1440,'height':900})]:
            ctx=await b.new_context(viewport=vp, device_scale_factor=1)
            pg=await ctx.new_page()
            errs=[]
            pg.on('pageerror',lambda e: errs.append(str(e)))
            pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
            for n in PAGES:
                errs.clear()
                await pg.goto(f'http://localhost:18931/{n}.html',wait_until='networkidle',timeout=60000)
                await pg.wait_for_timeout(1500)
                # force reveal
                await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
                info=await pg.evaluate('''()=>{
                  const W=document.documentElement.clientWidth; const out=[];
                  const sw=document.documentElement.scrollWidth;
                  document.querySelectorAll('main *').forEach(el=>{const r=el.getBoundingClientRect(); if(r.width>0 && r.right>W+1){ let p=el.parentElement, sc=false; while(p){const s=getComputedStyle(p); if(['auto','scroll','hidden'].includes(s.overflowX)&&p!==document.body&&p!==document.documentElement){sc=true;break} p=p.parentElement} if(!sc) out.push(el.tagName+'.'+el.className+' '+Math.round(r.right))}});
                  const mer=[...document.querySelectorAll('.mermaid')].map(m=>m.querySelector('svg')?'svg':'NOSVG:'+m.textContent.slice(0,40));
                  return {sw,W,over:out.slice(0,8),n:out.length,mer}}''')
                res[f'{name}/{n}']=dict(info,errs=errs[:5])
                await pg.screenshot(path=f'/workspace/shots/{name}-{n}.png',full_page=False)
            await ctx.close()
        await b.close()
        for k,v in res.items(): print(k,json.dumps(v,ensure_ascii=False)[:600])
asyncio.run(main())
