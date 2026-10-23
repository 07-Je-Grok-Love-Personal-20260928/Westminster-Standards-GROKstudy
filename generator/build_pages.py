# -*- coding: utf-8 -*-
import json, sys
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from content_more import TIMELINE, TL_CATS, MAP
from content_atlas import MAPS, OVERVIEW, CONFESSIONS
from atlas import mapblock, confession_chart
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')+'/'
D=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','standards.json')))
CRED=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs','assets','img','credits.json')))
def fig(fn,cap):
    m=CRED[fn]
    return f'<figure class="rv"><img loading="lazy" src="assets/img/{fn}" alt="{esc(cap)}"><figcaption>{cap}（图源：<a href="{m["page"]}" target="_blank" rel="noopener">Wikimedia Commons</a>，{esc(m["license"])}）</figcaption></figure>'
# ===================== INDEX =====================
def build_index():
    b=[]
    b.append('''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/assembly.jpg)"><div class="shine"></div><div class="floaty">🕊️</div>
<h1>威斯敏斯特标准<br>《信仰告白》·《大要理问答》·《小要理问答》</h1>
<p>一个站点读懂改革宗正统最重要的英语信仰文件：先跳出框架、从<b>整本圣经</b>与<b>神学核心</b>看全貌，再进入<b>逐章逐问</b>的细节；有时间线、故事线、地图、文化背景，有<b>圣经神学</b>与<b>圣约神学</b>，并以<b>欧陆改革宗</b>（三大普世信经 + 三项联合信条）与<b>长老会改革宗正统</b>两个视角对照阅读。</p>
<div class="chips"><span class="chip">📘 信仰告白 33章</span><span class="chip">📗 大要理 196问</span><span class="chip">📙 小要理 107问</span><span class="chip">🗺️ 地图·时间线</span><span class="chip">🧠 背诵·记忆训练</span><span class="chip">📱 手机/平板/电脑自适应</span></div></section>''')
    b.append('<div class="stats rv" style="margin-top:18px">'+''.join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v,k in [('1643','西敏会议开幕'),('5½年','全体会议时期（1643–1649）'),('33','信仰告白章数'),('196','大要理问答'),('107','小要理问答'),('3','王国：英格兰·苏格兰·爱尔兰')])+'</div>')
    from content_v2 import LEGEND, CALLOUTS
    import re as _re
    strip=lambda t:_re.sub(r'⟦\d+⟧','',t)
    nw=sum(len(strip(x['text'])) for c in D['wcf'] for x in c['secs']); nl=sum(len(strip(u['ques']+u['ans'])) for u in D['wlc']); ns=sum(len(strip(u['ques']+u['ans'])) for u in D['wsc'])
    b.append(h2('从这里开始','🚀','start'))
    cards=[('wcf.html','📘','信仰告白 · 逐章精解','原文 + 核心要义 + 圣经神学 + 圣约神学 + 欧陆对照 + 难点 + 应用 + 记忆钩子'),
           ('wlc.html','📗','大要理问答 · 196问','15个主题板块，牧者与成熟信徒的「讲道手册」'),
           ('wsc.html','📙','小要理问答 · 107问','10个主题板块，最适合家庭与初学者背诵'),
           ('history.html','🗺️','历史 · 地理 · 文化','时间线、故事线、总览地图、人物与派别、文化区域'),
           ('atlas.html','🧭','历史地图集','宗教改革传播、1640年代不列颠、西敏寺与耶路撒冷厅、全球传播、两大改革宗家族'),
           ('compare.html','⚖️','深度对比','三份文件异同、为何三份而非一份、与三项联合信条对照矩阵'),
           ('recite.html','🎙️','干净阅读版 · 背诵','遮盖答案、首字提示、字号调节、已背进度'),
           ('memory.html','🧠','记忆训练','口诀、记忆宫殿、翻转卡片、小测验'),
           ('creeds.html','📜','信经与联合信条原文','三大普世信经 + 比利时信条 + 海德堡 + 多特（逐字取自 ccifellowship.org）')]
    b.append('<div class="grid g4">'+''.join(f'<a class="card navcard rv" href="{u}"><div class="big">{i}</div><h3>{t}</h3><p>{d}</p></a>' for u,i,t,d in cards)+'</div>')
    b.append('<div class="grid g2">'+'<div class="card legendcard rv"><h3 style="margin-top:0">🖍️ 标注系统（全站统一，右上角 🖍️ 随时查看）</h3><ul class="lglist">'+''.join((f'<li class="lgh">{y}</li>' if x is None else f'<li><span class="lgx">{x}</span><span>{y}</span></li>') for x,y in LEGEND)+'</ul><ul class="lglist two">'+''.join(f'<li><span class="lgc {k}">{i}</span><span>{n}</span></li>' for k,i,n in CALLOUTS)+'</ul></div>'
      +'<div class="card rv"><h3 style="margin-top:0">📏 三份文件篇幅（正文字数，不含证明经文）</h3>'+bars([('📘 信仰告白',nw,'var(--a1)','wcf.html'),('📗 大要理问答',nl,'var(--a2)','wlc.html'),('📙 小要理问答',ns,'var(--a3)','wsc.html')],cls='rv')
      +f'<p class="muted small">按本站所用 RTF-USA 2024 简体译本统计（问+答/条文）。大要理约为小要理的 {nl/ns:.1f} 倍。</p>'
      +'<h3>🎨 主题</h3><p>点击右上角 🎨：5 套配色（晨曦 · 翡翠 · 绛红金 · 深海 · 暮光）× 浅色/深色/跟随系统，并可开关丝滑滚动与动画。</p></div></div>')
    # one page summary
    b.append(h2('一页读懂：为什么写 · 写了什么 · 怎么用','🧩','why'))
    b.append('''<div class="flow rv">
<div class="st"><div class="e">⚔️</div><b>处境</b><small>内战、国教危机、三个王国宗教分裂</small></div>
<div class="st"><div class="e">🤝</div><b>盟约</b><small>1643《庄严联盟与圣约》：追求三国在信仰告白、教会治理、敬拜指南与要理问答上的统一</small></div>
<div class="st"><div class="e">🏛️</div><b>会议</b><small>国会召集的神学家会议，在西敏寺逐句辩论</small></div>
<div class="st"><div class="e">📘</div><b>文件</b><small>信仰告白（1646/47）+ 大要理（1647/48）+ 小要理（1647/48）</small></div>
<div class="st"><div class="e">🌍</div><b>流传</b><small>苏格兰采纳 → 北美长老会 → 全球改革宗/长老会，含华人教会</small></div>
</div>''')
    b.append('<div class="grid">'+''.join(f'<div class="card rv {cls}"><h3>{t}</h3>{mk(c)}</div>' for t,c,cls in [
     ('❓ 为什么写（Why）','<p>直接原因：长期国会需要在废除主教制后重建英格兰教会的教义、治理与敬拜；苏格兰盟约派要求以“盟约”为条件提供军事援助，目标是<mark>三个王国宗教上的统一</mark>。深层原因：一百年宗教改革成果需要一份能抵御罗马天主教、阿米念主义、反律主义、索西尼主义等错误的成熟表述。</p>','bl-cov'),
     ('📝 写了什么（What）','<p><b>信仰告白</b>：从圣经论到末日审判的完整教义体系；<b>大要理问答</b>：以问答形式更详尽地展开信仰与本分，供讲台与成熟信徒；<b>小要理问答</b>：精炼可背的入门版本。三者结构一致：<mark>先“信什么”，后“行什么”</mark>。</p>','bl-rev'),
     ('🛠️ 怎样应用（How）','<p>个人：以第1问校准人生目的；家庭：以小要理问答作家庭敬拜教材；教会：作为讲道、门训、按立与教会纪律的教义标准；宣教：为华人教会提供成熟、经过历史检验的信仰语言。</p>','bl-sal')])+'</div>')
    b.append(callout('key-pt','📖 学习顺序（本站所用译本卷末托马斯·曼顿〔Thomas Manton〕序言原句）','<span class="verse">“先学习《小要理问答》，其次是《大要理问答》，最后是《信仰告白》。”</span>'))
    # whole bible
    b.append(h2('第一层：跳出框架——从整本圣经看','🌏','bible'))
    b.append('<p class="lead">西敏标准不是一套抽象哲学，而是对<b>圣经整体叙事</b>的系统总结。下表把圣经的救赎历史主线，与西敏标准、三项联合信条的对应位置并列，帮助你先看见「森林」，再看「树木」。</p>')
    rows=[('🌳 创造','创1–2','神是创造主，人按神形像受造，伊甸是圣所','WCF 4；WSC 9–10；WLC 15–17','HC 6；BC 12, 14'),
          ('🍎 行为之约·堕落','创2:16-17；创3；罗5','亚当作为代表元首违约，全人类在他里面堕落','WCF 6–7.2；WSC 12–19；WLC 20–29','HC 3–11；BC 14–15；CD III/IV'),
          ('🐍 第一福音','创3:15','女人的后裔要伤蛇的头——恩典之约的第一次宣告','WCF 7.3；WLC 30–31','HC 19；BC 17'),
          ('🌈 挪亚之约','创6–9','普遍恩典中保存世界，为救赎历史搭建舞台','WCF 5（护理）','BC 13'),
          ('⭐ 亚伯拉罕之约','创12, 15, 17','“要作你和你后裔的神”——因信称义，约的记号给儿女','WCF 7.5；11.6；28.4','HC 74；BC 34'),
          ('⛰️ 摩西之约','出19–24；利；申','律法、祭司、献祭、帐幕：预表基督；道德律永远有效','WCF 19；WLC 34, 91–148；WSC 39–81','HC 92–115；BC 25'),
          ('👑 大卫之约','撒下7；诗2；诗110','永远的王位，弥赛亚是大卫的子孙','WCF 8.1；WLC 45；WSC 26','HC 31'),
          ('📜 先知与新约应许','耶31:31-34；结36','新心、新灵、罪得赦免——内化的约','WCF 7.6；10.1','CD III/IV 11–12'),
          ('✝️ 基督：约的中保','福音书；来7–10','降卑、受死、复活、升天：成全行为之约的要求，施行恩典之约','WCF 8；WLC 36–56；WSC 21–28','HC 12–52；BC 18–21'),
          ('🔥 五旬节与教会','徒2；弗1–4','圣灵把基督的救恩施用给选民，召聚教会','WCF 10–18, 25–31；WLC 57–90','HC 53–85；BC 22–35'),
          ('🌅 新天新地','启21–22','审判、复活、约的完全成全：“神的帐幕在人间”','WCF 32–33；WLC 82–90；WSC 37–38','HC 52, 57–58；BC 37')]
    b.append('<div class="tbl rv"><table><thead><tr><th>救赎历史阶段</th><th>经文</th><th>主线</th><th>西敏标准</th><th>三项联合信条</th></tr></thead><tbody>'+''.join(f'<tr><td><b>{a}</b></td><td>{b_}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a,b_,c,d,e in rows)+'</tbody></table></div>')
    b.append('<div class="mermaid">'+esc('''flowchart LR
  C["🌳 创造"] --> F["🍎 堕落"] --> P["🐍 应许 创3:15"] --> N["🌈 挪亚"] --> A["⭐ 亚伯拉罕"] --> M["⛰️ 摩西"] --> D["👑 大卫"] --> J["📜 新约应许"] --> X(("✝️ 基督"))
  X --> CH["🔥 教会"] --> NC["🌅 新天新地"]
  style X fill:#fde68a,stroke:#b45309,stroke-width:3px''')+'</div>')
    # covenant theology
    b.append(h2('第二层：神学核心——圣约神学','🤝','covenant'))
    b.append('<p class="lead">西敏标准最显著的结构特征是<b>圣约</b>：神与人之间“距离是如此之远”，人要得着祝福，唯有神<b>屈尊降卑</b>以约的方式与人相交（WCF 7.1）。欧陆改革宗（布林格、乌尔西努、俄利维亚努等）是圣约神学的源头之一；西敏会议把它以信条形式系统化。</p>')
    b.append('<div class="mermaid">'+esc('''flowchart TB
  PS["🕊️ 救赎之约（永恒中·父与子）<br/>神学传统中的概念，WCF 8.1 与 WLC 31 隐含其意"]:::a
  CW["🍎 行为之约 / 生命之约<br/>WCF 7.2；19.1；WLC 20；WSC 12<br/>条件：完全、个人、永久的顺服"]:::w
  CG["🤝 恩典之约<br/>WCF 7.3；WLC 30–35；WSC 20<br/>与第二亚当基督及在祂里的选民立"]:::g
  OT["📜 律法时期的施行<br/>应许·预言·献祭·割礼·逾越节·预表"]:::o
  NT["✝️ 福音时期的施行<br/>圣道·洗礼·圣餐：更简明、更充分、更有效"]:::n
  PS --> CG
  CW -- 亚当违约 --> CG
  CG --> OT
  CG --> NT
  OT -. 本质同一 .- NT
  classDef a fill:#ede9fe,stroke:#7c3aed,color:#1f2937
  classDef w fill:#fee2e2,stroke:#dc2626,color:#1f2937
  classDef g fill:#fef3c7,stroke:#d97706,color:#1f2937
  classDef o fill:#e0f2fe,stroke:#0284c7,color:#1f2937
  classDef n fill:#dcfce7,stroke:#16a34a,color:#1f2937''')+'</div>')
    b.append('<div class="grid">'+''.join(f'<div class="card rv {c}"><h3>{t}</h3><p>{mk(d)}</p></div>' for t,d,c in [
      ('🍎 行为之约','亚当作为全人类的盟约元首，以完全顺服为条件得生命；违约则死。理解它，才能理解为何需要「第二亚当」以完全顺服成全律法（主动顺服），并替我们受刑（被动顺服）。','bl-man'),
      ('🤝 恩典之约','“基督是第二个亚当，恩典之约是与祂以及在祂里面的所有选民立的”（WLC 31）。神白白提供生命与救恩，要求信心，并应许赐下圣灵使人愿意并能够相信（WCF 7.3）。','bl-cov'),
      ('📜 一约两施行','旧约与新约不是两种救法，而是同一恩典之约在不同时期的施行（WCF 7.5–7.6）。这是婴儿洗礼、教会连续性、以经解经的基础。','bl-sal'),
      ('🇳🇱 与欧陆的连接','海德堡第74问以婴孩“与父母同属于神的圣约和教会”为洗礼根据；《比利时信条》第17条描写神在人堕落后“来寻找战兢地躲避他面的人”。两大传统共享同一圣约骨架，西敏在术语上更系统。','bl-chr')])+'</div>')
    # mind map
    b.append(h2('第三层：思维导图——三份文件一张图','🧠','mindmap'))
    b.append('<div class="mermaid">'+esc('''mindmap
  root((西敏标准))
    信仰告白 33章
      启示 1
      神 2-5
      人·约·基督 6-9
      救恩施行 10-18
      律法·自由·敬拜 19-24
      教会·圣礼 25-31
      末世 32-33
    大要理 196问
      当信什么 1-90
        神与作为
        恩典之约与中保
        恩典中·荣耀中与基督相交
      当尽本分 91-196
        道德律·十诫
        蒙恩之道 道·礼·祷告
    小要理 107问
      当信什么 1-38
      当尽本分 39-107
        十诫 45-81
        主祷文 99-107''')+'</div>')
    # continental lens
    b.append(h2('第四层：两大改革宗传统的阅读视角','🇳🇱','continental',toc='第四层：欧陆 + 长老会视角'))
    b.append('<div class="mermaid">'+esc('''flowchart LR
  R["🔥 宗教改革 16世纪"] --> EU["🇳🇱🇩🇪🇨🇭 欧陆改革宗"]
  R --> BR["🏴 不列颠改革宗"]
  EU --> BC["📕 比利时信条 1561"]
  EU --> HC["📗 海德堡要理问答 1563"]
  EU --> CD["📙 多特信经 1618–1619"]
  BR --> ART["39条 1563"]
  BR --> IA["爱尔兰信纲 1615"]
  IA --> WS["📘 西敏标准 1646–1648"]
  ART --> WS
  CD -. 同一正统共识 .- WS
  BC --> TFU(("三项联合信条"))
  HC --> TFU
  CD --> TFU
  TFU --> CR["今日：CanRC · URCNA · HRC · PRCA · 中国改革宗教会 …"]
  WS --> PR["今日：OPC · PCA · 苏格兰自由教会 …"]''')+'</div>')
    b.append('<div class="grid g2">'+
      '<div class="card rv bl-chr"><h3>📜 认信坐标</h3><p>欧陆改革宗教会（如加拿大归正教会 CanRC、北美联合改革宗教会 URCNA、传承改革宗 HRC、更正改革宗 PRCA，以及中文世界的中国改革宗教会、洛杉矶改革宗·恩约教会）以<b>三大普世信经 + 三项联合信条</b>为信仰准则；长老会（如 OPC）以<b>西敏标准</b>为准则。两者同属改革宗认信家族，教义体系高度一致。</p></div>'+
      '<div class="card rv bl-cov"><h3>🔍 阅读原则</h3><p>① 先以三大普世信经确认三一与基督论的大公根基；② 以三项联合信条为“母语”，把西敏标准当作同一家族中更详尽的「姊妹文件」；③ 在一致处互相丰富，在侧重不同处（如安息日实践、确据与信心的关系、教会与国家）以圣经为最终裁判（WCF 1.10；BC 7）。</p></div></div>')
    b.append('<div class="grid g2">'+callout('pr-pt','🏴 长老会改革宗正统怎样读','① 以<b>西敏标准</b>为教会的「从属标准」（圣经是唯一的最高标准，WCF 1.10）；② 教义与<b>敬拜、治理</b>一体：《公共敬拜指南》与《长老会教会治理形式》与信条同出一会；③ 以<span class="c-term">大要理问答</span>的十诫详解塑造伦理，以<span class="c-term">小要理问答</span>塑造家庭；④ 区分永恒教义与17世纪处境（如1788年美国对官员条款的修订）。',raw=True)
      +callout('eu-pt','🤝 两大传统怎样互相成全','<span class="u-cmp">欧陆传统</span>给西敏标准带来<b>温暖的安慰语言</b>（HC 1）、殉道与护教的视野（BC）、最详尽的预定论牧养（CD）；<span class="u-cmp">长老会传统</span>给欧陆读者带来<b>精密的定义</b>、清楚的圣约结构与详尽的伦理和蒙恩之道。核心教义完全一致，侧重点互补。',raw=True)+'</div>')
    b.append(callout('eu-pt','🏛️ 洛杉矶改革宗·恩约教会《我们的信仰》（原文摘录，来源 ccreformed.org/our-belief）','<span class="verse">“在恩约教会，我们相信并宣告：古代的基督教信经，即《使徒信经》、《尼西亚信经》、《亚他那修信经》，以及三联合信条，即《比利时信条》、《海德堡要理问答》、《多特信经》，包含了我们的教义准则，及公开宣告的信仰内容。这些信仰文件不是我们独有的。古代信经把我们连结在古代基督教会上，而三联合信条把我们连结在十六、十七世纪广大的改革宗传统中。”</span>'))
    b.append(callout('eu-pt','✍️ 改革宗初学者《信仰告白》（原文摘录，来源 reformedbeginner.net/statement-of-faith）','<span class="verse">“改革宗初学者博客认信普世大公教会所共同持守的大公信经：使徒信经、尼西亚信经、亚他那修信经； 并继承改革宗的认信传统，与历代改革宗基督徒同口承认以下的信仰文件忠心总结了圣经的教义系统：三联合信条（即海德堡要理问答、比利时信条、多特信经）；威敏斯特准则（威敏斯特信仰告白、威敏斯特大、小要理问答）。”</span>'))
    b.append(h2('第五层：从不同视角读','👓','lenses'))
    lenses=[('🏺','历史视角','把文件放回1640年代的战争、国会与盟约中：它们是「危机中的信仰告白」。'),('📚','圣经神学视角','跟随救赎历史的主线（创造—堕落—救赎—成全），看每一条教义在圣经故事中的位置。'),('🤝','圣约神学视角','以行为之约与恩典之约为骨架，理解律法与福音、旧约与新约、亚当与基督。'),('🏛️','系统神学视角','按「神论—人论—基督论—救恩论—教会论—末世论」检查体系的完整与一致。'),('🎶','敬拜视角','规范原则、安息日、圣礼、祷告：教义如何塑造主日。'),('👨‍👩‍👧','家庭与教育视角','要理问答原本就是为家庭与儿女写的：曼顿序言强调家长的教导责任。'),('⚖️','伦理与社会视角','大要理的十诫详解是一部完整的基督徒伦理学：家庭、经济、言语、心思。'),('🌏','华人教会视角','在没有基督教王国背景的处境中，学习区分永恒教义与17世纪的政治安排（如官员条款）。')]
    b.append('<div class="tbl rv"><table><thead><tr><th>视角</th><th>问什么</th></tr></thead><tbody>'+''.join(f'<tr><td><b>{i} {t}</b></td><td>{mk(d)}</td></tr>' for i,t,d in lenses)+'</tbody></table></div>')
    open(OUT+'index.html','w').write(page('index.html','总览：从整本圣经看西敏标准','\n'.join(b)))
# ===================== HISTORY =====================
def build_history():
    b=[]
    b.append('''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/jerusalem-chamber.jpg)"><div class="shine"></div><div class="floaty">🗺️</div><h1> 历史 · 地理 · 文化</h1>
<p>时间线、故事线、互动地图、人物与派别、文化区域——还原1640年代伦敦西敏寺里那场长达五年半的神学会议的<b>真实背景</b>与<b>真实情境</b>。</p></section>''')
    b.append(h2('时间线（可筛选）','⏳','timeline'))
    b.append('<div class="filters" data-for="#tl">'+''.join(f'<button data-k="{k}" class="{"on" if k=="all" else ""}">{v}</button>' for k,v in TL_CATS)+'</div>')
    b.append('<div class="tl" id="tl">'+''.join(f'<div class="ev{" big" if big else ""}" data-cat="{cat}" style="--dot:{col}"><span class="y">{y}</span>{t}</div>' for y,t,cat,col,big in TIMELINE)+'</div>')
    b.append('<p class="muted">注：时间线中关于普世信经与三项联合信条的年代说明以 ccifellowship.org 引言为准；西敏会议的日期依据通行的教会史记载整理。</p>')
    b.append(h2('故事线：六幕剧','🎭','story'))
    acts=[('第一幕 · 风暴前夜（1625–1640）','查理一世与大主教劳德推行高派礼仪与主教统治，清教徒受压。1637年，查理强迫苏格兰使用新祈祷书，爱丁堡圣吉尔斯大教堂爆发骚乱；1638年苏格兰人签署《国民圣约》，随后的「主教战争」迫使国王召开国会。','⛈️'),
          ('第二幕 · 国会与战争（1640–1643）','「长期国会」与国王的冲突升级为1642年内战。国会决心改革英格兰教会，于1643年颁令召开神学家会议，向国会提供意见——会议是国会的咨询机构，不是独立的教会总会。','⚔️'),
          ('第三幕 · 盟约（1643）','国会需要苏格兰军队，苏格兰则要求宗教上的盟约。《庄严联盟与圣约》由此产生，目标是三国在信仰告白、教会治理、敬拜指南与要理问答上的统一。苏格兰派出专员（如亨德森、卢瑟福、吉莱斯皮、贝利）参与会议。','🤝'),
          ('第四幕 · 耶路撒冷厅的日与夜（1643–1647）','会议先修订《三十九条》，后转而起草全新的文件。长老派、独立派（「异议弟兄」）、伊拉斯都派围绕教会治理激烈辩论；外面战火未熄（马斯顿荒原、纳斯比）。《公共敬拜指南》《教会治理形式》先后完成，1646年底信仰告白完成。','🕯️'),
          ('第五幕 · 文件诞生（1646–1648）','信仰告白附经文于1647年呈交；苏格兰教会总会于1647年8月批准。大小要理问答于1647年秋呈交，1648年附经文；苏格兰总会于1648年7月批准。英格兰国会虽部分采纳，但政局巨变使其未能在英格兰长期实行。','📘'),
          ('第六幕 · 王冠落地之后（1649–今天）','1649年查理一世被处决；1660年王政复辟，1662年大批清教徒牧师被逐。西敏标准却在苏格兰扎根（1690年再获确认），经由移民传到北美（1729年采纳法案、1788年修订），最终成为全球长老会与众多改革宗教会的信仰准则，也进入华人教会。','🌍')]
    b.append('<div class="grid g2">'+''.join(f'<div class="card rv"><h3>{i} {t}</h3><p>{mk(d)}</p></div>' for t,d,i in acts)+'</div>')
    b.append(h2('总览地图：从尼西亚到西敏','📍','mapsec'))
    b.append(mapblock(OVERVIEW,intro=False))
    b.append('<p class="cta"><a class="btn" href="atlas.html">🧭 打开「历史地图集」：宗教改革传播 · 1640年代不列颠 · 伦敦西敏区 · 全球传播 · 两大改革宗家族 →</a></p>')
    b.append('<div class="grid">'+fig('abbey.jpg','西敏寺西立面（约翰·布拉克 版画）')+fig('jerusalem-chamber.jpg','耶路撒冷厅——西敏会议的主要会场（19世纪插图）')+fig('assembly.jpg','约翰·罗杰斯·赫伯特所绘：西敏会议中独立派为良心自由辩护（1644年情景的19世纪历史画）')+'</div>')
    b.append('<div class="grid">'+fig('covenant.jpg','《庄严联盟与圣约》（1643）')+fig('dort.jpg','多特大会（17世纪荷兰版画）')+fig('heidelberg1563.jpg','1563年《海德堡要理问答》扉页')+'</div>')
    b.append(h2('会议中的人物与派别','👥','people'))
    parties=[('🟦 长老派（多数）','主张由长老会议治理教会，与苏格兰立场相近；如埃德蒙·卡拉米、安东尼·塔克尼、爱德华·雷诺兹等。'),('🟩 独立派（「异议弟兄」）','主张会众自治，人数少但影响大：托马斯·古德温、菲利普·奈、耶利米·巴勒斯等，1644年发表《辩护陈述》。'),('🟨 伊拉斯都派','主张国家对教会纪律有最终权柄：约翰·塞尔登、约翰·莱特富特、托马斯·科尔曼等。WCF 30.1「在国家官员以外」设立教会治理，正是对此的回应。'),('🟥 苏格兰专员','无表决权，但影响深远：亚历山大·亨德森、塞缪尔·卢瑟福、乔治·吉莱斯皮、罗伯特·贝利（其书信是重要史料）。'),('⬜ 主持人','威廉·特威斯（William Twisse）为首任会议主持（prolocutor），1646年去世后由查尔斯·赫尔（Charles Herle）接任。'),('🟪 缺席者','大主教厄舍（James Ussher）虽被提名却未出席，但他主导的《爱尔兰信纲》（1615）深刻影响了信仰告白的结构与用语。')]
    b.append('<div class="grid">'+''.join(f'<div class="card rv"><h3>{t}</h3><p>{mk(d)}</p></div>' for t,d in parties)+'</div>')
    b.append(h2('文化区域特征','🏰','culture'))
    rows=[('🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格兰','国教会（主教制）+ 清教运动；国会政治与普通法传统；伦敦印刷业与小册子战','清教徒「平实讲道」、守主日、家庭敬拜、良心问题（案例神学）','会议地点与召集者；信条的法律与政治处境（官员条款）'),
          ('🏴󠁧󠁢󠁳󠁣󠁴󠁿 苏格兰','长老制「柯克」（Kirk）、总会制度；盟约传统（1638国民圣约）','教会独立于王权的「两国论」、公开的教会纪律、要理问答教育','推动“统一”的动力；最终采纳并长期实行西敏标准'),
          ('☘️ 爱尔兰','厄舍与都柏林三一学院；1615年《爱尔兰信纲》；1641年叛乱','学术性的改革宗正统','信条结构与用语的蓝本之一'),
          ('🇳🇱 低地国家','在西班牙统治与逼迫下形成的改革宗教会；多特大会','殉道者信仰、会议制教会、诗篇吟唱、海德堡问答讲道','三项联合信条；国际改革宗正统的共识'),
          ('🇩🇪 普法尔茨','选帝侯腓德烈三世；海德堡大学','温暖、个人化的要理问答传统（“唯一的安慰”）','圣约神学先驱（乌尔西努、俄利维亚努）'),
          ('🇨🇭 日内瓦/瑞士','加尔文、贝扎、布林格','学院与流亡者网络；圣经注释传统','英格兰/苏格兰改教者的神学母校')]
    b.append('<div class="tbl rv"><table><thead><tr><th>区域</th><th>政治与教会结构</th><th>敬虔与文化特征</th><th>与西敏标准的关系</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>')
    open(OUT+'history.html','w').write(page('history.html','历史 · 地理 · 文化','\n'.join(b)))
# ===================== ATLAS (v3.0) =====================
def build_atlas():
    b=[]
    b.append('''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/dort.jpg)"><div class="shine"></div><div class="floaty">🧭</div><h1>历史地图集</h1>
<p>五幅主题地图，每幅都有<b>手绘示意图</b>（离线可用、带动画路线）和<b>可缩放的实景地图</b>（自带底图 + 在线瓦片自动切换），并配本图时间线与文化区域特征。所有日期与地点均附来源。</p></section>''')
    n=sum(len(m['places']) for m in MAPS)
    b.append('<div class="stats rv" style="margin-top:18px">'+''.join(f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v,k in [('5','主题地图'),(str(n),'标注地点'),('1517','起点：维登堡'),('1643','西敏会议开幕'),('1872','马偕抵淡水')])+'</div>')
    b.append('<nav class="mapnav rv" aria-label="地图目录">'+''.join(f'<a href="#map-{m["id"]}"><span>{m["icon"]}</span>{esc(m["title"].split("：")[0].split("（")[0])}</a>' for m in MAPS)+'</nav>')
    b.append(h2('信条年代图：一百多年里的告白浪潮','📊','confchart'))
    b.append('<p>把宗教改革时期的主要信条放在同一条时间轴上，就能看见西敏标准的位置：它是这场告白运动<mark>最晚、也最系统</mark>的成果之一，吸收了此前欧陆与不列颠一百多年的神学积累。</p>')
    b.append(confession_chart())
    for m in MAPS:
        b.append(h2(esc(m['title']),m['icon'],'map-'+m['id']))
        b.append(mapblock(m))
    b.append(h2('读图要点','🧠','takeaways'))
    b.append('<div class="grid g2">'+callout('key-pt','🎯 一句话','西敏标准是<span class="hl-date">1517–1619</span>一百年欧陆改革的<b>下游成果</b>，又是<span class="hl-date">1640年代</span>不列颠危机的<b>直接产物</b>，再经移民与宣教走向<b>全球</b>。',raw=True)
             +callout('mem-pt','🧠 记忆钩子','<b>四个城市串一条线</b>：日内瓦（神学）→ 爱丁堡（盟约）→ 西敏（成文）→ 费城（北美采纳）。',raw=True)
             +callout('cov-pt','🤝 与圣约神学','从海德堡的乌尔西努、俄利维亚努，到西敏信条第7章「行为之约 / 恩典之约」，圣约神学沿着这张地图从欧陆走进不列颠。',raw=False)
             +callout('warn-pt','🚫 常见误解','西敏会议<span class="u-err">不是</span>教会会议，而是<b>国会召集的咨询机构</b>；西敏标准在英格兰只短暂生效，真正长久采用它的是苏格兰与后来的各地长老会。',raw=True)+'</div>')
    open(OUT+'atlas.html','w').write(page('atlas.html','历史地图集 · 宗教改革到全球传播','\n'.join(b),desc='宗教改革在欧洲的传播、1640年代不列颠、伦敦西敏寺与耶路撒冷厅、西敏标准的全球传播、欧陆改革宗与长老会的地理分布：手绘示意图 + 实景地图 + 时间线 + 文化区域。'))
# ===================== COMPARE =====================
def build_compare():
    b=[]
    b.append('''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/dort.jpg)"><div class="shine"></div><div class="floaty">⚖️</div><h1> 深度对比</h1>
<p>三份西敏文件之间的异同；为什么需要三份而不是一份；它们各自要解决什么问题；以及西敏标准与欧陆<b>三项联合信条</b>、<b>三大普世信经</b>的系统对照。</p></section>''')
    b.append(h2('三份西敏文件总览','📊','three'))
    rows=[('体裁','系统性信条（章·节）','详尽的问答','精炼的问答'),
          ('完成/呈交','1646年12月；1647年附经文','1647年10月；1648年附经文','1647年11月；1648年附经文'),
          ('苏格兰批准','1647年8月','1648年7月2日','1648年7月'),
          ('篇幅','33章','196问','107问'),
          ('主要对象','教会与圣职人员：教义标准与界线','牧者讲道、教师、成熟信徒','儿童、家庭、初信者'),
          ('结构','圣经→神→人与约→基督→救恩→律法与敬拜→教会→末世','序言1–5；当信6–90；本分91–196','序言1–3；当信4–38；本分39–107'),
          ('圣约','第7章系统论述；19.1','20（生命之约）、30–35（恩典之约）','12（生命之约）、20（恩典之约）'),
          ('独有亮点','精密定义与驳谬（如1.6、7.5–7.6、11.1、18.3）','有形/无形教会；「恩典中/荣耀中」与基督相交；99问解经八规则；167问善用洗礼','第1问；第4问对神的定义；简洁可背'),
          ('语气','法庭式、宣告式（“我们相信”隐含）','教师式、细致、实践','教理问答式、简明、易记')]
    b.append('<div class="tbl rv"><table><thead><tr><th>维度</th><th>📘 信仰告白</th><th>📗 大要理问答</th><th>📙 小要理问答</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{"<b>"+x+"</b>" if i==0 else x}</td>' for i,x in enumerate(r))+'</tr>' for r in rows)+'</tbody></table></div>')
    b.append('<div class="card rv"><h3 style="margin-top:0">🔵🟢🟠 三份文件的共同核心与各自独有</h3><div class="venn" role="img" aria-label="三份文件韦恩图"><div class="c c1"><span><b>📘 信仰告白</b><br>精密定义 · 驳谬<br>官员 · 会议 · 婚姻</span></div><div class="c c2"><span><b>📗 大要理</b><br>有形/无形教会<br>恩典中/荣耀中<br>十诫八规则</span></div><div class="c c3"><span><b>📙 小要理</b><br>最短定义 · 易背</span></div><div class="mid">同一体系：<br>当信什么 +<br>当尽本分</div></div><p class="muted small">示意图（定性，不按比例）：三份文件出自同一会议、同一教义体系，差别在详略与功能。</p></div>')
    b.append(h2('为什么需要三份，而不是一份？','❓','whythree'))
    b.append('<div class="grid">'+''.join(f'<div class="card rv {c}"><h3>{t}</h3><p>{d}</p></div>' for t,d,c in [
      ('1️⃣ 功能不同','信条是教会公开的「界碑」，用于按立与纪律；要理问答是「课本」，用于教导与背诵。一份文件很难同时做到精密与易记。','bl-rev'),
      ('2️⃣ 对象不同','会议在起草过程中决定写两部要理问答：一部更精确、更全面，一部更简单、更短，供初学者使用。这正是大、小要理问答的分工。','bl-sal'),
      ('3️⃣ 盟约要求','《庄严联盟与圣约》追求的统一包括信仰告白与要理问答两项，因此两类文件都是「盟约任务」的组成部分。','bl-cov'),
      ('4️⃣ 改教传统','改教时期普遍「信条 + 要理问答」并行：如加尔文的日内瓦要理问答与法国信条；欧陆的《比利时信条》与《海德堡要理问答》。','bl-chr'),
      ('5️⃣ 教学阶梯','曼顿的建议：先小要理、再大要理、最后信仰告白——由浅入深、由记忆到理解再到体系。','bl-law'),
      ('6️⃣ 互相保护','三份文件同一体系、互相印证：要理问答的简洁表述受信条的精确定义保护，信条的抽象表述因要理问答而落地为生活。','bl-chu')])+'</div>')
    b.append(h2('各自要解决的问题','🎯','problems'))
    probs=[('📘 信仰告白','三国教会的教义统一；回应罗马天主教（圣经与传统、弥撒、炼狱）、阿米念主义（预定、恩典、坚忍）、反律主义（律法与成圣）、索西尼主义（三一、补赎）、重洗派（婴儿洗礼、官员）、伊拉斯都主义（教会治理权）'),
           ('📗 大要理问答','为讲台提供系统而详尽的教义大纲；尤其为伦理生活（十诫）与蒙恩之道（道、礼、祷告）提供牧养细节'),
           ('📙 小要理问答','在家庭与教会中培养下一代；让每个信徒都能用简短准确的话表达信仰（“荣耀神，永远因祂而喜乐”）')]
    b.append('<div class="tbl rv"><table><thead><tr><th>文件</th><th>主要针对的问题</th></tr></thead><tbody>'+''.join(f'<tr><td><b>{a}</b></td><td>{c}</td></tr>' for a,c in probs)+'</tbody></table></div>')
    b.append('<div class="mermaid">'+esc('''flowchart LR
  P["❓ 1640年代的问题"] --> P1["三国教会教义不统一<br/>罗马·阿米念·反律·索西尼"]
  P --> P2["讲台缺乏系统教义大纲"]
  P --> P3["家庭与儿童缺少可背的教材"]
  P1 --> W["📘 信仰告白<br/>界碑：精确、完整"]
  P2 --> L["📗 大要理问答<br/>教材：详尽、牧养"]
  P3 --> S["📙 小要理问答<br/>入门：简短、可背"]
  W -. 同一体系 .- L
  L -. 同一体系 .- S''')+'</div>')
    b.append(h2('同一教义在三份文件中的位置','🧭','matrix'))
    mx=[('圣经','1','2–5','2–3','2–7','—（参21、22）','—'),('神与三一','2','6–11','4–6','1, 8–11','25','—'),('预定','3','12–14','7–8','16','54','第一项'),('创造与护理','4–5','15–19','9–11','12–13','26–28','—'),('堕落与原罪','6','21–29','13–19','14–15','3–11','第三、四项'),('圣约','7','20, 30–35','12, 20','17（应许）','74（洗礼与约）','—'),('中保基督','8','36–56','21–28','18–21, 26','12–19, 29–52','第二项'),('自由意志','9','25, 149','—','14','8','第三、四项'),('有效呼召','10','67–68','31','—','54, 65','第三、四项'),('称义','11','70–73','33','22–23','59–64','第二项'),('成圣与善行','13, 16','75, 77–78','35','24','86–91','—'),('坚忍与确据','17–18','79–81','36','—','1, 53–54','第五项'),('律法与十诫','19','91–152','39–84','25','92–115','—'),('敬拜与安息日','21','108–121','45–62','—','96–98, 103','—'),('教会','25–26','61–65','—','27–29','54–55','—'),('圣礼','27–29','161–177','91–97','33–35','65–82','—'),('教会惩戒与治理','30–31','—','—','30–32','83–85','—'),('政府官员','23','—','—','36','—','—'),('末后之事','32–33','82–90','37–38','37','52, 57–58','—')]
    b.append('<div class="tbl rv"><table><thead><tr><th>教义</th><th>📘 WCF 章</th><th>📗 WLC 问</th><th>📙 WSC 问</th><th>📕 BC 条</th><th>📗 HC 问</th><th>📙 CD</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{"<b>"+x+"</b>" if i==0 else x}</td>' for i,x in enumerate(r))+'</tr>' for r in mx)+'</tbody></table></div>')
    b.append('<p class="muted">对应关系为学习用的参考索引（并非逐字对应）。BC=比利时信条，HC=海德堡要理问答，CD=多特信经。</p>')
    b.append(h2('西敏标准 vs 三项联合信条','🇳🇱','vs3fu'))
    rows=[('年代','1643–1648','1561 / 1563 / 1618–1619'),
          ('地点','伦敦·西敏寺','南尼德兰 / 海德堡 / 多特'),
          ('作者','国会召集的神学家会议（集体起草）','德布利 / 乌尔西努与俄利维亚努等 / 国际性总会'),
          ('处境','内战与三国宗教统一','逼迫中的护教 / 领地的教导 / 阿米念争议'),
          ('体裁','一部信条 + 两部要理问答（同一会议、同一体系）','一部信条 + 一部要理问答 + 一部护教性法规（不同时代、不同作者）'),
          ('起点','WSC 1：人生首要目的——荣耀神、以神为乐','HC 1：或生或死唯一的安慰——属于基督'),
          ('结构特色','「当信什么 / 当尽何本分」二分','HC：「罪与愁苦 / 得救 / 感恩」三分'),
          ('圣约','明确提出行为之约与恩典之约（WCF 7）','恩典之约贯穿（HC 74；BC 17, 34）；“行为之约”术语未直接出现'),
          ('预定','WCF 3（含“越过”与谨慎教导）','CD 第一项（更详细、更牧养）'),
          ('确据','WCF 18.3：完全确据不属于信仰的本质','HC 21：真信心包含确信；CD V 9–13 论确据'),
          ('安息日','WCF 21.7–8：严格的基督教安息日','HC 103：参与公共敬拜、一生不作恶、预尝永远安息'),
          ('教会治理','长老会议制（另有《教会治理形式》）','堂会—区会—总会（《多特教会规章》）'),
          ('政府官员','WCF 23（1788美国修订）','BC 36（ccifellowship注明1905年荷兰总会删除部分字句）'),
          ('今日主要使用者','长老会：OPC、PCA、苏格兰自由教会等','欧陆改革宗：CanRC、URCNA、HRC、PRCA、中国改革宗教会等')]
    DIFF={'结构特色','圣约','确据','安息日','预定','教会治理'}
    b.append('<div class="tbl rv"><table><thead><tr><th>维度</th><th>西敏标准</th><th>三项联合信条</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{"<b>"+x+"</b>"+(" <span class=\'c-ref\'>侧重不同</span>" if x in DIFF else "") if i==0 else (f"<span class=\'u-cmp\'>{x}</span>" if r[0] in DIFF else x)}</td>' for i,x in enumerate(r))+'</tr>' for r in rows)+'</tbody></table></div>')
    b.append('<p class="muted small">虚线下划线 = 两大传统侧重不同之处（并非教义冲突）。</p>')
    b.append('<div class="grid g2">'+callout('key-pt','✅ 本质一致','唯独圣经、三一神、神的主权与预定、全然败坏、基督的替代性补赎、唯独因信称义（归算）、圣灵的有效恩召、圣徒蒙保守、律法作为感恩生活的准则、属灵临在的圣餐观、婴儿洗礼、长老治理的教会与纪律——两套文件在这些核心上完全一致。')+callout('hard-pt','🔍 侧重不同','西敏更系统、更精密、更「经院式」，更突出圣约结构与伦理细节；三项联合信条更个人、更温暖（HC“我”的语言）、更具殉道与护教色彩（BC），并在预定论上有最详尽的牧养处理（CD）。')+'</div>')
    from content_v2 import AMREV
    b.append(h2('1647原文 vs 美国修订本','🇺🇸','amrev'))
    b.append('<p class="lead">本站正文是<b>1647年原文</b>的译本（RTF-USA）。今日美洲多数长老会（如 OPC、PCA）使用<b>美国修订本</b>。下表逐条对照（美国文本依据 <a href="https://opc.org/wcf.html" target="_blank" rel="noopener">opc.org/wcf.html</a>；「 」内为概括）。</p>')
    b.append('<div class="tbl rv"><table><thead><tr><th>条目</th><th>1647 原文（RTF本）</th><th>美国修订本（OPC 现行文本）</th><th>修订时间</th></tr></thead><tbody>'+''.join(f'<tr><td><b><a style="white-space:nowrap" href="wcf.html#c{a.split(".")[0]}">WCF {a}</a></b></td><td>{esc(o)}</td><td><span class="u-cmp">{esc(n)}</span></td><td>{"1788年（美国长老会首届总会前采纳）" if y=="1788" else "其后的修订（各教会年份不同）"}</td></tr>' for a,o,n,y in AMREV)+'</tbody></table></div>')
    b.append(callout('hard-pt','🔍 为什么要知道这些修订？','修订集中在<span class="u-err">国家官员与教会的关系</span>以及个别处境性表述上；有关神、基督、救恩、圣约的核心教义<b>没有改变</b>。欧陆一方也有类似的调整：ccifellowship 版《比利时信条》第36条注明1905年荷兰总会删除了部分字句。',raw=True))
    b.append(h2('与三大普世信经的关系','🕊️','ecumenical'))
    b.append('<p>《比利时信条》第9条说：“在这一教义上，我们甘愿接受《使徒信经》、《尼西亚信经》和《亚他拿修信经》，以及其他与它们不相悖，且受到教父们一致认可的信经。”（ccifellowship.org 原文）西敏标准没有单独列出普世信经，但其三一论（WCF 2.3）与基督论（WCF 8.2）完全承接尼西亚与迦克墩的界线；小要理问答末尾所附的主祷文、十诫与使徒信经（历史上常随印本附录）也显示其大公根基。</p>')
    b.append('<div class="tbl rv"><table><thead><tr><th>普世信经</th><th>核心</th><th>西敏标准中的回响</th></tr></thead><tbody><tr><td><b>使徒信经</b></td><td>三一架构的洗礼信仰告白</td><td>WLC/WSC「当信什么」部分的骨架；HC 23–58 逐句讲解</td></tr><tr><td><b>尼西亚信经</b></td><td>子与父同质；圣灵是主</td><td>WCF 2.3“同享一个本质、相同的权能、同样的永恒”；WLC 9–11</td></tr><tr><td><b>亚他那修信经</b></td><td>三一与基督二性的精确表述</td><td>WCF 8.2 两性“没有相互转化、没有结合成一个、也没有混在一起”；WLC 36–40</td></tr></tbody></table></div>')
    open(OUT+'compare.html','w').write(page('compare.html','深度对比','\n'.join(b)))
