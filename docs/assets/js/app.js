/* Westminster Standards GROKstudy v3 — interactions (deferred, rAF-throttled, lazy libs) */
(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const LS={get:(k,d)=>{try{const v=localStorage.getItem('wsg_'+k);return v===null?d:JSON.parse(v)}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem('wsg_'+k,JSON.stringify(v))}catch(e){}}};
const root=document.documentElement, body=document.body;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const isMobile=()=>matchMedia('(max-width:980px)').matches;
const idle=window.requestIdleCallback||(f=>setTimeout(f,200));
const loadScript=(src)=>new Promise((res,rej)=>{const s=document.createElement('script');s.src=src;s.async=true;s.onload=res;s.onerror=rej;document.head.appendChild(s)});
const loadCSS=(href)=>{const l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l)};

/* ---------- theme: palette + mode (applied pre-paint by inline BOOT script) ---------- */
const mq=matchMedia('(prefers-color-scheme: dark)');
function applyMode(){const m=LS.get('mode','auto');root.dataset.theme=m==='auto'?(mq.matches?'dark':'light'):m;
  $$('#modeSeg button').forEach(b=>b.classList.toggle('on',b.dataset.mode===m));}
function applyPalette(p){root.dataset.palette=p;$$('.sw').forEach(b=>b.classList.toggle('on',b.dataset.pal===p));
  const c=getComputedStyle(root).getPropertyValue('--a1').trim();const tm=$('meta[name=theme-color]');if(tm&&c)tm.content=c;}
mq.addEventListener&&mq.addEventListener('change',()=>{if(LS.get('mode','auto')==='auto'){applyMode();themeChanged()}});
let themeTimer;function themeChanged(){clearTimeout(themeTimer);themeTimer=setTimeout(()=>{reMermaid();LMAPS.forEach(m=>m.restyle())},120)}
const LMAPS=[];
applyMode();applyPalette(LS.get('palette','aurora'));
$$('.sw').forEach(b=>b.addEventListener('click',()=>{LS.set('palette',b.dataset.pal);applyPalette(b.dataset.pal);themeChanged()}));
$$('#modeSeg button').forEach(b=>b.addEventListener('click',()=>{LS.set('mode',b.dataset.mode);applyMode();themeChanged()}));
function syncOpts(){$$('#optSeg button').forEach(b=>{const k=b.dataset.opt;b.classList.toggle('on',LS.get('motion','on')!=='off')})}
$$('#optSeg button').forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.opt;
  {const off=LS.get('motion','on')!=='off';LS.set('motion',off?'off':'on');root.classList.toggle('no-motion',off)}syncOpts()}));
syncOpts();
/* popovers */
const pops=[['themeBtn','themePanel'],['legendBtn','legendPanel']];
function closePops(except){pops.forEach(([b,p])=>{if(p!==except){$('#'+p)?.classList.remove('open');$('#'+b)?.setAttribute('aria-expanded','false')}})}
pops.forEach(([b,p])=>{const bt=$('#'+b),pn=$('#'+p);if(!bt||!pn)return;bt.addEventListener('click',e=>{e.stopPropagation();const o=!pn.classList.contains('open');closePops(p);pn.classList.toggle('open',o);bt.setAttribute('aria-expanded',o)});pn.addEventListener('click',e=>e.stopPropagation())});
document.addEventListener('click',()=>closePops());
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closePops();body.classList.remove('toc-open')}});

/* ---------- TOC ---------- */
const toc=$('#tocList'), main=$('main');
function buildToc(){const hs=$$('h2.h, h3.h',main);hs.forEach((h,i)=>{if(!h.id)h.id='s'+i});
  if(toc&&!toc.dataset.custom)toc.innerHTML=hs.map(h=>`<li class="${h.tagName==='H3'?'l3':'l2'}"><a href="#${h.id}">${h.dataset.toc||h.textContent.trim()}</a></li>`).join('');return hs}
