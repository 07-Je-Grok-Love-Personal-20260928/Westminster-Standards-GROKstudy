/* Westminster Standards GROKstudy v2 — interactions (deferred, rAF-throttled, lazy libs) */
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
let themeTimer;function themeChanged(){clearTimeout(themeTimer);themeTimer=setTimeout(()=>{reMermaid()},120)}
applyMode();applyPalette(LS.get('palette','aurora'));
$$('.sw').forEach(b=>b.addEventListener('click',()=>{LS.set('palette',b.dataset.pal);applyPalette(b.dataset.pal);themeChanged()}));
$$('#modeSeg button').forEach(b=>b.addEventListener('click',()=>{LS.set('mode',b.dataset.mode);applyMode();themeChanged()}));
function syncOpts(){$$('#optSeg button').forEach(b=>{const k=b.dataset.opt;b.classList.toggle('on',k==='smooth'?LS.get('smooth',true):LS.get('motion','on')!=='off')})}
$$('#optSeg button').forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.opt;
  if(k==='smooth'){const v=!LS.get('smooth',true);LS.set('smooth',v);v?startLenis():stopLenis()}
  else{const off=LS.get('motion','on')!=='off';LS.set('motion',off?'off':'on');root.classList.toggle('no-motion',off)}syncOpts()}));
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
$('#tocBtn')?.addEventListener('click',()=>{if(isMobile())body.classList.toggle('toc-open');else{body.classList.toggle('toc-off');LS.set('tocoff',body.classList.contains('toc-off'))}setTimeout(()=>window.__map&&window.__map.invalidateSize(),400)});
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

/* ---------- scroll: progress + to-top (one rAF per frame max) ---------- */
const pg=$('.progress i'), tt=$('.totop');let ticking=false,lastTop=-1;
function onFrame(){ticking=false;const h=root;const y=h.scrollTop||window.scrollY;if(y===lastTop)return;lastTop=y;const max=h.scrollHeight-h.clientHeight||1;
  if(pg)pg.style.transform='scaleX('+Math.min(1,y/max).toFixed(4)+')';if(tt)tt.classList.toggle('show',y>600)}
addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(onFrame)}},{passive:true});onFrame();
tt?.addEventListener('click',()=>{lenis?lenis.scrollTo(0):scrollTo({top:0,behavior:RM?'auto':'smooth'})});

/* ---------- reveal + stagger + counters + charts ---------- */
$$('.grid,.stats,.flow,.chain,.rings').forEach(g=>{let i=0;[...g.children].forEach(c=>{if(c.classList.contains('rv')){c.style.setProperty('--d',Math.min(i,6)*0.06+'s');i++}})});
const rio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const t=e.target;t.classList.add('in');rio.unobserve(t);if(t.matches('.stats'))countUp(t)}}),{rootMargin:'0px 0px -6% 0px'});
$$('.rv,.bars,.stats').forEach(el=>rio.observe(el));
function countUp(box){if(RM||root.classList.contains('no-motion'))return;$$('.stat .v',box).forEach(v=>{const t=v.textContent.trim();if(!/^\d{1,4}$/.test(t))return;const n=+t,from=n>1000?n-60:0,t0=performance.now();
  const step=now=>{const p=Math.min(1,(now-t0)/1100),e=1-Math.pow(1-p,3);v.textContent=Math.round(from+(n-from)*e);if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)})}
/* pause hero animations when off-screen */
const hio=new IntersectionObserver(es=>es.forEach(e=>e.target.classList.toggle('paused',!e.isIntersecting)));$$('.hero').forEach(h=>hio.observe(h));

/* ---------- tabs ---------- */
$$('.tabs').forEach(t=>{t.classList.add('js');const bs=$$('.tb',t),ps=$$('.tp',t);
  const sel=i=>{bs.forEach((b,j)=>{b.classList.toggle('on',j===i);b.setAttribute('aria-selected',j===i)});ps.forEach((p,j)=>p.classList.toggle('on',j===i))};
  bs.forEach((b,i)=>{b.addEventListener('click',()=>sel(i));b.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){bs[(i+1)%bs.length].focus();sel((i+1)%bs.length)}if(e.key==='ArrowLeft'){bs[(i-1+bs.length)%bs.length].focus();sel((i-1+bs.length)%bs.length)}})})});

