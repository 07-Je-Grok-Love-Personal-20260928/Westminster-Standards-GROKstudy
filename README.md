# 威斯敏斯特标准-20261022-v2.1-GROKstudy

**Westminster-Standards-20261022-v2.1-GROKstudy**：《威斯敏斯特信仰告白》《威斯敏斯特大要理问答》《威斯敏斯特小要理问答》深度学习站（简体中文）。

## 🌐 在线访问（v2.1，当前版本）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Westminster-Standards-GROKstudy/ |
| Surge | https://westminster-standards-20261022-v2-1-grokser.surge.sh |
| Netlify | https://westminster-standards-20261022-v2-1-grokser.netlify.app |

GitHub Release：https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v2.1-20261022

### 🗄️ 历史版本存档（仍可访问）

| 版本 | Git 标签 / Release（含整站 zip） | Surge | Netlify |
|---|---|---|---|
| v2.0（2026-10-21） | [v2.0-20261021](https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v2.0-20261021) | https://westminster-standards-20261021-v2-grokser.surge.sh | https://westminster-standards-20261021-v2-grokser.netlify.app |
| v1.0（2026-10-20） | [v1.0-20261020](https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy/releases/tag/v1.0-20261020) | https://westminster-standards-20261020-v1-grokser.surge.sh | https://westminster-standards-20261020-v1-grokser.netlify.app |

GitHub Pages 始终显示最新版本。恢复旧版：`git checkout v2.0-20261021` 或 `git checkout v1.0-20261020`（静态站点在 `docs/`），或下载对应 Release 中的 zip。

源码仓库：https://github.com/07-Je-Grok-Love-Personal-20260928/Westminster-Standards-GROKstudy

## 📚 内容

| 页面 | 内容 |
|---|---|
| `index.html` 总览 | 为什么写/写了什么/怎样用；整本圣经救赎历史主线与西敏标准、三项联合信条对照表；圣约神学结构图；三份文件思维导图；欧陆改革宗阅读视角；八种解读视角 |
| `history.html` 历史·地理 | 可筛选时间线（325–2024）、六幕故事线、Leaflet 互动地图（西敏寺、耶路撒冷厅、爱丁堡、海德堡、多特等）、历史图片、人物与派别、文化区域特征表 |
| `wcf.html` 信仰告白 | 33 章全文（172 节，附证明经文）＋逐章：核心要义、圣经神学、圣约神学、欧陆改革宗视角、难点、应用、记忆钩子、三项联合信条原文对照 |
| `wlc.html` 大要理问答 | 196 问全文，分 15 个主题板块；每个板块有核心要义，以及圣经神学 / 圣约神学 / 欧陆对照 / 长老会正统 / 应用五个视角，另附记忆钩子 |
| `wsc.html` 小要理问答 | 107 问全文，分 10 个主题板块，各板块的视角与大要理相同 |
| `compare.html` 深度对比 | 三份文件对比与韦恩图、为何三份而非一份、问题→文件流程图、教义位置矩阵、西敏标准 vs 三项联合信条（标出侧重不同）、1647原文 vs 美国修订本、与三大普世信经的关系 |
| `recite.html` 背诵版 | 三份文件干净全文；阅读 / 遮盖答案 / 首字提示三种模式；字号调节；已背进度（本机保存） |
| `memory.html` 记忆训练 | 背诵进度环、标注记忆法、年代口诀、33 章口诀、记忆宫殿、十诫与主祷文口诀、大要理结构口诀、十诫解释八规则（WLC 99）口诀、小要理翻转卡片、小测验 |
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

## ⚡ 性能

### v2.0 → v2.1（Google Chrome 155 headless，本地服务器未开 gzip）

| 页面 | Lighthouse 移动端分数 | FCP | LCP | TBT |
|---|---|---|---|---|
| 总览 index | 93 → **94** | 2.1 s → 2.3 s | 2.9 s → **2.6 s** | 30 → **20 ms** |
| 信仰告白 wcf | 68 → **70** | 4.5 s → **4.4 s** | 5.7 s → **5.1 s** | 10 → **0 ms** |
| 背诵版 recite | 82 → 82 | 3.6 s → 3.6 s | 3.6 s → 3.6 s | 0 → 0 ms |
| 历史 history | 97 → 96 | 1.3 s → 1.7 s | 2.6 s → 2.6 s | 20 → **0 ms** |

