# -*- coding: utf-8 -*-
"""Build-time Mermaid → inline SVG (no runtime Mermaid on the page).
Renders with sentinel colours, then swaps them for CSS variables so the SVG follows every theme/palette.
Cache: data/mermaid_cache.json (keyed by source hash) – Playwright only needed when a diagram changes."""
import re, os, json, hashlib, html, glob, sys
HERE=os.path.dirname(os.path.abspath(__file__)); DOCS=os.path.join(HERE,'..','docs')
CACHE=os.path.join(HERE,'data','mermaid_cache.json')
VER='mm10.9.1-v6'
S={'tint':'#a10101','tint2':'#a20202','a1':'#a30303','a2':'#a40404','ink':'#a50505','card':'#a60606','line':'#a70707'}
for i in range(12): S[f's{i}']=f'#b{i:x}{i:x}1{i:x}1'.replace(' ','0')[:7]
for i in range(12): S[f'l{i}']=f'#c{i:x}{i:x}2{i:x}2'[:7]
TV=dict(darkMode=False,background=S['card'],primaryColor=S['tint'],primaryBorderColor=S['a1'],primaryTextColor=S['ink'],
 secondaryColor=S['tint2'],secondaryBorderColor=S['a2'],secondaryTextColor=S['ink'],tertiaryColor=S['card'],tertiaryBorderColor=S['a2'],tertiaryTextColor=S['ink'],
 lineColor=S['line'],textColor=S['ink'],mainBkg=S['tint'],nodeBorder=S['a1'],clusterBkg=S['tint2'],clusterBorder=S['a2'],titleColor=S['ink'],
 edgeLabelBackground=S['card'],nodeTextColor=S['ink'],fontSize='15px')
for i in range(12): TV[f'cScale{i}']=S[f's{i}']; TV[f'cScaleLabel{i}']=S[f'l{i}']; TV[f'cScalePeer{i}']=S['a1']
CFG=dict(startOnLoad=False,theme='base',securityLevel='strict',fontFamily='PingFang SC, Microsoft YaHei, Noto Sans SC, Noto Sans CJK SC, sans-serif',
 themeVariables=TV,flowchart=dict(useMaxWidth=True,htmlLabels=True,curve='basis',padding=18),mindmap=dict(useMaxWidth=True,padding=14))
RX=re.compile(r'<div class="mermaid"([^>]*)>(.*?)</div>',re.S)
def key(src): return hashlib.sha1((VER+src).encode()).hexdigest()[:16]
def themeify(svg):
    for k,v in S.items():
        svg=re.sub(re.escape(v),f'var(--mm-{k})',svg,flags=re.I)
    svg=svg.replace('#59f9f9','var(--mm-line)').replace('rgba(166, 6, 6, 0.5)','var(--mm-card)')
    svg=re.sub(r'rgb\(\d+\.\d+, ?\d+\.\d+, ?\d+\.\d+\)','var(--mm-line)',svg)
    svg=re.sub(r'hsl\([^)]*\)','var(--mm-a1)',svg)
    svg=re.sub(r'(section-root text\{fill:)var\(--mm-ink\)',r'\1#fff',svg)
    # presentation attributes cannot take var(): move to style
    svg=re.sub(r'\s(fill|stroke)="(var\(--mm-[a-z0-9]+\))"',lambda m:f' style="{m.group(1)}:{m.group(2)}"',svg)
    return svg

def prune_css(css,used):
    out=[];i=0;n=len(css)
    while i<n:
        j=css.find('{',i)
        if j<0: break
        sel=css[i:j].strip()
        if sel.startswith('@'):
            d=0;k=j
            while k<n:
                if css[k]=='{': d+=1
                elif css[k]=='}':
                    d-=1
                    if d==0: break
                k+=1
            out.append(css[i:k+1]); i=k+1; continue
        k=css.find('}',j); body=css[j:k+1]
        keep=[]
        for part in sel.split(','):
            cls=re.findall(r'\.([A-Za-z_][\w-]*)',part)
            if not cls or all(c in used for c in cls): keep.append(part.strip())
        if keep: out.append(','.join(keep)+body)
        i=k+1
    return ''.join(out)
def slim(svg):
    used=set()
    for m in re.finditer(r'class="([^"]*)"',svg): used|=set(m.group(1).split())
    svg=re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+prune_css(m.group(1),used)+'</style>',svg,count=1,flags=re.S)
    svg=re.sub(r'(\d+\.\d{2})\d+',r'\1',svg)
    return svg
def render(srcs):
    from playwright.sync_api import sync_playwright
    out={}
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'),args=['--no-sandbox']); pg=b.new_page(viewport={'width':1200,'height':900})
        pg.set_content('<html><body style="font-family:'+CFG['fontFamily']+'"></body></html>')
        pg.add_script_tag(path=os.path.join(DOCS,'assets','vendor','mermaid','mermaid.min.js'))
        pg.evaluate('c=>mermaid.initialize(c)',CFG)
        for k,src in srcs.items():
            svg=pg.evaluate('async([id,s])=>{const r=await mermaid.render(id,s);return r.svg}',['mmd-'+k,src])
            out[k]=slim(themeify(svg))
        b.close()
    return out
def main():
    cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    files=sorted(glob.glob(os.path.join(DOCS,'*.html'))); need={}; todo=[]
    for f in files:
        s=open(f).read()
        for m in RX.finditer(s):
            src=html.unescape(m.group(2)).strip(); k=key(src)
            if k not in cache: need[k]=src
        todo.append((f,s))
    if need: cache.update(render(need)); json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
    used=set(); n=0
    for f,s in todo:
        def rep(m):
            nonlocal n
            src=html.unescape(m.group(2)).strip(); k=key(src); used.add(k); n+=1
            svg=cache[k]
            mw=re.search(r'max-width:\s*([\d.]+)px',svg); w=float(mw.group(1)) if mw else 600
            wide=' data-wide' if w>560 else ''
            return f'<div class="mermaid mm-pre"{wide} style="--mmw:{min(w,760):.0f}px" data-done role="img" aria-label="{"思维导图" if src.startswith("mindmap") else "流程图"}">{svg}</div>'
        s2=RX.sub(rep,s)
        if s2!=s: open(f,'w').write(s2)
    for k in list(cache):
        if k not in used: del cache[k]
    json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
    left=set()
    for k in used: left|=set(re.findall(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\([^)]*\)',cache[k]))
    print('mermaid prerendered',n,'diagrams; rendered now',len(need),'; non-themed colours left:',sorted(left)[:30])
if __name__=='__main__': main()
