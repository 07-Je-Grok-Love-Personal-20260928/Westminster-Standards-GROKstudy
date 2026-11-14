"""v3.2 full QA: pages x widths x palettes x light/dark. Per load: scroll through, hydrate all, open every <details>, click every tab,
every map view tab (concept / story; live map is tested separately with tiles blocked), TOC toggle, theme panel + legend panel, skim/cloze;
then check horizontal overflow, elements outside the viewport, truncation, concept-map label overlap, panel overflow, console errors."""
import sys,json,os,re
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(__file__))
from importlib import util
spec=util.spec_from_file_location('c31',os.path.join(os.path.dirname(__file__),'v31','check31.py'))
src=open(os.path.join(os.path.dirname(__file__),'v31','check31.py')).read()
JS_LAYOUT=re.search(r"JS_LAYOUT='''(.*?)'''",src,re.S).group(1)
JS_CONTRAST=re.search(r"JS_CONTRAST='''(.*?)'''",src,re.S).group(1).replace('\\\\','\\')
PAGES=os.environ.get('PAGES','index,history,atlas,wcf,wlc,wsc,compare,recite,memory,creeds,sources').split(',')
PALS=os.environ.get('PALS','aurora,jade,crimson,ocean,sunset,parchment,ink,sakura,royal,nord').split(',')
WS=[int(x) for x in sys.argv[1].split(',')]
base=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:18931/'
tag=sys.argv[3] if len(sys.argv)>3 else 'x'
PANEL='''()=>{const W=innerWidth,H=innerHeight,o=[];for(const s of ['#themePanel','#legendPanel']){const e=document.querySelector(s);if(!e||!e.classList.contains('open'))continue;const r=e.getBoundingClientRect();if(r.left<-1||r.right>W+1||r.top<-1||r.bottom>H+1)o.push(s+' '+[r.left,r.right,r.top,r.bottom].map(Math.round))}
 const t=document.querySelector('.toc');if(t){const r=t.getBoundingClientRect();if(r.width&&getComputedStyle(t).visibility!=='hidden'&&(r.right>W+1))o.push('toc '+Math.round(r.right))}
 const f=document.querySelector('.fab');if(f){const r=f.getBoundingClientRect();if(r.right>W+1||r.bottom>H+1)o.push('fab')}return o}'''