let hs=buildToc();
if(!isMobile()&&LS.get('tocoff',false))body.classList.add('toc-off');
$('#tocBtn')?.addEventListener('click',()=>{if(isMobile())body.classList.toggle('toc-open');else{body.classList.toggle('toc-off');LS.set('tocoff',body.classList.contains('toc-off'))}setTimeout(()=>LMAPS.forEach(m=>m.map.invalidateSize()),400)});
$('.scrim')?.addEventListener('click',()=>body.classList.remove('toc-open'));
toc?.addEventListener('click',e=>{if(e.target.tagName==='A'&&isMobile())body.classList.remove('toc-open')});
const tf=$('#tocFilter');if(tf)tf.addEventListener('input',()=>{const v=tf.value.trim();$$('li',toc).forEach(li=>li.style.display=!v||li.textContent.includes(v)?'':'none')});
let activeIO;
function watchActive(){activeIO&&activeIO.disconnect();const links=new Map($$('a',toc||document.createElement('div')).map(a=>[a.getAttribute('href').slice(1),a]));const box=$('.toc');
  activeIO=new IntersectionObserver(es=>{es.forEach(e=>{if(!e.isIntersecting)return;const a=links.get(e.target.id);if(!a)return;links.forEach(x=>x.classList.remove('active'));a.classList.add('active');
    if(box&&!isMobile()){const top=a.offsetTop-box.clientHeight/2;if(Math.abs(box.scrollTop-top)>box.clientHeight/3)box.scrollTo({top,behavior:RM?'auto':'smooth'})}})},{rootMargin:'-12% 0px -78% 0px'});
  const obs=$$('h2.h, h3.h, .rq[id]',main).filter(h=>links.has(h.id));obs.forEach(h=>activeIO.observe(h));
  /* exact fix-up after scrolling settles (binary search over heading positions; layout is clean so this is cheap) */
  let st;const settleActive=()=>{const lim=innerHeight*0.25;let lo=0,hi=obs.length-1,ans=-1;while(lo<=hi){const m=(lo+hi)>>1;const t=obs[m].getBoundingClientRect().top;if(t<=lim){ans=m;lo=m+1}else hi=m-1}
    const el=obs[Math.max(0,ans)];const a=el&&links.get(el.id);if(a&&!a.classList.contains('active')){links.forEach(x=>x.classList.remove('active'));a.classList.add('active');if(box&&!isMobile()){const top=a.offsetTop-box.clientHeight/2;box.scrollTo({top,behavior:'auto'})}}};
  window.__settleActive=settleActive;removeEventListener('scroll',window.__stH||(()=>{}));window.__stH=()=>{clearTimeout(st);st=setTimeout(settleActive,140)};addEventListener('scroll',window.__stH,{passive:true});setTimeout(settleActive,900)}
watchActive();
window.__rebuildToc=()=>{watchActive()};

/* ---------- scroll: progress + floating nav cluster (one rAF per frame max) ---------- */
const pg=$('.progress i'), fab=$('.fab'), fr=$('.fab .fr1'), fm=$('.fab-main');let ticking=false,lastTop=-1,dirY=0;
const SDA=window.CSS&&CSS.supports&&CSS.supports('animation-timeline: scroll()');if(SDA)root.classList.add('sda');
let maxS=0;const remax=()=>{maxS=root.scrollHeight-root.clientHeight||1};
function onFrame(){ticking=false;const y=window.scrollY;if(y===lastTop)return;const dy=y-lastTop;lastTop=y;if(!maxS)remax();const p=Math.min(1,y/maxS);
  if(!SDA){if(pg)pg.style.transform='scaleX('+p.toFixed(4)+')';if(fr)fr.style.strokeDashoffset=(100-p*100).toFixed(1)}
  if(fab){dirY=dy>0?Math.min(dirY+dy,400):Math.max(dirY+dy,-400);if(dirY>160&&y>500){fab.classList.add('hide');dirY=0}else if(dirY<-60||y<200||p>.985){fab.classList.remove('hide');dirY=Math.min(dirY,0)}}}
addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(onFrame)}},{passive:true});addEventListener('resize',()=>{maxS=0},{passive:true});new ResizeObserver(()=>{maxS=0}).observe(body);requestAnimationFrame(onFrame);
if(fab){const setOpen=o=>{fab.classList.toggle('open',o);fm.setAttribute('aria-expanded',o)};
  fm.addEventListener('click',e=>{e.stopPropagation();setOpen(!fab.classList.contains('open'))});
  document.addEventListener('click',e=>{if(!fab.contains(e.target))setOpen(false)});
  fab.addEventListener('keydown',e=>{if(e.key==='Escape'){setOpen(false);fm.focus()}});
  const nav=window.navigation, bk=$('[data-act=back]',fab), fw=$('[data-act=fwd]',fab);
  const syncNav=()=>{if(nav&&'canGoBack' in nav){bk.disabled=!nav.canGoBack;fw.disabled=!nav.canGoForward}else bk.disabled=history.length<2};syncNav();nav&&nav.addEventListener&&nav.addEventListener('currententrychange',syncNav);
  if(!$('#tocList'))$('[data-act=toc]',fab).hidden=true;
  fab.addEventListener('click',e=>{const b=e.target.closest('[data-act]');if(!b)return;const k=b.dataset.act;
    if(k==='back')history.back();else if(k==='fwd')history.forward();
    else if(k==='top'){scrollTo({top:0,behavior:RM?'auto':'smooth'});fab.classList.remove('hide')}
    else if(k==='bottom'){const f=$('footer.foot')||main.lastElementChild;goTo(f,true)}
    else if(k==='toc'){if(isMobile())body.classList.add('toc-open');else{body.classList.remove('toc-off');LS.set('tocoff',false)}setTimeout(()=>{const a=$('#tocList a.active')||$('#tocList a');a&&a.focus({preventScroll:false})},isMobile()?320:60)}
    if(k!=='toc')setOpen(false)})}

