# -*- coding: utf-8 -*-
"""v3.2 visual modules: covenant river (animated), three-density comparison (verbatim texts from standards.json), six-act story reel."""
import json, re, os
from common import esc, mk, tabs
HERE=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(HERE,'data','standards.json')))
_st=lambda t:re.sub(r'⟦\d+⟧','',t)
RIVER=[('🕊️','永恒','救赎之约','父与子（WCF 8.1）'),('🌳','创1–2','创造 · 行为之约','亚当为代表元首（WCF 7.2）'),('🍎','创3','堕落','全人类在亚当里（WCF 6）'),
       ('🐍','创3:15','第一福音','恩典之约首次宣告（WCF 7.3）'),('🌈','创9','挪亚','保存世界的舞台'),('⭐','创17','亚伯拉罕','“作你和你后裔的神”'),
       ('⛰️','出19–24','摩西','律法 · 献祭 · 预表'),('👑','撒下7','大卫','永远的王位'),('📜','耶31','新约应许','新心 · 赦罪'),
       ('✝️','福音书','基督','约的中保（WCF 8）'),('🔥','徒2','教会','圣灵施行救恩'),('🌅','启21–22','新天新地','约的完全成全')]
def river():
    li=''.join(f'<li style="--i:{i}"{" class=\"hub\"" if ic=="✝️" else ""}><span class="rvx-ic" aria-hidden="true">{ic}</span><span class="rvx-y">{esc(y)}</span><b>{esc(h)}</b><small>{mk(esc(t))}</small></li>' for i,(ic,y,h,t) in enumerate(RIVER))
    return (f'<figure class="rvx rv scene" aria-label="救赎历史之河：一个恩典之约的展开"><div class="rvx-line" aria-hidden="true"><i></i></div><ol>{li}</ol>'
            '<figcaption><span class="rvx-k"><i class="k1"></i>律法时期的施行（应许 · 预言 · 献祭 · 割礼 · 逾越节）</span><span class="rvx-k"><i class="k2"></i>福音时期的施行（圣道 · 洗礼 · 圣餐）</span>'
            '<span class="muted small">🌊 动态图：光点沿着救赎历史流动；<b>一个恩典之约、两个施行时期</b>（WCF 7.5–7.6），在基督里汇合。</span></figcaption></figure>')
TOPICS=[('称义','📜',(11,1),70,33,['WCF 用连续的「不是……而是」划清界线：不是灌输的义，不是信心本身或信靠之举算为义，而是基督的顺服与满足。','WLC 把称义拆成三个动作：赦免、接纳、算为义；并点明归算的是基督「完全的顺服和完全的满足」。','WSC 只保留骨架：恩典 · 赦罪 · 算为义 · 归算基督的义 · 唯独信心。']),
        ('恩典之约','🤝',(7,3),32,20,['WCF 给出定义：白白赐生命与救恩，要求信心，并应许圣灵使人「愿意并能够」相信。','WLC 补上中保与顺服的位置：顺服是信仰的证据、对神的感恩、得救的道路。','WSC 从牧养的问题切入（「神是否听任全人类灭亡？」），以拣选为源头。']),
        ('成圣','🌱',(13,1),75,35,['WCF 描写过程：罪的辖制被摧毁、情欲渐被治死、恩典越来越刚强。','WLC 从永恒拣选讲到「悔改得生的种子」被放入心中。','WSC 一句话：照神形像更新全人，越来越向罪死、向义活。']),
        ('神是谁','✨',(2,1),7,4,['WCF 并列属性与作为：既「极其慈爱」，又「决不为有罪的人开脱」。','WLC 展开完整的属性清单（全然充足、无所不在、不可测度……）。','WSC 把属性收成一个可背的公式：七项属性 × 「无限 · 永恒 · 不变」。']),
        ('得救的信心','🙌',(14,2),72,86,['WCF 讲信心如何对待全部圣经：对命令顺从、对警戒战兢、对应许欢喜。','WLC 讲信心的发生：先看见罪与苦难、自知无力，再接受并倚靠基督。','WSC 最短的定义：单单接受祂、依靠祂而得救。'])]
def density():
    items=[]
    for name,ic,(c,s),lq,sq,notes in TOPICS:
        wt=_st(D['wcf'][c-1]['secs'][s-1]['text']); wt=re.sub(r'^[一二三四五六七八九十]+、','',wt)
        lu=D['wlc'][lq-1]; su=D['wsc'][sq-1]
        cols=[('📘','WCF',f'{c}.{s}',f'wcf.html#c{c}',wt,'',notes[0],'var(--a1)'),('📗','WLC',str(lq),f'wlc.html#q{lq}',_st(lu['ans']),lu['ques'],notes[1],'var(--a2)'),('📙','WSC',str(sq),f'wsc.html#q{sq}',_st(su['ans']),su['ques'],notes[2],'var(--a3)')]
        mx=max(len(x[4]) for x in cols)
        h='<div class="dens">'+''.join(f'<div class="dn" style="--c:{col}"><div class="dn-h"><span>{e} <b>{d} {r}</b></span><a class="c-ref" href="{href}">原文 →</a></div><div class="dn-bar" title="{len(t)} 字"><i style="--w:{len(t)/mx:.3f}"></i><em>{len(t)} 字</em></div>'
                                     +(f'<p class="dn-q">{esc(q)}</p>' if q else '')+f'<p class="dn-t q-src">“{esc(t)}”</p><p class="dn-n">🔎 {mk(esc(n))}</p></div>' for e,d,r,href,t,q,n,col in cols)+'</div>'
        items.append(('key-pt',f'{ic} {name}',h))
    return tabs(items,'dens')+'<p class="muted small">引文逐字取自本站正文（RTF-USA 简体中文新版），去掉了经文脚注编号；字数为该段中文字符数。🔎 行为本站的阅读提示，不是原文。</p>'
ACTS=[('⛈️','1625–1640','风暴前夜','祈祷书骚乱 → 国民圣约 → 主教战争'),('⚔️','1640–1643','国会与战争','长期国会召集神学家会议'),('🤝','1643','盟约','庄严联盟与圣约：三国统一'),
      ('🕯️','1643–1647','耶路撒冷厅','长老派、独立派、伊拉斯都派辩论'),('📘','1646–1648','文件诞生','信条与大小要理问答完成、获苏格兰批准'),('🌍','1649–今天','走向世界','苏格兰 → 北美 → 亚洲')]
def acts_reel():
    lis=''.join(f'<li style="--i:{i}"><span class="st-n">{i+1}</span><span class="st-ic" aria-hidden="true">{ic}</span><span class="st-y">{esc(y)}</span><b>{esc(h)}</b><span class="st-t">{esc(t)}</span></li>' for i,(ic,y,h,t) in enumerate(ACTS))
    return f'<figure class="story" aria-label="六幕剧分镜"><ol class="st-reel" style="--n:6">{lis}</ol><div class="st-bar" aria-hidden="true"><i></i></div><figcaption class="muted small">🎬 六幕分镜 · 自动轮播（离开屏幕即暂停），点任一幕定格；详细剧情见下方卡片。</figcaption></figure>'