out=[]
DONE=set()
if os.path.exists(f'/workspace/perf/v32/qa_{tag}.jsonl'):
    for l in open(f'/workspace/perf/v32/qa_{tag}.jsonl'):
        r=json.loads(l); out.append(r); DONE.add((r['w'],r['pal'],r['mode']))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in WS:
        for pal in PALS:
            for md in ('light','dark'):
                if (w,pal,md) in DONE: continue
                ctx=b.new_context(viewport={'width':w,'height':844 if w<500 else 900},has_touch=w<500,is_mobile=w<500)
                ctx.route(re.compile(r'openstreetmap|arcgisonline|opentopomap|autonavi|earthdata|cyclosm'),lambda r:r.abort())
                ctx.add_init_script(f"localStorage.setItem('wsg_palette',JSON.stringify('{pal}'));localStorage.setItem('wsg_mode',JSON.stringify('{md}'))")
                for n in PAGES:
                    x=ctx.new_page(); errs=[]
                    x.on('pageerror',lambda e:errs.append('PE '+str(e)[:140])); x.on('console',lambda m: m.type=='error' and not re.search(r'net::ERR_FAILED|ERR_CONNECTION|Failed to load resource',m.text) and errs.append(m.text[:140]))
                    x.goto(base+n+'.html',wait_until='load',timeout=90000)
                    h=x.evaluate('document.documentElement.scrollHeight')
                    for y in range(0,h,2000): x.evaluate(f'scrollTo({{top:{y},behavior:"instant"}})'); x.wait_for_timeout(15)
                    x.evaluate('window.__hydrateAll&&window.__hydrateAll()'); x.wait_for_timeout(150)
                    nd=x.evaluate("(()=>{const d=[...document.querySelectorAll('main details')];d.forEach(e=>e.open=true);window.__hydrateAll&&window.__hydrateAll();document.querySelectorAll('main details').forEach(e=>e.open=true);return document.querySelectorAll('main details').length})()")
                    x.wait_for_timeout(200)
                    r=x.evaluate(JS_LAYOUT); r['details']=nd
                    # tabs (all), map view tabs (concept/story), each layout-checked
                    nt=x.evaluate("(()=>{let n=0;document.querySelectorAll('.tabs .tb, .mtabs [data-v=s], .mtabs [data-v=c]').forEach(b=>{b.click();n++});return n})()")
                    x.wait_for_timeout(300); r2=x.evaluate(JS_LAYOUT)
                    x.evaluate("document.querySelectorAll('.mtabs [data-v=s]').forEach(b=>b.click())"); x.wait_for_timeout(250); r3=x.evaluate(JS_LAYOUT)
                    r['tabsClicked']=nt
                    for k in ('bad','trunc'):
                        r[k]=(r.get(k) or [])+[v for v in (r2.get(k) or [])+(r3.get(k) or []) if v not in (r.get(k) or [])]
                    r['docOverflow']=max(r['docOverflow'],r2['docOverflow'],r3['docOverflow'])
                    r['lblOv']=[max(r['lblOv'][0],r2['lblOv'][0]),r['lblOv'][1]+r2['lblOv'][1]]
                    r['tabsOverflow']=x.evaluate("[...document.querySelectorAll('.tabs,.mtabs')].filter(t=>t.getBoundingClientRect().right>innerWidth+1).length")
                    # TOC, theme picker, legend, modes
                    pan=[]
                    x.evaluate("scrollTo({top:document.documentElement.scrollHeight/3,behavior:'instant'})"); x.wait_for_timeout(150)
                    C=lambda sel:x.evaluate(f"(()=>{{const e=document.querySelector('{sel}');if(!e)return 0;e.click();return 1}})()")
                    try:
                        C('#tocBtn'); x.wait_for_timeout(400); pan+=x.evaluate(PANEL); C('#tocBtn'); x.evaluate("document.body.classList.remove('toc-open')"); x.wait_for_timeout(200)
                        C('#themeBtn'); x.wait_for_timeout(240); pan+=x.evaluate(PANEL)
                        C('#themePanel [data-opt=skim]'); C('#themePanel [data-opt=cloze]'); C('#themePanel [data-opt=cloze]')
                        sk=x.evaluate("document.documentElement.classList.contains('skim')||document.documentElement.classList.contains('cloze')")
                        if sk: pan.append('mode-not-cleared')
                        C('#legendBtn'); x.wait_for_timeout(240); pan+=x.evaluate(PANEL); x.keyboard.press('Escape')
                        C('.fab-main'); x.wait_for_timeout(240); pan+=x.evaluate(PANEL); x.keyboard.press('Escape')
                    except Exception as e: pan.append('click-fail '+str(e)[:80])
                    r['panels']=pan; r['docOverflow2']=x.evaluate('document.documentElement.scrollWidth-innerWidth')
                    if w==390: r['contrast']=x.evaluate(JS_CONTRAST)
                    r['errs']=errs; r.update(page=n,w=w,pal=pal,mode=md)
                    out.append(r); x.close()
                ctx.close()
                with open(f'/workspace/perf/v32/qa_{tag}.jsonl','a') as f:
                    for r in out[-len(PAGES):]: f.write(json.dumps(r,ensure_ascii=False)+'\n')
                print(tag,w,pal,md,'done',len(out),flush=True)
    b.close()
json.dump(out,open(f'/workspace/perf/v32/qa_{tag}.json','w'),ensure_ascii=False)
probs=[r for r in out if r['docOverflow']>0 or r['docOverflow2']>0 or r.get('bad') or r.get('trunc') or r.get('topbarOverlap') or r['errs'] or not str(r.get('mermaid','0/')).startswith('0/') or r.get('imgs') or r.get('tabsOverflow') or r['lblOv'][0]>0 or r['panels'] or (r.get('contrast') and min(r['contrast'].values())<4.5)]
print('checked',len(out),'problems',len(probs))
for r in probs[:30]: print(json.dumps({k:r[k] for k in r if k not in ('contrast',)},ensure_ascii=False)[:420])
if any(r.get('contrast') for r in probs): print('contrast-low',[ (r['page'],r['pal'],r['mode'],{k:v for k,v in r['contrast'].items() if v<4.5}) for r in probs if r.get('contrast') and min(r['contrast'].values())<4.5][:20])
