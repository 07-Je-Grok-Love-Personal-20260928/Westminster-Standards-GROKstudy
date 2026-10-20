/* Westminster Standards GROKstudy — interactions */
(function(){
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const LS={get:(k,d)=>{try{const v=localStorage.getItem('wsg_'+k);return v===null?d:JSON.parse(v)}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem('wsg_'+k,JSON.stringify(v))}catch(e){}}};
// theme
const root=document.documentElement;
root.dataset.theme=LS.get('theme',(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
document.addEventListener('DOMContentLoaded',()=>{
  const tb=$('#themeBtn'); if(tb){tb.textContent=root.dataset.theme==='dark'?'☀️':'🌙';tb.onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';LS.set('theme',root.dataset.theme);tb.textContent=root.dataset.theme==='dark'?'☀️':'🌙';if(window.__remermaid)window.__remermaid()}}
  // TOC
  const toc=$('#tocList'), main=$('main');
  const hs=$$('h2.h, h3.h',main);
  hs.forEach((h,i)=>{if(!h.id)h.id='s'+i});
  if(toc){toc.innerHTML=hs.map(h=>`<li class="${h.tagName==='H3'?'l3':'l2'}"><a href="#${h.id}">${h.dataset.toc||h.textContent.trim()}</a></li>`).join('')}
  const isMobile=()=>matchMedia('(max-width:980px)').matches;
  if(!isMobile()&&LS.get('tocoff',false))document.body.classList.add('toc-off');
  const tbtn=$('#tocBtn'); if(tbtn)tbtn.onclick=()=>{if(isMobile())document.body.classList.toggle('toc-open');else{document.body.classList.toggle('toc-off');LS.set('tocoff',document.body.classList.contains('toc-off'))}setTimeout(()=>window.__map&&window.__map.invalidateSize(),400)};
  const scrim=$('.scrim'); if(scrim)scrim.onclick=()=>document.body.classList.remove('toc-open');
  if(toc)toc.addEventListener('click',e=>{if(e.target.tagName==='A'&&isMobile())document.body.classList.remove('toc-open')});
  const tf=$('#tocFilter'); if(tf)tf.oninput=()=>{const v=tf.value.trim();$$('li',toc).forEach(li=>li.style.display=!v||li.textContent.includes(v)?'':'none')};
  // active section
  const links=new Map($$('a',toc||document.createElement('div')).map(a=>[a.getAttribute('href').slice(1),a]));
  const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){links.forEach(a=>a.classList.remove('active'));const a=links.get(e.target.id);if(a){a.classList.add('active');const r=a.getBoundingClientRect(),tr=toc.parentElement.getBoundingClientRect();if(r.top<tr.top+40||r.bottom>tr.bottom-20)a.scrollIntoView({block:'center',behavior:'smooth'})}}})},{rootMargin:'-15% 0px -75% 0px'});
  hs.forEach(h=>io.observe(h));
  // progress + totop
  const pg=$('.progress'), tt=$('.totop');
  const onScroll=()=>{const h=document.documentElement;const p=h.scrollTop/(h.scrollHeight-h.clientHeight||1);if(pg)pg.style.width=(p*100)+'%';if(tt)tt.classList.toggle('show',h.scrollTop>600)};
  addEventListener('scroll',onScroll,{passive:true}); onScroll();
  if(tt)tt.onclick=()=>scrollTo({top:0,behavior:'smooth'});
  // reveal
  const rio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');rio.unobserve(e.target)}}),{rootMargin:'0px 0px -6% 0px'});
  $$('.rv').forEach(el=>rio.observe(el));
  // refs toggle
  const rb=$('#refsBtn'); if(rb){if(LS.get('norefs',false))document.body.classList.add('no-refs');rb.onclick=()=>{document.body.classList.toggle('no-refs');LS.set('norefs',document.body.classList.contains('no-refs'))}}
  // filter for doc pages
  const df=$('#docFilter'); if(df)df.oninput=()=>{const v=df.value.trim();$$('[data-search]').forEach(el=>{el.classList.toggle('hide',!!v&&!el.textContent.includes(v))});$$('.grp').forEach(g=>{if(!v){g.open=g.dataset.open==='1';return}g.open=true})};
  // timeline filters
  $$('.filters[data-for]').forEach(f=>{f.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',f).forEach(x=>x.classList.remove('on'));b.classList.add('on');const k=b.dataset.k;$$(f.dataset.for+' [data-cat]').forEach(ev=>ev.classList.toggle('hide',k!=='all'&&!ev.dataset.cat.split(' ').includes(k)))})});
  // memorized marks
  const done=LS.get('done',{});
  $$('.memo').forEach(m=>{const k=m.dataset.k;if(done[k])m.classList.add('done');m.onclick=e=>{e.stopPropagation();done[k]=!done[k];m.classList.toggle('done',!!done[k]);m.textContent=done[k]?'✔ 已背':'☆ 标记';LS.set('done',done);updateCount()};m.textContent=done[k]?'✔ 已背':'☆ 标记'});
  function updateCount(){$$('[data-count]').forEach(el=>{const p=el.dataset.count;const n=Object.keys(done).filter(k=>done[k]&&k.startsWith(p)).length;el.textContent=n})}
  updateCount();
  // reveal answers in hide mode
  document.addEventListener('click',e=>{const a=e.target.closest('.ansbody');if(a&&(document.body.classList.contains('mode-hide')||document.body.classList.contains('mode-cloze')))a.classList.toggle('show')});
  if(window.__pageInit)window.__pageInit();
  // mermaid
  if(window.mermaid){const src=new Map();$$('.mermaid').forEach((m,i)=>src.set(m,m.textContent));
    const run=()=>{const dark=root.dataset.theme==='dark';mermaid.initialize({startOnLoad:false,theme:dark?'dark':'base',securityLevel:'loose',themeVariables:dark?{}:{primaryColor:'#e0e7ff',primaryBorderColor:'#6366f1',primaryTextColor:'#1d2433',lineColor:'#7c3aed',fontFamily:'PingFang SC, Microsoft YaHei, sans-serif'},flowchart:{useMaxWidth:true,htmlLabels:true},mindmap:{useMaxWidth:true}});
      src.forEach((t,m)=>{m.removeAttribute('data-processed');m.innerHTML=t});mermaid.run({nodes:[...src.keys()]}).catch(e=>console.warn(e))};
    window.__remermaid=run; run();}
});
})();
document.addEventListener('DOMContentLoaded',()=>{const a=document.querySelector('.topnav a.on');if(a&&a.parentElement.scrollWidth>a.parentElement.clientWidth){const n=a.parentElement;n.scrollLeft=a.offsetLeft-n.offsetLeft-8}});
