# -*- coding: utf-8 -*-
"""v3.0 maps: (a) hand-drawn concept maps (static SVG land layer + animated HTML pins, works offline)
(b) live Leaflet maps (self-hosted Natural Earth base + keyless tile providers with failover; see app.js)"""
import json
import math
from common import mk
from common import esc
from geo import Proj, svg_land, svg_rivers
from content_atlas import CATCOL, CATNAME, CONFESSIONS, FAMNAME
VW=1000
def _w(s):  # approximate label width in viewBox units at the pessimistic reference (font 16.4u)
    f=16.4; return sum(f if ord(c)>0x2e80 else f*0.56 for c in s)
def _place_labels(pts,H=10000,extra=()):
    """greedy collision-avoiding label placement; pts: [(x,y,name,when)] -> ([dir|'x'], boxes). 'x' = no room: label hidden, number shown"""
    boxes=[(x-15,y-15,x+15,y+15) for x,y,_,_ in pts]+list(extra); dirs=[]
    def ov(a,b): return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    for i,(x,y,n,w) in enumerate(pts):
        bw=max(_w(n),_w(w)*0.8)+8; bh=36
        cands={'r':(x+16,y-bh/2,x+16+bw,y+bh/2),'l':(x-16-bw,y-bh/2,x-16,y+bh/2),'t':(x-bw/2,y-18-bh,x+bw/2,y-18),'b':(x-bw/2,y+18,x+bw/2,y+18+bh),
               'tr':(x+8,y-12-bh,x+8+bw,y-12),'br':(x+8,y+12,x+8+bw,y+12+bh),'tl':(x-8-bw,y-12-bh,x-8,y-12),'bl':(x-8-bw,y+12,x-8,y+12+bh)}
        best=None
        for d,bx in cands.items():
            pen=sum(ov(bx,o) for o in boxes)
            if bx[0]<4 or bx[2]>VW-4 or bx[1]<4 or bx[3]>H-4: pen+=50000
            if best is None or pen<best[0]: best=(pen,d,bx)
            if pen==0: break
        if best[0]>40: dirs.append('x')
        else: dirs.append(best[1]); boxes.append(best[2])
    return dirs,boxes
def _curve(x1,y1,x2,y2,bend=0.18):
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
    cx,cy=mx-dy/L*L*bend,my+dx/L*L*bend
    return f'M{x1:.1f},{y1:.1f}Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}',(0.25*x1+0.5*cx+0.25*x2,0.25*y1+0.5*cy+0.25*y2)
