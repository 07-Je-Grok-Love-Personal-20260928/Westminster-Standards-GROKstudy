# -*- coding: utf-8 -*-
import html, re, json
VERSION='v2.0'; DATE='2026-10-21'
SITE_TITLE='威斯敏斯特标准 · 深度学习站'
PAGES=[('index.html','🏠','总览'),('history.html','🗺️','历史·地理'),('wcf.html','📘','信仰告白'),('wlc.html','📗','大要理问答'),('wsc.html','📙','小要理问答'),('compare.html','⚖️','深度对比'),('recite.html','🎙️','背诵版'),('memory.html','🧠','记忆训练'),('creeds.html','📜','信经与联合信条'),('sources.html','🔗','来源')]
CATS={'rev':('启示论','📖'),'god':('神论','✨'),'man':('人论·罪','💔'),'cov':('圣约','🤝'),'chr':('基督论','✝️'),'sal':('救恩论','🌱'),'law':('律法·伦理·敬拜','📜'),'chu':('教会·圣礼','⛪'),'end':('末世论','🌅')}
PALETTES=[('aurora','晨曦','#4f46e5','#9333ea','#f59e0b'),('jade','翡翠','#059669','#0d9488','#84cc16'),('crimson','绛红金','#b91c1c','#9a3412','#ca8a04'),('ocean','深海','#0369a1','#4338ca','#06b6d4'),('sunset','暮光','#e11d48','#f97316','#a855f7')]
esc=lambda s: html.escape(str(s),quote=True)
def fmt(t):
    t=esc(t)
    return re.sub(r'⟦(\d+)⟧',r'<sup class="fn">\1</sup>',t)
def refs_html(refs):
    if not refs: return ''
    ks=sorted(refs,key=lambda k:int(re.sub(r'\D','',k) or 0))
    return '<div class="refs">📎 '+'；'.join(f'<b>{esc(k)}</b> {esc(refs[k].strip().rstrip("。；;，, "))}' for k in ks)+'</div>'
def legend():
    return '<div class="legend">'+''.join(f'<span class="tag t-{k}">{v[1]} {v[0]}</span>' for k,v in CATS.items())+'</div>'
# ---------- note-marking system ----------
TERMS=['行为之约','恩典之约','救赎之约','生命之约','有效呼召','有效恩召','称义','成圣','收养','归算','预定','拣选','越过','护理','普遍恩典','规范原则','安息日','主日','主动顺服','被动顺服','中保','圣礼','三一','位格','正典','以经解经','全然败坏','原罪','本罪','坚忍','确据','道德律','礼仪律','司法律','基督徒自由','有形教会','无形教会','与基督联合','蒙恩之道','三职','降卑','升高','重生','悔改','信心','律法三用','属灵临在','化质说','天国的钥匙','预表','圣约','次因','形像','十诫','主祷文','救赎历史']
TERMS.sort(key=len,reverse=True)
BOOKS='创出利民申书士得撒王代拉尼斯伯诗箴传歌赛耶哀结但何珥摩俄拿弥鸿哈番该亚玛太可路约徒罗林加弗腓西帖提多门来雅彼犹启'
BIB=re.compile(r'(?<![\u4e00-\u9fff])((?:撒[上下]|王[上下]|代[上下]|林[前后]|帖[前后]|提[前后]|彼[前后]|约[壹贰叁一二三]|['+BOOKS+r'])\d+(?::\d+(?:[-–]\d+)?(?:,\d+)?)?(?:[-–]\d+)?(?:[；;，,]\s*\d+:\d+(?:[-–]\d+)?)*)(?=[^\d:]|$)')
REF=re.compile(r'((?:WCF|WLC|WSC|HC|BC|CD)\s?[0-9IV][0-9IV./–\-, ]*[0-9IV])')
CMP=re.compile(r'([^。；<>]*(?:侧重|不同|差异|区别|相比|而西敏|更突出|更强调|更系统|更个人)[^。；<>]*)')
def mk(s, cmp=False):
    """apply the documented marking system to commentary html (not to source texts)"""
    s=s.replace('<span class="hard">','<span class="u-err">').replace('<span class="key">','<span class="c-term">')
    out=[]; depth=0; used=set()
    for tok in re.split(r'(<[^>]+>)',s):
        if tok.startswith('<'):
            t=tok[1:].split()[0].rstrip('>') if len(tok)>2 else ''
            if t in ('a','mark','span','b','sup','summary','code'): depth+=1
            elif t in ('/a','/mark','/span','/b','/sup','/summary','/code'): depth=max(0,depth-1)
            out.append(tok); continue
        if depth==0 and tok:
            tok=BIB.sub(lambda m:f'<span class="u-bib">{m.group(1)}</span>' if re.search(r'\d',m.group(1)) and (':' in m.group(1) or len(m.group(1))<=6) else m.group(1),tok)
            tok=REF.sub(r'<span class="c-ref">\1</span>',tok)
            def term(m):
                w=m.group(0)
                if w in used: return w
                used.add(w); return f'<span class="c-term">{w}</span>'
            # only in plain segments (avoid inside newly inserted spans)
            parts=re.split(r'(<span class="(?:u-bib|c-ref)">.*?</span>)',tok)
            tok=''.join(p if p.startswith('<span') else re.sub('|'.join(map(re.escape,TERMS)),term,p) for p in parts)
            if cmp:
                parts=re.split(r'(<[^>]+>)',tok)
                tok=''.join(p if p.startswith('<') else CMP.sub(lambda m:f'<span class="u-cmp">{m.group(1)}</span>' if len(m.group(1))>5 else m.group(1),p) for p in parts)
        out.append(tok)
    return ''.join(out)