# ===================== MEMORY =====================
def build_memory():
    wsc=[dict(q=u['q'],k=u['ques'],a=__import__('re').sub(r'⟦\d+⟧','',u['ans'])) for u in D['wsc']]
    wcft=[c['title'] for c in D['wcf']]
    b=[]
    b.append('''<section class="hero" style="background-image:var(--hero-grad),url(assets/img/abbey.jpg)"><div class="shine"></div><div class="floaty">🧠</div><h1>🧠 记忆训练营</h1><p>口诀 + 记忆宫殿 + 翻转卡片 + 小测验：把「读过」变成“记住”，把“记住”变成“活出”。</p></section>''')
    b.append(h2('我的背诵进度','📈','progress'))
    b.append('<div class="rings">'+''.join(f'<div class="pring rv" data-ring="{p}" data-total="{t}" style="--c:{c}"><svg viewBox="0 0 110 110"><circle class="bgc" cx="55" cy="55" r="45"/><circle class="fgc" cx="55" cy="55" r="45" stroke-dasharray="283" stroke-dashoffset="283"/></svg><b>0 / {t}</b><span>{n}</span></div>' for p,t,c,n in [('wsc-',107,'var(--a3)','📙 小要理问答'),('wlc-',196,'var(--a2)','📗 大要理问答'),('wcf-',172,'var(--a1)','📘 信仰告白（节）')])+'</div>')
    b.append('<p class="muted">在<a href="recite.html">背诵版</a>或问答页点击「☆ 标记」，进度自动保存在本机。</p>')
    b.append(callout('mem-pt','🖍️ 用标注系统帮助记忆','先只读 <mark>荧光底</mark> 的金句；第二遍加上 <span class="c-term">彩色术语</span>；第三遍留意 <span class="u-err">波浪线难点</span> 与 <span class="u-cmp">虚线对比</span>；最后用 <span class="u-bib">实线经文</span> 复述证据。',raw=True))
    b.append(h2('五个数字记住全局','🔢','numbers'))
    b.append('<div class="stats">'+''.join(f'<div class="stat rv"><div class="v">{v}</div><div class="k">{k}</div></div>' for v,k in [('1643','开会·立约'),('1646','信条完成'),('1647','两部要理问答呈交'),('1648','苏格兰批准要理问答'),('33·196·107','章·问·问')])+'</div>')
    b.append(callout('mem-pt','🎵 年代口诀','<b>「四三开会立盟约，四六信条交国会，四七要理双出炉，四八苏格兰全通过。」</b>'))
    b.append(h2('信仰告白33章口诀','📘','wcf33'))
    rhyme=['一经二神三预旨，','四造五护六堕罪，','七约八保九意志，','十召十一称为义，','十二收养十三圣，','十四信心十五悔，','十六善行十七坚，','十八确据十九律，','二十自由二一拜，','二二誓愿二三官，','二四婚姻二五会，','二六相通二七礼，','二八洗礼二九餐，','三十惩戒三一议，','三二死后三三审。']
    b.append('<div class="bigquote rv">'+'<br>'.join(rhyme)+'</div>')
    b.append('<p class="muted">口诀为本站学习整理；各章正式标题见下方记忆宫殿。</p>')
    b.append(h2('记忆宫殿：走过一座「七间房」的教堂','🏛️','palace'))
    rooms=[('rev','🚪 门廊（1）','圣经：进门先读约书',[1]),('god','🕍 中殿（2–5）','神、预旨、创造、护理：抬头仰望穹顶',[2,3,4,5]),('man','🕳️ 地窖（6–9）','堕落、圣约、中保、自由意志：从深处被拯救',[6,7,8,9]),('sal','🌿 回廊（10–18）','呼召→称义→收养→成圣→信→悔→善行→坚忍→确据：一路向前走',list(range(10,19))),('law','📜 法庭（19–24）','律法、自由、敬拜、起誓、官员、婚姻：生活的秩序',list(range(19,25))),('chu','⛪ 圣所（25–31）','教会、相通、圣礼、洗礼、圣餐、惩戒、会议：神的家',list(range(25,32))),('end','🌅 钟楼（32–33）','死后与审判：钟声宣告主必再来',[32,33])]
    b.append('<div class="grid">'+''.join(f'<div class="card rv bl-{c}"><h3>{t}</h3><p>{d}</p><div>'+''.join(f'<a class="pill" href="wcf.html#c{n}">{n}. {esc(wcft[n-1])}</a>' for n in ns)+'</div></div>' for c,t,d,ns in rooms)+'</div>')
    b.append(h2('小要理问答结构口诀','📙','wscmap'))
    b.append('<div class="flow rv">'+''.join(f'<div class="st"><div class="e">{e}</div><b>{t}</b><small>{s}</small></div>' for e,t,s in [('🎯','1–3','目的·准则'),('✨','4–11','神·预旨·创造·护理'),('💔','12–19','约·堕落·罪'),('✝️','20–28','恩典之约·救赎主'),('🌱','29–38','召·义·子·圣'),('🔟','39–81','本分·十诫'),('🔥','82–87','罪·信·悔'),('💧','88–97','道·礼'),('🙏','98–107','祷告·主祷文')])+'</div>')
    b.append(callout('mem-pt','🔟 十诫一句话',raw=True,content='<b>一“谁”二“怎”三“名”四“时”</b>（拜谁·怎样拜·怎样称名·何时拜）；<b>五“权”六“命”七“洁”八“财”九“真”十“心”</b>（权柄·生命·贞洁·财产·真理·心思）。'))
    b.append(callout('mem-pt','🙏 主祷文六求',raw=True,content='<b>前三求为神</b>：愿名为圣、愿国降临、愿旨意行；<b>后三求为我</b>：日用饮食、赦免罪债、不遇试探。'))
    b.append(h2('大要理问答结构口诀','📗','wlcmap'))
    b.append('<div class="flow rv">'+''.join(f'<div class="st"><div class="e">{e}</div><b>{t}</b><small>{s}</small></div>' for e,t,s in [('🎯','1–5','目的·圣经'),('✨','6–20','神·预旨·创造·护理·生命之约'),('💔','21–29','堕落·罪·刑罚'),('🤝','30–35','恩典之约'),('✝️','36–56','中保：位格·三职·两状态'),('⛪','57–65','施行·教会'),('🌱','66–81','恩典中相交'),('🌅','82–90','荣耀中相交'),('📜','91–97','道德律三用'),('🔟','98–148','十诫'),('⚖️','149–153','罪的轻重与出路'),('💧','154–177','圣道与圣礼'),('🙏','178–196','祷告')])+'</div>')
    b.append(callout('mem-pt','🧠 「前90信、后106行」',raw=True,content='大要理问答以<b>第90问</b>为分水岭：<b>1–90</b> 当信什么（神 → 人 → 约 → 基督 → 恩典中 → 荣耀中），<b>91–196</b> 当尽何本分（律法 → 十诫 → 罪与出路 → 蒙恩之道）。口诀：「<b>神人约主，恩荣两交；律诫罪道，祷告收尾</b>」。'))
    b.append(callout('mem-pt','📏 十诫解释八规则（WLC 99，概括）',raw=True,content='<ol style="margin:.3em 0 0 1.2em"><li><b>完全</b>：律法要求全人完全的顺服。</li><li><b>属灵</b>：管到悟性、意志、情感与心灵。</li><li><b>互见</b>：同一件事可在几条诫命中从不同角度被要求或禁止。</li><li><b>正反</b>：吩咐一项本分，就禁止相反的罪；禁止一项罪，就吩咐相反的本分。</li><li><b>时机</b>：所禁止的任何时候都不可行；所吩咐的总是本分，但不是每项本分时时都要做。</li><li><b>同类</b>：一项罪或本分之下，同类的一切连同其原因、手段、机会都包括在内。</li><li><b>推己</b>：自己当守的，也要按身份帮助别人守。</li><li><b>助人</b>：别人当守的，我们要按身份与呼召帮助他们。</li></ol>口诀：「<b>全灵互反，时类己人</b>」。逐字原文见 <a href="wlc.html#q99">大要理第99问</a>。'))
    b.append(h2('翻转卡片：小要理问答','🃏','flashsec'))
    b.append('''<div class="card"><div class="filters"><select id="fRange" class="btn"><option value="1-107">全部 1–107</option><option value="1-38">当信 1–38</option><option value="39-81">十诫 39–81</option><option value="82-107">蒙恩之道 82–107</option></select>
<button class="btn" id="fPrev">⬅️ 上一张</button><button class="btn pri" id="fFlip">🔄 翻转</button><button class="btn" id="fNext">下一张 ➡️</button><button class="btn" id="fRand">🎲 随机</button></div>
<div class="flash" id="flash"><div class="inner"><div class="face front" id="fFront"></div><div class="face back" id="fBack"></div></div></div>
<p class="muted center">点击卡片或按空格翻转；←/→ 切换。</p></div>''')
    b.append(h2('小测验','✅','quizsec'))
    b.append('''<div class="grid g2"><div class="card"><h3>📘 这一章是第几章？</h3><div id="q1"></div></div><div class="card"><h3>📙 这个答案属于哪一问？</h3><div id="q2"></div></div></div>''')
    js='<script>const WSC='+json.dumps(wsc,ensure_ascii=False)+';const WCFT='+json.dumps(wcft,ensure_ascii=False)+''';
window.__pageInit=function(){
 const $=s=>document.querySelector(s); let list=WSC.slice(), i=0;
 const fl=$('#flash'), fr=$('#fFront'), bk=$('#fBack');
 function show(){const u=list[i];fl.classList.remove('flip');fr.innerHTML='<div style="font-size:14px;opacity:.8">小要理 第'+u.q+'问</div><div>'+u.k+'</div>';setTimeout(()=>bk.innerHTML='<div>'+u.a+'</div>',200)}
 $('#fRange').onchange=e=>{const [a,b]=e.target.value.split('-').map(Number);list=WSC.filter(u=>u.q>=a&&u.q<=b);i=0;show()};
 $('#fPrev').onclick=()=>{i=(i-1+list.length)%list.length;show()};$('#fNext').onclick=()=>{i=(i+1)%list.length;show()};
 $('#fRand').onclick=()=>{i=Math.floor(Math.random()*list.length);show()};$('#fFlip').onclick=()=>fl.classList.toggle('flip');fl.onclick=()=>fl.classList.toggle('flip');
 document.addEventListener('keydown',e=>{if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;if(e.key===' '){e.preventDefault();fl.classList.toggle('flip')}if(e.key==='ArrowRight')$('#fNext').click();if(e.key==='ArrowLeft')$('#fPrev').click()});
 show();
 const sh=a=>a.map(x=>[Math.random(),x]).sort((p,q)=>p[0]-q[0]).map(x=>x[1]);
 function quiz(el,mk){let score=0,tot=0;function next(){const {prompt,opts,ans}=mk();el.innerHTML='<p style="font-family:var(--serif);font-size:17px">'+prompt+'</p><div class="filters">'+opts.map(o=>'<button data-v="'+o+'">'+o+'</button>').join('')+'</div><p class="muted">得分 '+score+' / '+tot+'</p>';
   el.querySelectorAll('button').forEach(b=>b.onclick=()=>{tot++;if(+b.dataset.v===ans){score++;b.style.background='#16a34a';b.style.color='#fff'}else{b.style.background='#dc2626';b.style.color='#fff';el.querySelector('[data-v="'+ans+'"]').style.background='#16a34a'}setTimeout(next,900)})}next()}
 quiz($('#q1'),()=>{const n=1+Math.floor(Math.random()*33);const s=new Set([n]);while(s.size<4)s.add(1+Math.floor(Math.random()*33));return {prompt:'“'+WCFT[n-1]+'”是第几章？',opts:sh([...s]),ans:n}});
 quiz($('#q2'),()=>{const u=WSC[Math.floor(Math.random()*WSC.length)];const s=new Set([u.q]);while(s.size<4)s.add(1+Math.floor(Math.random()*107));return {prompt:'“'+(u.a.length>70?u.a.slice(0,70)+'……':u.a)+'”',opts:sh([...s]),ans:u.q}});
};</script>'''
    open(OUT+'memory.html','w').write(page('memory.html','记忆训练','\n'.join(b),js=js))