RIVERS={'eu':['Thames','Rhine','Seine','Loire','Rhône','Danube','Elbe'],'world':[]}
def concept(m):
    mid=m['id']; base=m['base']
    if base=='london':
        P=Proj(m['bbox'],VW); H=P.H; landd=''
        th=m['thames']; pts=[P(lng,lat) for lat,lng in th]
        ext=[(pts[0][0]+(pts[0][0]-pts[1][0])*4,pts[0][1]+(pts[0][1]-pts[1][1])*4)]+pts+[(pts[-1][0]+(pts[-1][0]-pts[-2][0])*4,pts[-1][1]+(pts[-1][1]-pts[-2][1])*4)]
        riv='M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in ext)
        # true-to-scale river width (~230 m at Westminster Bridge); 0.001° lng ≈ 69.4 m at 51.5°N
        rw=230/69.4*abs(P(-0.120,51.5)[0]-P(-0.121,51.5)[0])
        (rx1,ry1),(rx2,ry2)=pts[1],pts[2]; ang=math.degrees(math.atan2(ry2-ry1,rx2-rx1)); rmx,rmy=(rx1+rx2)/2,(ry1+ry2)/2
        # schematic Abbey footprint (west front by the Jerusalem Chamber -> Henry VII Chapel at the east end)
        a=P(-0.12875,51.49945); b=P(-0.12600,51.49905)
        extra=(f'<path class="cm-river big" style="stroke-width:{rw:.0f}px" d="{riv}"/><text class="cm-rvl" transform="translate({rmx:.0f} {rmy:.0f}) rotate({ang:.0f})" dy="7">泰晤士河 River Thames</text>'
               f'<g class="cm-bld"><path d="M{a[0]:.1f},{a[1]-9:.1f}L{b[0]:.1f},{b[1]-9:.1f}L{b[0]:.1f},{b[1]+9:.1f}L{a[0]:.1f},{a[1]+9:.1f}Z"/><path d="M{(a[0]+b[0])/2-8:.1f},{(a[1]+b[1])/2-40:.1f}h16v80h-16z"/></g>')
    else:
        P,landd=svg_land(m['bbox'],VW,res='50m' if base in ('eu','asia') else '110m',tol=0.7 if base in ('eu','asia') else 0.9)
        H=P.H; riv=svg_rivers(P,RIVERS.get(base,[])) if base=='eu' else ''
        extra=f'<path class="cm-river" d="{riv}"/>' if riv else ''
    ids={p[0]:p for p in m['places']}
    xy={p[0]:P(p[2],p[1]) for p in m['places']}
    # spread pins that sit on top of each other (schematic only; true positions are in the live map)
    ks=list(xy); D=34
    for _ in range(60):
        moved=False
        for i in range(len(ks)):
            for j in range(i+1,len(ks)):
                (ax,ay),(bx,by)=xy[ks[i]],xy[ks[j]]; dx,dy=bx-ax,by-ay; d=math.hypot(dx,dy)
                if d<D:
                    if d<1e-6: dx,dy,d=0.0,1.0,1.0
                    push=(D-d)/2+0.5; ux,uy=dx/d,dy/d
                    xy[ks[i]]=(ax-ux*push,ay-uy*push); xy[ks[j]]=(bx+ux*push,by+uy*push); moved=True
        if not moved: break
    xy={k:(min(VW-22,max(22,x)),min(H-22,max(22,y))) for k,(x,y) in xy.items()}
    # compass rose goes in the first corner that has no pins
    corners=[(VW-70,H-78),(80,H-78),(VW-70,92),(80,92)]
    rx,ry=next((c for c in corners if all(abs(x-c[0])>70 or abs(y-c[1])>80 for x,y in xy.values())),corners[0])
    dirs,taken=_place_labels([(xy[p[0]][0],xy[p[0]][1],p[3],p[4]) for p in m['places']],H,[(rx-55,ry-57,rx+55,ry+48)])
    taken=list(taken)
    def ov(a,b): return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])
    routes=''; rl=''
    for i,(a,b,lab,kind) in enumerate(m['routes']):
        (x1,y1),(x2,y2)=xy[a],xy[b]
        bend=0.16 if kind!='sea' else 0.22
        d,(lx,ly)=_curve(x1,y1,x2,y2,bend)
        if lab:  # route label only where it collides with nothing (else it lives in the timeline + live-map tooltip)
            L_=math.hypot(x2-x1,y2-y1) or 1; cx,cy=(x1+x2)/2-(y2-y1)*bend,(y1+y2)/2+(x2-x1)*bend; w=_w(lab)*0.98+10; ok=None
            for t in (0.5,0.38,0.62,0.28,0.72):
                qx=(1-t)**2*x1+2*(1-t)*t*cx+t*t*x2; qy=(1-t)**2*y1+2*(1-t)*t*cy+t*t*y2
                for oy in (-6,16):
                    bx=(qx-w/2,qy+oy-17,qx+w/2,qy+oy+4)
                    if bx[0]>4 and bx[2]<VW-4 and bx[1]>4 and bx[3]<H-4 and not any(ov(bx,o) for o in taken): ok=(qx,qy+oy,bx); break
                if ok: break
            if ok: taken.append(ok[2]); lx,ly=ok[0],ok[1]+6
            else: lab=''
        routes+=f'<path class="rt rt-{kind}" pathLength="1" style="--rd:{0.25+i*0.18:.2f}s" d="{d}" marker-end="url(#ah-{mid})"/>'
        rl+=(f'<text class="rtl" x="{lx:.0f}" y="{ly-6:.0f}">{esc(lab)}</text>') if lab else ''
    sea_cls='cm-seaf' if base!='london' else 'cm-paper'
    static=f'''<svg class="cm-base" viewBox="0 0 {VW} {H}" aria-hidden="true" focusable="false"><defs><filter id="rough-{mid}" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
<pattern id="wv-{mid}" width="46" height="22" patternUnits="userSpaceOnUse"><path d="M2 12q9-7 18 0t18 0" class="cm-wave"/></pattern></defs>
<rect class="{sea_cls}" width="{VW}" height="{H}"/>{f'<rect width="{VW}" height="{H}" fill="url(#wv-{mid})"/>' if base!='london' else ''}
{f'<g filter="url(#rough-{mid})"><path class="cm-shadow" d="{landd}" transform="translate(4 5)"/><path class="cm-land" d="{landd}"/></g>' if landd else ''}{extra}
<g class="cm-rose" transform="translate({rx} {ry})"><circle r="30"/><path d="M0-40L7 0L0 40L-7 0Z"/><path class="n" d="M0-40L7 0L-7 0Z"/><text y="-46">N</text></g></svg>'''
    over=f'''<svg class="cm-over" viewBox="0 0 {VW} {H}" aria-hidden="true" focusable="false"><defs><marker id="ah-{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ah"/></marker></defs>{routes}{rl}</svg>'''
    pins=''
    for i,p in enumerate(m['places']):
        k,lat,lng,name,when,icon,cat,desc=p; x,y=xy[k]
        pins+=(f'<button class="pin{' nolbl' if dirs[i]=='x' else ''}" type="button" data-i="{i}" style="left:{x/VW*100:.2f}%;top:{y/H*100:.2f}%;--c:{CATCOL[cat]};--pd:{0.2+i*0.07:.2f}s" aria-label="{esc(name)}，{esc(when)}">'
               f'<span class="pd">{icon}</span><span class="pn">{i+1}</span><span class="pl pl-{dirs[i]}"><b>{esc(name)}</b><small>{esc(when)}</small></span></button>')
    cats=[]
    for p in m['places']:
        if p[6] not in cats: cats.append(p[6])
    leg=''.join(f'<span><i style="background:{CATCOL[c]}"></i>{CATNAME[c]}</span>' for c in cats)
    wide=VW/H>2
    stage=f'<div class="cm-stage">{static}{over}<div class="cm-pins">{pins}</div></div>'
    if wide: stage=f'<div class="hscroll cm-wide" tabindex="0" aria-label="宽幅地图（可横向滚动）">{stage}</div>'
    return f'''<figure class="cmap" data-cmap="{mid}" style="--ar:{VW}/{H}">{stage}
<figcaption><span class="cm-leg">{leg}</span><span class="muted small">🎨 手绘示意图：海岸线据 Natural Earth（公有领域）自绘，<b>不画现代国界</b>；离线可用。点按地名查看说明。</span></figcaption></figure>'''
def mapblock(m, intro=True):
    mid=m['id']
    data={'base':m['base'],'view':m['view'],'places':[dict(k=p[0],lat=p[1],lng=p[2],n=p[3],w=p[4],i=p[5],c=CATCOL[p[6]],d=p[7]) for p in m['places']],
          'routes':[dict(a=a,b=b,l=l,k=k) for a,b,l,k in m['routes']]}
    if m.get('thames'): data['thames']=m['thames']
    tl=''.join(f'<li><b>{esc(y)}</b><span>{mk(esc(t))}</span></li>' for y,t in m['timeline'])
    pl=''.join(f'<li data-i="{i}"><span class="pn" style="--c:{CATCOL[p[6]]}">{i+1}</span><span class="pe">{p[5]}</span><b>{esc(p[3])}</b> <span class="hl-date">{esc(p[4])}</span><br><span class="muted">{mk(esc(p[7]))}</span></li>' for i,p in enumerate(m['places']))
    hdr=('维度','欧陆改革宗','长老会（西敏）') if mid=='geo' else ('维度','⚖️ 多特 1618–1619','🏛️ 西敏 1643–1649') if mid=='dortwm' else ('区域','教会与社会','文化与敬虔')
    cul='<div class="tbl rv"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in hdr)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{mk(esc(x))}</td>' for x in r)+'</tr>' for r in m['culture'])+'</tbody></table></div>'
    src='<details class="msrc"><summary>📚 本图事实来源（'+str(len(m['src']))+'）</summary><ul>'+''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n,u in m['src'])+'</ul></details>'
    return f'''<div class="mapbox" id="mb-{mid}">
{f'<p class="lead">{mk(esc(m["intro"]))}</p>' if intro else ''}
<div class="mtabs" role="tablist" aria-label="地图视图"><button role="tab" class="on" aria-selected="true" data-v="c">🎨 手绘示意图</button>{'<button role="tab" aria-selected="false" data-v="s">🎬 情景讲解</button>' if STORY.get(mid) else ''}<button role="tab" aria-selected="false" data-v="l">🛰️ 实景地图</button><button class="mplay" type="button" aria-label="按时间顺序播放">▶ 按时间播放</button></div>
<div class="mview mv-c on">{concept(m)}</div>
{f'<div class="mview mv-s">{SCENES[mid]() if mid in SCENES else ""}{story(mid,m["title"])}</div>' if STORY.get(mid) else ''}
<div class="mview mv-l"><div class="lmap" data-base="{m['base']}"></div><p class="muted small lcap">🛰️ <b>14 个免密钥地图源</b>（OpenStreetMap 及德国/法国镜像 · HOT · CyclOSM · OpenTopoMap · Esri · NASA · 高德），「⚡自动」先测速再选最快的一家，失败自动换下一家；全部不可用时显示本站自带的 <b>Natural Earth 离线底图</b>（永不失效）。右上角可手动切换来源、↻ 重新测速。高德地图采用 GCJ-02 坐标，切换到高德时标记会自动校正。</p></div>
<script type="application/json" class="mdata">{json.dumps(data,ensure_ascii=False,separators=(',',':'))}</script>
<div class="minfo" aria-live="polite"><span class="muted">👆 点按地图上的地点，或点「▶ 按时间播放」。</span></div>
<div class="grid g2 mside"><div class="card"><h4>📍 地点（按编号）</h4><ol class="mplaces">{pl}</ol></div><div class="card"><h4>⏳ 本图时间线</h4><ol class="mtl">{tl}</ol></div></div>
{('<h4 class="mcul">🏰 文化区域特征</h4>'+cul) if m['culture'] else ''}{src}
</div>'''
def confession_chart():
    """SVG dot-plot of real confession dates 1525–1650 (collision-free label lanes)"""
    y0,y1=1525,1650; W,H,C=1000,360,180; X=lambda y:40+(y-y0)/(y1-y0)*(W-80)
    placed=[]; out=[]
    for i,(y,n,f) in enumerate(CONFESSIONS):
        x=X(y); w=sum(15 if ord(c)>0x2e80 else 8.4 for c in n)+10
        choice=None
        for lane in range(4):
            for up in ((True,False) if i%2==0 else (False,True)):
                ly=(C-38-lane*38) if up else (C+52+lane*38)
                bx=(x-w/2,ly-34,x+w/2,ly+4)
                if not any(bx[0]<o[2] and o[0]<bx[2] and bx[1]<o[3] and o[1]<bx[3] for o in placed):
                    choice=(up,ly,bx);break
            if choice:break
        up,ly,bx=choice; placed.append(bx); col=FAMNAME[f][1]
        out.append(f'<g class="cf" style="--c:{col};--cd:{i*0.08:.2f}s"><line x1="{x:.1f}" y1="{C}" x2="{x:.1f}" y2="{ly+8 if up else ly-36:.0f}"/><circle cx="{x:.1f}" cy="{C}" r="7"/><text x="{x:.1f}" y="{ly:.0f}" text-anchor="middle">{n}</text><text class="cy" x="{x:.1f}" y="{ly-18:.0f}" text-anchor="middle">{y}</text></g>')
    ticks=''.join(f'<g class="tk"><line x1="{X(t):.1f}" y1="{C-5}" x2="{X(t):.1f}" y2="{C+5}"/><text x="{X(t):.1f}" y="{C+21}" text-anchor="middle">{t}</text></g>' for t in range(1530,1651,20))
    leg=''.join(f'<span><i style="background:{c}"></i>{n}</span>' for k,(n,c) in FAMNAME.items())
    return f'''<figure class="cfchart rv"><div class="hscroll"><svg viewBox="0 0 {W} {H}" role="img" aria-label="宗教改革时期主要信条年代图"><line class="ax" x1="30" y1="{C}" x2="{W-30}" y2="{C}"/>{ticks}{''.join(out)}</svg></div><figcaption class="cm-leg">{leg}</figcaption></figure>'''