/* ---------- refs toggle / filters / timeline ---------- */
const rb=$('#refsBtn');if(rb){if(LS.get('norefs',false))body.classList.add('no-refs');rb.addEventListener('click',()=>{body.classList.toggle('no-refs');LS.set('norefs',body.classList.contains('no-refs'))})}
const df=$('#docFilter');if(df){let tmr;df.addEventListener('input',()=>{clearTimeout(tmr);tmr=setTimeout(()=>{const v=df.value.trim();$$('[data-search]').forEach(el=>{el.classList.toggle('hide',!!v&&!el.textContent.includes(v))});$$('.grp').forEach(g=>{if(!v){g.open=g.dataset.open==='1';return}g.open=true})},180)})}
$$('.filters[data-for]').forEach(f=>{f.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',f).forEach(x=>x.classList.remove('on'));b.classList.add('on');const k=b.dataset.k;$$(f.dataset.for+' [data-cat]').forEach(ev=>ev.classList.toggle('hide',k!=='all'&&!ev.dataset.cat.split(' ').includes(k)))})});

/* ---------- memorised marks + progress rings ---------- */
const done=LS.get('done',{});
$$('.memo').forEach(m=>{const k=m.dataset.k;const paint=()=>{m.classList.toggle('done',!!done[k]);m.textContent=done[k]?'✔ 已背':'☆ 标记'};paint();m.addEventListener('click',e=>{e.stopPropagation();done[k]=!done[k];paint();LS.set('done',done);updateCount()})});
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
  mmLoading=import('https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs').then(m=>m.default).catch(()=>loadScript('https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js').then(()=>window.mermaid)).then(m=>{mm=m;mm.initialize(mmConfig());return mm});return mmLoading}
let mmQueue=Promise.resolve(), lastScroll=0;addEventListener('scroll',()=>{lastScroll=performance.now()},{passive:true});
/* heavy work only when the user is not actively scrolling, and in idle time */
const whenCalm=()=>new Promise(res=>{const calm=()=>performance.now()-lastScroll>250;const chk=()=>{if(calm())idle(()=>calm()?res():setTimeout(chk,160),{timeout:1500});else setTimeout(chk,160)};chk()});
function renderMermaid(el){if(!mmSrc.has(el))mmSrc.set(el,el.textContent);mmQueue=mmQueue.then(whenCalm).then(()=>getMermaid()).then(m=>whenCalm().then(()=>m)).then(m=>{el.removeAttribute('data-processed');el.innerHTML=mmSrc.get(el);return m.run({nodes:[el]})}).then(()=>{el.setAttribute('data-done','');el.setAttribute('data-lenis-prevent','');mmDone.add(el)}).catch(e=>{console.warn(e);el.setAttribute('data-done','');el.innerHTML='<p class="muted">图表加载失败（可能是网络限制），请刷新重试。</p>'})}
function reMermaid(){if(!mm)return;mm.initialize(mmConfig());mmDone.forEach(el=>renderMermaid(el))}
const mEls=$$('.mermaid');if(mEls.length){addEventListener('load',()=>whenCalm().then(getMermaid),{once:true});mEls.forEach(el=>mmSrc.set(el,el.textContent));const mio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){mio.unobserve(e.target);renderMermaid(e.target)}}),{rootMargin:'1400px 0px'});mEls.forEach(el=>mio.observe(el))}

/* ---------- lazy Leaflet ---------- */
const mapEl=$('#map');if(mapEl&&window.__mapInit){mapEl.textContent='🗺️ 地图加载中…';const lio=new IntersectionObserver(es=>{if(!es.some(e=>e.isIntersecting))return;lio.disconnect();loadCSS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css');
  loadScript('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js').then(()=>{mapEl.textContent='';mapEl.style.display='block';window.__mapInit();mapEl.setAttribute('data-lenis-prevent','')}).catch(()=>{mapEl.innerHTML='<p style="padding:20px">地图组件加载失败（可能是网络限制），请刷新重试。</p>'})},{rootMargin:'600px 0px'});lio.observe(mapEl)}

/* ---------- silky smooth wheel scrolling (desktop only, Lenis) ---------- */
let lenis=null;
const PREVENT='.toc,.tbl,.mermaid,#map,.pop,.leaflet-container,.flash .face,.topnav,.tbar,select,textarea';
function startLenis(){if(lenis||RM||!matchMedia('(pointer:fine)').matches||!LS.get('smooth',true))return;
  loadScript('https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js').then(()=>{if(lenis||!window.Lenis)return;
    $$(PREVENT).forEach(n=>n.setAttribute('data-lenis-prevent',''));
    lenis=new window.Lenis({lerp:0.11,smoothWheel:true,wheelMultiplier:1,prevent:n=>!!(n.closest&&n.closest(PREVENT))});window.__lenis=lenis;
    const raf=t=>{if(!lenis)return;lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf)}).catch(()=>{})}
function stopLenis(){if(lenis){lenis.destroy();lenis=null;window.__lenis=null}}
/* accurate in-page navigation: render skipped content-visibility blocks above the target first */
function topOff(){return (parseInt(getComputedStyle(root).getPropertyValue('--top-h'))||58)+12}
function settle(t){const cvs=$$('.cv').filter(c=>c.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING||c.contains(t));cvs.forEach(c=>c.style.contentVisibility='visible');t.getBoundingClientRect();setTimeout(()=>requestAnimationFrame(()=>requestAnimationFrame(()=>cvs.forEach(c=>c.style.contentVisibility=''))),500)}
function goTo(t,smooth){settle(t);const y=()=>t.getBoundingClientRect().top+(root.scrollTop||scrollY)-topOff();
  if(lenis&&smooth){lenis.scrollTo(y(),{duration:1.1,onComplete:()=>{const d=t.getBoundingClientRect().top-topOff();if(Math.abs(d)>4)lenis.scrollTo(y(),{immediate:true})}});return}
  scrollTo({top:y(),behavior:smooth&&!RM?'smooth':'auto'});
  let n=0;const fix=()=>{const d=t.getBoundingClientRect().top-topOff();if(Math.abs(d)>4&&n++<6)scrollTo({top:y(),behavior:'auto'})};if(smooth&&!RM){addEventListener('scrollend',fix,{once:true});setTimeout(fix,1200)}else{requestAnimationFrame(fix);setTimeout(fix,700)}}
window.__goTo=goTo;
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey)return;const id=decodeURIComponent(a.getAttribute('href').slice(1));const t=id&&document.getElementById(id);if(!t)return;
  e.preventDefault();history.pushState(null,'','#'+id);goTo(t,true)});
if(location.hash.length>1){const t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t){if('scrollRestoration' in history)history.scrollRestoration='manual';requestAnimationFrame(()=>goTo(t,false))}}
idle(startLenis);

/* ---------- page hooks ---------- */
if(window.__pageInit)window.__pageInit();
const a=$('.topnav a.on');if(a){const n=a.parentElement;if(n.scrollWidth>n.clientWidth)n.scrollLeft=a.offsetLeft-n.offsetLeft-8}
})();
