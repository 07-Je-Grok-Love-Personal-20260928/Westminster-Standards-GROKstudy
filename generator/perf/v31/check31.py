import sys,json
from playwright.sync_api import sync_playwright
PAGES=['index','history','atlas','wcf','wlc','wsc','compare','recite','memory','creeds','sources']
import os
if os.environ.get('PAGES'): PAGES=os.environ['PAGES'].split(',')
mode=sys.argv[1]  # layout | themes
base=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:18931/'
pals=os.environ.get('PALS','aurora,jade,crimson,ocean,sunset,parchment,ink,sakura,royal,nord').split(',')
JS_LAYOUT='''()=>{const W=innerWidth,bad=[];const skip=e=>e.closest('.cm-stage,.hscroll,.lmap,.fab,.tbl,.mermaid,.topnav,.tbar,.leaflet-container,.pop,.toc,.backdrop,.hero .shine,.flash,.venn');
for(const e of document.querySelectorAll('main *')){if(skip(e))continue;const r=e.getBoundingClientRect();if(r.width===0)continue;if(r.right>W+1||r.left<-1){bad.push(e.tagName+'.'+e.className+' '+Math.round(r.left)+'/'+Math.round(r.right));if(bad.length>5)break}}
const trunc=[];for(const e of document.querySelectorAll('main *')){const cs=getComputedStyle(e);if((cs.overflowX==='hidden'||cs.textOverflow==='ellipsis')&&e.scrollWidth>e.clientWidth+2&&!skip(e)&&!e.matches('details,.hero,.donut .ring,.bar .bt,.qa,.card,.callout,.chain a,.stat,.mermaid,.src,.cv')){trunc.push(e.tagName+'.'+e.className);if(trunc.length>5)break}}
const tb=document.querySelector('.topbar').getBoundingClientRect();const kids=[...document.querySelector('.topbar').children].map(c=>c.getBoundingClientRect());let ov=0;for(let i=0;i<kids.length-1;i++)if(kids[i].right>kids[i+1].left+1)ov++;
return {docOverflow:document.documentElement.scrollWidth-W,bad,trunc,topbarOverlap:ov,mermaid:[...document.querySelectorAll('.mermaid')].filter(m=>!m.querySelector('svg')).length+'/'+document.querySelectorAll('.mermaid').length,
 imgs:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length,map:null,lblOv:(()=>{let n=0,ex=[];document.querySelectorAll('.cm-stage').forEach(st=>{const S=st.getBoundingClientRect();const rs=[...st.querySelectorAll('.pl,.pin')].filter(e=>getComputedStyle(e).display!=='none').map(e=>[e,e.getBoundingClientRect()]);for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){const [a,A]=rs[i],[b,B]=rs[j];if(a.contains(b)||b.contains(a))continue;if(!(a.matches('.pl')||b.matches('.pl')))continue;const w=Math.min(A.right,B.right)-Math.max(A.left,B.left),h=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);if(w>3&&h>3){n++;if(ex.length<4)ex.push((a.textContent+'|'+b.textContent).slice(0,40))}}});return [n,ex]})()}}'''
