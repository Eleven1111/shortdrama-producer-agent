# shortdrama-producer-agent

**用大白话描述想法，拿到可直接开拍的生产级视频 prompt。**

shortdrama-producer 是一个视频 prompt 生产 Agent：你用日常语言说想法，它按真实剧组
的写法产出 Seedance / 可灵 / Sora 等模型的完整 prompt。它的每条规则都追溯自
**588,686 条真实生产资产**的测量，而不是 prompt 写作的江湖经验。

运行于 Claude Code · Codex · Cursor · Windsurf · Gemini CLI · GitHub Copilot · WorkBuddy。
只写 prompt 和脚本——绝不提交渲染任务、绝不花你的额度。

**当前版本 v3.14.0** · 架构图见 [docs/](docs)

语言：[中文](#中文) · [English](#english)

---

## 中文

### 30 秒上手

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

重启终端，然后直接说人话：

```
雨夜，一个女孩在便利店门口等人
```

这就是一条完整请求。焦段、画幅、负面约束、平台上限——都是 Agent 的活，你不需要懂。

### FABE：它凭什么值得用

每行按「特征 → 优势 → 收益 → 证据」读完，30 秒判断适不适合你：

| 特征 Feature | 优势 Advantage | 收益 Benefit（对你） | 证据 Evidence |
|---|---|---|---|
| **语料驱动生成**：每条 prompt 先检索 7,824 条真实生产范例，模仿真实写法 | 形态落在真实生产的安全区，不是「cinematic, 4k」套话 | 首次可用率高，少交试错学费 | folder 级 Recall@1 **80.0%**、Recall@5 **100%**（固定种子可复现，`scripts/eval_retrieval.py`） |
| **导演工艺层**（14 节）：一镜一动机、光=情绪、保真预算、终点画像、2D 媒介语法 | 从「语料里大家怎么写」升级到「为什么这么写」 | 镜头有导演意图，成片有戏，不飘 | 每条工艺可追溯测量，二手经验标注置信度 |
| **跨镜一致性机制**：三面板设定图 + 锚点逐字复用 + 版本注册表 | 一致性靠图锁定，不靠重复文本 | 同一角色全剧一张脸 | 真实资产 **87.32%** 带参考图；**46.8%** 带 `_vN` 版本 |
| **三级生产模式**：单镜 → 短剧（镜间闭环）→ 长片（五层状态栈） | 每级是前级的严格超集，规则不换体系 | 从一条 prompt 到一部剧，同一套方法 | 集内节奏用 **137 场 / 42 转场 / 14 冲突模式**实测数据校准 |
| **10 种模型方言路由** | 工艺层不变，只翻译语法 | 换模型不用重学 | 每族方言依据官方文档调研，置信度分级标注 |
| **交付前机械化质检**：12 道门 + 反渣词库 + 连续性链检查，fail 回炉 | 交付前拦截，不是交付后道歉 | 你拿到的都是过闸成品 | 4,154 组真实修订统计支撑；结构校验做过故障注入测试 |

### 架构

三张图看懂全部信息流（SVG 源文件在 [docs/](docs)）：

![端到端信息流](docs/architecture-e2e.svg)
*端到端流转：输入 → 路由 → 知识层（按需拉取）→ 生成层（单镜 / 短剧双管线）→ 质检层（fail 红色虚线回炉）→ 输出层。底部虚线框为开发期 harness，不进运行时。*

![短剧镜间闭环](docs/architecture-shot-loop.svg)
*短剧模式每镜一轮循环：节拍桶分账 → 逐镜 prompt → 连续性闸门 → 用户接受 → 状态机更新 → 下一镜。只有已接受镜头进入 canon。*

![长片五层状态栈](docs/architecture-longform.svg)
*长片模式（≥3 集 / ≥60 镜 / 电影）叠加五层状态栈：项目圣经 → 集圣经 → 场景卡 → 批次状态机 → 镜，每层各有冻结点。*

### 三种生产模式

| 模式 | 触发 | 你额外拿到 |
|---|---|---|
| 单镜头 | 一条需求 | 一条可粘贴 prompt（cinema 600-2000 词 / quick 80-300） |
| 短剧 | 多镜头 / 分镜 | 故事拆解 · 角色设定图 prompt · 连续性圣经 · 分镜表 · 镜间状态机 |
| 长片 | ≥3 集 / ≥60 镜 / 电影 | 五层状态栈 · 集内节奏实测校准 · 风格先导批 · 跨集版本注册表 |

### 模型方言

Seedance 原生。点名其他模型时自动翻译方言（工艺层不变）：
**Gemini Omni · 可灵 Kling · Sora · Runway · 海螺 Hailuo · 即梦 Jimeng · Vidu · Wan · Pika**。
每族方言（时长上限 / 对白引号 / 音频写法 / 参考槽位）依据官方文档调研，置信度分级。

### 使用方式

Agent 动手前先选交付物：

| 你说 | 你拿到 |
|---|---|
| *（没特别说）* | 完整方案：简报 + 素材映射 + 连续性 + 可粘贴 prompt |
| 「只要提示词」 | 一个 `text` 代码块，别的都没有 |
| 「只要脚本」 | 可拍脚本，不含 prompt 外壳 |
| 「为什么效果差」 | 只诊断——不会擅自重写你的东西 |
| 「按原结构改」 | 定点修改，并说明改了什么 |

诊断你已有的 prompt：

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

### 安装

```bash
./install.sh                          # 自动检测终端
./install.sh --target codex           # 指定终端
./install.sh --update                 # 更新已安装版本
```

### 设计哲学

- **每条规则都用一次测量换取自己的位置。** 追溯不到统计的经验不进库；二手证据如实标注。
- **自主 = 你永远不做技术活**，不是 Agent 从不提问。只有「猜错代价高」的维度才问，
  一律给具体选项，最多一轮。
- **学写法，不拿内容。** 源项目的角色、道具、世界观在明确黑名单里，绝不进你的产出。

### 诚实的边界

- **产出质量尚未用真实渲染验证。** A/B 框架（`eval/render_loop/`）就绪、24 条 prompt
  已备、金丝雀纪律已立，但渲染未跑。在那之前，本项目不对真实成片质量做任何声称。
- 检索语料中 Hell Grind 为 0.9% 采样；Cully Hill Boys 为 cluster 去重后全文件夹覆盖。
- 平台数据二手来源标注未验证。**运行时 UI 永远优先于本仓库。**

### 验证

```bash
python3 scripts/validate_structure.py   # 结构防腐（契约·镜像·死链）
python3 scripts/eval_retrieval.py       # 检索质量，固定种子
python3 scripts/continuity_check.py     # 短剧批次连续性链核对
```

### 致谢

本项目站在这些项目的肩膀上，特此感谢：

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)**（MIT，by @iamemily2050）
  —— 反渣词库六类渣词与题材禁区、2D/动漫媒介语法、终点画像、失败图谱、
  续写五模式、保真预算分配、金丝雀渲染纪律均蒸馏自其 Skill OS v6.7，全部按本项目
  红线裁剪并标注来源。
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)**
  —— 本次蒸馏旅程的入口：其对照分析报告指明了 Emily2040 仓库这一更优来源。