/* ---------- v3.1 progressive hydration: off-screen chapters / closed <details> live in <template> until needed ---------- */
const hyq=[];let hyBusy=false;
function hydrate(el){const t=el&&el.querySelector(':scope>template');if(!t){el&&el.classList.add('hy');return}
  t.replaceWith(t.content);el.classList.add('hy');initScope(el)}
function initScope(sc){watchLz(sc);initTabs(sc);paintMemos(sc);stagger(sc);$$('.rv,.bars,.stats',sc).forEach(x=>rio.observe(x));if(window.__onHydrate)window.__onHydrate(sc)}
function hydrateAll(){let n;do{n=$$('.lz:not(.hy),details.lzd:not(.hy)');n.forEach(hydrate)}while(n.length)}
function pump(){hyBusy=false;const t0=performance.now();while(hyq.length&&performance.now()-t0<8)hydrate(hyq.shift());if(hyq.length){hyBusy=true;requestAnimationFrame(pump)}}
const lzio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){lzio.unobserve(e.target);hyq.push(e.target);if(!hyBusy){hyBusy=true;requestAnimationFrame(pump)}}}),{rootMargin:'1600px 0px'});
const watchLz=sc=>$$('.lz:not(.hy)',sc).forEach(x=>lzio.observe(x));
document.addEventListener('toggle',e=>{const d=e.target;if(d.matches&&d.matches('details.lzd')&&d.open)hydrate(d)},true);
/* find an id even if it still sits inside a template; hydrate its ancestors */
function findId(id){for(let k=0;k<6;k++){const el=document.getElementById(id);if(el){let d=el.closest('details:not([open])');while(d){d.open=true;d=d.parentElement.closest('details:not([open])')}return el}
  const ts=$$('template');const t=ts.find(x=>x.content.getElementById(id))||ts.find(x=>[...x.content.querySelectorAll('template')].some(y=>y.content.getElementById(id)));if(!t)return null;hydrate(t.parentElement)}return null}
window.__findId=findId;window.__hydrateAll=hydrateAll;window.__hydrate=hydrate;
/* ---------- reveal + stagger + counters + charts ---------- */
function stagger(sc){$$('.grid,.stats,.flow,.chain,.rings',sc).forEach(g=>{let i=0;[...g.children].forEach(c=>{if(c.classList.contains('rv')){c.style.setProperty('--d',Math.min(i,6)*0.06+'s');i++}})})}stagger(document);
const rio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const t=e.target;t.classList.add('in');rio.unobserve(t);if(t.matches('.stats'))countUp(t)}}),{rootMargin:'0px 0px -6% 0px'});
$$('.rv,.bars,.stats').forEach(el=>rio.observe(el));watchLz(document);
function countUp(box){if(RM||root.classList.contains('no-motion'))return;$$('.stat .v',box).forEach(v=>{const t=v.textContent.trim();if(!/^\d{1,4}$/.test(t))return;const n=+t,from=n>1000?n-60:0,t0=performance.now();
  const step=now=>{const p=Math.min(1,(now-t0)/1100),e=1-Math.pow(1-p,3);v.textContent=Math.round(from+(n-from)*e);if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)})}
/* pause hero animations when off-screen */
const hio=new IntersectionObserver(es=>es.forEach(e=>e.target.classList.toggle('paused',!e.isIntersecting)));$$('.hero').forEach(h=>hio.observe(h));