BOOT='''<script>(function(){try{var d=document.documentElement,g=function(k){var v=localStorage.getItem('wsg_'+k);return v?JSON.parse(v):null};var m=g('mode')||'auto';var t=m==='auto'?(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'):m;d.dataset.theme=t;d.dataset.palette=g('palette')||'aurora';if(g('motion')==='off')d.classList.add('no-motion');}catch(e){}})();</script>'''
def page(fn,title,body,head='',js='',desc=''):
    nav=''.join(f'<a href="{p}" class="{"on" if p==fn else ""}"><span class="ni">{i}</span>{t}</a>' for p,i,t in PAGES)
    sw=''.join(f'<button class="sw" data-pal="{k}" title="{n}" style="--s1:{a};--s2:{b};--s3:{c}"><i></i><span>{n}</span></button>' for k,n,a,b,c in PALETTES)
    from content_v2 import LEGEND, CALLOUTS
    lg=''.join(f'<li><span class="lgx">{a}</span><span>{b}</span></li>' for a,b in LEGEND)
    lc=''.join(f'<li><span class="lgc {k}">{i}</span><span>{n}</span></li>' for k,i,n in CALLOUTS)
    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="light" data-palette="aurora">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)} | {SITE_TITLE}</title>
<meta name="description" content="{esc(desc or '《威斯敏斯特信仰告白》《大要理问答》《小要理问答》全文与深度解读：历史时间线、故事线、地图、圣经神学、圣约神学、欧陆改革宗与长老会正统视角、背诵与记忆训练。')}">
<meta name="theme-color" content="#4f46e5">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📘</text></svg>">
{BOOT}
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="assets/css/style.css?v={VERSION}">
{head}
<script src="assets/js/app.js?v={VERSION}" defer></script>
</head>
<body>
<div class="backdrop" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="topbar">
  <button class="iconbtn" id="tocBtn" title="显示/隐藏目录" aria-label="目录">☰</button>
  <a class="brand" href="index.html"><span class="logo">W</span><span class="t">西敏标准·GROKstudy</span></a>
  <nav class="topnav">{nav}</nav>
  <button class="iconbtn" id="legendBtn" title="标注图例" aria-label="标注图例">🖍️</button>
  <button class="iconbtn" id="themeBtn" title="主题与显示" aria-label="主题">🎨</button>
</header>
<div class="progress"><i></i></div>
<div class="scrim"></div>
<div class="pop" id="themePanel" role="dialog" aria-label="主题">
  <h4>🎨 配色主题</h4><div class="swatches">{sw}</div>
  <h4>🌗 明暗</h4><div class="seg" id="modeSeg"><button data-mode="light">☀️ 浅色</button><button data-mode="dark">🌙 深色</button><button data-mode="auto">🖥️ 跟随系统</button></div>
  <h4>⚙️ 体验</h4><div class="seg" id="optSeg"><button data-opt="smooth">🪶 丝滑滚动</button><button data-opt="motion">✨ 动画</button></div>
  <p class="muted small">设置保存在本机浏览器。丝滑滚动仅在电脑（鼠标滚轮）上启用，手机使用原生滚动。</p>
