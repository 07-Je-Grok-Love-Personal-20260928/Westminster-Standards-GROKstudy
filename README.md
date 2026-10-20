# 威斯敏斯特标准-20261020-v1.0-GROKstudy

**Westminster-Standards-20261020-v1.0-GROKstudy**：《威斯敏斯特信仰告白》《威斯敏斯特大要理问答》《威斯敏斯特小要理问答》深度学习站（简体中文）。

## 🌐 在线访问（3 个部署）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Westminster-Standards-GROKstudy/ |
| Surge | https://westminster-standards-20261020-v1-grokser.surge.sh |
| Netlify | https://westminster-standards-20261020-v1-grokser.netlify.app |

源码仓库：https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy

## 📚 内容

| 页面 | 内容 |
|---|---|
| `index.html` 总览 | 为什么写/写了什么/怎样用；整本圣经救赎历史主线与西敏标准、三项联合信条对照表；圣约神学结构图；三份文件思维导图；欧陆改革宗阅读视角；八种解读视角 |
| `history.html` 历史·地理 | 可筛选时间线（325–2024）、六幕故事线、Leaflet 互动地图（西敏寺、耶路撒冷厅、爱丁堡、海德堡、多特等）、历史图片、人物与派别、文化区域特征表 |
| `wcf.html` 信仰告白 | 33 章全文（172 节，附证明经文）＋逐章：核心要义、圣经神学、圣约神学、欧陆改革宗视角、难点、应用、记忆钩子、三项联合信条原文对照 |
| `wlc.html` 大要理问答 | 196 问全文，分 15 个主题板块精解 |
| `wsc.html` 小要理问答 | 107 问全文，分 10 个主题板块精解 |
| `compare.html` 深度对比 | 三份文件对比、为何三份而非一份、各自要解决的问题、教义位置矩阵、西敏标准 vs 三项联合信条、与三大普世信经的关系 |
| `recite.html` 背诵版 | 三份文件干净全文；阅读 / 遮盖答案 / 首字提示三种模式；字号调节；已背进度（本机保存） |
| `memory.html` 记忆训练 | 年代口诀、33 章口诀、记忆宫殿、十诫与主祷文口诀、小要理翻转卡片、小测验 |
| `creeds.html` 信经与联合信条 | 三大普世信经、比利时信条、海德堡要理问答、多特信经（逐字取自 ccifellowship.org） |
| `sources.html` 来源 | 原文来源、延伸资源、版本记录、图片署名 |

## 🔖 原文来源

- 西敏三份文件中文正文：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024 RTF-USA，免费分发，非卖品），1647 原文版本译本。
- 三大普世信经、三项联合信条：https://ccifellowship.org （中国改革宗教会《敬拜手册》），逐字照录。
- 摘录：https://www.ccreformed.org/our-belief/ 、https://www.reformedbeginner.net/statement-of-faith/
- 图片：Wikimedia Commons（公有领域 / CC0）；地图：© OpenStreetMap 贡献者。
- 讲解、图表、口诀为学习整理，不代表任何教会的官方解释。

## 🛠️ 目录结构与构建

```
docs/            # 发布的静态网站（GitHub Pages / Surge / Netlify 均发布此目录）
build/           # 生成器（Python 3）
  data/standards.json   # 从 RTF-USA PDF 提取的西敏三份文件（含证明经文）
  data/cci_struct.json  # 从 ccifellowship.org 抓取的信经与三项联合信条
  content_wcf.py        # 信仰告白逐章解读
  content_more.py       # 大小要理分组解读、时间线、地图数据
  build_docs.py         # 生成 wcf/wlc/wsc/recite/creeds 页面
  build_pages.py        # 生成 index/history/compare/memory/sources 页面
```

重新生成：`cd build && python3 build_docs.py && python3 build_pages.py`

部署：
```bash
surge docs westminster-standards-20261020-v1-grokser.surge.sh
netlify deploy --prod --dir docs --site <site-id>
```

## 🗂️ 版本说明

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v1.0 | 2026-10-20 | 首次发布：10 个页面；三份西敏文件全文与证明经文；逐章/分组解读；时间线、故事线、互动地图；Mermaid 流程图与思维导图；深度对比；背诵模式与记忆训练；三大普世信经与三项联合信条原文；毛玻璃 UI、深浅色主题、可隐藏目录、手机/平板/电脑自适应。 |

后续版本请按 `主题-日期-版本号-GROKser` 规则更新 Surge / Netlify 域名，并在此表追加记录。