/* ---------- tabs ---------- */
/* v3.1: delegated (works for lazily hydrated content too) */
const initTabs=sc=>$$('.tabs:not(.js)',sc).forEach(t=>t.classList.add('js'));initTabs(document);
function selTab(t,i){const bs=$$(':scope>.tbar>.tb',t),ps=$$(':scope>.tp',t);bs.forEach((b,j)=>{b.classList.toggle('on',j===i);b.setAttribute('aria-selected',j===i)});ps.forEach((p,j)=>p.classList.toggle('on',j===i))}
document.addEventListener('click',e=>{const b=e.target.closest('.tabs .tb');if(!b)return;const t=b.closest('.tabs');selTab(t,$$(':scope>.tbar>.tb',t).indexOf(b))});
document.addEventListener('keydown',e=>{const b=e.target.closest&&e.target.closest('.tabs .tb');if(!b||(e.key!=='ArrowRight'&&e.key!=='ArrowLeft'))return;const t=b.closest('.tabs'),bs=$$(':scope>.tbar>.tb',t),n=bs.length,i=(bs.indexOf(b)+(e.key==='ArrowRight'?1:n-1))%n;bs[i].focus();selTab(t,i)});

/* ---------- refs toggle / filters / timeline ---------- */
const rb=$('#refsBtn');if(rb){if(LS.get('norefs',false))body.classList.add('no-refs');rb.addEventListener('click',()=>{body.classList.toggle('no-refs');LS.set('norefs',body.classList.contains('no-refs'))})}
const df=$('#docFilter');if(df){let tmr;df.addEventListener('focus',()=>idle(hydrateAll),{once:true});df.addEventListener('input',()=>{clearTimeout(tmr);tmr=setTimeout(()=>{hydrateAll();const v=df.value.trim();$$('[data-search]').forEach(el=>{el.classList.toggle('hide',!!v&&!el.textContent.includes(v))});$$('.grp').forEach(g=>{if(!v){g.open=g.dataset.open==='1';return}g.open=true})},180)})}
$$('.filters[data-for]').forEach(f=>{f.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',f).forEach(x=>x.classList.remove('on'));b.classList.add('on');const k=b.dataset.k;$$(f.dataset.for+' [data-cat]').forEach(ev=>ev.classList.toggle('hide',k!=='all'&&!ev.dataset.cat.split(' ').includes(k)))})});

/* ---------- memorised marks + progress rings ---------- */
const done=LS.get('done',{});
const paintMemo=m=>{const k=m.dataset.k;m.classList.toggle('done',!!done[k]);m.textContent=done[k]?'✔ 已背':'☆ 标记'};const paintMemos=sc=>$$('.memo',sc).forEach(paintMemo);paintMemos(document);
document.addEventListener('click',e=>{const m=e.target.closest('.memo');if(!m)return;e.stopPropagation();const k=m.dataset.k;done[k]=!done[k];paintMemo(m);LS.set('done',done);updateCount()});
function updateCount(){$$('[data-count]').forEach(el=>{const p=el.dataset.count;el.textContent=Object.keys(done).filter(k=>done[k]&&k.startsWith(p)).length});
  $$('.pring[data-ring]').forEach(r=>{const p=r.dataset.ring,tot=+r.dataset.total;const n=Object.keys(done).filter(k=>done[k]&&k.startsWith(p)).length;const c=r.querySelector('.fgc');const L=2*Math.PI*45;c.style.strokeDasharray=L;c.style.strokeDashoffset=L*(1-Math.min(1,n/tot));r.querySelector('b').textContent=n+' / '+tot})}
updateCount();
document.addEventListener('click',e=>{const a=e.target.closest('.ansbody');if(a&&(body.classList.contains('mode-hide')||body.classList.contains('mode-cloze')))a.classList.toggle('show')});

/* ---------- lazy Mermaid (ESM, code-split) ---------- */
let mm=null, mmLoading=null; const mmSrc=new Map(); const mmDone=new Set();
const probe=(v)=>{const s=document.createElement('span');s.style.color=v;s.style.display='none';body.appendChild(s);const c=getComputedStyle(s).color;s.remove();return toHex(c)};
function toHex(c){let m=c.match(/color\(srgb ([\d.e-]+) ([\d.e-]+) ([\d.e-]+)/);let r,g,b;if(m){[r,g,b]=[m[1],m[2],m[3]].map(x=>Math.round(Math.max(0,Math.min(1,+x))*255))}else{m=c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)/);if(!m)return c;[r,g,b]=[m[1],m[2],m[3]].map(x=>Math.round(+x))}return '#'+[r,g,b].map(x=>x.toString(16).padStart(2,'0')).join('')}
function mmConfig(){const dark=root.dataset.theme==='dark';const a1=probe('var(--a1)'),a2=probe('var(--a2)'),ink=probe('var(--ink)'),card=probe('var(--card2)'),line=probe('color-mix(in srgb, var(--a2) 70%, var(--ink))');
  const tint=probe(dark?'color-mix(in srgb, var(--a1) 30%, #111827)':'color-mix(in srgb, var(--a1) 12%, #ffffff)');
  const tint2=probe(dark?'color-mix(in srgb, var(--a2) 28%, #111827)':'color-mix(in srgb, var(--a2) 10%, #ffffff)');
  return {startOnLoad:false,theme:'base',securityLevel:'loose',darkMode:dark,fontFamily:'PingFang SC, Microsoft YaHei, Noto Sans SC, sans-serif',
    themeVariables:{darkMode:dark,background:card,primaryColor:tint,primaryBorderColor:a1,primaryTextColor:ink,secondaryColor:tint2,secondaryBorderColor:a2,secondaryTextColor:ink,tertiaryColor:card,tertiaryTextColor:ink,lineColor:line,textColor:ink,mainBkg:tint,nodeBorder:a1,clusterBkg:tint2,edgeLabelBackground:card,fontSize:'15px'},
    flowchart:{useMaxWidth:true,htmlLabels:true,curve:'basis'},mindmap:{useMaxWidth:true}}}
function getMermaid(){if(mm)return Promise.resolve(mm);if(mmLoading)return mmLoading;
  mmLoading=loadScript('assets/vendor/mermaid/mermaid.min.js').then(()=>window.mermaid).then(m=>{mm=m;mm.initialize(mmConfig());return mm});return mmLoading}
let mmQueue=Promise.resolve(), lastScroll=0;addEventListener('scroll',()=>{lastScroll=performance.now()},{passive:true});
/* heavy work only when the user is not actively scrolling, and in idle time */
const whenCalm=()=>new Promise(res=>{const calm=()=>performance.now()-lastScroll>250;const chk=()=>{if(calm())idle(()=>calm()?res():setTimeout(chk,160),{timeout:1500});else setTimeout(chk,160)};chk()});
function renderMermaid(el){if(!mmSrc.has(el))mmSrc.set(el,el.textContent);mmQueue=mmQueue.then(whenCalm).then(()=>getMermaid()).then(m=>whenCalm().then(()=>m)).then(m=>{el.removeAttribute('data-processed');el.innerHTML=mmSrc.get(el);return m.run({nodes:[el]})}).then(()=>{el.setAttribute('data-done','');mmDone.add(el)}).catch(e=>{console.warn(e);el.setAttribute('data-done','');el.innerHTML='<p class="muted">图表加载失败（可能是网络限制），请刷新重试。</p>'})}
function reMermaid(){if(!mm)return;mm.initialize(mmConfig());mmDone.forEach(el=>renderMermaid(el))}
/* v2.1: diagrams are pre-rendered to SVG at build time; runtime Mermaid is only a fallback for un-rendered blocks */
const mEls=$$('.mermaid:not([data-done])');if(mEls.length){mEls.forEach(el=>mmSrc.set(el,el.textContent));const mio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){mio.unobserve(e.target);renderMermaid(e.target)}}),{rootMargin:'1400px 0px'});mEls.forEach(el=>mio.observe(el))}

