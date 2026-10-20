# -*- coding: utf-8 -*-
import html, re, json
VERSION='v1.0'; DATE='2026-10-20'
SITE_TITLE='威斯敏斯特标准 · 深度学习站'
PAGES=[('index.html','🏠','总览'),('history.html','🗺️','历史·地理'),('wcf.html','📘','信仰告白'),('wlc.html','📗','大要理问答'),('wsc.html','📙','小要理问答'),('compare.html','⚖️','深度对比'),('recite.html','🎙️','背诵版'),('memory.html','🧠','记忆训练'),('creeds.html','📜','信经与联合信条'),('sources.html','🔗','来源')]
CATS={'rev':('启示论','📖'),'god':('神论','✨'),'man':('人论·罪','💔'),'cov':('圣约','🤝'),'chr':('基督论','✝️'),'sal':('救恩论','🌱'),'law':('律法·伦理·敬拜','📜'),'chu':('教会·圣礼','⛪'),'end':('末世论','🌅')}
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
def page(fn,title,body,head='',js='',desc=''):
    nav=''.join(f'<a href="{p}" class="{"on" if p==fn else ""}">{i} {t}</a>' for p,i,t in PAGES)
    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)} | {SITE_TITLE}</title>
<meta name="description" content="{esc(desc or '《威斯敏斯特信仰告白》《大要理问答》《小要理问答》全文与深度解读：历史时间线、故事线、地图、圣经神学、圣约神学、欧陆改革宗对照、背诵与记忆训练。')}">
<meta name="theme-color" content="#3b5bdb">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📘</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={VERSION}">
{head}
</head>
<body>
<div class="backdrop"><i></i><i></i><i></i></div>
<header class="topbar">
  <button class="iconbtn" id="tocBtn" title="显示/隐藏目录" aria-label="目录">☰</button>
  <a class="brand" href="index.html"><span class="logo">W</span><span class="t">西敏标准·GROKstudy</span></a>
  <nav class="topnav">{nav}</nav>
  <button class="iconbtn" id="themeBtn" title="切换深色/浅色" aria-label="主题">🌙</button>
</header>
<div class="progress"></div>
<div class="scrim"></div>
<div class="layout">
  <aside class="toc" aria-label="目录">
    <h4>📑 本页目录</h4>
    <input id="tocFilter" type="search" placeholder="筛选目录…">
    <ol id="tocList"></ol>
  </aside>
  <main><div class="wrap">
{body}
<footer class="foot">
  <div><b>西敏标准 · 深度学习站</b>（Westminster-Standards-{DATE.replace('-','')}-{VERSION}-GROKstudy）</div>
  <div>西敏三份文件中文正文：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024 RTF-USA，免费分发）。三大普世信经与三项联合信条原文：<a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（中国改革宗教会《敬拜手册》）。解读、图表、记忆法为本站学习整理，仅供学习，不代表任何教会的官方解释。</div>
  <div class="muted">版本 {VERSION} · 更新于 {DATE}（台北时间） · <a href="sources.html">来源与致谢</a></div>
</footer>
  </div></main>
</div>
<button class="iconbtn totop" title="回到顶部">⬆️</button>
<script src="assets/js/app.js?v={VERSION}"></script>
{js}
</body></html>'''
MERMAID_JS='<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>'
def h2(t,icon,id=None,toc=None):
    return f'<h2 class="h rv"{f" id={chr(34)}{id}{chr(34)}" if id else ""}{f" data-toc={chr(34)}{esc(toc)}{chr(34)}" if toc else ""}><span class="ic">{icon}</span><span>{t}</span></h2>'
def h3(t,id=None,toc=None):
    return f'<h3 class="h"{f" id={chr(34)}{id}{chr(34)}" if id else ""}{f" data-toc={chr(34)}{esc(toc)}{chr(34)}" if toc else ""}>{t}</h3>'
def callout(kind,label,content):
    return f'<div class="callout {kind}"><b class="lbl">{label}</b>{content}</div>'