JS_CONTRAST='''()=>{const L=c=>{const m=c.match(/[\\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return [0.2126*f(m[0])+0.7152*f(m[1])+0.0722*f(m[2]),m[3]===undefined?1:m[3]]};
const bgOf=e=>{while(e){const c=getComputedStyle(e).backgroundColor;const a=c.match(/[\\d.]+/g);if(a&&(a.length<4||+a[3]>0.5))return c;e=e.parentElement}return getComputedStyle(document.body).backgroundColor};
const res={};for(const sel of ['.c-term','.c-ref','.callout b.lbl','.callout','mark','.u-bib','.tb','main section:not(.hero) p','.muted','.toc li a','.qa .a','.c-neg','.q-sum','.q-src','.m-blue','.m-green','.u-key','.hl-person']){const e=document.querySelector(sel);if(!e)continue;const fg=L(getComputedStyle(e).color.replace(/color\\(srgb ([\\d.]+) ([\\d.]+) ([\\d.]+)\\)/,(m,a,b,c)=>`rgb(${a*255},${b*255},${c*255})`));const bc=bgOf(e).replace(/color\\(srgb ([\\d.]+) ([\\d.]+) ([\\d.]+)(?: \\/ ([\\d.]+))?\\)/,(m,a,b,c,d)=>`rgba(${a*255},${b*255},${c*255},${d||1})`);const bg=L(bc);const r=(Math.max(fg[0],bg[0])+.05)/(Math.min(fg[0],bg[0])+.05);res[sel]=+r.toFixed(2)}return res}'''
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    combos=[('aurora','light')] if mode=='layout' else [(pa,m) for pa in pals for m in ('light','dark')] if mode=='all' else [(pa,m) for pa in pals for m in ('light','dark')]
    WS=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else (390,768,1440)
    for w in WS:
        for pal,md in combos:
            ctx=b.new_context(viewport={'width':w,'height':844 if w<500 else 900})
            ctx.add_init_script(f"localStorage.setItem('wsg_palette',JSON.stringify('{pal}'));localStorage.setItem('wsg_mode',JSON.stringify('{md}'))")
            for n in PAGES:
                x=ctx.new_page(); errs=[]
                x.on('pageerror',lambda e:errs.append(str(e)[:120])); x.on('console',lambda m: m.type=='error' and errs.append(m.text[:120]))
                x.goto(base+n+'.html',wait_until='load',timeout=90000)
                if mode=='layout':
                    h=x.evaluate('document.documentElement.scrollHeight')
                    for y in range(0,h,700): x.evaluate(f'scrollTo(0,{y})'); x.wait_for_timeout(60)
                    x.wait_for_timeout(2500)
                    r=x.evaluate(JS_LAYOUT)
                elif mode=='all':
                    h=x.evaluate('document.documentElement.scrollHeight')
                    for y in range(0,h,1100): x.evaluate(f'scrollTo(0,{y})'); x.wait_for_timeout(35)
                    x.wait_for_timeout(900); x.evaluate('window.__hydrateAll&&window.__hydrateAll()'); x.wait_for_timeout(200)
                    r=x.evaluate(JS_LAYOUT); x.evaluate('scrollTo(0,document.documentElement.scrollHeight/3)'); x.wait_for_timeout(300)
                    r['contrast']=x.evaluate(JS_CONTRAST); r['theme']=x.evaluate('document.documentElement.dataset.theme+"/"+document.documentElement.dataset.palette')
                    for t in x.query_selector_all('.tabs .tb')[:12]:
                        try: t.click(timeout=1500)
                        except Exception: pass
                    r['tabsOverflow']=x.evaluate("[...document.querySelectorAll('.tabs')].filter(t=>t.getBoundingClientRect().right>innerWidth+1).length")
                else:
                    x.wait_for_timeout(400); x.evaluate('scrollTo(0,document.documentElement.scrollHeight/3)'); x.wait_for_timeout(500)
                    r={'docOverflow':x.evaluate('document.documentElement.scrollWidth-innerWidth'),'contrast':x.evaluate(JS_CONTRAST),'theme':x.evaluate('document.documentElement.dataset.theme+"/"+document.documentElement.dataset.palette')}
                r['errs']=errs; r.update(page=n,w=w,pal=pal,mode=md)
                out.append(r); x.close()
            ctx.close()
    b.close()
json.dump(out,open(f'/workspace/perf/v31/check_{mode}_{os.environ.get('TAG','')}_{"-".join(map(str,WS))}.json','w'),ensure_ascii=False,indent=0)
probs=[r for r in out if r.get('docOverflow',0)>0 or r.get('bad') or r.get('trunc') or r.get('topbarOverlap') or r['errs'] or (r.get('mermaid') and not r['mermaid'].startswith('0/')) or r.get('imgs') or r.get('tabsOverflow') or (r.get('lblOv') and r['lblOv'][0]>0) or (r.get('map') is not None and r.get('map')==0) or (r.get('contrast') and min(r['contrast'].values())<4.5)]
print('checked',len(out),'problems',len(probs))
for r in probs[:40]: print(json.dumps(r,ensure_ascii=False)[:400])