/* ---------- v3.0 maps: hand-drawn concept maps + live Leaflet maps with tile failover ---------- */
const NM=()=>RM||root.classList.contains('no-motion');
const escH=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
/* keyless providers only (terms checked 2026-10): OSM standard, OSM France HOT, OpenTopoMap. No tile prefetching. */
const TILES=[
 {id:'osm',n:'OpenStreetMap',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',o:{maxZoom:19,attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'}},
 {id:'hot',n:'OSM France · HOT',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',o:{maxZoom:19,subdomains:'abc',attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors · 风格 <a href="https://www.hotosm.org/" target="_blank" rel="noopener">HOT</a> · 托管 <a href="https://www.openstreetmap.fr/" target="_blank" rel="noopener">OSM France</a>'}},
 {id:'topo',n:'OpenTopoMap',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',o:{maxZoom:17,subdomains:'abc',attribution:'Kartendaten: © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-Mitwirkende, SRTM | Kartendarstellung: © <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'}}];
window.__tileLog=[];
let leafletP=null;const getLeaflet=()=>leafletP||(leafletP=(loadCSS('assets/vendor/leaflet/leaflet.css'),loadScript('assets/vendor/leaflet/leaflet.js').then(()=>window.L)));
const geoP={};const getGeo=b=>geoP[b]||(geoP[b]=fetch('assets/geo/'+b+'.json').then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}));
const yearOf=w=>{const m=String(w).match(/\d{3,4}/);return m?+m[0]:9999};
function curve(a,b,bend){const n=24,mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],cx=mx-dy*bend,cy=my+dx*bend,pts=[];for(let i=0;i<=n;i++){const t=i/n,u=1-t;pts.push([u*u*a[0]+2*u*t*cx+t*t*b[0],u*u*a[1]+2*u*t*cy+t*t*b[1]])}return pts}
function liveMap(box,data,onPick){
  const el=$('.lmap',box);el.textContent='🗺️ 地图加载中…';
  return getLeaflet().then(L=>{el.textContent='';const coarse=matchMedia('(pointer:coarse)').matches;
    const map=L.map(el,{zoomSnap:.5,scrollWheelZoom:false,dragging:!coarse,tap:false,worldCopyJump:true,preferCanvas:false});
    map.createPane('basePane').style.zIndex=150;const rend=L.canvas({pane:'basePane',padding:.3});
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    map.attributionControl.addAttribution('底图 <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（公有领域）');
    const st={map,base:null,layer:null,idx:-1,ok:0,err:0,timer:0};
    /* self-hosted vector base (never fails): Natural Earth land/rivers/lakes, or the Thames for the London map */
    function baseStyle(f){const k=f&&f.properties&&f.properties.k;const land=probe('var(--geo-land)'),coast=probe('var(--geo-coast)'),riv=probe('var(--geo-river)');
      return k==='river'?{color:riv,weight:1.2,opacity:.8,fill:false}:k==='lake'?{color:riv,weight:.6,fillColor:probe('var(--geo-sea)'),fillOpacity:1}:k==='thames'?{color:riv,weight:22,opacity:.55,lineCap:'round'}:{color:coast,weight:1,fillColor:land,fillOpacity:1}}
    el.style.background=probe('var(--geo-sea)');
    const addBase=gj=>{st.base=L.geoJSON(gj,{renderer:rend,pane:'basePane',interactive:false,style:baseStyle}).addTo(map)};
    if(data.base==='london'){addBase({type:'Feature',properties:{k:'thames'},geometry:{type:'LineString',coordinates:(data.thames||[]).map(p=>[p[1],p[0]])}})}
    else getGeo(data.base).then(addBase).catch(e=>console.warn('geo base',e));
    st.restyle=()=>{el.style.background=probe('var(--geo-sea)');st.base&&st.base.setStyle(baseStyle);drawRoutes()};
    /* places + routes */
    const P=new Map(data.places.map((p,i)=>[p.k,Object.assign({i},p)]));
    const mk=data.places.map((p,i)=>L.marker([p.lat,p.lng],{title:p.n,riseOnHover:true,icon:L.divIcon({className:'',html:`<div class="lpin" style="--c:${p.c}">${p.i}</div>`,iconSize:[28,28],iconAnchor:[14,14]})})
      .bindTooltip(escH(p.n),{className:'ltip',direction:'right',offset:[12,0]})
      .bindPopup(`<b>${p.i} ${escH(p.n)}</b><br><span class="hl-date">${escH(p.w)}</span><p style="margin:.4em 0 0">${escH(p.d)}</p>`,{maxWidth:260})
      .on('click',()=>onPick(i,true)).addTo(map));
    let rl=null;function drawRoutes(){rl&&map.removeLayer(rl);const cs=getComputedStyle(root),c1=cs.getPropertyValue('--a1').trim(),c2=cs.getPropertyValue('--a2').trim(),cb=cs.getPropertyValue('--bad').trim();
      rl=L.layerGroup(data.routes.map(r=>{const a=P.get(r.a),b=P.get(r.b);if(!a||!b)return null;const col=r.k==='march'?cb:r.k==='flow'?c1:c2;
        return L.polyline(curve([a.lat,a.lng],[b.lat,b.lng],r.k==='sea'?.22:.16),{color:col,weight:3,opacity:.85,dashArray:r.k==='sea'?'6 7':null,interactive:!!r.l}).bindTooltip(escH(r.l||''),{sticky:true,className:'ltip'})}).filter(Boolean)).addTo(map)}
    drawRoutes();
    const b=L.latLngBounds(data.places.map(p=>[p.lat,p.lng]));map.fitBounds(b,{padding:[30,30],maxZoom:data.base==='london'?17:7});
    /* control: provider select + live status */
    const Ctl=L.Control.extend({onAdd(){const d=L.DomUtil.create('div','mctl');d.innerHTML='<span class="mst wait">⏳ 准备瓦片…</span><select aria-label="在线瓦片来源"><option value="auto">自动（失败时切换）</option>'+TILES.map(t=>`<option value="${t.id}">${t.n}</option>`).join('')+'<option value="none">仅离线底图</option></select>';L.DomEvent.disableClickPropagation(d);L.DomEvent.disableScrollPropagation(d);return d}});
    const ctl=new Ctl({position:'topright'}).addTo(map),cd=ctl.getContainer(),stEl=$('.mst',cd),sel=$('select',cd);
    const status=(c,t)=>{stEl.className='mst '+c;stEl.textContent=t;box.dataset.tiles=c+':'+(st.idx>=0?TILES[st.idx].id:'none')};
    const T=()=>window.__tileTimeout||6000;
    function clear(){clearTimeout(st.timer);if(st.layer){const ly=st.layer;st.layer=null;map.removeLayer(ly);ly.off('tileload tileerror')}}
    function use(i){clear();const mode=sel.value;
      if(i<0||i>=TILES.length){st.idx=-1;status('off',mode==='none'?'🧭 仅离线底图（已手动选择）':'🧭 离线底图（在线瓦片均不可用）');window.__tileLog.push([data.base,'offline']);return}
      st.idx=i;st.ok=0;st.err=0;const t=TILES[i];status('wait','⏳ 正在连接 '+t.n+'…');
      const ly=L.tileLayer(t.u,Object.assign({updateWhenIdle:true,keepBuffer:1,referrerPolicy:'strict-origin-when-cross-origin'},t.o));st.layer=ly;
      ly.on('tileload',()=>{if(st.layer!==ly)return;st.ok++;if(st.ok===1){clearTimeout(st.timer);status('on','✅ 在线瓦片：'+t.n);window.__tileLog.push([data.base,t.id,'ok'])}});
      ly.on('tileerror',()=>{if(st.layer!==ly)return;st.err++;if((st.ok===0&&st.err>=3)||st.err-st.ok>=8)fail('error')});
      st.timer=setTimeout(()=>{if(st.layer===ly&&st.ok===0)fail('timeout')},T());ly.addTo(map)}
    function fail(why){const t=TILES[st.idx];window.__tileLog.push([data.base,t&&t.id,why]);
      if(sel.value==='auto')use(st.idx+1);else{clear();st.idx=-1;status('off','❌ '+(t?t.n:'')+' 不可用，已保留离线底图')}}
    function apply(){const v=sel.value;v==='auto'?use(0):v==='none'?use(-1):use(TILES.findIndex(t=>t.id===v))}
    sel.value=LS.get('tiles','auto');if(![...sel.options].some(o=>o.value===sel.value))sel.value='auto';
    sel.addEventListener('change',()=>{LS.set('tiles',sel.value);apply()});apply();
    /* wheel zoom / drag only after the user engages the map (no scroll-jacking) */
    if(coarse){const h=L.DomUtil.create('div','lhint',el);h.textContent='👆 点按地图以启用拖动；双指缩放';map.once('click',()=>{map.dragging.enable();h.remove()})}
    map.on('focus click',()=>map.scrollWheelZoom.enable());map.on('blur',()=>map.scrollWheelZoom.disable());
    st.focus=(i,pan)=>{const m=mk[i];if(!m)return;if(pan)map.panTo(m.getLatLng(),{animate:!NM()});m.openPopup()};
    LMAPS.push(st);return st})
   .catch(e=>{console.warn(e);el.innerHTML='<p style="padding:20px">交互地图组件加载失败；请使用「🎨 手绘示意图」（离线可用）。</p>'})}
