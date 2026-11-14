"""v3.3: build-time hierarchical outline (3 levels) for every page.
Scans the page body (including content parked in <template> for progressive hydration),
assigns ids where missing, numbers level-1 entries (一、二、…) in the page and the TOC,
and returns compact JSON [[level,id,label,num],...] that app.js renders as a collapsible tree."""
import re, json, html as H
CN='零一二三四五六七八九十'
def cnum(n):
    if n<=10: return CN[n]
    if n<20: return '十'+CN[n-10]
    return CN[n//10]+'十'+(CN[n%10] if n%10 else '')
LEVELS={'default':{'h2':1,'h3':2},
        'atlas.html':{'h2':2,'h4':3},
        'wcf.html':{'h2':2,'h3':3},
        'wlc.html':{'h2':2,'h3':3},
        'wsc.html':{'h2':2,'h3':3},
        'index.html':{'h2':2,'h3':3},'compare.html':{'h2':2,'h3':3},'memory.html':{'h2':2,'h3':3},
        'history.html':{'h2':1,'h3':2,'h4':3}}
OPEN=re.compile(r'<(h2|h3|h4|div|section|details|p|li|article)\b([^>]*)>')
def _label(raw):
    raw=re.sub(r'<(span|small) class="(?:muted|hn)[^"]*"[^>]*>.*?</\1>','',raw,flags=re.S)
    raw=re.sub(r'<button\b.*?</button>','',raw,flags=re.S)
    raw=re.sub(r'<sup\b.*?</sup>','',raw,flags=re.S)
    t=H.unescape(re.sub(r'<[^>]+>',' ',raw))
    t=re.sub(r'\s+',' ',t).strip()
    return t
def outline(fn, body):
    lv_of=LEVELS.get(fn,LEVELS['default'])
    items=[];edits=[];used=set(re.findall(r'\bid="([^"]+)"',body));n=0
    for m in OPEN.finditer(body):
        tag,attrs=m.group(1),m.group(2)
        d=re.search(r'\bdata-lv="(\d)"',attrs)
        if d: lv=int(d.group(1))
        elif tag in ('h2','h3','h4') and 'data-notoc' not in attrs:
            if tag=='h2' and not re.search(r'class="h\b',attrs): continue
            lv=lv_of.get(tag)
        else: continue
        if not lv: continue
        tm=re.search(r'\bdata-toc="([^"]*)"',attrs)
        if tm: label=H.unescape(tm.group(1))
        elif tag in ('h2','h3','h4'):
            e=body.find(f'</{tag}>',m.end()); label=_label(body[m.end():e])
        elif tag=='details':
            s=re.match(r'\s*<summary[^>]*>(.*?)</summary>',body[m.end():],re.S); label=_label(s.group(1)) if s else ''
        else:
            label=_label(body[m.end():m.end()+300])[:40]
        if not label: continue
        im=re.search(r'\bid="([^"]+)"',attrs)
        if im: id_=im.group(1)
        else:
            n+=1; id_=f't{n}'
            while id_ in used: n+=1; id_=f't{n}'
            used.add(id_); edits.append((m.start()+1+len(tag),f' id="{id_}"'))
        items.append([lv,id_,label,'',m.end(),tag,attrs])
    # numbering: level-1 -> 一、二…; level-2 -> 1, 2… inside its parent unless the labels already carry numbers
    k1=0;groups={};cur1=None
    for it in items:
        if it[0]==1: k1+=1; it[3]=cnum(k1); cur1=it[1]; groups[cur1]=[]
        elif it[0]==2 and cur1: groups[cur1].append(it)
    NUMRE=re.compile(r'^\W*(第|\d|Q\d|[一二三四五六七八九十]+[、.])')
    for g in groups.values():
        if g and not any(NUMRE.match(x[2]) for x in g):
            for i,x in enumerate(g,1): x[3]=str(i)
    for it in items:
        if it[0]==1 and (it[5] in ('h2',) or 'class="part' in it[6]):
            edits.append((it[4],f'<span class="hn" aria-hidden="true">{it[3]}</span>'))
    for pos,ins in sorted(edits,key=lambda e:-e[0]): body=body[:pos]+ins+body[pos:]
    data=[[a,b,c,d] if d else [a,b,c] for a,b,c,d,*_ in items]
    return body, json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
