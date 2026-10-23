import sys,json
from playwright.sync_api import sync_playwright
base,tag=sys.argv[1],sys.argv[2]
pages=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] else ['index','wcf','wlc','wsc','recite','creeds','history','atlas','compare','memory','sources']
INIT='''window.__m={lt:[],cls:0,ev:[]};
try{new PerformanceObserver(l=>l.getEntries().forEach(e=>__m.lt.push([e.startTime,e.duration]))).observe({type:'longtask',buffered:true})}catch(e){}
try{new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)__m.cls+=e.value})).observe({type:'layout-shift',buffered:true})}catch(e){}
try{new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(e.interactionId)__m.ev.push([e.name,Math.round(e.duration)])})).observe({type:'event',durationThreshold:16,buffered:true})}catch(e){}'''
thr=float(sys.argv[4]) if len(sys.argv)>4 else 4
w=int(sys.argv[5]) if len(sys.argv)>5 else 390
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':w,'height':844 if w<500 else 900},device_scale_factor=2 if w<500 else 1,has_touch=w<500,is_mobile=w<500)
    ctx.add_init_script(INIT)
    for n in pages:
        pg=ctx.new_page();cdp=ctx.new_cdp_session(pg);cdp.send('Emulation.setCPUThrottlingRate',{'rate':thr});cdp.send('Performance.enable')
        pg.goto(f'{base}{n}.html',wait_until='load',timeout=120000);pg.wait_for_timeout(3000)
        nav=pg.evaluate("(()=>{const t=performance.getEntriesByType('navigation')[0];const f=performance.getEntriesByName('first-contentful-paint')[0];return {dcl:Math.round(t.domContentLoadedEventEnd),load:Math.round(t.loadEventEnd),fcp:f?Math.round(f.startTime):null,nodes:document.getElementsByTagName('*').length,html_kb:Math.round(t.transferSize/1024)}})()")
        m={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
        nav['script_ms']=round(m['ScriptDuration']*1000);nav['layout_ms']=round(m['LayoutDuration']*1000);nav['style_ms']=round(m['RecalcStyleDuration']*1000);nav['heapMB']=round(m['JSHeapUsedSize']/1e6,1)
        lt=pg.evaluate('__m.lt');nav['tbt']=round(sum(max(0,d-50) for s,d in lt));nav['maxLT']=round(max([d for s,d in lt],default=0))
        def tap(sel):
            try:
                el=pg.locator(sel).first
                if el.count() and el.is_visible(): (el.tap() if w<500 else el.click()); pg.wait_for_timeout(450)
            except Exception as e: pass
        for s in ('#themeBtn','#themeBtn','.fab-main','.fab-main','.mtabs [data-v]:nth-child(2)'): tap(s)
        pg.keyboard.press('Escape');pg.wait_for_timeout(300)
        pg.evaluate("window.scrollBy(0,innerHeight*3)");pg.wait_for_timeout(800);pg.evaluate("window.scrollBy(0,innerHeight*6)");pg.wait_for_timeout(800)
        ev=pg.evaluate('__m.ev');nav['inp']=max([d for _,d in ev],default=0);nav['cls']=round(pg.evaluate('__m.cls'),3)
        print(tag,w,n,json.dumps(nav),flush=True);pg.close()
    b.close()
