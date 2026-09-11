# Seedance Short-Drama Producer Agent

**Describe an idea in plain words. Get a production-grade Seedance prompt back.**

An agent that writes Seedance 2.0 / 2.5 video prompts the way working productions write
them — because it learned from **588,686 real production assets**, not from prompt-writing
folklore.

Runs in Claude Code, Codex, Cursor, Windsurf, Gemini CLI, GitHub Copilot, and WorkBuddy.
It writes prompts and scripts only — it never submits a render job or spends your credits.

**Current release: v3.14.0** · Architecture diagrams in [docs/](docs).

[English](#english) · [中文](#中文)

---

## English

### Quick start

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

Restart your terminal, then just talk to it:

```
雨夜，一个女孩在便利店门口等人
```

That is a complete request. You do not need to know about focal lengths, aspect ratios,
or negative constraints — those are the agent's job.

### What it does

| Capability | What it means for you |
|---|---|
| **Retrieves real production examples** | Every prompt is modelled on how a real crew wrote that kind of shot — not on generic "cinematic, 4k" filler |
| **Routes by how much you said** | Six vague words get three concrete directions to pick from; a detailed brief goes straight to output |
| **Knows platform limits** | Won't hand you a 60-second prompt that your platform physically cannot run |
| **Locks cross-shot consistency** | Character sheets and reference anchors, so faces stop drifting between cuts |
| **Diagnoses existing prompts** | Bring your own underperforming prompt and get a data-backed list of what is missing |
| **Hardens constraints automatically** | Adds the things a first draft predictably forgets |
| **Speaks 10 model dialects** | Same craft layer, correct syntax for Gemini Omni, Kling, Sora, Runway, Hailuo, Jimeng, Vidu, Wan, Pika |

### Why it is different

Most prompt tools encode one person's taste. This one encodes **what a 588,686-asset
production actually did**, and every rule in it traces back to a measurement.

Three examples of the difference that makes:

- **It knows how creators iterate.** Analysis of 4,154 real prompt revisions shows
  **69.7% of them add constraints**, while section skeletons barely change (2–6%). So after
  drafting, the agent tightens constraints instead of polishing prose — the thing that
  actually moves output quality.
- **It knows consistency is not a text problem.** **87.32%** of source assets carry
  reference images. Repeating an appearance paragraph in every shot still drifts, so the
  agent produces three-panel character sheets and anchors to them.
- **It knows platform ceilings are not constants.** Duration and ratio are measured per
  platform and never hardcoded — the same Seedance model is wrapped differently by
  different hosts.

### Evidence

Nothing above is a claim without a number behind it.

| Asset | Scale | Verified how |
|---|---|---|
| Retrieval corpus | **7,824** production prompts (937 folders, 562 gold-tagged) | folder-level Recall@1 **80.0%**, Recall@5 **100%** (`scripts/eval_retrieval.py`, fixed seed) |
| Iteration lessons | **4,154** real prompt revisions | Constraints split into three evidence tiers; cross-project verified vs single-project |
| Reference registry | **1,391** assets · **1,607** appearance cards | Anchor→name mapping covers **100%** of corpus anchors |
| Image-prompt analysis | **61,554** prompts | Character-sheet format and asset-binding conventions measured, not assumed |
| Platform matrix | **404,994** generation parameters | Every figure tagged `[measured]` / `[official]` / `[reported]` / `[unverified]` |

Claims the project deliberately does **not** make are listed under
[Honest limits](#honest-limits).

### Usage

The agent picks a deliverable before doing anything else:

| You say | You get |
|---|---|
| *(nothing specific)* | Full direction: brief + asset mapping + continuity + one paste-ready prompt |
| "只要提示词" / "just the prompt" | One `text` block, nothing else |
| "只要脚本" / "just the script" | Playable script — no prompt wrapper |
| "为什么效果差" / "diagnose this" | Diagnosis only — it will not silently rewrite your work |
| "按原结构改" / "keep my structure" | Targeted revision, with a summary of what changed |

**Single shot**, **short drama** (multi-shot with hard cuts) and **long-form** (≥3 episodes
or film scale) are all supported. Short drama additionally produces a story breakdown,
character-sheet prompts, a continuity bible and a shot list; long-form layers a five-layer
state stack (project bible → episode bible → scene card → batch → shot) on top, with
episode rhythm calibrated against real measured density data.

Diagnose a prompt you already have:

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

It reports internal contradictions, missing sections (measured against the corpus), missing
constraints (measured against real revisions), and spec violations — ordered by impact.

### Workflow

```
Step 0    Pick the deliverable        full-direction / prompt-only / script-only / diagnosis / revision
Step 1    Parse intent + route        single shot / short drama / long-form (≥3 episodes or film)
Step 1.5  Model & platform check      dialect routing when a non-Seedance model is named
Step 2    Retrieve real examples      BM25 over 7,824 production prompts
Step 3    Build the brief             unanswered dimensions come from the assumption list
Step 3.5  Bind your assets            what to keep, item by item
Step 4    Generate                    10 hard rules + fidelity budget + ending profiles
Step 4.5  Appearance authority        1,607 real appearance cards
Step 4.6  Reference images            three-panel character sheets for cross-shot consistency
Step 5    Self-check                  12-gate quality gate (quick-ref) + anti-slop repair
Step 5.5  Harden constraints          add what first drafts predictably miss
Step 6    Deliver                     clean, paste-ready
```

### Architecture

![End-to-end information flow](docs/architecture-e2e.svg)
*End-to-end flow: input → routing → knowledge (pulled on demand) → generation (single-shot / short-drama pipelines) → QC with a fail loop back into generation → delivery. The dashed band at the bottom is the dev-time harness, not part of the runtime.*

![Short-drama per-shot loop](docs/architecture-shot-loop.svg)
*Short-drama mode runs a loop per shot: beat buckets → per-shot prompt → continuity gates → user acceptance → state machine → next shot. Only accepted shots enter canon; failures are looked up in the failure atlas, not re-rolled blind.*

![Long-form five-layer state stack](docs/architecture-longform.svg)
*Long-form mode (≥3 episodes / ≥60 shots / film) layers a five-state-stack protocol on top: project bible → episode bible → scene card → batch state machine → shot, each with its own freeze point; all short-drama rules stay in force.*

### Repository layout

```
shortdrama-producer-agent/
├── AGENTS.md                    # Agent definition — cross-terminal standard
├── SKILL.md                     # Skill-compatible layer (Claude Code / WorkBuddy)
├── agents/openai.yaml           # OpenAI metadata
├── install.sh                   # One-command install, auto-detects terminals
├── scripts/
│   ├── seedance_search.py       # Zero-dependency BM25 retriever
│   ├── seedance_corpus.jsonl.gz # 7,824 production prompts
│   ├── diagnose_prompt.py       # Data-backed prompt diagnosis
│   ├── continuity_check.py      # Batch-level continuity chain checker
│   ├── eval_retrieval.py        # Retrieval quality evaluation
│   └── validate_structure.py    # Structural anti-rot checks
├── references/                  # craft libraries, protocols & data (27 registered)
│   ├── quick-ref.md             #   Level-0 routing card + 12 delivery gates
│   ├── model-adaptation.md      #   dialects: Omni / Kling / Sora / Runway / Hailuo…
│   ├── directorial-craft.md     #   14 sections: motion, light, blocking, budget, endings
│   ├── anti-slop-lexicon.md     #   six slop classes + per-genre refusals
│   ├── longform-protocol.md     #   ≥3 episodes / film: five-layer state stack
│   ├── style-bible.md           #   series-level look governance
│   ├── platform-capabilities.md #   evidence-graded platform matrix
│   ├── iteration-lessons.md     #   what 4,154 revisions changed
│   └── story_level/             #   act structure, character journeys, beat patterns
├── docs/                        # architecture diagrams (SVG)
├── tests/behavior-cases.json    # 17 workflow behaviour specs
└── eval/render_loop/            # A/B render experiment harness
```

### Design philosophy

**Every rule earns its place with a measurement.** If a guideline cannot be traced to
corpus statistics, it does not go in. Where evidence is second-hand or unverified, it is
labelled as such rather than presented as fact.

**Autonomy means you never do technical work — not that the agent never asks.** It handles
focal length, ratio, style anchors and model parameters silently. It asks only about things
that are expensive to guess wrong, always as concrete options, never as open questions,
and never more than one round.

**Learn the writing, never take the content.** The corpus teaches structure and phrasing.
Source-project characters, props and world settings are on an explicit blocklist and must
never reach your output.

**Verification over assertion.** Retrieval quality is measured, not asserted. Structural
checks are fault-injection tested. The render loop's arithmetic was validated against
constructed data before shipping.

### Boundaries

- **Writes prompts and scripts only.** Never submits a render job, never spends credits,
  never claims a video was generated.
- **Reference/setup images for video consistency are in scope.** Standalone image
  creation (posters, illustrations) is not.
- **Models: Seedance native.** Gemini Omni / Kling / Sora / Runway / Hailuo / Jimeng /
  Vidu / Wan / Pika are supported as dialect translation — the craft layer does not change.
- **Never imports source-project stories, characters or props into your work.**

### Honest limits

- **Output quality has not been validated against actual renders.** An A/B harness exists
  (`eval/render_loop/`) with 24 prompts prepared, but the renders have not been run. Until
  they are, no claim is made about real-world output quality.
- Retrieval covers Hell Grind at 0.9% sampling; Cully Hill Boys is cluster-deduplicated at
  full folder coverage.
- Platform figures for Dreamina modes are second-hand and marked unverified. **Runtime UI
  always takes precedence over this repository.**

### Verification

```bash
python3 scripts/validate_structure.py   # structural anti-rot
python3 scripts/eval_retrieval.py       # retrieval quality, fixed seed
```

CI runs both on every PR, plus manifest linting, retrieval and diagnoser smoke tests,
`install.sh` syntax, and README bilingual completeness.

### License

MIT License · Copyright (c) 2026 Eleven1111. See [LICENSE](LICENSE).
Corpus provenance, anonymisation scope and third-party rights: [NOTICE.md](NOTICE.md).
Concept-level distillations with attribution: [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) (MIT)
and [slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit).

```bash
./install.sh --update    # update an existing install
```

---

## 中文

### 快速开始

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

重启终端，然后直接说人话：

```
雨夜，一个女孩在便利店门口等人
```

这就是一条完整请求。你不需要懂焦段、画幅、负面约束——那是 Agent 的活。

### 它做什么

| 能力 | 对你意味着什么 |
|---|---|
| **检索真实生产范例** | 每条 prompt 都照着真实剧组怎么写这类镜头来写，不是「cinematic, 4k」这类套话 |
| **按你说了多少来分流** | 六个字的模糊想法给你三个可拍方向挑；信息足够就直接出片 |
| **知道平台限制** | 不会给你一条 60 秒的 prompt，而你的平台根本跑不了 |
| **锁定跨镜一致性** | 角色设定图 + 锚点引用，脸不再一镜一个样 |
| **诊断已有 prompt** | 把你自己写的、效果不好的 prompt 拿来，给你一份有数据依据的缺口清单 |
| **自动加固约束** | 补上初稿必然会漏的东西 |
| **会说 10 种模型方言** | 工艺层不变，语法切换：Gemini Omni、可灵、Sora、Runway、海螺、即梦、Vidu、Wan、Pika |

### 凭什么不一样

大多数 prompt 工具封装的是某个人的审美。这个封装的是**一个 58.8 万条资产的真实生产
项目实际怎么做**，每条规则都能追溯到一次测量。

三个例子说明这个差别有多实在：

- **它知道创作者是怎么改的。** 4,154 组真实修订的分析显示：**69.7% 的修订是在加约束**，
  而段落骨架几乎不动（增删仅 2–6%）。所以 Agent 出完初稿后去加固约束，而不是润色文采
  ——前者才是真正影响成片的那一半。
- **它知道一致性不是文本问题。** 源资产里 **87.32%** 带参考图。同一段外观描述在每个
  镜头重写十遍，脸照样漂。所以 Agent 会先产三面板角色设定图，再用锚点引用它。
- **它知道平台上限不是常量。** 时长与画幅按平台实测，绝不写死——同一个 Seedance 模型，
  不同平台封装出来的能力不一样。

### 证据

上面每一句都有数字撑着。

| 资产 | 规模 | 怎么验证的 |
|---|---|---|
| 检索语料 | **7,824** 条生产 prompt（覆盖 937 个文件夹，562 条金标） | folder 级 Recall@1 **80.0%**、Recall@5 **100%**（`scripts/eval_retrieval.py`，固定种子） |
| 迭代教训 | **4,154** 组真实修订 | 约束分三层证据强度：跨项目验证 / 单项目高频 / 项目专属黑名单 |
| 参考资产注册表 | **1,391** 个资产 · **1,607** 张外观卡 | 锚点→名称映射覆盖语料中 **100%** 的锚点 |
| 图像 prompt 分析 | **61,554** 条 | 设定图格式与素材绑定写法是实测出来的，不是想当然 |
| 平台能力矩阵 | **404,994** 条生成参数 | 每条标注 `[实证]` / `[官方]` / `[报道]` / `[未验证]` |

本项目**刻意不做**的声称，见 [诚实的边界](#诚实的边界)。

### 使用方法

Agent 动手之前先选交付物：

| 你说 | 你拿到 |
|---|---|
| *（没特别说）* | 完整方案：简报 + 素材映射 + 连续性 + 一条可粘贴 prompt |
| 「只要提示词」 | 一个 `text` 代码块，别的都没有 |
| 「只要脚本」 | 可拍脚本，不含 prompt 外壳 |
| 「为什么效果差」 | 只诊断——不会擅自把你的东西重写一遍 |
| 「按原结构改」 | 定点修改，并说明改了什么 |

**单镜头**、**短剧**（多镜头硬切）与**长片**（≥3 集或电影规格）都支持。短剧模式会额外
产出故事拆解、角色设定图 prompt、连续性圣经和分镜表；长片模式在其上叠加五层状态栈
（项目圣经 → 集圣经 → 场景卡 → 批次 → 镜），集内节奏用真实密度数据校准。

诊断你已有的 prompt：

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

它会报出内部矛盾、缺失段落（对照语料实测）、缺失约束（对照真实修订）与规格问题，
按影响排序。

### 工作流

```
Step 0    选交付物            完整方案 / 只要prompt / 只要脚本 / 诊断 / 改写
Step 1    解析意图 + 分流      单镜 / 短剧 / 长片（≥3 集或电影规格）
Step 1.5  模型与平台检查       点名非 Seedance 模型时做方言路由
Step 2    检索真实范例         对 7,824 条生产 prompt 做 BM25
Step 3    生成简报            没答的维度走假设清单
Step 3.5  绑定你的素材         逐项写清保留什么
Step 4    生成                全语料统计出的 10 条硬规则 + 保真预算 + 终点画像
Step 4.5  外观权威            1,607 张真实外观卡
Step 4.6  参考图              三面板设定图，锁跨镜一致性
Step 5    自检                12 道质量门（quick-ref）+ 反渣修复
Step 5.5  加固约束            补上初稿必然会漏的
Step 6    交付                干净、可直接粘贴
```

### 架构

![端到端信息流](docs/architecture-e2e.svg)
*端到端流转：输入 → 路由 → 知识层（按需拉取）→ 生成层（单镜 / 短剧双管线）→ 质检层（fail 红色虚线回炉生成层）→ 输出层。底部虚线框为开发期 harness，不进运行时。*

![短剧镜间闭环](docs/architecture-shot-loop.svg)
*短剧模式每镜一轮循环：节拍桶分账 → 逐镜 prompt → 连续性闸门 → 用户接受 → 状态机更新 → 下一镜。只有已接受镜头进入 canon；失败先查失败图谱，不凭感觉重roll。*

![长片五层状态栈](docs/architecture-longform.svg)
*长片模式（≥3 集 / ≥60 镜 / 电影）在短剧规则之上叠加五层状态栈：项目圣经 → 集圣经 → 场景卡 → 批次状态机 → 镜，每层各有冻结点。*

### 目录结构

```
shortdrama-producer-agent/
├── AGENTS.md                    # Agent 定义 —— 跨终端标准
├── SKILL.md                     # skill 兼容层（Claude Code / WorkBuddy）
├── agents/openai.yaml           # OpenAI 元数据
├── install.sh                   # 一条命令安装，自动检测终端
├── scripts/
│   ├── seedance_search.py       # 零依赖 BM25 检索器
│   ├── seedance_corpus.jsonl.gz # 7,824 条生产 prompt
│   ├── diagnose_prompt.py       # 数据驱动的 prompt 诊断
│   ├── continuity_check.py      # 批次级连续性链核对
│   ├── eval_retrieval.py        # 检索质量评测
│   └── validate_structure.py    # 结构防腐校验
├── references/                  # 工艺库、协议与知识数据（manifest 登记 27 项）
│   ├── quick-ref.md             #   Level-0 速查卡 + 交付前 12 门
│   ├── model-adaptation.md      #   方言：Omni / 可灵 / Sora / Runway / 海螺…
│   ├── directorial-craft.md     #   14 节：运动/光/调度/预算/终点画像
│   ├── anti-slop-lexicon.md     #   六类渣词 + 题材禁区
│   ├── longform-protocol.md     #   ≥3 集 / 电影：五层状态栈
│   ├── style-bible.md           #   剧集级美学治理
│   ├── platform-capabilities.md #   带证据分级的平台矩阵
│   ├── iteration-lessons.md     #   4,154 组修订改了什么
│   └── story_level/             #   幕结构、角色旅程、节拍模式
├── docs/                        # 架构图（SVG）
├── tests/behavior-cases.json    # 17 条 workflow 行为规格
└── eval/render_loop/            # A/B 渲染实验框架
```

### 设计哲学

**每条规则都要用一次测量换取自己的位置。** 追溯不到语料统计的经验，就不写进去。
证据是二手或未经验证的，就如实标注，不当成事实呈现。

**自主不等于从不发问，而是你永远不做技术活。** 焦段、画幅、风格锚、模型参数由 Agent
静默处理；只有「猜错代价高」的维度才问你，而且一律给具体选项、绝不用开放问句、
最多问一轮。

**学写法，不拿内容。** 语料教的是结构与措辞。源项目的角色、道具、世界观设定进了
明确的黑名单，绝不允许出现在你的产出里。

**验证优先于断言。** 检索质量是测出来的，不是声称的；结构校验做过故障注入；渲染回环
的算术先用构造数据验过才交付。

### 边界

- **只产出 prompt 与脚本。** 绝不提交渲染任务、不消耗额度、不声称已经生成了视频。
- **服务于视频一致性的参考图/设定图属于职责内**；独立图像创作（海报、插画）不做。
- **模型支持：Seedance 原生。** Gemini Omni / 可灵 / Sora / Runway / 海螺 / 即梦 /
  Vidu / Wan / Pika 以方言翻译支持——工艺层不变。
- **绝不把源项目的故事、角色、道具搬进你的作品。**

### 诚实的边界

- **产出质量尚未用真实渲染验证过。** A/B 实验框架（`eval/render_loop/`）已就绪、
  24 条 prompt 已备好，但渲染没有跑。在那批数据出来之前，本项目不对真实成片质量
  做任何声称。
- 检索语料中 Hell Grind 为 0.9% 采样；Cully Hill Boys 为 cluster 去重后的全文件夹覆盖。
- Dreamina 各模式的平台数据是二手来源、标注为未验证。**运行时 UI 永远优先于本仓库。**

### 验证

```bash
python3 scripts/validate_structure.py   # 结构防腐
python3 scripts/eval_retrieval.py       # 检索质量，固定种子
```

CI 在每个 PR 上跑这两项，外加 manifest 校验、检索与诊断器冒烟测试、`install.sh`
语法检查、README 双语完整性。

### 许可证

MIT License · Copyright (c) 2026 Eleven1111. 见 [LICENSE](LICENSE)。
语料来源、匿名化范围与第三方权利声明见 [NOTICE.md](NOTICE.md)。
概念级蒸馏致谢：[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)（MIT）与
[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)。

```bash
./install.sh --update    # 更新已安装版本
```
