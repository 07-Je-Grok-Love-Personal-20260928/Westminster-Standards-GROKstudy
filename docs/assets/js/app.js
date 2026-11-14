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
/* v3.2 options: motion · glass (small fixed elements only; off on low-end / reduced-motion) · skim (重点模式) · cloze (遮挡背诵) */
const GLASS_OK=()=>!RM&&(CSS.supports('backdrop-filter','blur(2px)')||CSS.supports('-webkit-backdrop-filter','blur(2px)'))&&(navigator.deviceMemory||8)>=4&&(navigator.hardwareConcurrency||8)>=4;
const OPTS={motion:{get:()=>LS.get('motion','on')!=='off',set:v=>{LS.set('motion',v?'on':'off');root.classList.toggle('no-motion',!v);applyGlass()}},
  glass:{get:()=>LS.get('glass','on')!=='off',set:v=>{LS.set('glass',v?'on':'off');applyGlass()}},
  skim:{get:()=>root.classList.contains('skim'),set:v=>{root.classList.toggle('skim',v);v&&OPTS.cloze.get()&&OPTS.cloze.set(false)}},
  cloze:{get:()=>root.classList.contains('cloze'),set:v=>{root.classList.toggle('cloze',v);if(!v)$$('.rev').forEach(e=>e.classList.remove('rev'));v&&OPTS.skim.get()&&OPTS.skim.set(false)}}};
function applyGlass(){root.classList.toggle('glass',GLASS_OK()&&OPTS.glass.get()&&OPTS.motion.get())}
function syncOpts(){$$('[data-opt]').forEach(b=>{const o=OPTS[b.dataset.opt];if(o){const on=o.get();b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)}})}
document.addEventListener('click',e=>{const b=e.target.closest('[data-opt]');if(b&&OPTS[b.dataset.opt]){const o=OPTS[b.dataset.opt];o.set(!o.get());syncOpts();return}
  if(root.classList.contains('cloze')){const m=e.target.closest('main :is(mark,.u-key,.m-blue,.m-green,.hl-date)');if(m){m.classList.toggle('rev');e.preventDefault()}}},true);
applyGlass();
syncOpts();
/* popovers */
const pops=[['themeBtn','themePanel'],['legendBtn','legendPanel']];
function closePops(except){pops.forEach(([b,p])=>{if(p!==except){$('#'+p)?.classList.remove('open');$('#'+b)?.setAttribute('aria-expanded','false')}})}
pops.forEach(([b,p])=>{const bt=$('#'+b),pn=$('#'+p);if(!bt||!pn)return;bt.addEventListener('click',e=>{e.stopPropagation();const o=!pn.classList.contains('open');closePops(p);pn.classList.toggle('open',o);bt.setAttribute('aria-expanded',o)});pn.addEventListener('click',e=>e.stopPropagation())});
document.addEventListener('click',()=>closePops());
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closePops();body.classList.remove('toc-open')}});

/* ---------- v3.3 TOC: build-time 3-level outline → collapsible tree · resizable · scroll-spy ---------- */
const tocBox=$('.toc'), toc=$('#tocList'), main=$('main');
const tEsc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const TD=(()=>{try{return JSON.parse($('#tocData').textContent)}catch(e){return[]}})();
const NODES=[],ROOTS=[];{const st=[];TD.forEach((r,i)=>{const n={lv:r[0],id:r[1],t:r[2],num:r[3]||'',kids:[],par:null,i,d:0,open:false};
  while(st.length&&st[st.length-1].lv>=n.lv)st.pop();if(st.length){n.par=st[st.length-1];n.par.kids.push(n);n.d=n.par.d+1}else ROOTS.push(n);st.push(n);NODES.push(n)})}
ROOTS.forEach(n=>n.open=true);
let actN=null;
const shownRoot=n=>{const el=document.getElementById(n.id);return !(el&&el.closest('.hide'))};
function liH(n){const has=n.kids.length>0,on=actN&&(actN===n),path=actN&&isAnc(n,actN);
  return `<li class="t${Math.min(n.d+1,3)}${has?' has':''}${n.open?' open':''}${path?' path':''}" data-i="${n.i}"><div class="tr">${has?`<button type="button" class="tg" aria-expanded="${n.open}" aria-label="${n.open?'折叠':'展开'}：${tEsc(n.t)}"></button>`:'<span class="tg0"></span>'}<a href="#${n.id}"${on?' class="active" aria-current="location"':''}>${n.num?`<span class="tn">${n.num}</span>`:''}<span class="tt">${tEsc(n.t)}</span></a></div>${has&&n.open?`<ol>${n.kids.map(liH).join('')}</ol>`:''}</li>`}
