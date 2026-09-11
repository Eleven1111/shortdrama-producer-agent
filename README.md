# shortdrama-producer-agent

**张口就来，从想法到可直接开拍的生产级视频 prompt，就用它。**

这是个视频 prompt 生产 Agent。你不用学任何 prompt 写法——「雨夜，一个女孩在便利店门口等人」这样的大白话就够了。它会把焦段、画幅、平台上限这些你不想操心的事全部补齐，交给你一条 Seedance / 可灵 / 谷歌 Omni 直接能用的完整 prompt。

它不是靠 prompt 写作玄学堆出来的。**58 万多条真实生产资产**，一条条测出来的规则，才敢写进库里。

跑在 Claude Code · Codex · Cursor · Windsurf · Gemini CLI · GitHub Copilot · WorkBuddy 上。
只写 prompt 和脚本——绝不提交渲染任务、绝不花你的额外 token。

**当前版本 v3.14.0** · 架构图在 [docs/](docs)

语言：[中文](#中文) · [English](#english)

---

## 中文

### 30 秒上手

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

重启终端，直接说人话：

```
雨夜，一个女孩在便利店门口等人
```

完了，这就是全部操作。什么焦段、画幅、负面词、平台上限——那是 Agent 的活，不是你的。

### 它能帮你干什么

一句话：**让你少交试错学费。**

- **写得像真人剧组。** 每条 prompt 生成前先翻 7,824 条真实生产范例，照着行业里真实的写法来，不是「cinematic, 4k」那种一眼 AI 味的套话。实测检索命中：首条 80%、前五条 100%（固定种子可复现）。
- **镜头有导演在。** 14 节导演工艺垫在底层：一镜一个动机、光是情绪、每个镜头有终点。成片是「拍的」，不是「生成的」。
- **角色不会换脸。** 三面板设定图 + 锚点逐字复用 + 版本注册表，全剧一张脸。真实资产里 87.32% 带参考图、46.8% 打版本号——这套机制是从数据里长出来的，不是拍脑袋。
- **从小到大一套打法。** 一条 prompt、一部短剧、一部电影，同一个体系，规则不用换。短剧有镜间闭环，长片有五层状态栈；集内节奏用 137 场 / 42 转场 / 14 种冲突模式的实测数据校准过。
- **换模型不用重学。** Seedance 原生，点名 Gemini Omni、可灵、Sora、Runway、海螺、即梦、Vidu、Wan、Pika 自动切方言。导演思路不变，只翻译语法。
- **交付前先过质检。** 12 道门 + 反渣词库 + 连续性链检查，不合格打回重写。你收到的都是过了闸的，问题拦截在交付前，而不是交付后道歉。

### 架构

三张图看完全部信息流（SVG 源文件在 [docs/](docs)）：

![端到端信息流](docs/architecture-e2e.svg)
*从你的一句话进来，到成品出去的全过程。质检不合格会沿红色虚线打回重写。底部虚线框是开发期的测试台架，不参与日常运行。*

![短剧镜间闭环](docs/architecture-shot-loop.svg)
*短剧模式每拍一镜走一圈：先按节拍分账，再写这条 prompt，过连续性检查，你点头了才算数——只有你接受的镜头才进入正史。*

![长片五层状态栈](docs/architecture-longform.svg)
*拍长片（≥3 集 / ≥60 镜 / 电影）时往上叠五层状态栈：项目圣经 → 集圣经 → 场景卡 → 批次状态机 → 单镜，层层有冻结点，防止写着写着人设崩了。*

### 三种生产模式

| 你要拍 | 怎么触发 | 你会拿到 |
|---|---|---|
| 一个镜头 | 说一条需求 | 一条能直接粘贴的 prompt（完整版 600-2000 词 / 快速版 80-300 词） |
| 一部短剧 | 说要多镜头 / 分镜 | 故事拆解 · 角色设定图 prompt · 连续性圣经 · 分镜表 · 镜间状态机 |
| 一部长片 | ≥3 集 / ≥60 镜 / 电影 | 五层状态栈 · 实测校准的集内节奏 · 风格先导批 · 跨集版本注册表 |

### 怎么用

Agent 动手前会先问自己一个问题：你到底要什么？

| 你说 | 你拿到 |
|---|---|
| 什么都没说 | 全套方案：简报 + 素材映射 + 连续性 + 可粘贴 prompt |
| 「只要提示词」 | 一个 `text` 代码块，别的没有 |
| 「只要脚本」 | 能开拍的脚本，不带 prompt 外壳 |
| 「为什么效果差」 | 只诊断，不擅自动你的东西 |
| 「按原结构改」 | 定点修改，改了哪告诉你 |

想体检自己手头的 prompt：

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

### 安装

```bash
./install.sh                          # 自动认出你的终端
./install.sh --target codex           # 指定装到哪
./install.sh --update                 # 更新已装版本
```

### 几条底线

- **每条规则都是测出来的，不是编的。** 追溯不到统计数据的经验不进库；二手消息如实标注。
- **自主的意思是你不用干技术活**，不是它从来不问。只有猜错代价大的问题它才问，一次问清，给选项，不烦你。
- **学写法，不抄内容。** 参考项目的角色、道具、世界观在黑名单里，绝不会出现在你的产出里。

### 说实话的部分

- **成片质量还没经过真实渲染验证。** A/B 测试框架（`eval/render_loop/`）备好了，24 条 prompt 准备好了，金丝雀纪律立好了——但渲染还没跑。跑完之前，我们不对真实成片质量吹一句牛。
- 检索语料里 Hell Grind 是 0.9% 抽样，Cully Hill Boys 是去重后的全文件夹覆盖。
- 平台数据部分来自二手来源，已标注未验证。**真机 UI 永远比这个仓库大。**

### 自己动手验证

```bash
python3 scripts/validate_structure.py   # 结构有没有烂掉
python3 scripts/eval_retrieval.py       # 检索质量，固定种子可复现
python3 scripts/continuity_check.py     # 短剧批次连续性链核对
```

### 谢谢这些项目

这个项目站在别人的肩膀上：

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)**（MIT，by @iamemily2050）
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)**（MIT，by @slipknot0130）
- 语料来源项目的创作者们（Hell Grind / Cully Hill Boys 公开资产）——匿名化范围见 [NOTICE.md](NOTICE.md)。

