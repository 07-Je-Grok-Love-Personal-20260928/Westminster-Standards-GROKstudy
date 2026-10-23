import sys,json,re
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18931/'
H={'osm':re.compile(r'https://tile\.openstreetmap\.org/'),'hot':re.compile(r'https://[abc]\.tile\.openstreetmap\.fr/'),'topo':re.compile(r'https://[abc]\.tile\.opentopomap\.org/')}
cases=[('none blocked',[],'abort'),('OSM blocked',['osm'],'abort'),('OSM+HOT blocked',['osm','hot'],'abort'),('all blocked',['osm','hot','topo'],'abort'),('OSM hangs (timeout)',['osm'],'hang'),('all hang (timeout)',['osm','hot','topo'],'hang')]
res=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,blk,how in cases:
        ctx=b.new_context(viewport={'width':1280,'height':900})
        ctx.add_init_script("window.__tileTimeout=3000")
        for k in blk:
            if how=='abort': ctx.route(H[k],lambda r:r.abort('connectionrefused'))
            else: ctx.route(H[k],lambda r:None)  # never fulfil
        x=ctx.new_page();errs=[];x.on('pageerror',lambda e:errs.append(str(e)[:150]))
        x.goto(base+'atlas.html',wait_until='load')
        x.evaluate("document.getElementById('mb-reform').scrollIntoView()")
        x.click('#mb-reform .mtabs [data-v=l]')
        x.wait_for_function("(document.getElementById('mb-reform').dataset.tiles||'').match(/^(on|off)/)",timeout=30000)
        x.wait_for_timeout(1200)
        st=x.evaluate("document.getElementById('mb-reform').dataset.tiles");txt=x.inner_text('#mb-reform .mst')
        base_ok=x.evaluate("document.querySelectorAll('#mb-reform .leaflet-basePane-pane canvas, #mb-reform .leaflet-pane canvas').length")
        loaded=x.evaluate("document.querySelectorAll('#mb-reform .leaflet-tile-loaded').length")
        x.locator('#mb-reform .mv-l').screenshot(path=f"/workspace/perf/v3/tiles_{len(res)}.png")
        res.append(dict(case=name,status=st,text=txt,tilesLoaded=loaded,baseCanvas=base_ok,log=x.evaluate('window.__tileLog'),errs=errs))
        ctx.close()
    b.close()
for r in res: print(json.dumps(r,ensure_ascii=False))
json.dump(res,open('/workspace/perf/v3/tiles.json','w'),ensure_ascii=False,indent=1)