function initMapbox(box){
  let data;try{data=JSON.parse($('.mdata',box).textContent)}catch(e){return}
  const cm=$('.cmap',box),pins=$$('.pin',box),info=$('.minfo',box),lis=$$('.mplaces li',box),tabs=$$('.mtabs [data-v]',box),views={c:$('.mv-c',box),l:$('.mv-l',box)},play=$('.mplay',box);
  let live=null,liveP=null,cur=-1,timer=0;
  function show(i,fromMap){const p=data.places[i];if(!p)return;cur=i;pins.forEach((x,j)=>x.classList.toggle('on',j===i));lis.forEach((x,j)=>x.classList.toggle('on',j===i));
    info.style.setProperty('--c',p.c);info.innerHTML=`<div class="mi-h"><b>${p.i} ${escH(p.n)}</b><span class="hl-date">${escH(p.w)}</span><span class="muted small">${i+1} / ${data.places.length}</span></div><div>${escH(p.d)}</div>`;
    if(live&&!fromMap&&views.l.classList.contains('on'))live.focus(i,true)}
  function view(v){tabs.forEach(t=>{const on=t.dataset.v===v;t.classList.toggle('on',on);t.setAttribute('aria-selected',on)});views.c.classList.toggle('on',v==='c');views.l.classList.toggle('on',v==='l');
    if(v==='l'){if(!liveP)liveP=liveMap(box,data,(i,fm)=>show(i,fm)).then(s=>{live=s||null;if(live&&cur>=0)live.focus(cur,false)});else live&&live.map.invalidateSize()}}
  tabs.forEach(t=>t.addEventListener('click',()=>view(t.dataset.v)));
  pins.forEach(p=>p.addEventListener('click',()=>{stop();show(+p.dataset.i)}));
  lis.forEach(li=>li.addEventListener('click',()=>{stop();show(+li.dataset.i);const r=box.getBoundingClientRect();if(r.top<0)goTo(box,true)}));
  const order=data.places.map((p,i)=>i).sort((a,b)=>yearOf(data.places[a].w)-yearOf(data.places[b].w)||a-b);
  function stop(){clearTimeout(timer);timer=0;if(play){play.classList.remove('on');play.textContent='▶ 按时间播放'}}
  play&&play.addEventListener('click',()=>{if(timer){stop();return}play.classList.add('on');play.textContent='⏸ 暂停';let k=0;const step=()=>{show(order[k]);k++;timer=k<order.length?setTimeout(step,NM()?2600:2000):0;if(!timer)setTimeout(stop,2000)};step()});
  if(cm){const io=new IntersectionObserver(es=>es.forEach(e=>{cm.classList.toggle('play',e.isIntersecting);if(e.isIntersecting)cm.classList.add('seen')}),{rootMargin:'0px 0px -10% 0px'});io.observe(cm)}
}
$$('.mapbox').forEach(initMapbox);