const isAnc=(a,n)=>{for(let p=n.par;p;p=p.par)if(p===a)return true;return false};
function renderToc(){if(!toc)return;toc.innerHTML=ROOTS.filter(shownRoot).map(liH).join('')}
function rerenderNode(n){const li=toc&&toc.querySelector(`li[data-i="${n.i}"]`);if(li)li.outerHTML=liH(n);else renderToc()}
renderToc();
toc?.addEventListener('click',e=>{const tg=e.target.closest('.tg');if(tg){e.preventDefault();const n=NODES[+tg.closest('li').dataset.i];n.open=!n.open;rerenderNode(n);return}
  if(e.target.closest('a')&&isMobile())body.classList.remove('toc-open')});
/* tooltip only when the single-line title is actually cut off */
toc?.addEventListener('pointerover',e=>{const a=e.target.closest('a');if(!a)return;const t=a.querySelector('.tt');if(!t)return;if(t.scrollWidth>t.clientWidth+1)a.title=t.textContent;else a.removeAttribute('title')});
tocBox?.addEventListener('click',e=>{const b=e.target.closest('[data-tc]');if(!b)return;const o=b.dataset.tc==='open';NODES.forEach(n=>n.open=o?n.kids.length>0:false);if(!o&&actN){}renderToc()});
const tf=$('#tocFilter');if(tf)tf.addEventListener('input',()=>{const v=tf.value.trim().toLowerCase();if(!v){renderToc();return}
  const hit=NODES.filter(n=>n.t.toLowerCase().includes(v)&&shownRoot(rootOf(n))).slice(0,150);
  toc.innerHTML=hit.length?hit.map(n=>`<li class="t${Math.min(n.d+1,3)} flat"><div class="tr"><span class="tg0"></span><a href="#${n.id}">${n.num?`<span class="tn">${n.num}</span>`:''}<span class="tt">${tEsc(n.t)}</span>${n.par?`<small class="tp">${tEsc(n.par.t)}</small>`:''}</a></div></li>`).join(''):'<li class="none">没有匹配的条目</li>'});
const rootOf=n=>{while(n.par)n=n.par;return n};
/* scroll-spy: binary search over the outline targets that are currently in the DOM (hydrated, visible) */
let targets=[],tDirty=true;
function collect(){targets=[];NODES.forEach(n=>{const el=document.getElementById(n.id);if(el&&el.getClientRects().length)targets.push({n,el})});tDirty=false}
function tocVisible(){return tocBox&&(isMobile()?body.classList.contains('toc-open'):!body.classList.contains('toc-off'))}
function spy(force){if(!toc||!NODES.length||(!force&&!tocVisible()))return;if(tDirty)collect();if(!targets.length)return;const lim=innerHeight*0.28;let lo=0,hi=targets.length-1,ans=0;
  while(lo<=hi){const m=(lo+hi)>>1;if(targets[m].el.getBoundingClientRect().top<=lim){ans=m;lo=m+1}else hi=m-1}
  setAct(targets[ans].n)}
function setAct(n){if(n===actN)return;actN=n;let need=null;for(let p=n.par;p;p=p.par)if(!p.open){p.open=true;need=p}
  if(need){let top=need;while(top.par&&!top.par.open)top=top.par;rerenderNode(rootOf(n))}
  $$('a.active',toc).forEach(a=>{a.classList.remove('active');a.removeAttribute('aria-current')});$$('li.path',toc).forEach(l=>l.classList.remove('path'));
  const li=toc.querySelector(`li[data-i="${n.i}"]`);if(!li)return;const a=li.querySelector(':scope>.tr>a');a.classList.add('active');a.setAttribute('aria-current','location');
  for(let p=li.parentElement.closest('li');p;p=p.parentElement.closest('li'))p.classList.add('path');
  if(tocBox.matches(':hover'))return;const br=tocBox.getBoundingClientRect(),ar=a.getBoundingClientRect();
  if(ar.top<br.top+70||ar.bottom>br.bottom-24)tocBox.scrollTop+=ar.top-br.top-br.height*0.4}