# ---------------- v3.2 情景讲解图 ----------------
from content_v32 import STORY
def story(mid,title=''):
    beats=STORY.get(mid)
    if not beats: return ''
    lis=''.join(f'<li style="--i:{i}"><span class="st-n">{i+1}</span><span class="st-ic" aria-hidden="true">{ic}</span><span class="st-y">{esc(y)}</span><b>{esc(h)}</b><span class="st-t">{mk(esc(t))}</span></li>' for i,(ic,y,h,t) in enumerate(beats))
    return f'<figure class="story" aria-label="情景讲解：{esc(title)}"><ol class="st-reel" style="--n:{len(beats)}">{lis}</ol><div class="st-bar" aria-hidden="true"><i></i></div><figcaption class="muted small">🎬 {len(beats)} 个镜头讲完这张图 · 自动轮播（离开屏幕即暂停），点任一镜头可定格</figcaption></figure>'
def _t(x,y,s,cls='',anchor='middle',extra=''):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'
def scene_brit():
    """三王国关系：王权 vs 盟约；1643 英苏结盟"""
    K=[('苏格兰','🏴',330,92,'sco','1637 祈祷书骚乱','1638 国民圣约'),('英格兰','🏛️',470,300,'eng','1642 内战爆发','1643 西敏会议'),('爱尔兰','☘️',150,300,'ire','1641 叛乱','1642 苏格兰军登陆阿尔斯特')]
    g=''
    for n,ic,x,y,c,a,b in K:
        g+=f'<g class="sc-k sc-{c}"><circle cx="{x}" cy="{y}" r="74"/>{_t(x,y-14,ic,"sc-ic")}{_t(x,y+20,n,"sc-h")}{_t(x,y+46,a,"sc-s")}{_t(x,y+68,b,"sc-s")}</g>'
    crown='<g class="sc-crown"><circle cx="320" cy="222" r="38"/>'+_t(320,218,'👑','sc-ic')+_t(320,246,'查理一世','sc-s2')+'</g>'
    arrows=('<path class="sc-ar sc-bad" pathLength="1" d="M300 188Q300 160 318 168"/><path class="sc-ar sc-bad" pathLength="1" d="M356 238Q392 262 404 272"/><path class="sc-ar sc-bad" pathLength="1" d="M284 236Q240 262 222 272"/>'
            '<path class="sc-link" d="M392 132Q520 190 498 232"/>'+_t(560,170,'1643 庄严联盟与圣约','sc-lk','middle'))
    goal='<g class="sc-goal"><rect x="30" y="396" width="580" height="54" rx="14"/>'+_t(320,430,'🎯 目标：三国在 信仰告白 · 教会治理 · 敬拜 · 要理问答 上统一','sc-gt')+'</g>'
    return f'<figure class="scene sc-brit"><div class="sc-wrap hscroll" tabindex="0" aria-label="情景图（窄屏可横向滑动）"><svg viewBox="0 0 640 464" role="img" aria-label="三王国关系示意：王权强推礼仪，苏格兰与英格兰国会结盟，目标是三国宗教统一">{arrows}{g}{crown}{goal}</svg></div><figcaption class="muted small">🎭 情景图：红色箭头＝王权施压与冲突；金色连线＝1643年英格兰国会与苏格兰结盟。</figcaption></figure>'
