import sys,json
from playwright.sync_api import sync_playwright
port,tag=sys.argv[1],sys.argv[2]
pages=['index','wcf','recite','history','compare']
JS='''()=>new Promise(res=>{const d=[];let last=performance.now(),t0=last;let lt=0;
 try{new PerformanceObserver(l=>l.getEntries().forEach(e=>lt+=e.duration)).observe({type:'longtask',buffered:false})}catch(e){}
 function f(t){d.push(t-last);last=t;window.scrollBy(0,innerHeight*0.06);if(t-t0<5000)requestAnimationFrame(f);else{
 const n=d.length,avg=d.reduce((a,b)=>a+b,0)/n;res({fps:+(1000/avg).toFixed(1),jank:+(100*d.filter(x=>x>33.4).length/n).toFixed(1),p95:+d.sort((a,b)=>a-b)[Math.floor(n*.95)].toFixed(1),longtask:Math.round(lt)})}}
 requestAnimationFrame(f)})'''
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--enable-gpu-rasterization'])
    for w,h,thr in ((390,844,4),(1440,900,1)):
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if w<500 else 1)
        for n in pages:
            pg=ctx.new_page();cdp=ctx.new_cdp_session(pg)
            cdp.send('Emulation.setCPUThrottlingRate',{'rate':thr})
            pg.goto(f'http://127.0.0.1:{port}/{n}.html',wait_until='load',timeout=90000);pg.wait_for_timeout(2500)
            cdp.send('Performance.enable')
            m0={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
            r=pg.evaluate(JS)
            m1={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
            for k in ('LayoutDuration','RecalcStyleDuration','ScriptDuration','TaskDuration'):
                r[k[:-8]+'_ms']=round((m1[k]-m0[k])*1000)
            print(tag,w,n,json.dumps(r,ensure_ascii=False),flush=True);pg.close()
    b.close()