let spyT=0;addEventListener('scroll',()=>{if(!spyT)spyT=setTimeout(()=>{spyT=0;spy()},140)},{passive:true});
addEventListener('scrollend',()=>spy());addEventListener('resize',()=>{tDirty=true},{passive:true});
let tdT;function tocDirty(){clearTimeout(tdT);tdT=setTimeout(()=>{tDirty=true;spy()},250)}
setTimeout(()=>spy(true),700);
window.__rebuildToc=()=>{actN=null;renderToc();tDirty=true;spy(true)};
window.__tocSpy=()=>spy(true);
/* show / hide */
if(!isMobile()&&LS.get('tocoff',false))body.classList.add('toc-off');
$('#tocBtn')?.addEventListener('click',()=>{if(isMobile())body.classList.toggle('toc-open');else{body.classList.toggle('toc-off');LS.set('tocoff',body.classList.contains('toc-off'))}setTimeout(()=>{LMAPS.forEach(m=>m.map.invalidateSize());spy()},400)});
$('.scrim')?.addEventListener('click',()=>body.classList.remove('toc-open'));
/* drag to resize (mouse, pen, touch): edge handle · ←/→ keys · double-click resets */
if(tocBox){const rs=document.createElement('div');rs.className='toc-rs';rs.tabIndex=0;rs.setAttribute('role','separator');rs.setAttribute('aria-orientation','vertical');rs.setAttribute('aria-label','调整目录宽度');rs.title='拖动调整目录宽度 · 双击恢复默认';rs.innerHTML='<i></i>';tocBox.appendChild(rs);
  const MINW=220,maxW=()=>Math.round(innerWidth*(isMobile()?0.92:0.6));
  const setW=(w,save)=>{w=Math.round(Math.max(MINW,Math.min(w,maxW())));root.style.setProperty('--toc-w',w+'px');rs.setAttribute('aria-valuenow',w);if(save)LS.set('tocw',w);return w};
  const done=()=>{LMAPS.forEach(m=>m.map.invalidateSize());tDirty=true};
  rs.addEventListener('pointerdown',e=>{if(e.button>0)return;e.preventDefault();try{rs.setPointerCapture(e.pointerId)}catch(_){}const x0=e.clientX,w0=tocBox.getBoundingClientRect().width;let w=w0,raf=0;body.classList.add('toc-drag');
    const mv=ev=>{w=w0+ev.clientX-x0;if(!raf)raf=requestAnimationFrame(()=>{raf=0;setW(w)})};
    const up=()=>{rs.removeEventListener('pointermove',mv);rs.removeEventListener('pointerup',up);rs.removeEventListener('pointercancel',up);cancelAnimationFrame(raf);body.classList.remove('toc-drag');if(Math.abs(w-w0)>2)setW(w,true);done()};
    rs.addEventListener('pointermove',mv);rs.addEventListener('pointerup',up);rs.addEventListener('pointercancel',up)});
  rs.addEventListener('dblclick',()=>{LS.set('tocw',0);root.style.removeProperty('--toc-w');rs.removeAttribute('aria-valuenow');done()});
  rs.addEventListener('keydown',e=>{if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;e.preventDefault();setW(tocBox.getBoundingClientRect().width+(e.key==='ArrowRight'?24:-24),true);done()});
  window.__tocSetW=w=>{setW(w,true);done()}}

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
function initScope(sc){watchLz(sc);tocDirty();initTabs(sc);paintMemos(sc);stagger(sc);$$('.rv,.bars,.stats',sc).forEach(x=>rio.observe(x));initViz(sc);if(window.__onHydrate)window.__onHydrate(sc)}
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
/* v3.2: 14 keyless tile providers in 3 groups (checked 2026-11-14; CARTO dropped: since 2026-09-25 it serves "API KEY REQUIRED" tiles without a key).
   Auto mode races one probe tile per provider (fastest reachable first, cached 30 min per session), then fails over down that ranking;
   the self-hosted Natural Earth layer is always underneath. Gaode uses GCJ-02: markers are shifted to match while it is shown. */