/* v3.1: Lenis removed — native scrolling (smoother on phones/trackpads, zero main-thread scroll work) */
const PREVENT='.toc,.tbl,.mermaid,.lmap,.hscroll,.pop,.leaflet-container,.flash .face,.topnav,.tbar,select,textarea';
/* accurate in-page navigation: render skipped content-visibility blocks above the target first */
function topOff(){return (parseInt(getComputedStyle(root).getPropertyValue('--top-h'))||58)+12}
function settle(t){$$('.lz:not(.hy)').filter(c=>c.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING).forEach(hydrate);const cvs=$$('.cv,.lz').filter(c=>c.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING||c.contains(t));cvs.forEach(c=>c.style.contentVisibility='visible');t.getBoundingClientRect();setTimeout(()=>requestAnimationFrame(()=>{/* lock each block's real height as its placeholder size, so reverting to content-visibility:auto never shifts the page */const hs=cvs.map(c=>c.getBoundingClientRect().height);cvs.forEach((c,i)=>{c.style.containIntrinsicSize='auto '+Math.round(hs[i])+'px';c.style.contentVisibility=''})}),500)}
function goTo(t,smooth){settle(t);const y=()=>t.getBoundingClientRect().top+(root.scrollTop||scrollY)-topOff();
  /* 'instant' overrides CSS scroll-behavior:smooth; then re-check a few times while late layout settles, unless the user takes over */
  let user=false;const stop=()=>{user=true};['wheel','touchstart','keydown','pointerdown'].forEach(ev=>addEventListener(ev,stop,{once:true,passive:true}));
  const fix=()=>{if(user)return;const d=t.getBoundingClientRect().top-topOff();if(Math.abs(d)>4)scrollTo({top:y(),behavior:'instant'})};
  if(smooth&&!RM){scrollTo({top:y(),behavior:'smooth'});addEventListener('scrollend',fix,{once:true});[1300,2000].forEach(ms=>setTimeout(fix,ms))}
  else{scrollTo({top:y(),behavior:'instant'});requestAnimationFrame(fix);[150,400,800,1300,2000].forEach(ms=>setTimeout(fix,ms))}}
window.__goTo=goTo;
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey)return;const id=decodeURIComponent(a.getAttribute('href').slice(1));const t=id&&findId(id);if(!t)return;
  e.preventDefault();history.pushState(null,'','#'+id);goTo(t,true)});
if(location.hash.length>1){const t=findId(decodeURIComponent(location.hash.slice(1)));if(t){if('scrollRestoration' in history)history.scrollRestoration='manual';requestAnimationFrame(()=>goTo(t,false))}}

/* ---------- page hooks ---------- */
if(window.__pageInit)window.__pageInit();
const a=$('.topnav a.on');if(a){const n=a.parentElement;if(n.scrollWidth>n.clientWidth)n.scrollLeft=a.offsetLeft-n.offsetLeft-8}
})();
