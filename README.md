# 威斯敏斯特标准-20261021-v2.0-GROKstudy

**Westminster-Standards-20261021-v2.0-GROKstudy**：《威斯敏斯特信仰告白》《威斯敏斯特大要理问答》《威斯敏斯特小要理问答》深度学习站（简体中文）。

## 🌐 在线访问（v2.0，当前版本）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Westminster-Standards-GROKstudy/ |
| Surge | https://westminster-standards-20261021-v2-grokser.surge.sh |
| Netlify | https://westminster-standards-20261021-v2-grokser.netlify.app |

### 🗄️ v1.0 存档（2026-10-20，仍可访问）

| 内容 | 链接 |
|---|---|
| Git 标签 / Release（含整站 zip） | https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v1.0-20261020 |
| Surge（v1） | https://westminster-standards-20261020-v1-grokser.surge.sh |
| Netlify（v1） | https://westminster-standards-20261020-v1-grokser.netlify.app |

恢复 v1：`git checkout v1.0-20261020`（静态站点在 `docs/`），或下载 Release 中的 zip。

源码仓库：https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy

## 📚 内容

| 页面 | 内容 |
|---|---|
| `index.html` 总览 | 为什么写/写了什么/怎样用；整本圣经救赎历史主线与西敏标准、三项联合信条对照表；圣约神学结构图；三份文件思维导图；欧陆改革宗阅读视角；八种解读视角 |
| `history.html` 历史·地理 | 可筛选时间线（325–2024）、六幕故事线、Leaflet 互动地图（西敏寺、耶路撒冷厅、爱丁堡、海德堡、多特等）、历史图片、人物与派别、文化区域特征表 |
| `wcf.html` 信仰告白 | 33 章全文（172 节，附证明经文）＋逐章：核心要义、圣经神学、圣约神学、欧陆改革宗视角、难点、应用、记忆钩子、三项联合信条原文对照 |
| `wlc.html` 大要理问答 | 196 问全文，分 15 个主题板块精解 |
| `wsc.html` 小要理问答 | 107 问全文，分 10 个主题板块精解 |
| `compare.html` 深度对比 | 三份文件对比与韦恩图、为何三份而非一份、问题→文件流程图、教义位置矩阵、西敏标准 vs 三项联合信条（标出侧重不同）、1647原文 vs 美国修订本、与三大普世信经的关系 |
| `recite.html` 背诵版 | 三份文件干净全文；阅读 / 遮盖答案 / 首字提示三种模式；字号调节；已背进度（本机保存） |
| `memory.html` 记忆训练 | 背诵进度环、标注记忆法、年代口诀、33 章口诀、记忆宫殿、十诫与主祷文口诀、小要理翻转卡片、小测验 |
| `creeds.html` 信经与联合信条 | 三大普世信经、比利时信条、海德堡要理问答、多特信经（逐字取自 ccifellowship.org） |
| `sources.html` 来源 | 原文来源、延伸资源、版本记录、图片署名 |

## 🖍️ 标注系统（全站统一，右上角 🖍️ 查看图例）

| 标注 | 含义 |
|---|---|
| **粗体** | 关键词 |
| 彩色字 | 神学术语 |
| 荧光底 | 必背金句 / 核心结论 |
| 实线下划线 | 圣经出处 |
| 虚线下划线 | 对比 / 区别 |
| 波浪线 | 难点 / 易错 / 争议 |
| 小标签 `WLC 31` | 文献交叉索引 |
| “ ” | 原文逐字引用 |
| 「 」 | 术语 / 口诀 / 概括（非原文） |

提示框：🎯 核心要义 · 🔍 难点辨析 · 🧠 记忆钩子 · 🚫 常见误解 · 🛠️ 生活应用 · 📚 圣经神学 · 🤝 圣约神学 · 🇳🇱 欧陆改革宗 · 🏴 长老会正统。

## 🎨 主题

5 套配色（晨曦 · 翡翠 · 绛红金 · 深海 · 暮光）× 浅色 / 深色 / 跟随系统；设置保存在 localStorage，页面加载前即应用（无闪烁）。

## ⚡ 性能（v1.0 → v2.0）

测量环境：本机 headless Chromium；Lighthouse 12.8 移动端默认模拟（慢速 4G + 4 倍 CPU 降速，本地服务器未开 gzip）；滚动测试为 5 秒连续滚动的帧间隔统计（脚本见 `build/perf/`）。