</div>
<div class="pop" id="legendPanel" role="dialog" aria-label="标注图例">
  <h4>🖍️ 标注系统（全站统一）</h4><ul class="lglist">{lg}</ul>
  <h4>🧩 提示框</h4><ul class="lglist two">{lc}</ul>
</div>
<div class="layout">
  <aside class="toc" aria-label="目录">
    <h4>📑 本页目录</h4>
    <input id="tocFilter" type="search" placeholder="筛选目录…">
    <ol id="tocList"></ol>
  </aside>
  <main><div class="wrap">
{body}
<footer class="foot">
  <div><b>西敏标准 · 深度学习站</b>（威斯敏斯特标准-{DATE.replace('-','')}-{VERSION}-GROKstudy）</div>
  <div>西敏三份文件中文正文：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024 RTF-USA，免费分发）。三大普世信经与三项联合信条原文：<a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（中国改革宗教会《敬拜手册》）。解读、图表、记忆法为本站学习整理，仅供学习，不代表任何教会的官方解释。</div>
  <div class="muted">版本 {VERSION} · 更新于 {DATE}（台北时间） · <a href="sources.html">来源与致谢</a> · <a href="https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy" target="_blank" rel="noopener">源码</a></div>
</footer>
  </div></main>
</div>
<button class="iconbtn totop" title="回到顶部" aria-label="回到顶部">⬆️</button>
{js}
</body></html>'''
MERMAID_JS=''   # mermaid is lazy-loaded by app.js when a diagram scrolls near the viewport
def h2(t,icon,id=None,toc=None):
    return f'<h2 class="h rv"{f" id={chr(34)}{id}{chr(34)}" if id else ""}{f" data-toc={chr(34)}{esc(toc)}{chr(34)}" if toc else ""}><span class="ic">{icon}</span><span>{t}</span></h2>'
def h3(t,id=None,toc=None):
    return f'<h3 class="h"{f" id={chr(34)}{id}{chr(34)}" if id else ""}{f" data-toc={chr(34)}{esc(toc)}{chr(34)}" if toc else ""}>{t}</h3>'
def callout(kind,label,content,raw=False):
    return f'<div class="callout {kind}"><b class="lbl">{label}</b>{content if raw else mk(content, cmp=kind in ("eu-pt","pr-pt"))}</div>'
def tabs(items,uid):
    """items: list of (kind,label,html) -> accessible tab panel (CSS-only fallback shows all)"""
    btns=''.join(f'<button role="tab" class="tb {k}{" on" if i==0 else ""}" aria-selected="{"true" if i==0 else "false"}" data-i="{i}">{l}</button>' for i,(k,l,h) in enumerate(items))
    pans=''.join(f'<div role="tabpanel" class="tp callout {k}{" on" if i==0 else ""}" data-i="{i}"><b class="lbl">{l}</b>{h}</div>' for i,(k,l,h) in enumerate(items))
    return f'<div class="tabs" id="{uid}"><div class="tbar" role="tablist">{btns}</div>{pans}</div>'
def bars(rows,unit='',maxv=None,cls=''):
    """rows: (label,value,color,href) -> animated CSS bar chart (real data)"""
    mx=maxv or max(v for _,v,_,_ in rows)
    return '<div class="bars '+cls+'">'+''.join(f'<a class="bar" {f"href={chr(34)}{h}{chr(34)}" if h else ""} style="--w:{v/mx:.4f};--c:{c}"><span class="bl">{l}</span><span class="bt"><i></i></span><span class="bv">{v}{unit}</span></a>' for l,v,c,h in rows)+'</div>'
def donut(parts,center,sub=''):
    """parts: (label,value,color) -> conic-gradient donut with legend"""
    tot=sum(v for _,v,_ in parts); acc=0; segs=[]
    for l,v,c in parts:
        segs.append(f'{c} {acc/tot*360:.1f}deg {(acc+v)/tot*360:.1f}deg'); acc+=v
    lg=''.join(f'<li><i style="background:{c}"></i>{l}<b>{v}</b></li>' for l,v,c in parts)
    return f'<div class="donut rv"><div class="ring" style="background:conic-gradient({",".join(segs)})"><div class="hole"><b>{center}</b><small>{sub}</small></div></div><ul>{lg}</ul></div>'