- 语料来源项目（Hell Grind / Cully Hill Boys 公开资产）的创作者们——匿名化处理见
  [NOTICE.md](NOTICE.md)。

### 许可证

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
语料来源与第三方权利声明：[NOTICE.md](NOTICE.md)

---

## English

### Quick start in 30 seconds

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

Restart your terminal, then just talk:

```
A rainy night. A girl waiting outside a convenience store.
```

That is a complete request. Focal lengths, aspect ratios, negative constraints and
platform ceilings are the agent's job, not yours.

### Why this agent (FABE)

Each row reads Feature → Advantage → Benefit → Evidence:

| Feature | Advantage | Benefit (to you) | Evidence |
|---|---|---|---|
| **Corpus-driven generation**: every prompt is grounded in 7,824 retrieved real production prompts | Output lands in the safe zone of how crews actually write | High first-try usability, less tuition paid in failed renders | Folder-level Recall@1 **80.0%**, Recall@5 **100%** (fixed seed, `scripts/eval_retrieval.py`) |
| **Directorial craft layer** (14 sections): one intention per shot, light = emotion, fidelity budget, ending profiles, 2D medium grammar | Upgrades from "how corpora write" to "why this, here" | Shots carry intent; footage feels directed, not generated | Every rule traces to a measurement; second-hand knowledge is confidence-labelled |
| **Cross-shot consistency**: three-panel character sheets + verbatim anchors + version registry | Identity is locked by images, not repeated text | One face for the whole series | **87.32%** of source assets carry references; **46.8%** carry `_vN` versions |
| **Three production modes**: single shot → short drama (per-shot loop) → long-form (five-layer state stack) | Each level is a strict superset of the last — one system throughout | The same method scales from one prompt to a series | Episode rhythm calibrated on **137 scenes / 42 transitions / 14 conflict patterns** of real data |
| **10 model dialects** | Craft layer unchanged, syntax translated | Switch models without relearning | Each dialect researched from official docs, confidence-graded |
| **Mechanical pre-delivery QC**: 12 gates + anti-slop lexicon + continuity chain check, fail loops back | Catches problems before delivery, not after | You only ever receive gated output | Backed by 4,154 real revision statistics; structural checks are fault-injection tested |