def scene_london():
    """文件诞生流水线"""
    S=[('🗂️','委员会起草','分组起草初稿'),('🗣️','全体辩论','逐条、逐句辩论'),('📖','附上经文','国会要求附经文'),('🏛️','呈交国会','送往隔壁国会'),('🏴','苏格兰批准','1647 / 1648 总会')]
    w=124; g=''
    for i,(ic,h,s) in enumerate(S):
        x=20+i*w
        g+=f'<g class="sc-st" style="--i:{i}"><rect x="{x}" y="60" width="{w-16}" height="150" rx="16"/>{_t(x+(w-16)/2,108,ic,"sc-ic")}{_t(x+(w-16)/2,148,h,"sc-h2")}{_t(x+(w-16)/2,176,s,"sc-s")}</g>'
        if i<len(S)-1: g+=f'<path class="sc-arrow" d="M{x+w-14} 135h12"/>'
    doc='<g class="sc-doc"><rect x="-14" y="-18" width="28" height="36" rx="4"/><path d="M-8-8h16M-8 0h16M-8 8h10"/></g>'
    return f'<figure class="scene sc-london"><div class="sc-wrap hscroll" tabindex="0" aria-label="情景图（窄屏可横向滑动）"><svg viewBox="0 0 640 250" role="img" aria-label="西敏文件的产生流程：委员会起草、全体辩论、附经文、呈交国会、苏格兰总会批准">{_t(320,34,"一份文件是怎样诞生的（1643–1648）","sc-title")}{g}<g class="sc-mv">{doc}</g></svg></div><figcaption class="muted small">📄 动画：文件从起草一路走到苏格兰总会批准。信仰告白1646年12月完成、1647年附经文；苏格兰总会1647年8月批准；大小要理问答1648年批准。</figcaption></figure>'