# ===================== SOURCES =====================
def build_sources():
    b=['<section class="hero"><div class="shine"></div><div class="floaty">🔗</div><h1>🔗 来源 · 致谢 · 版本</h1><p>本站坚持：引用原文逐字照录、注明出处（“ ”内为逐字原文；「 」内为术语或概括）；讲解与图表为学习整理，不冒充原文。</p></section>']
    b.append(h2('原文来源','📚','src'))
    b.append('<div class="tbl"><table><thead><tr><th>内容</th><th>来源</th><th>说明</th></tr></thead><tbody>'
      '<tr><td>西敏信仰告白、大要理问答、小要理问答（全文及证明经文）</td><td><a href="https://rtf-usa.com" target="_blank" rel="noopener">RTF-USA</a>《威斯敏斯特标准》简体中文新版，贾少彬 译，© 2024 RTF-USA</td><td>原书注明“FOR FREE DISTRIBUTION ONLY – NOT FOR SALE”。为1647年原文版本的译本。本站从其公开PDF中提取文字并重新排版；个别排版断行与脚注位置经程序整理，如有出入以原书为准。</td></tr>'
      '<tr><td>三大普世信经、比利时信条、海德堡要理问答、多特信经</td><td><a href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">ccifellowship.org《敬拜手册》</a></td><td>逐字取自网站（2026-10-20 抓取），仅调整排版。用户提供的PDF《中国改革宗教会 敬拜手册（2015版）》与网站同源，本站以网站文本为准。</td></tr>'
      '<tr><td>“我们的信仰”摘录</td><td><a href="https://www.ccreformed.org/our-belief/" target="_blank" rel="noopener">洛杉矶改革宗·恩约教会</a></td><td>逐字摘录</td></tr>'
      '<tr><td>“信仰告白”摘录</td><td><a href="https://www.reformedbeginner.net/statement-of-faith/" target="_blank" rel="noopener">改革宗初学者</a></td><td>逐字摘录</td></tr>'
      '<tr><td>美国修订本对照</td><td><a href="https://opc.org/wcf.html" target="_blank" rel="noopener">opc.org/wcf.html</a></td><td>正统长老会（OPC）现行英文本，用于「1647原文 vs 美国修订本」对照（中文为本站概括）</td></tr>'
      '<tr><td>历史图片</td><td>Wikimedia Commons</td><td>公有领域 / CC0，见各图片说明</td></tr>'
      '<tr><td>离线地图底图（手绘示意图与实景地图的矢量底图）</td><td><a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a> 1:50m / 1:110m 陆地、河流、湖泊（本站合并陆地多边形，不画现代国界）</td><td>公有领域（public domain）</td></tr>'
      '<tr><td>在线地图瓦片 ①</td><td><a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> 标准瓦片（遵守 <a href="https://operations.osmfoundation.org/policies/tiles/" target="_blank" rel="noopener">瓦片使用政策</a>：显示署名、不预取）</td><td>© OpenStreetMap 贡献者，ODbL</td></tr>'
      '<tr><td>在线地图瓦片 ②（自动备用）</td><td><a href="https://www.openstreetmap.fr/" target="_blank" rel="noopener">OSM France</a> 托管的 Humanitarian（HOT）样式</td><td>© OpenStreetMap 贡献者；样式 HOT，托管 OSM France</td></tr>'
      '<tr><td>在线地图瓦片 ③（自动备用）</td><td><a href="https://opentopomap.org/" target="_blank" rel="noopener">OpenTopoMap</a></td><td>Kartendaten: © OpenStreetMap-Mitwirkende, SRTM｜Kartendarstellung: © OpenTopoMap（CC-BY-SA）</td></tr>'
      '</tbody></table></div>')
    b.append(h2('延伸学习资源','🧭','more'))
    links=[('欧陆改革宗','https://canrc.org','Canadian Reformed Churches'),('欧陆改革宗','https://www.urcna.org','United Reformed Churches in North America'),('欧陆改革宗','https://heritagereformed.com','Heritage Reformed Congregations'),('欧陆改革宗','https://www.prca.org','Protestant Reformed Churches in America'),('长老会改革宗','https://opc.org','Orthodox Presbyterian Church（含西敏标准英文本）'),('神学院','https://www.wts.edu','Westminster Theological Seminary（含 WCF 英文本 wts.edu/wcf）'),('神学院','https://crts.edu','Canadian Reformed Theological Seminary'),('神学院','https://canadianreformedseminary.ca','Canadian Reformed Seminary'),('中文','https://ccifellowship.org','中国改革宗教会（敬拜手册、海德堡要理问答证道）'),('中文','https://www.ccreformed.org','洛杉矶改革宗·恩约教会'),('中文','https://www.reformedbeginner.net','改革宗初学者'),('中文','https://rtf-usa.com','RTF-USA 改革宗翻译社')]
    b.append('<div class="grid g4">'+''.join(f'<a class="card navcard" href="{u}" target="_blank" rel="noopener"><span class="pill">{k}</span><h3 style="font-size:16px">{u.replace("https://","")}</h3><p>{d}</p></a>' for k,u,d in links)+'</div>')
    b.append(h2('版本记录','🗂️','versions'))
    b.append('<div class="tl"><div class="ev big" style="--dot:var(--a1)"><span class="y">v3.0 · 2026-10-23</span>聚焦「历史 · 地图 · 文化」：新增<a href="atlas.html">🧭 地图集</a>（宗教改革欧洲、1640年代不列颠群岛、伦敦西敏区与耶路撒冷厅、西敏标准的全球旅程、欧陆改革宗 vs 长老会地理），每张图都有离线可用的手绘示意图（动画路线与地标）和可缩放的实景地图（自带 Natural Earth 底图 + 三家免密钥瓦片自动切换）、本图时间线、文化特征与来源；主要信条年代图；右下角悬浮导航（首页/目录/后退/前进/顶部/底部 + 阅读进度）；页面间视图过渡与悬停预取；新增「史卷」配色；标注系统扩充（年代、地名、人物、蓝/绿底、双下划线、左色条段落）；信仰告白页渲染分块以减少长任务。v2.1 存档：<a href="https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v2.1-20261022" target="_blank" rel="noopener">GitHub Release v2.1-20261022</a>。</div><div class="ev" style="--dot:#0891b2"><span class="y">v2.1 · 2026-10-22</span>流程图与思维导图改为构建时预渲染的 SVG（页面不再运行 Mermaid，颜色随主题切换）；Mermaid / Leaflet / Lenis 全部自托管，不依赖 CDN（只有地图底图来自 OpenStreetMap）；大、小要理问答每个板块新增「圣约神学 · 长老会正统 · 生活应用」三个视角；记忆训练新增大要理结构口诀与「十诫解释八规则」口诀。v2.0 存档：<a href="https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v2.0-20261021" target="_blank" rel="noopener">GitHub Release v2.0-20261021</a>。</div><div class="ev" style="--dot:#7c3aed"><span class="y">v2.0 · 2026-10-21</span>性能重构（移除大面积毛玻璃与模糊动画、Mermaid/Leaflet 按需懒加载、content-visibility、rAF 节流、脚本 defer、电脑端丝滑滚动）；5 套配色 × 浅/深/跟随系统；全站统一标注系统与图例；每章新增「长老会正统」与「常见误解」；1647 原文 vs 美国修订本对照；救恩次序链、篇幅统计图、环形图、韦恩图、背诵进度环；引文规范（“ ”=逐字原文，「 」=概括）并全面复核。v1.0 存档：<a href="https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v1.0-20261020" target="_blank" rel="noopener">GitHub Release v1.0-20261020</a>。</div><div class="ev" style="--dot:#16a34a"><span class="y">v1.0 · 2026-10-20</span>首次发布：总览（整本圣经/圣约神学/思维导图/欧陆视角/多视角）、历史地理（时间线/故事线/Leaflet地图/人物/文化区域）、信仰告白33章逐章精解、大要理196问与小要理107问分组精解、深度对比、背诵版、记忆训练、信经与三项联合信条原文、来源页。</div></div>')
    b.append(h2('图片署名','🖼️','credits'))
    b.append('<ul>'+''.join(f'<li><a href="{m["page"]}" target="_blank" rel="noopener">{esc(m["title"])}</a> — {esc(m["license"])}</li>' for m in CRED.values())+'</ul>')
    open(OUT+'sources.html','w').write(page('sources.html','来源 · 致谢 · 版本','\n'.join(b)))
if __name__=='__main__':
    build_index(); build_history(); build_atlas(); build_compare(); build_memory(); build_sources(); print('pages ok')