const OSMA='© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors';
const ESRIA=t=>'Powered by <a href="https://www.esri.com/" target="_blank" rel="noopener">Esri</a>'+(t?' | Sources: '+t:'');
const GDA='© <a href="https://www.amap.com/" target="_blank" rel="noopener">高德地图 AutoNavi</a>';
const ESRI='https://server.arcgisonline.com/ArcGIS/rest/services/';
const TILES=[
 {id:'osm',g:'w',n:'OpenStreetMap',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',o:{maxZoom:19,attribution:OSMA}},
 {id:'osmde',g:'w',n:'OpenStreetMap 德国',u:'https://tile.openstreetmap.de/{z}/{x}/{y}.png',o:{maxZoom:18,attribution:OSMA}},
 {id:'osmfr',g:'w',n:'OpenStreetMap 法国',u:'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',o:{maxZoom:19,subdomains:'abc',attribution:OSMA+' · 托管 <a href="https://www.openstreetmap.fr/" target="_blank" rel="noopener">OSM France</a>'}},
 {id:'hot',g:'w',n:'OSM 人道主义（HOT）',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',o:{maxZoom:19,subdomains:'abc',attribution:OSMA+' · 风格 <a href="https://www.hotosm.org/" target="_blank" rel="noopener">HOT</a> · 托管 <a href="https://www.openstreetmap.fr/" target="_blank" rel="noopener">OSM France</a>'}},
 {id:'cyclosm',g:'w',n:'CyclOSM',u:'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',o:{maxZoom:19,subdomains:'abc',attribution:OSMA+' · <a href="https://www.cyclosm.org" target="_blank" rel="noopener">CyclOSM</a>'}},
 {id:'esri',g:'w',n:'Esri 街道图',u:ESRI+'World_Street_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:19,attribution:ESRIA('Esri, HERE, Garmin, USGS, Intermap, NRCAN, Esri Japan, METI, Esri China (Hong Kong), TomTom')}},
 {id:'esrigray',g:'w',n:'Esri 浅灰底图',u:ESRI+'Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:16,attribution:ESRIA('Esri, HERE, Garmin, OpenStreetMap contributors')}},
 {id:'esridark',g:'w',n:'Esri 深灰底图',u:ESRI+'Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:16,attribution:ESRIA('Esri, HERE, Garmin, OpenStreetMap contributors')}},
 {id:'natgeo',g:'t',n:'Esri 国家地理风格',u:ESRI+'NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:16,attribution:ESRIA('National Geographic, Esri, Garmin, HERE, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC')}},
 {id:'topo',g:'t',n:'OpenTopoMap（地形）',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',o:{maxZoom:17,subdomains:'abc',attribution:'Kartendaten: '+OSMA+', SRTM | Kartendarstellung: © <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'}},
 {id:'esrisat',g:'t',n:'Esri 卫星影像',u:ESRI+'World_Imagery/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:19,attribution:ESRIA('Esri, Maxar, Earthstar Geographics, and the GIS User Community')}},
 {id:'nasa',g:'t',n:'NASA 蓝色弹珠（地形晕渲）',u:'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief_Bathymetry/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg',o:{maxZoom:8,maxNativeZoom:8,attribution:'Imagery <a href="https://earthdata.nasa.gov/gibs" target="_blank" rel="noopener">NASA GIBS</a> (Blue Marble)'}},
 {id:'gaode',g:'c',gcj:1,n:'高德地图（中文标注）',u:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',o:{maxZoom:18,minZoom:3,subdomains:'1234',attribution:GDA}},
 {id:'gaodesat',g:'c',gcj:1,n:'高德卫星影像',u:'https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',o:{maxZoom:18,minZoom:3,subdomains:'1234',attribution:GDA}}];
const TGROUP={w:'🌍 全球街道图',t:'🏔️ 地形 · 卫星',c:'🇨🇳 中国大陆友好（GCJ-02，已自动校正标记）'};
const AUTO_IDS=['osm','esri','osmde','osmfr','hot','gaode','natgeo','topo','cyclosm','nasa'];
window.__tileLog=[];
/* WGS-84 -> GCJ-02 (only inside mainland China; elsewhere the two are identical) */
function wgs2gcj(lat,lng){const out=lng<72.004||lng>137.8347||lat<0.8293||lat>55.8271;if(out)return [lat,lng];
  const a=6378245,ee=.00669342162296594323,PI=Math.PI,x=lng-105,y=lat-35;
  let dLat=-100+2*x+3*y+.2*y*y+.1*x*y+.2*Math.sqrt(Math.abs(x))+(20*Math.sin(6*x*PI)+20*Math.sin(2*x*PI))*2/3+(20*Math.sin(y*PI)+40*Math.sin(y/3*PI))*2/3+(160*Math.sin(y/12*PI)+320*Math.sin(y*PI/30))*2/3;
  let dLng=300+x+2*y+.1*x*x+.1*x*y+.1*Math.sqrt(Math.abs(x))+(20*Math.sin(6*x*PI)+20*Math.sin(2*x*PI))*2/3+(20*Math.sin(x*PI)+40*Math.sin(x/3*PI))*2/3+(150*Math.sin(x/12*PI)+300*Math.sin(x/30*PI))*2/3;
  const r=lat/180*PI;let m=Math.sin(r);m=1-ee*m*m;const s=Math.sqrt(m);dLat=dLat*180/((a*(1-ee))/(m*s)*PI);dLng=dLng*180/(a/s*Math.cos(r)*PI);return [lat+dLat,lng+dLng]}
/* one probe tile per provider, in parallel; fastest reachable first. Cached for the session. */
let rankP=null;
function tileRank(lat,lng){if(rankP)return rankP;
  try{const c=JSON.parse(sessionStorage.getItem('wsg_tilerank')||'null');if(c&&c.t>Date.now()-30*60e3)return rankP=Promise.resolve(c.r)}catch(e){}
  const z=4,n=1<<z,x=Math.floor((lng+180)/360*n),la=lat*Math.PI/180,y=Math.floor((1-Math.log(Math.tan(la)+1/Math.cos(la))/Math.PI)/2*n);
  const T0=performance.now(),cand=TILES.filter(t=>AUTO_IDS.includes(t.id));
  rankP=new Promise(res=>{const got=[];let done=0,fin=false;
    const finish=()=>{if(fin)return;fin=true;const ok=got.sort((a,b)=>a[1]-b[1]).map(g=>g[0]);const rest=AUTO_IDS.filter(i=>!ok.includes(i));const r={ok,rest,ms:got.map(g=>[g[0],Math.round(g[1])])};
      window.__tileLog.push(['rank',JSON.stringify(r.ms)]);if(ok.length)try{sessionStorage.setItem('wsg_tilerank',JSON.stringify({t:Date.now(),r}))}catch(e){}res(r)};
    cand.forEach(t=>{const im=new Image();im.referrerPolicy='strict-origin-when-cross-origin';const sd=(t.o.subdomains||'a')[0];
      const tm=setTimeout(()=>{im.src='';end()},window.__probeTimeout||4000);
      function end(){clearTimeout(tm);done++;if(done===cand.length)finish();else if(got.length>=3)setTimeout(finish,250)}
      im.onload=()=>{got.push([t.id,performance.now()-T0]);end()};im.onerror=end;
      im.src=t.u.replace('{s}',sd).replace('{z}',z).replace('{x}',x).replace('{y}',y).replace('{r}','')})});
  return rankP}

let leafletP=null;const getLeaflet=()=>leafletP||(leafletP=(loadCSS('assets/vendor/leaflet/leaflet.css'),loadScript('assets/vendor/leaflet/leaflet.js').then(()=>window.L)));
const geoP={};const getGeo=b=>geoP[b]||(geoP[b]=fetch('assets/geo/'+b+'.json').then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}));
const yearOf=w=>{const m=String(w).match(/\d{3,4}/);return m?+m[0]:9999};
function curve(a,b,bend){const n=24,mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],cx=mx-dy*bend,cy=my+dx*bend,pts=[];for(let i=0;i<=n;i++){const t=i/n,u=1-t;pts.push([u*u*a[0]+2*u*t*cx+t*t*b[0],u*u*a[1]+2*u*t*cy+t*t*b[1]])}return pts}
const SEAS={eu:[[56.2,3.2,'北 海'],[46.5,-9.5,'大 西 洋'],[54.6,-12.5,'爱尔兰海外'],[40.5,5.5,'地 中 海'],[56.5,19.5,'波罗的海']],asia:[[29.5,125.5,'东 海'],[35.6,123.6,'黄 海'],[20.8,116,'南 海'],[24,121.9,'台 湾'],[38.8,120.8,'渤海']],world:[[33,-42,'大 西 洋'],[30,-140,'太 平 洋'],[25,165,'太 平 洋'],[-5,75,'印 度 洋'],[48,-38,'北 大 西 洋']]};
function liveMap(box,data,onPick){
  const el=$('.lmap',box);el.textContent='🗺️ 地图加载中…';
  return getLeaflet().then(L=>{el.textContent='';const coarse=matchMedia('(pointer:coarse)').matches;
    const map=L.map(el,{zoomSnap:.5,scrollWheelZoom:false,dragging:!coarse,tap:false,worldCopyJump:true,preferCanvas:false});
    map.createPane('basePane').style.zIndex=150;map.createPane('seaPane').style.zIndex=160;map.getPane('seaPane').style.pointerEvents='none';
    const rend=L.canvas({pane:'basePane',padding:.3});
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    map.attributionControl.addAttribution('离线底图 <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（公有领域）');
    const st={map,base:null,layer:null,idx:-1,ok:0,err:0,timer:0,gcj:false,order:[]};
    /* self-hosted vector base (never fails): Natural Earth land/rivers/lakes + graticule + sea names, or the Thames for the London map */
    function baseStyle(f){const k=f&&f.properties&&f.properties.k;const land=probe('var(--geo-land)'),coast=probe('var(--geo-coast)'),riv=probe('var(--geo-river)');
      return k==='river'?{color:riv,weight:1.2,opacity:.8,fill:false}:k==='lake'?{color:riv,weight:.6,fillColor:probe('var(--geo-sea)'),fillOpacity:1}:k==='thames'?{color:riv,weight:22,opacity:.55,lineCap:'round'}:k==='grat'?{color:coast,weight:.6,opacity:.22,dashArray:'3 5',fill:false}:{color:coast,weight:1.1,fillColor:land,fillOpacity:1}}
    el.style.background=probe('var(--geo-sea)');
    const addBase=gj=>{st.base=L.geoJSON(gj,{renderer:rend,pane:'basePane',interactive:false,style:baseStyle}).addTo(map)};
    if(data.base==='london'){addBase({type:'Feature',properties:{k:'thames'},geometry:{type:'LineString',coordinates:(data.thames||[]).map(p=>[p[1],p[0]])}})}
    else{const step=data.base==='world'?15:5,gr=[];for(let lo=-180;lo<=180;lo+=step)gr.push([[lo,-80],[lo,84]]);for(let la=-75;la<=80;la+=step)gr.push([[-180,la],[180,la]]);
      getGeo(data.base).then(gj=>{gj.features.unshift({type:'Feature',properties:{k:'grat'},geometry:{type:'MultiLineString',coordinates:gr}});addBase(gj)}).catch(e=>console.warn('geo base',e));
      (SEAS[data.base]||[]).forEach(s=>L.marker([s[0],s[1]],{pane:'seaPane',interactive:false,keyboard:false,icon:L.divIcon({className:'lsea',html:s[2],iconSize:[120,20],iconAnchor:[60,10]})}).addTo(map))}
    st.restyle=()=>{el.style.background=probe('var(--geo-sea)');st.base&&st.base.setStyle(baseStyle);drawRoutes();if(sel.value==='auto'&&st.idx>=0){const want=pref(TILES[st.idx].id);if(want!==TILES[st.idx].id)use(TILES.findIndex(t=>t.id===want))}};
    /* places + routes (shifted to GCJ-02 while a Gaode layer is shown) */
    const ll=p=>st.gcj?wgs2gcj(p.lat,p.lng):[p.lat,p.lng];
    const P=new Map(data.places.map((p,i)=>[p.k,Object.assign({i},p)]));
    const mk=data.places.map((p,i)=>L.marker(ll(p),{title:p.n,riseOnHover:true,icon:L.divIcon({className:'',html:`<div class="lpin" style="--c:${p.c}">${p.i}</div>`,iconSize:[28,28],iconAnchor:[14,14]})})
      .bindTooltip(escH(p.n),{className:'ltip',direction:'right',offset:[12,0]})
      .bindPopup(`<b>${p.i} ${escH(p.n)}</b><br><span class="hl-date">${escH(p.w)}</span><p style="margin:.4em 0 0">${escH(p.d)}</p>`,{maxWidth:260})
      .on('click',()=>onPick(i,true)).addTo(map));
    let rl=null;function drawRoutes(){rl&&map.removeLayer(rl);const cs=getComputedStyle(root),c1=cs.getPropertyValue('--a1').trim(),c2=cs.getPropertyValue('--a2').trim(),cb=cs.getPropertyValue('--bad').trim();
      rl=L.layerGroup(data.routes.map(r=>{const a=P.get(r.a),b=P.get(r.b);if(!a||!b)return null;const col=r.k==='march'?cb:r.k==='flow'?c1:c2;
        return L.polyline(curve(ll(a),ll(b),r.k==='sea'?.22:.16),{color:col,weight:3,opacity:.85,dashArray:r.k==='sea'?'6 7':null,interactive:!!r.l}).bindTooltip(escH(r.l||''),{sticky:true,className:'ltip'})}).filter(Boolean)).addTo(map)}
    function relocate(g){if(st.gcj===g)return;st.gcj=g;mk.forEach((m,i)=>m.setLatLng(ll(data.places[i])));drawRoutes()}
    drawRoutes();
    const b=L.latLngBounds(data.places.map(p=>[p.lat,p.lng]));map.fitBounds(b,{padding:[30,30],maxZoom:data.base==='london'?17:7});
    /* control: grouped provider select + live status + retry */
    const opts=Object.entries(TGROUP).map(([g,n])=>`<optgroup label="${n}">`+TILES.filter(t=>t.g===g).map(t=>`<option value="${t.id}">${t.n}</option>`).join('')+'</optgroup>').join('');
    const Ctl=L.Control.extend({onAdd(){const d=L.DomUtil.create('div','mctl');d.innerHTML='<span class="mst wait">⏳ 准备瓦片…</span><div class="mrow"><select aria-label="地图底图来源"><option value="auto">⚡ 自动：测速选最快，失败自动切换</option>'+opts+'<optgroup label="🧭 离线"><option value="none">仅离线底图（Natural Earth）</option></optgroup></select><button type="button" class="mre" title="重新测速并重试" aria-label="重新测速并重试">↻</button></div>';L.DomEvent.disableClickPropagation(d);L.DomEvent.disableScrollPropagation(d);return d}});
    const ctl=new Ctl({position:'topright'}).addTo(map),cd=ctl.getContainer(),stEl=$('.mst',cd),sel=$('select',cd);
    const status=(c,t)=>{stEl.className='mst '+c;stEl.textContent=t;box.dataset.tiles=c+':'+(st.idx>=0?TILES[st.idx].id:'none');
      /* offline layer only shows while no online layer is up (some providers have transparent water; avoids double coastlines) */
      const hide=c==='on';['basePane','seaPane'].forEach(n=>{const pn=map.getPane(n);if(pn)pn.style.visibility=hide?'hidden':''})};
    const T=()=>window.__tileTimeout||6000;
    /* auto mode keeps the ranked provider as is (hook kept for future theme-specific styles) */
    const pref=id=>id;
    function clear(){clearTimeout(st.timer);if(st.layer){const ly=st.layer;st.layer=null;map.removeLayer(ly);ly.off('tileload tileerror')}}
    function off(msg){clear();st.idx=-1;relocate(false);status('off',msg);window.__tileLog.push([data.base,'offline'])}
    function use(i){clear();
      if(i<0||i>=TILES.length){off(sel.value==='none'?'🧭 仅离线底图（已手动选择）':'🧭 离线底图（在线地图均不可用，可点 ↻ 重试）');return}
      st.idx=i;st.ok=0;st.err=0;const t=TILES[i];status('wait','⏳ 正在连接 '+t.n+'…');relocate(!!t.gcj);
      const ly=L.tileLayer(t.u,Object.assign({updateWhenIdle:true,keepBuffer:1,referrerPolicy:'strict-origin-when-cross-origin',detectRetina:false},t.o));st.layer=ly;
      ly.on('tileload',()=>{if(st.layer!==ly)return;st.ok++;if(st.ok===1){clearTimeout(st.timer);status('on','✅ '+t.n+(sel.value==='auto'?'（自动）':''));window.__tileLog.push([data.base,t.id,'ok'])}});
      ly.on('tileerror',()=>{if(st.layer!==ly)return;st.err++;if((st.ok===0&&st.err>=3)||st.err-st.ok>=8)fail('error')});
      st.timer=setTimeout(()=>{if(st.layer===ly&&st.ok===0)fail('timeout')},T());ly.addTo(map)}
    const nextAuto=()=>{const k=st.order.shift();return k?TILES.findIndex(t=>t.id===pref(k)):-1};
    function fail(why){const t=TILES[st.idx];window.__tileLog.push([data.base,t&&t.id,why]);
      if(sel.value==='auto')use(nextAuto());else off('❌ '+(t?t.n:'')+' 暂不可用，已显示离线底图；可改选其他来源');}
    function auto(){status('wait','⚡ 正在测速 '+AUTO_IDS.length+' 个地图源…');const c=map.getCenter();
      tileRank(c.lat,c.lng).then(r=>{if(sel.value!=='auto')return;st.order=r.ok.concat(r.rest);use(nextAuto())})}
    function apply(){const v=sel.value;v==='auto'?auto():v==='none'?use(-1):use(TILES.findIndex(t=>t.id===v))}
    sel.value=LS.get('tiles','auto');if(![...sel.options].some(o=>o.value===sel.value))sel.value='auto';
    sel.addEventListener('change',()=>{LS.set('tiles',sel.value);apply()});
    $('.mre',cd).addEventListener('click',()=>{rankP=null;try{sessionStorage.removeItem('wsg_tilerank')}catch(e){}apply()});apply();
    /* wheel zoom / drag only after the user engages the map (no scroll-jacking) */
    if(coarse){const h=L.DomUtil.create('div','lhint',el);h.textContent='👆 点按地图以启用拖动；双指缩放';map.once('click',()=>{map.dragging.enable();h.remove()})}
    map.on('focus click',()=>map.scrollWheelZoom.enable());map.on('blur',()=>map.scrollWheelZoom.disable());
    st.focus=(i,pan)=>{const m=mk[i];if(!m)return;if(pan)map.panTo(m.getLatLng(),{animate:!NM()});m.openPopup()};
    LMAPS.push(st);return st})
   .catch(e=>{console.warn(e);el.innerHTML='<p style="padding:20px">交互地图组件加载失败；请使用「🎨 手绘示意图」或「🎬 情景讲解」（离线可用）。</p>'})}
function initMapbox(box){
  let data;try{data=JSON.parse($('.mdata',box).textContent)}catch(e){return}
  const cm=$('.cmap',box),pins=$$('.pin',box),info=$('.minfo',box),lis=$$('.mplaces li',box),tabs=$$('.mtabs [data-v]',box),views={c:$('.mv-c',box),s:$('.mv-s',box),l:$('.mv-l',box)},play=$('.mplay',box);
  let live=null,liveP=null,cur=-1,timer=0;
  function show(i,fromMap){const p=data.places[i];if(!p)return;cur=i;pins.forEach((x,j)=>x.classList.toggle('on',j===i));lis.forEach((x,j)=>x.classList.toggle('on',j===i));
    info.style.setProperty('--c',p.c);info.innerHTML=`<div class="mi-h"><b>${p.i} ${escH(p.n)}</b><span class="hl-date">${escH(p.w)}</span><span class="muted small">${i+1} / ${data.places.length}</span></div><div>${escH(p.d)}</div>`;
    if(live&&!fromMap&&views.l.classList.contains('on'))live.focus(i,true)}
  function view(v){tabs.forEach(t=>{const on=t.dataset.v===v;t.classList.toggle('on',on);t.setAttribute('aria-selected',on)});Object.entries(views).forEach(([k,e])=>e&&e.classList.toggle('on',k===v));
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
/* v3.2 情景讲解：story reels cycle a spotlight only while on screen; animated scenes start when seen */
function initViz(sc){$$('.story:not(.inited)',sc).forEach(sr=>{sr.classList.add('inited');const li=$$('.st-reel li',sr),bar=$('.st-bar i',sr);let k=-1,t=0;
  const go=i=>{k=i%li.length;li.forEach((x,j)=>{x.classList.toggle('cur',j===k);x.classList.toggle('past',j<k)});bar&&(bar.style.transform=`scaleX(${(k+1)/li.length})`)};
  li.forEach((x,i)=>x.addEventListener('click',()=>{clearInterval(t);t=0;go(i)}));
  new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){sr.classList.add('seen');if(!NM()&&!t){go(k<0?0:k);t=setInterval(()=>go(k+1),2600)}else if(NM())go(li.length-1)}else{clearInterval(t);t=0}}),{rootMargin:'0px 0px -12% 0px'}).observe(sr)});
$$('.scene:not(.inited)',sc).forEach(x=>{x.classList.add('inited');new IntersectionObserver(es=>es.forEach(e=>{x.classList.toggle('run',e.isIntersecting);if(e.isIntersecting)x.classList.add('seen')}),{rootMargin:'0px 0px -10% 0px'}).observe(x)});}
initViz(document);
/* v3.2 地图源体检: probe every provider once on the user's own network */
$$('.tilecheck').forEach(tc=>{const btn=$('.tc-run',tc),out=$('.tc-out',tc);btn.addEventListener('click',()=>{btn.disabled=true;btn.textContent='⏳ 测速中…';
  const z=4,x=8,y=5,T0=performance.now(),res={};
  out.innerHTML='<ul class="tc-list">'+TILES.map(t=>`<li data-id="${t.id}"><span class="tc-s">⏳</span><b>${escH(t.n)}</b><span class="tc-g">${escH(TGROUP[t.g].split('（')[0])}</span><span class="tc-ms"></span></li>`).join('')+'<li><span class="tc-s">✅</span><b>Natural Earth 离线底图</b><span class="tc-g">🧭 本站自带</span><span class="tc-ms">永远可用</span></li></ul>';
  let left=TILES.length;TILES.forEach(t=>{const im=new Image(),li=$(`li[data-id="${t.id}"]`,out),t0=performance.now();let done=false;
    const fin=(ok)=>{if(done)return;done=true;clearTimeout(tm);li.classList.add(ok?'ok':'bad');$('.tc-s',li).textContent=ok?'✅':'❌';$('.tc-ms',li).textContent=ok?Math.round(performance.now()-t0)+' ms':'无法连接';
      if(--left===0){btn.disabled=false;btn.textContent='↻ 再测一次';const n=$$('li.ok',out).length;out.insertAdjacentHTML('beforeend',`<p class="tc-sum">${n} / ${TILES.length} 个在线地图源可用${n?'；实景地图的「⚡自动」会优先用最快的那一家':'；请使用手绘示意图或离线底图'}。</p>`)}};
    const tm=setTimeout(()=>{im.src='';fin(false)},8000);im.onload=()=>fin(true);im.onerror=()=>fin(false);im.referrerPolicy='strict-origin-when-cross-origin';
    const zz=t.o.minZoom>z?t.o.minZoom:z;im.src=t.u.replace('{s}',(t.o.subdomains||'a')[0]).replace('{z}',zz).replace('{x}',x).replace('{y}',y).replace('{r}','')})})});



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