### Architecture

Three diagrams cover the whole information flow (SVG sources in [docs/](docs)):

![End-to-end information flow](docs/architecture-e2e.svg)
*Input → routing → knowledge (pulled on demand) → generation (single-shot / short-drama pipelines) → QC with a fail loop back into generation → delivery. The dashed band at the bottom is the dev-time harness.*

![Short-drama per-shot loop](docs/architecture-shot-loop.svg)
*Short drama runs one loop per shot: beat buckets → per-shot prompt → continuity gates → user acceptance → state machine → next shot. Only accepted shots enter canon.*

![Long-form five-layer state stack](docs/architecture-longform.svg)
*Long-form (≥3 episodes / ≥60 shots / film) layers a five-state-stack protocol on top: project bible → episode bible → scene card → batch state machine → shot, each with its own freeze point.*

### Three production modes

| Mode | Trigger | You additionally get |
|---|---|---|
| Single shot | one request | one paste-ready prompt (cinema 600-2000 words / quick 80-300) |
| Short drama | multi-shot / storyboard | story breakdown · character-sheet prompts · continuity bible · shotlist · per-shot state machine |
| Long-form | ≥3 episodes / ≥60 shots / film | five-layer state stack · measured episode rhythm · style-pilot batch · cross-episode version registry |

### Model dialects

Seedance native. Naming another model triggers dialect translation (craft layer unchanged):
**Gemini Omni · Kling · Sora · Runway · Hailuo · Jimeng · Vidu · Wan · Pika**.
Each dialect (duration ceilings, dialogue quoting, audio phrasing, reference slots) is
researched from official documentation and confidence-graded.

### Usage

The agent picks a deliverable first:

| You say | You get |
|---|---|
| *(unspecified)* | Full direction: brief + asset mapping + continuity + one paste-ready prompt |
| "just the prompt" | One `text` block, nothing else |
| "just the script" | Playable script, no prompt wrapper |
| "diagnose this" | Diagnosis only — no silent rewrite |
| "keep my structure" | Targeted revision, changes summarised |

Diagnose an existing prompt:

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

### Install

```bash
./install.sh                          # auto-detects terminals
./install.sh --target codex           # pick a terminal
./install.sh --update                 # update an existing install
```

### Design philosophy

- **Every rule earns its place with a measurement.** Guidelines that cannot be traced to
  statistics do not ship; second-hand evidence is labelled as such.
- **Autonomy means you never do technical work** — not that the agent never asks. It asks
  only about expensive-to-guess dimensions, always with concrete options, one round max.
- **Learn the writing, never take the content.** Source-project characters, props and
  world settings are blocklisted from your output.

### Honest limits

- **Output quality is not yet validated against real renders.** The A/B harness
  (`eval/render_loop/`) is ready, 24 prompts are prepared, canary discipline is in place —
  but the renders have not been run. No claim is made about real-world output quality
  until then.
- Retrieval covers Hell Grind at 0.9% sampling; Cully Hill Boys is cluster-deduplicated
  at full folder coverage.
- Second-hand platform figures are marked unverified. **Runtime UI always takes
  precedence over this repository.**

### Verification

```bash
python3 scripts/validate_structure.py   # structural anti-rot
python3 scripts/eval_retrieval.py       # retrieval quality, fixed seed
python3 scripts/continuity_check.py     # short-drama continuity chain check
```

### Acknowledgements

This project stands on the shoulders of:

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)** (MIT, by
  @iamemily2050) — the anti-slop lexicon and genre refusals, 2D/anime medium grammar,
  ending profiles, failure atlas, five continuation modes, fidelity budget allocation and
  the canary render discipline are all distilled from its Skill OS v6.7, re-cut against
  this project's red lines with source attribution.
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)**
  — the entry point of this distillation journey: its comparison report pointed to the
  Emily2040 repository as the stronger upstream source.
- The creators behind the source corpora (public Hell Grind / Cully Hill Boys assets) —
  anonymisation scope in [NOTICE.md](NOTICE.md).

### License

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
Corpus provenance and third-party rights: [NOTICE.md](NOTICE.md)