def scene_dortwm():
    """两个会议的结构：国际 vs 三国"""
    L=[('英格兰',-90),('苏格兰',-52),('普法尔茨',-14),('黑森',24),('拿骚',62),('不来梅',100),('瑞士',138),('日内瓦',176),('法国 ✕',214)]
    cx,cy,R=168,236,100; g=''
    for i,(n,a) in enumerate(L):
        import math as _m
        x=cx+R*_m.cos(_m.radians(a)); y=cy+R*_m.sin(_m.radians(a)); miss='✕' in n
        g+=f'<path class="sc-sp{" miss" if miss else ""}" pathLength="1" style="--i:{i}" d="M{x:.0f} {y:.0f}L{cx} {cy}"/><g class="sc-nd{" miss" if miss else ""}" style="--i:{i}"><circle cx="{x:.0f}" cy="{y:.0f}" r="9"/>{_t(round(x+(14 if x>=cx else -14)),round(y+6),n,"sc-s3","start" if x>=cx else "end")}</g>'
    left=f'<g>{g}<circle class="sc-hub" cx="{cx}" cy="{cy}" r="44"/>{_t(cx,cy-4,"⚖️ 多特","sc-h2")}{_t(cx,cy+20,"1618–1619","sc-s")}</g>'
    rx=482
    right=(f'<g class="sc-r"><circle class="sc-hub wa" cx="{rx}" cy="230" r="50"/>{_t(rx,226,"🏛️ 西敏","sc-h2")}{_t(rx,250,"1643–1649","sc-s")}'
           f'<g class="sc-box b1"><rect x="{rx-90}" y="66" width="180" height="56" rx="12"/>{_t(rx,92,"英格兰神学家","sc-h3")}{_t(rx,113,"最多121位牧师（投票）","sc-s")}</g><path class="sc-sp2" pathLength="1" d="M{rx} 122V180"/>'
           f'<g class="sc-box b2"><rect x="{rx-90}" y="338" width="180" height="56" rx="12"/>{_t(rx,364,"国会议员 30 位","sc-h3")}{_t(rx,385,"上院10 · 下院20（列席）","sc-s")}</g><path class="sc-sp2" pathLength="1" d="M{rx} 338V280"/>'
                      f'<path class="sc-sp2 sco" pathLength="1" d="M{rx+100} 196Q{rx+80} 214 {rx+50} 222"/><g class="sc-box b4"><rect x="{rx+52}" y="152" width="96" height="44" rx="12"/>{_t(rx+100,180,"苏格兰专员","sc-s3")}</g></g>')
    mid=f'<line class="sc-div" x1="345" y1="56" x2="345" y2="420"/>{_t(172,40,"国际性：各国教会来「会诊」","sc-title")}{_t(490,40,"三国性：国会召集、苏格兰参与","sc-title")}'
    return f'<figure class="scene sc-dortwm"><div class="sc-wrap sc-panels"><svg viewBox="0 18 345 412" role="img" aria-label="多特大会的组成：各国代表">{_t(172,40,"国际性：各国教会来「会诊」","sc-title")}{left}</svg><svg viewBox="345 18 295 412" role="img" aria-label="西敏会议的组成：英格兰神学家、国会议员、苏格兰专员">{_t(490,40,"三国性：国会召集、苏格兰参与","sc-title")}{right}</svg></div><figcaption class="muted small">🧩 结构图：多特的外国代表来自英格兰、苏格兰、普法尔茨、黑森、拿骚、不来梅、瑞士各城与日内瓦；法国代表被国王禁止出境。西敏的苏格兰专员不投票，以本国教会专员身份参与。</figcaption></figure>'
SCENES={'brit':scene_brit,'london':scene_london,'dortwm':scene_dortwm}