| 滚动测试（5 秒连续滚动） | v2.0 | v2.1 |
|---|---|---|
| 手机 390px（CPU 降速 4 倍）index | 57.2 fps，长任务 282 ms | **60.2 fps，长任务 0 ms** |
| 手机 390px compare | 58.0 fps，长任务 181 ms | **60.2 fps，长任务 0 ms** |
| 手机 390px wcf / recite / history | 59.1 / 60.2 / 59.0 fps | 59.1 / 60.2 / 59.3 fps（history 长任务 102 → 60 ms） |
| 电脑 1440px（5 页） | 59.3–60.2 fps | 58.0–60.1 fps，长任务只在 wcf 出现（51 ms） |

v2.1 的主要改进：流程图与思维导图在构建时预渲染为 SVG，页面不再下载和运行约 3 MB 的 Mermaid，这消除了滚动到图表时出现的长任务；地图初始化也推迟到滚动停下之后。

### v1.0 → v2.0

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
- 第三方库（均自托管于 `docs/assets/vendor/`，附各自 LICENSE）：Mermaid 10.9.1（只在构建时使用，页面中作为备用）、Leaflet 1.9.4、Lenis 1.1.20。只有地图底图从 OpenStreetMap 在线加载。
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
  content_v21.py        # v2.1：大小要理各板块的圣约神学 / 长老会正统 / 应用
  prerender_mermaid.py  # v2.1：构建时把 Mermaid 渲染为 SVG（颜色替换为 CSS 变量，可随主题切换；结果缓存在 data/mermaid_cache.json）
  build_all.sh          # 一键构建：生成页面 → 预渲染图表 → 引文核对
  audit.py / fixquotes.py # 引文核对：“ ”内文字须与原文语料逐字一致
  perf/                 # 性能与布局检查脚本（Lighthouse、滚动帧率、3 宽度 × 10 主题检查）
  build_docs.py         # 生成 wcf/wlc/wsc/recite/creeds 页面
  build_pages.py        # 生成 index/history/compare/memory/sources 页面
```

重新生成：`build/build_all.sh`（只有图表源码改动时才需要 Playwright + Chrome）

部署：
```bash
npx -y surge docs westminster-standards-20261022-v2-1-grokser.surge.sh   # 部署后删除 surge 生成的 docs/CNAME
npx -y netlify-cli deploy --prod --dir docs --site <site-id>
```

## 🗂️ 版本说明

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v2.1 | 2026-10-22 | **性能**：Mermaid 图表改为构建时预渲染的 SVG，颜色用 CSS 变量，随 5 套配色和浅/深色切换；页面不再运行 Mermaid，滚动到图表时的长任务消失；宽图在手机上可横向滑动。Mermaid / Leaflet / Lenis 全部自托管，不依赖 CDN。地图在滚动停下后才初始化。**内容**：大、小要理问答 25 个板块各新增「圣约神学 · 长老会正统 · 生活应用」三个标签页；记忆训练新增大要理结构口诀与「十诫解释八规则」口诀。**检查**：10 页 × 3 种宽度 × 10 种主题组合，无溢出、无重叠、无 JS 错误；引文核对通过。 |
| v2.0 | 2026-10-21 | **性能**：移除大面积 backdrop-filter 与模糊动画（仅顶栏保留轻度毛玻璃）；Mermaid（ESM 分包）与 Leaflet 改为进入视口才加载；长内容 `content-visibility:auto`；滚动处理 rAF 节流 + passive；脚本 defer；去掉阻塞渲染的网络字体；电脑端 Lenis 丝滑滚动（手机原生）；尊重“减少动态效果”。**主题**：5 套配色 × 浅/深/跟随系统，无闪烁。**标注系统**：统一图例（粗体/彩色术语/荧光/实线·虚线·波浪下划线/交叉索引/提示框）。**内容**：每章新增「长老会正统」与「常见误解」，解读改为标签页以精简篇幅；1647原文 vs 美国修订本对照；救恩次序链；篇幅统计、环形图、韦恩图、问题→文件流程图、两大传统谱系图、背诵进度环。**引文规范**：“ ”只用于逐字原文（程序核对 RTF 译本与 ccifellowship 语料，圣经引文按和合本核对），其余改用「 」。 |
| v1.0 | 2026-10-20 | 首次发布：10 个页面；三份西敏文件全文与证明经文；逐章/分组解读；时间线、故事线、互动地图；Mermaid 流程图与思维导图；深度对比；背诵模式与记忆训练；三大普世信经与三项联合信条原文；毛玻璃 UI、深浅色主题、可隐藏目录、手机/平板/电脑自适应。 |

归档：Git 标签 `v1.0-20261020`、`v2.0-20261021`、`v2.1-20261022`，每个都有对应的 GitHub Release（含整站 zip）。

后续版本请按 `主题-日期-版本号-GROKser` 规则更新 Surge / Netlify 域名，并在此表追加记录。
