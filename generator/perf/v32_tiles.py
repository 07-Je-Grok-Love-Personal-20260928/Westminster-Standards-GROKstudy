"""v3.2 map failover tests: block / hang provider hosts and check what the live map ends up showing."""
import sys,json,re
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18931/'
H={'carto':r'basemaps\.cartocdn\.com','esri':r'server\.arcgisonline\.com','osm':r'tile\.openstreetmap\.org','osmde':r'tile\.openstreetmap\.de','hot':r'tile\.openstreetmap\.fr/hot',
   'cyclosm':r'tile-cyclosm\.openstreetmap\.fr','topo':r'opentopomap\.org','gaode':r'autonavi\.com'}
ALL=list(H)
cases=[
 dict(name='1 正常网络（无拦截）',blk=[],how='abort'),
 dict(name='2 CARTO+Esri+OSM 拦截',blk=['carto','esri','osm'],how='abort'),
 dict(name='3 仅高德可用（模拟中国大陆）',blk=[k for k in ALL if k!='gaode'],how='abort',map='asia'),
 dict(name='4 全部拦截',blk=ALL,how='abort'),
 dict(name='5 全部无响应（超时）',blk=ALL,how='hang'),
 dict(name='6 测速通过、但正式瓦片失败（OSM）',blk=[],how='abort',late='osm',only='osm'),
 dict(name='7 深色主题 + 仅 CARTO 可用',blk=[k for k in ALL if k!='carto'],how='abort',dark=True),
 dict(name='8 手动选择 Esri 卫星',blk=[],how='abort',pick='esrisat'),
 dict(name='9 手动选择被拦截的源（OSM 德国）',blk=['osmde'],how='abort',pick='osmde'),
 dict(name='10 伦敦街区图：仅 Esri 可用',blk=[k for k in ALL if k!='esri'],how='abort',map='london'),
]
res=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for c in cases:
        ctx=b.new_context(viewport={'width':1280,'height':900})
        ctx.add_init_script("window.__tileTimeout=2500;window.__probeTimeout=2500;"+("localStorage.setItem('wsg_mode','\"dark\"');" if c.get('dark') else "localStorage.setItem('wsg_mode','\"light\"');")+(f"localStorage.setItem('wsg_tiles','\"{c['pick']}\"');" if c.get('pick') else "localStorage.removeItem('wsg_tiles');"))
        for k in c['blk']:
            rx=re.compile(H[k])
            if c['how']=='abort': ctx.route(rx,lambda r:r.abort('connectionrefused'))
            else: ctx.route(rx,lambda r:None)
        if c.get('only'):  # block everything except OSM; OSM probe (z=4) passes but real tiles fail
            for k in ALL:
                if k!=c['only']: ctx.route(re.compile(H[k]),lambda r:r.abort('connectionrefused'))
            ctx.route(re.compile(H[c['late']]+r'/(?!4/)'),lambda r:r.abort('connectionrefused'))
        x=ctx.new_page();errs=[];x.on('pageerror',lambda e:errs.append(str(e)[:150]))
        x.goto(base+'atlas.html',wait_until='load')
        mid=c.get('map','reform')
        x.evaluate(f"__goTo(document.getElementById('mb-{mid}'))");x.wait_for_timeout(500)
        x.click(f'#mb-{mid} .mtabs [data-v=l]')
        x.wait_for_function(f"(document.getElementById('mb-{mid}').dataset.tiles||'').match(/^(on|off)/)",timeout=90000)
        x.wait_for_timeout(1500)
        st=x.evaluate(f"document.getElementById('mb-{mid}').dataset.tiles");txt=x.inner_text(f'#mb-{mid} .mst')
        loaded=x.evaluate(f"document.querySelectorAll('#mb-{mid} .leaflet-tile-loaded').length")
        base_ok=x.evaluate(f"document.querySelectorAll('#mb-{mid} .leaflet-basePane-pane canvas').length")
        pins=x.evaluate(f"document.querySelectorAll('#mb-{mid} .lpin').length")
        x.locator(f'#mb-{mid} .mv-l').screenshot(path=f"/workspace/perf/v32/tiles_{len(res)+1}.png")
        res.append(dict(case=c['name'],status=st,text=txt,tilesLoaded=loaded,offlineBase=base_ok,pins=pins,log=x.evaluate('window.__tileLog'),errs=errs))
        print(json.dumps(res[-1],ensure_ascii=False)[:600],flush=True)
        ctx.close()
    b.close()
json.dump(res,open('/workspace/perf/v32/tiles.json','w'),ensure_ascii=False,indent=1)
