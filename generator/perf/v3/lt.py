import sys,json
from playwright.sync_api import sync_playwright
port=sys.argv[1]; page=sys.argv[2] if len(sys.argv)>2 else 'wcf'
JS='''()=>new Promise(res=>{const L=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>L.push([Math.round(e.startTime),Math.round(e.duration)]))).observe({type:'longtask'});
let t0=performance.now();function f(t){window.scrollBy(0,innerHeight*0.06);if(t-t0<5000)requestAnimationFrame(f);else res({L,y:scrollY})}requestAnimationFrame(f)})'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    pg=ctx.new_page();cdp=ctx.new_cdp_session(pg);cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    pg.goto(f'http://127.0.0.1:{port}/{page}.html',wait_until='load');pg.wait_for_timeout(2500)
    b.start_tracing(page=pg,categories=['devtools.timeline','disabled-by-default-devtools.timeline'])
    r=pg.evaluate(JS)
    tr=b.stop_tracing()
    print(r)
    ev=json.loads(tr)['traceEvents']
    tops=sorted([e for e in ev if e.get('ph')=='X' and e.get('dur',0)>20000],key=lambda e:-e['dur'])[:15]
    for e in tops: print(e['name'],round(e['dur']/1000),json.dumps(e.get('args',{}))[:200])
    b.close()
