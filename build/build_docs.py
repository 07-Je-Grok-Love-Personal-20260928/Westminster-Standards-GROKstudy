# -*- coding: utf-8 -*-
import json, re, sys
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from content_wcf import WCF
from content_more import WSC_GROUPS, WLC_GROUPS
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')+'/'
D=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','standards.json')))
C=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','cci_struct.json')))
BC={a['no']:a for a in C['bc']}
HC={i['q']:dict(i,ld=x['ld'],url=x['url']) for x in C['hc'] for i in x['items']}
CDH={'I':C['cd'][0],'II':C['cd'][1],'III/IV':C['cd'][2],'V':C['cd'][3]}
CN='一二三四五六七八九十'
def cn(n):
    if n<=10: return CN[n-1]
    if n<20: return '十'+CN[n-11]
    return CN[n//10-1]+'十'+(CN[n%10-1] if n%10 else '')
XREF={1:('2–3','2–5'),2:('4–6','6–11'),3:('7–8','12–14'),4:('9–10','15–17'),5:('11','18–19'),6:('13–19','21–29'),7:('12, 20','20, 30–35'),8:('21–28','36–56'),9:('13, 18','21, 25'),10:('29–31','57–60, 66–68'),11:('33','70–73'),12:('34','74'),13:('35','75, 77–78'),14:('86','72–73'),15:('87','76'),16:('','75, 78'),17:('36','79'),18:('36','80–81'),19:('39–84','91–152'),20:('',''),21:('45–62, 88, 98–107','103–121, 178–196'),22:('53–56','111–114'),23:('63–66','123–133'),24:('70–72','137–139'),25:('','61–65'),26:('','63–65'),27:('91–93','161–164'),28:('94–95','165–167'),29:('96–97','168–177'),30:('',''),31:('',''),32:('37–38','84–87'),33:('38','88–90')}
def qlinks(s,doc):
    if not s: return '—'
    out=[]
    for part in s.split(','):
        part=part.strip(); a=part.split('–')[0]
        out.append(f'<a href="{doc}.html#q{a}">{part}</a>')
    return '，'.join(out)
def contin(c):
    """Continental cross-reference blocks with verbatim ccifellowship text"""
    blocks=[]
    for n in c.get('bc',[]):
        a=BC[n]; blocks.append(f'<details><summary>📕 比利时信条 · {esc(a["title"])}</summary><div class="dbody cbox">{a["html"]}<p class="muted">原文来源：<a href="{a["url"]}" target="_blank" rel="noopener">ccifellowship.org</a></p></div></details>')
    hcs=c.get('hc',[])
    if hcs:
        inner=''.join(f'<div class="qa"><div class="q"><span class="n">HC {q}</span><span>{esc(HC[q]["ques"])}<span class="muted">（主日{HC[q]["ld"]}）</span></span></div><div class="a cbox">{HC[q]["html"]}</div></div>' for q in hcs)
        blocks.append(f'<details><summary>📗 海德堡要理问答 · 第{hcs[0]}{"–"+str(hcs[-1]) if len(hcs)>1 else ""}问（{len(hcs)}问）</summary><div class="dbody">{inner}<p class="muted">原文来源：ccifellowship.org《海德堡要理问答》</p></div></details>')
    for h in c.get('cd',[]):
        s=CDH[h]
        lst=''.join(f'<li><a href="{a["url"]}" target="_blank" rel="noopener">{esc(a["title"])}</a></li>' for a in s['arts'])
        blocks.append(f'<details><summary>📙 多特信经 · {esc(s["title"])}</summary><div class="dbody"><p>本项条目（全文见「信经与联合信条」页）：</p><ol>{lst}</ol></div></details>')
    return ''.join(blocks) or '<p class="muted">三项联合信条无直接对应条目，可参「深度对比」页的说明。</p>'
# ================= WCF =================
def wcf_section(s, recite=False):
    num=s['sec']
    if 'ot' in s:
        body=fmt(s['text'])+'<br><b>旧约：</b>'+'、'.join(esc(x) for x in s['ot'])+'<br><b>新约：</b>'+'、'.join(esc(x) for x in s['nt'])+'<br>'+fmt(s['tail'])
    else: body=fmt(s['text'])
    return f'<p class="ansbody">{body}</p>'+refs_html(s['refs'])
def build_wcf():
    from content_v2 import PR, WARN, ORDO, AMREV
    W=D['wcf']; parts=[]
    parts.append(f'''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/jerusalem-chamber.jpg)"><div class="shine"></div><div class="floaty">📘</div>
<h1>《西敏信仰告白》逐章精解</h1>
<p>1646年完成、1647年附经文呈交的<b>33章 · {sum(len(c['secs']) for c in W)}节</b>信仰告白。每章：<b>核心一句话</b> → <b>原文</b>（RTF-USA 2024 简体译本）→ 解读标签页（圣经神学 · 圣约神学 · 欧陆改革宗 · 长老会正统 · 难点 · 应用）→ 记忆钩子与常见误解 → 三项联合信条<b>原文</b>对照。</p>
<div class="chips"><span class="chip">📖 33 章</span><span class="chip">🧩 {sum(len(c['secs']) for c in W)} 节</span><span class="chip">📎 附证明经文</span><span class="chip">🏛️ 1647 原文版本</span><span class="chip">🖍️ 统一标注系统</span></div></section>''')
    parts.append(h2('全局地图：33章的七大板块','🗺️','map33'))
    blocks=[('rev','启示：神如何说话',[1]),('god','神与他的作为',[2,3,4,5]),('man','人、罪与约',[6,7,8,9]),('sal','救恩的施行',list(range(10,19))),('law','律法、自由、敬拜与社会',list(range(19,25))),('chu','教会与圣礼',list(range(25,32))),('end','末后的事',[32,33])]
    g=''
    for cat,name,chs in blocks:
        chips=''.join(f'<a class="pill" href="#c{n}">{n}. {esc(W[n-1]["title"])}</a>' for n in chs)
        g+=f'<div class="card bl-{cat} rv"><h3 style="margin:0 0 6px">{CATS[cat][1]} {name}<span class="muted small" style="margin-left:auto">{sum(len(W[n-1]["secs"]) for n in chs)} 节</span></h3>{chips}</div>'
    parts.append(f'<div class="grid">{g}</div>')
    parts.append('<div class="grid g2">'+'<div class="card rv"><h3 style="margin-top:0">📊 各章篇幅（节数，点击跳转）</h3>'+bars([(f"{c['no']}. {c['title']}",len(c['secs']),f"var(--c-{WCF[c['no']]['cat']})",f"#c{c['no']}") for c in W],cls='rv')+'<p class="muted small">数据：按本站所用 RTF-USA 2024 译本统计；第1章（圣经）10节最长，第12章（收养）只有1节。</p></div>'
      +'<div>'+'<div class="mermaid">'+esc('''flowchart TB
  A["📖 圣经 1"] --> B["✨ 神 2-5"]
  B --> C["💔 堕落 6"]
  C --> D["🤝 圣约 7"]
  D --> E["✝️ 中保基督 8"]
  E --> F["🌱 救恩施行 9-18"]
  F --> G["📜 感恩生活 19-24"]
  G --> H["⛪ 教会与圣礼 25-31"]
  H --> I["🌅 末后之事 32-33"]''')+'</div>'
      +callout('key-pt','🧭 阅读线索','整本信条沿着<mark>「神说话 → 神是谁 → 人怎样堕落 → 神怎样立约拯救 → 被救的人怎样生活、聚集、盼望」</mark>展开。',raw=True)+'</div></div>')
    parts.append(h3('🔗 救恩的次序（第10–18章 + 第32–33章）','ordo'))
    parts.append('<div class="chain">'+''.join(f'<a class="rv" href="#c{r.split("–")[0].split(".")[0]}"><span class="e">{e}</span><b>{t}</b><small>WCF {r} · {w}</small></a>' for e,t,r,w in ORDO)+'</div>')
    parts.append(callout('hard-pt','🔍 读法提示','这是<span class="u-err">逻辑次序</span>，不是一定的时间先后：称义、收养在信的那一刻同时发生；成圣、信心与悔改贯穿一生。',raw=True))
    parts.append('<div class="card"><input id="docFilter" type="search" placeholder="🔍 搜索信条正文与解读（如：称义、安息日、圣约）" style="width:100%;padding:10px 14px;border-radius:12px;border:1px solid var(--line);background:var(--card2);color:var(--ink);font-size:15px"><div class="muted" style="margin-top:6px">☰ 隐藏/显示目录 · 🖍️ 查看标注图例 · <button class="btn" id="refsBtn">📎 显示/隐藏证明经文</button></div>'+legend()+'</div>')
    AM={r[0].split('.')[0] for r in AMREV}
    for ch in W:
        n=ch['no']; c=WCF[n]; cat=c['cat']
        secs=''.join(f'<div data-search>{wcf_section(s)}</div>' for s in ch['secs'])
        xs,xl=XREF[n]
        am=''
        if str(n) in AM:
            am=callout('pr-pt','🇺🇸 1647原文 vs 美国修订本',' '.join(f'<b>{r[0]}</b>：原文{esc(r[1])}；美国修订本（如OPC现行文本）{esc(r[2])}。' for r in AMREV if r[0].split('.')[0]==str(n))+' 详见<a href="compare.html#amrev">深度对比</a>。',raw=True)
        tb=tabs([('bt-pt','📚 圣经神学',mk(c['bt'])),('cov-pt','🤝 圣约神学',mk(c['ct'])),('eu-pt','🇳🇱 欧陆改革宗',mk(c['eu'],cmp=True)),('pr-pt','🏴 长老会正统',mk(PR[n],cmp=True)),('hard-pt','🔍 难点',mk(c['hard'])),('app-pt','🛠️ 应用',mk(c['app']))],f'tab{n}')
        parts.append(f'''<section class="sec" id="c{n}" data-search>
{h2(f"第{cn(n)}章 {esc(ch['title'])}",c['icon'],None,f"{n}. {ch['title']}")}
<div class="cv">
<div><span class="tag t-{cat}">{CATS[cat][1]} {CATS[cat][0]}</span><span class="pill">📍 关键经文：<span class="u-bib" style="white-space:normal">{esc(c['verses'])}</span></span><span class="pill">📙 小要理：{qlinks(xs,'wsc')}</span><span class="pill">📗 大要理：{qlinks(xl,'wlc')}</span></div>
{callout('key-pt','🎯 核心要义',c['key'])}
<details open><summary>📜 原文（{len(ch['secs'])}节）· RTF-USA 2024 简体译本</summary><div class="dbody src">{secs}</div></details>
{tb}
<div class="grid g2">{callout('mem-pt','🧠 记忆钩子',c['mem'])}{callout('warn-pt','🚫 常见误解',WARN[n])}</div>
{am}
<details><summary>🔗 对照三项联合信条原文（ccifellowship.org）</summary><div class="dbody">{contin(c)}</div></details>
</div>
</section>''')
    open(OUT+'wcf.html','w').write(page('wcf.html','西敏信仰告白 · 逐章精解','\n'.join(parts)))
# ================= Catechisms =================
def qa_card(doc,u):
    return f'''<div class="qa" id="q{u['q']}" data-search><div class="q"><span class="n">{u['q']}</span><span style="flex:1">{fmt(u['ques'])}</span><button class="memo" data-k="{doc}-{u['q']}">☆ 标记</button></div><div class="a ansbody">{fmt(u['ans'])}</div>{refs_html(u['refs'])}</div>'''
def build_cat(doc):
    data=D[doc]; groups=WSC_GROUPS if doc=='wsc' else WLC_GROUPS
    Q={u['q']:u for u in data}
    if doc=='wsc':
        title='西敏小要理问答 · 107问精解'; h1='📙《西敏小要理问答》107问'
        intro='1647年11月呈交国会的「简短易记」版本，为初学者和儿女而写。<b>第1–38问：人当信什么；第39–107问：神要求人尽什么本分。</b>历代被誉为最精炼的要理问答之一。'
        mm='''flowchart TB
  A["🎯 1-3 人生目的与圣经"] --> B["📖 当信什么 4-38"]
  A --> C["📜 当尽何本分 39-107"]
  B --> B1["✨ 神 4-11"] --> B2["💔 约与堕落 12-19"] --> B3["✝️ 恩典之约与基督 20-28"] --> B4["🌱 救恩施行 29-38"]
  C --> C1["🔟 律法与十诫 39-81"] --> C2["🔥 罪·信·悔 82-87"] --> C3["💧 圣道与圣礼 88-97"] --> C4["🙏 祷告与主祷文 98-107"]'''
        img='abbey.jpg'
    else:
        title='西敏大要理问答 · 196问精解'; h1='📗《西敏大要理问答》196问'
        intro='1647年10月呈交国会，「更精确、更全面」，主要供牧者讲道与成熟信徒深入学习。<b>第1–90问：人当信什么；第91–196问：人当尽何本分。</b>其特色在于“与基督联合”的恩惠（恩典中/荣耀中）、详尽的十诫伦理与蒙恩之道。'
        mm='''flowchart TB
  A["🎯 1-5 序言"] --> B["📖 当信什么 6-90"]
  A --> C["📜 当尽何本分 91-196"]
  B --> B1["✨ 神·预旨·创造·护理 6-20"] --> B2["💔 堕落与罪 21-29"] --> B3["🤝 恩典之约 30-35"] --> B4["✝️ 中保基督 36-56"] --> B5["⛪ 施行·教会 57-65"] --> B6["🌱 恩典中 66-81"] --> B7["🌅 荣耀中 82-90"]
  C --> C1["📜 道德律 91-97"] --> C2["🔟 十诫 98-148"] --> C3["⚖️ 罪与出路 149-153"] --> C4["💧 道与圣礼 154-177"] --> C5["🙏 祷告 178-196"]'''
        img='covenant.jpg'
    parts=[f'''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/{img})"><div class="shine"></div><div class="floaty">{'📙' if doc=='wsc' else '📗'}</div><h1>{h1}</h1><p>{intro}</p>
<div class="chips"><span class="chip">正文：RTF-USA 2024 简体译本</span><span class="chip">附证明经文</span><span class="chip">☆ 可标记「已背」</span><span class="chip">已背：<b data-count="{doc}-">0</b> / {len(data)}</span></div></section>''']
    parts.append(h2('结构总览','🧭','overview'))
    parts.append(f'<div class="mermaid">{esc(mm)}</div>')
    parts.append(callout('key-pt','🧭 两部要理问答的分工',('先背<mark>小要理问答</mark>：用最少的字说准每条教义；需要展开时，查对应的<a href="wlc.html">大要理问答</a>与<a href="wcf.html">信仰告白</a>章节。' if doc=='wsc' else '大要理问答是<mark>讲台与教师的手册</mark>：比小要理多出「有形/无形教会」「恩典中/荣耀中与基督相交」「十诫解释八规则」「善用洗礼」等内容。'),raw=True))
    if doc=='wlc':
        parts.append(callout('key-pt','📜 苏格兰教会总会批准法案（1648年7月2日，本站所用译本所附）',f'<div class="src" style="font-size:15px">{esc(D["wlc_act"].replace("西敏大要理问答","").strip())}</div>'))
    parts.append('<div class="card"><input id="docFilter" type="search" placeholder="🔍 搜索问答（如：称义、圣餐、第五诫）" style="width:100%;padding:10px 14px;border-radius:12px;border:1px solid var(--line);background:var(--glass2);color:var(--ink);font-size:15px"><div class="muted" style="margin-top:6px"><button class="btn" id="refsBtn">📎 显示/隐藏证明经文</button> · 想遮盖答案自测？请到 <a href="recite.html">背诵版</a>。</div></div>')
    parts.append(legend())
    parts.append('<div class="grid g2">'+'<div class="card rv"><h3 style="margin-top:0">🍩 “信”与“行”的比例</h3>'+(donut([('序言 1–3',3,'var(--a3)'),('当信什么 4–38',35,'var(--a1)'),('当尽本分 39–107',69,'var(--a2)')],'107','问') if doc=='wsc' else donut([('序言 1–5',5,'var(--a3)'),('当信什么 6–90',85,'var(--a1)'),('当尽本分 91–196',106,'var(--a2)')],'196','问'))+'<p class="muted small">按问答编号统计。近三分之二篇幅讲“本分”——十诫、蒙恩之道与祷告，显示西敏传统「教义必须落实为敬虔」。</p></div>'
      +'<div class="card rv"><h3 style="margin-top:0">📊 各板块问数（点击跳转）</h3>'+bars([(f"{g['r'][0]}–{g['r'][1]} {g['title']}",g['r'][1]-g['r'][0]+1,f"var(--c-{g['cat']})",f"#g{g['r'][0]}") for g in groups],cls='rv')+'</div></div>')
    for g in groups:
        a,b=g['r']; cat=g['cat']
        chunks=[]
        rng=list(range(a,b+1))
        for i in range(0,len(rng),8):
            chunks.append('<div class="cv">'+''.join(qa_card(doc,Q[q]) for q in rng[i:i+8])+'</div>')
        tb=tabs([('bt-pt','📚 圣经神学',mk(g['bt'])),('eu-pt','🇳🇱 欧陆对照',mk(g['eu'],cmp=True))],f'tab{doc}{a}')
        parts.append(f'''<section class="sec">{h2(f"第{a}–{b}问 · {g['title']}",g['icon'],f"g{a}",f"{a}–{b} {g['title']}")}
<span class="tag t-{cat}">{CATS[cat][1]} {CATS[cat][0]}</span>
{callout('key-pt','🎯 核心要义',g['key'])}
<div class="grid g2"><div>{tb}</div>{callout('mem-pt','🧠 记忆钩子',g['mem'])}</div>
<details class="grp" open data-open="1"><summary>📜 原文：第{a}–{b}问（{b-a+1}问）</summary><div class="dbody">{''.join(chunks)}</div></details></section>''')
    open(OUT+f'{doc}.html','w').write(page(f'{doc}.html',title,'\n'.join(parts),js=MERMAID_JS))
# ================= Recite =================
def build_recite():
    W=D['wcf']
    wcf=''.join(f'<section class="rdoc-sec" id="r-wcf-{ch["no"]}"><h3 class="h" data-toc="信条 {ch["no"]}. {esc(ch["title"])}">第{cn(ch["no"])}章 {esc(ch["title"])}</h3><div class="src cv">'+''.join(f'<div class="qa rq" data-search><button class="memo" data-k="wcf-{ch["no"]}-{i+1}">☆ 标记</button>{wcf_section(s)}</div>' for i,s in enumerate(ch['secs']))+'</div></section>' for ch in W)
    def cat(doc):
        items=[x for x in D[doc]]
        return ''.join('<div class="cv">'+_cat(doc,items[i:i+10])+'</div>' for i in range(0,len(items),10))
    def _cat(doc,items):
        return ''.join(f'<div class="qa rq" id="r-{doc}-{u["q"]}" data-search><div class="q"><span class="n">{u["q"]}</span><span style="flex:1">{fmt(u["ques"])}</span><button class="memo" data-k="{doc}-{u["q"]}">☆ 标记</button></div><div class="a ansbody">{fmt(u["ans"])}</div>{refs_html(u["refs"])}</div>' for u in items)
    wsc_groups=''.join(f'<h3 class="h" data-toc="小要理 {g["r"][0]}–{g["r"][1]} {g["title"]}">第{g["r"][0]}–{g["r"][1]}问 · {g["title"]}</h3>' for g in WSC_GROUPS)
    body=f'''<section class="hero"><div class="shine"></div><div class="floaty">🎙️</div><h1> 干净阅读版 · 背诵模式</h1>
<p>三份西敏文件的<b>纯净全文</b>（无解读干扰），可切换：阅读 / 遮盖答案（点击揭开）/ 首字提示（填空背诵）；可调字号、隐藏证明经文、标记已背进度（保存在本机浏览器）。</p>
<div class="chips"><span class="chip">信条已背 <b data-count="wcf-">0</b></span><span class="chip">大要理已背 <b data-count="wlc-">0</b>/196</span><span class="chip">小要理已背 <b data-count="wsc-">0</b>/107</span></div></section>
<div class="recite-bar" id="rbar">
 <select id="rDoc"><option value="wsc">📙 小要理问答（107）</option><option value="wlc">📗 大要理问答（196）</option><option value="wcf">📘 信仰告白（33章）</option></select>
 <select id="rMode"><option value="read">📖 阅读</option><option value="hide">🙈 遮盖答案</option><option value="cloze">✍️ 首字提示</option></select>
 <label class="pill">字号 <input id="rSize" type="range" min="15" max="26" value="18" style="vertical-align:middle;width:90px"></label>
 <button class="btn" id="refsBtn">📎 经文</button>
 <input id="docFilter" type="search" placeholder="🔍 搜索/跳转" style="flex:1;min-width:120px">
 <button class="btn" id="rShowAll">👁️ 全部揭开</button>
</div>
<div class="reading">
<div class="rdoc" data-doc="wsc">{h2('西敏小要理问答（全文）','📙','rd-wsc')}{cat('wsc')}</div>
<div class="rdoc hide" data-doc="wlc">{h2('西敏大要理问答（全文）','📗','rd-wlc')}{cat('wlc')}</div>
<div class="rdoc hide" data-doc="wcf">{h2('西敏信仰告白（全文）','📘','rd-wcf')}{wcf}</div>
</div>
<p class="muted">正文来源：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024，免费分发，非卖品）。</p>'''
    js='''<script>
window.__pageInit=function(){
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const doc=$('#rDoc'),mode=$('#rMode'),size=$('#rSize');
 const LSg=(k,d)=>{try{return JSON.parse(localStorage.getItem('wsg_'+k))??d}catch(e){return d}},LSs=(k,v)=>{try{localStorage.setItem('wsg_'+k,JSON.stringify(v))}catch(e){}};
 const h=location.hash.match(/^#(wsc|wlc|wcf)/); doc.value=h?h[1]:LSg('rdoc','wsc'); mode.value=LSg('rmode','read'); size.value=LSg('rsize',18);
 function cloze(el){ if(el.dataset.cz)return; el.dataset.orig=el.innerHTML; const t=el.textContent.replace(/\\d+(?=[，。；、：！？」”）]|$)/g,'');
   el.dataset.cz=t.replace(/[&<>]/g,'').replace(/([\\u4e00-\\u9fff])([\\u4e00-\\u9fff]+)/g,(m,a,b)=>a+'<span class="cl">'+b+'</span>'); }
 function apply(){ $$('.rdoc').forEach(d=>d.classList.toggle('hide',d.dataset.doc!==doc.value));
   document.body.classList.toggle('mode-hide',mode.value==='hide'); document.body.classList.toggle('mode-cloze',mode.value==='cloze');
   $$('.ansbody').forEach(el=>{ el.classList.remove('show'); if(mode.value==='cloze'){cloze(el);el.innerHTML=el.dataset.cz} else if(el.dataset.orig){el.innerHTML=el.dataset.orig} });
   document.querySelector('.reading').style.setProperty('--rfs',size.value+'px');
   LSs('rdoc',doc.value);LSs('rmode',mode.value);LSs('rsize',size.value);
   // rebuild TOC for visible doc
   const toc=document.getElementById('tocList'); const vis=document.querySelector('.rdoc:not(.hide)');
   toc.dataset.custom='1'; toc.innerHTML=[...vis.querySelectorAll('h2.h,h3.h,.rq[id]')].filter(e=>e.tagName!=='DIV'||e.id.match(/-(1|\\d*0|\\d*5)$/)).map(e=>{const t=e.tagName==='DIV'?('第'+e.id.split('-').pop()+'问'):(e.dataset.toc||e.textContent);return `<li class="${e.tagName==='H2'?'l2':'l3'}"><a href="#${e.id}">${t}</a></li>`}).join('');
   if(window.__rebuildToc)window.__rebuildToc();
 }
 [doc,mode,size].forEach(x=>x.addEventListener('input',apply));
 $('#rShowAll').onclick=()=>$$('.ansbody').forEach(el=>el.classList.add('show'));
 apply();
};
</script>'''
    open(OUT+'recite.html','w').write(page('recite.html','干净阅读版 · 背诵模式',body,js=js))
# ================= Creeds & Three Forms (verbatim ccifellowship) =================
def build_creeds():
    parts=[f'''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/heidelberg1563.jpg)"><div class="shine"></div><div class="floaty">📜</div><h1> 三大普世信经 · 三项联合信条（原文）</h1>
<p>本页全部原文<b>逐字取自</b> <a style="color:#fde68a" href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">ccifellowship.org《敬拜手册》</a>（中国改革宗教会），未作任何改动；仅为阅读排版而调整格式。欧陆改革宗以此为教义准则，本站以它们作为解读西敏标准的「对照坐标」。</p>
<div class="chips"><span class="chip">使徒信经</span><span class="chip">尼西亚信经</span><span class="chip">亚他那修信经</span><span class="chip">比利时信条 37条</span><span class="chip">海德堡要理问答 129问</span><span class="chip">多特信经 4项</span></div></section>''']
    parts.append(h2('普世信经','🕊️','creeds'))
    parts.append(f'<div class="card rv">{C["creeds_intro"]}</div>')
    parts.append('<div class="filters"><button class="btn" id="creedHide">🙈 遮盖/显示信经正文（背诵）</button></div>')
    for cr in C['creeds']:
        body=''.join(f'<p>{p}</p>' for p in cr['body'])
        parts.append(f'''{h3(f"✝️ {esc(cr['title'])}",cr['id'])}<div class="card rv"><p class="muted">{cr['intro']}</p><div class="bigquote ansbody creedbody">{body}</div><p class="muted">原文：<a href="{cr['url']}" target="_blank" rel="noopener">{cr['url']}</a></p></div>''')
    parts.append(h2('比利时信条（1561）','📕','bc'))
    parts.append(f'<div class="card">{C["bc_intro"]}</div>')
    parts.append(''.join(f'<details id="bc{a["no"]}"><summary>{esc(a["title"])}</summary><div class="dbody cbox">{a["html"]}<p class="muted"><a href="{a["url"]}" target="_blank" rel="noopener">原文链接</a></p></div></details>' for a in C['bc']))
    parts.append(h2('海德堡要理问答（1563）','📗','hc'))
    parts.append(f'<div class="card">{C["hc_intro"]}</div>')
    sec_of=lambda ld: '引言' if ld==1 else ('第一部 论人的罪和愁苦' if ld<=4 else ('第二部 论我们的得救' if ld<=31 else '第三部 论感恩'))
    cur=None
    for x in C['hc']:
        s=sec_of(x['ld'])
        if s!=cur: parts.append(h3('📘 '+s,'hc-'+str(x['ld']))); cur=s
        inner=''.join(f'<div class="qa"><div class="q"><span class="n">{i["q"]}</span><span>{esc(i["ques"])}</span></div><div class="a cbox">{i["html"]}</div></div>' for i in x['items'])
        parts.append(f'<details id="ld{x["ld"]}"><summary>主日 {x["ld"]}（第{x["items"][0]["q"]}–{x["items"][-1]["q"]}问）· {esc(x["items"][0]["ques"])}</summary><div class="dbody">{inner}<p class="muted"><a href="{x["url"]}" target="_blank" rel="noopener">原文链接</a></p></div></details>')
    parts.append(h2('多特信经（1618–1619）','📙','cd'))
    parts.append(f'<div class="card">{C["cd_intro"]}</div>')
    for s in C['cd']:
        parts.append(h3('📙 '+esc(s['title']),'cd-'+s['id']))
        if s['intro'].strip(): parts.append(f'<div class="card">{s["intro"]}</div>')
        parts.append(''.join(f'<details><summary>{esc(a["title"])}</summary><div class="dbody cbox">{a["html"]}<p class="muted"><a href="{a["url"]}" target="_blank" rel="noopener">原文链接</a></p></div></details>' for a in s['arts']))
    js='<script>window.__pageInit=function(){const b=document.getElementById("creedHide");let on=false;b.onclick=()=>{on=!on;document.body.classList.toggle("mode-hide",on)}}</script>'
    open(OUT+'creeds.html','w').write(page('creeds.html','三大普世信经与三项联合信条（原文）','\n'.join(parts),js=js))
if __name__=='__main__':
    build_wcf(); build_cat('wsc'); build_cat('wlc'); build_recite(); build_creeds(); print('docs ok')