### 许可证

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
语料来源与第三方权利：[NOTICE.md](NOTICE.md)

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

That's it. Focal lengths, aspect ratios, negative constraints, platform ceilings — the agent's job, not yours.

### What it actually does for you

Short version: **it saves you the tuition of failed renders.**

- **It writes like real crews do.** Every prompt is grounded in 7,824 real production examples before generation — not the "cinematic, 4k" AI smell. Measured retrieval: 80% hit at top-1, 100% at top-5 (fixed seed, reproducible).
- **Every shot has a director.** A 14-section craft layer sits underneath: one intention per shot, light as emotion, every shot has an ending. Footage feels *filmed*, not *generated*.
- **Faces don't drift.** Three-panel character sheets + verbatim anchors + a version registry keep one face for the whole series. In the source assets, 87.32% carry references and 46.8% carry version tags — this mechanism grew out of data, not guesswork.
- **One system, any scale.** One prompt, a short drama, a feature film — same rules throughout. Short drama adds a per-shot loop; long-form adds a five-layer state stack. Episode rhythm is calibrated on real data: 137 scenes, 42 transitions, 14 conflict patterns.
- **Switch models without relearning.** Seedance is native; name Gemini Omni, Kling, Sora, Runway, Hailuo, Jimeng, Vidu, Wan or Pika and it translates the dialect. The directing stays, only the grammar changes.
- **QC before delivery, not apologies after.** 12 gates + an anti-slop lexicon + a continuity chain check. Fails loop back for a rewrite. What you receive has already passed the gate.

### Architecture

Three diagrams cover the whole information flow (SVG sources in [docs/](docs)):

![End-to-end information flow](docs/architecture-e2e.svg)
*From your one sentence to the finished output. QC failures loop back along the red dashed line. The dashed band at the bottom is the dev-time harness — not part of daily runs.*

![Short-drama per-shot loop](docs/architecture-shot-loop.svg)
*Short drama walks one loop per shot: split the beats, write the prompt, pass continuity checks, get your sign-off — only shots you accept become canon.*

![Long-form five-layer state stack](docs/architecture-longform.svg)
*For long-form (≥3 episodes / ≥60 shots / film), a five-layer stack goes on top: project bible → episode bible → scene card → batch state machine → shot. Each layer has a freeze point, so nobody's character falls apart halfway through.*

### Three production modes

| You're making | Trigger | You get |
|---|---|---|
| One shot | a single request | one paste-ready prompt (full 600-2000 words / quick 80-300) |
| A short drama | multi-shot / storyboard | story breakdown · character-sheet prompts · continuity bible · shotlist · per-shot state machine |
| A long-form piece | ≥3 episodes / ≥60 shots / film | five-layer state stack · measured episode rhythm · style-pilot batch · cross-episode version registry |

### How to use it

Before doing anything, the agent asks itself one question: what do you actually want?

| You say | You get |
|---|---|
| *(nothing in particular)* | The full package: brief + asset mapping + continuity + a paste-ready prompt |
| "just the prompt" | One `text` block, nothing else |
| "just the script" | A shootable script, no prompt wrapper |
| "why does this look bad" | Diagnosis only — your work stays untouched |
| "edit, keep my structure" | Targeted changes, each one reported |

Health-check a prompt you already have:

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

### Install

```bash
./install.sh                          # finds your terminal automatically
./install.sh --target codex           # or pick one
./install.sh --update                 # update an existing install
```

### A few ground rules

- **Every rule was measured, not invented.** If a piece of advice can't be traced to data, it doesn't ship. Second-hand info is labelled as such.
- **Autonomy means you never do the technical work** — not that it never asks. It only asks when guessing wrong is expensive: concrete options, one round, then it gets out of your way.
- **Learn the writing, never take the content.** Source-project characters, props and world settings are blocklisted from your output.

### The honest part

- **Output quality is not yet validated against real renders.** The A/B harness (`eval/render_loop/`) is ready, 24 prompts are prepared, canary discipline is in place — but the renders haven't run. Until then, we make zero claims about real-world output quality.
- Retrieval covers Hell Grind at 0.9% sampling; Cully Hill Boys is cluster-deduplicated at full folder coverage.
- Some platform figures come from second-hand sources and are marked unverified. **The live product UI always outranks this repo.**

### Verify it yourself

```bash
python3 scripts/validate_structure.py   # has the structure rotted?
python3 scripts/eval_retrieval.py       # retrieval quality, fixed seed
python3 scripts/continuity_check.py     # short-drama continuity chain check
```

### Thanks

This project stands on the shoulders of:

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)** (MIT, by @iamemily2050)
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)** (MIT, by @slipknot0130)
- The creators behind the source corpora (public Hell Grind / Cully Hill Boys assets) — anonymisation scope in [NOTICE.md](NOTICE.md).

### License

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
Corpus provenance and third-party rights: [NOTICE.md](NOTICE.md)