| 页面 | Lighthouse 分数 | FCP | LCP | 传输量 |
|---|---|---|---|---|
| 总览 index | 41 → **99** | 12.7 s → **1.1 s** | 13.4 s → **2.1 s** | 2,238 → **227 KiB** |
| 信仰告白 wcf | 55 → **74** | 25.9 s → **3.5 s** | 26.8 s → **5.0 s** | 4,953 → **793 KiB** |
| 背诵版 recite | 55 → **88** | 14.6 s → **3.0 s** | 15.8 s → **3.2 s** | 2,742 → **462 KiB** |
| 历史 history | 60 → **97** | 6.2 s → **1.1 s** | 7.9 s → **2.6 s** | 1,364 → **308 KiB** |

| 滚动帧率（1440px 电脑） | v1.0 | v2.0 |
|---|---|---|
| index | 39.9 fps（卡顿帧 10%） | **59.3 fps**（0.3%） |
| wcf | 40.9 fps（9.2%） | **60.1 fps**（0%） |
| recite | 30.3 fps（27%） | **60.1 fps**（0%） |
| history | 36.1 fps（18.2%） | **60.0 fps**（0%） |
| compare | 55.6 fps（1.8%） | **59.9 fps**（0%） |

手机（390px，4 倍 CPU 降速）滚动 56.6–60.2 fps；首次滚到图表时，Mermaid 在滚动停顿的空闲时间渲染。

## 🔖 原文来源

- 西敏三份文件中文正文：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024 RTF-USA，免费分发，非卖品），1647 原文版本译本。
- 三大普世信经、三项联合信条：https://ccifellowship.org （中国改革宗教会《敬拜手册》），逐字照录。
- 摘录：https://www.ccreformed.org/our-belief/ 、https://www.reformedbeginner.net/statement-of-faith/
- 美国修订本对照：https://opc.org/wcf.html （OPC 现行英文本）
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
  content_v2.py         # v2：长老会正统视角、常见误解、美国修订对照、图例
  audit.py / fixquotes.py # 引文核对：“ ”内文字须与原文语料逐字一致
  perf/                 # 性能与布局检查脚本（Lighthouse、滚动帧率、3 宽度 × 10 主题检查）
  build_docs.py         # 生成 wcf/wlc/wsc/recite/creeds 页面
  build_pages.py        # 生成 index/history/compare/memory/sources 页面
```

重新生成：`cd build && python3 build_docs.py && python3 build_pages.py`

部署：
```bash
surge docs westminster-standards-20261021-v2-grokser.surge.sh   # 部署后删除 surge 生成的 docs/CNAME
netlify deploy --prod --dir docs --site <site-id>
```

## 🗂️ 版本说明

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v2.0 | 2026-10-21 | **性能**：移除大面积 backdrop-filter 与模糊动画（仅顶栏保留轻度毛玻璃）；Mermaid（ESM 分包）与 Leaflet 改为进入视口才加载；长内容 `content-visibility:auto`；滚动处理 rAF 节流 + passive；脚本 defer；去掉阻塞渲染的网络字体；电脑端 Lenis 丝滑滚动（手机原生）；尊重“减少动态效果”。**主题**：5 套配色 × 浅/深/跟随系统，无闪烁。**标注系统**：统一图例（粗体/彩色术语/荧光/实线·虚线·波浪下划线/交叉索引/提示框）。**内容**：每章新增「长老会正统」与「常见误解」，解读改为标签页以精简篇幅；1647原文 vs 美国修订本对照；救恩次序链；篇幅统计、环形图、韦恩图、问题→文件流程图、两大传统谱系图、背诵进度环。**引文规范**：“ ”只用于逐字原文（程序核对 RTF 译本与 ccifellowship 语料，圣经引文按和合本核对），其余改用「 」。 |
| v1.0 | 2026-10-20 | 首次发布：10 个页面；三份西敏文件全文与证明经文；逐章/分组解读；时间线、故事线、互动地图；Mermaid 流程图与思维导图；深度对比；背诵模式与记忆训练；三大普世信经与三项联合信条原文；毛玻璃 UI、深浅色主题、可隐藏目录、手机/平板/电脑自适应。 |

v1.0 归档：Git 标签 `v1.0-20261020` 与 GitHub Release（含整站 zip）。

后续版本请按 `主题-日期-版本号-GROKser` 规则更新 Surge / Netlify 域名，并在此表追加记录。
