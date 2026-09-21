# shortdrama-producer-agent

**张口就来。从一句大白话，到能直接开拍的视频 prompt。**

你不会写 prompt，也不该会。

「雨夜，一个女孩在便利店门口等人」——把话说到这个程度就够了。焦段、画幅、光、负面词、你那个平台到底能吃多长，全不用你操心。出来就是一条能直接粘进 Seedance、可灵或者谷歌 Omni 的完整 prompt。

它凭什么是这个水平？因为库里的每一句话，都是从 58 万多条真实生产素材里量出来的。不是「我感觉这样更好」，是「真实创作者里有 45.4% 确实这么干」。

跑在 Claude Code · Codex · Cursor · Windsurf · Gemini CLI · GitHub Copilot · WorkBuddy 上。
只写 prompt 和脚本——它不会替你点「生成」，也不会偷偷烧你的 token。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.17.0-blue.svg)](manifest.json)
[![Corpus](https://img.shields.io/badge/corpus-7%2C824%20real%20prompts-green.svg)](scripts/seedance_corpus.jsonl.gz)
[![Dependencies](https://img.shields.io/badge/dependencies-python3%20stdlib%20only-brightgreen.svg)](scripts)
[![CI](https://github.com/Eleven1111/shortdrama-producer-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Eleven1111/shortdrama-producer-agent/actions/workflows/ci.yml)

**当前版本 v3.19.0** · 架构图在 [docs/](docs)

语言：[中文](#中文) · [English](#english)

---

## 中文

### 先跑起来

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

重启终端，用平常说话的口气告诉它就行：

```
雨夜，一个女孩在便利店门口等人
```

就这样。真的没有第二步。

### 它到底替你挡掉了什么

写视频 prompt 最难的从来不是词穷，是你不知道自己在犯错。

「cinematic, 4k, masterpiece」这种词，你写了也没人拦你，只是它一点用都没有。角色第一镜长得挺像样，第五镜开始换脸，你只能从头再来。想拍 60 秒，做完才发现平台只吃 15 秒，白忙一场。

这三件事它都在生成**之前**拦住了。不是交给你之后再跟你说抱歉，是压根不让你拿到有问题的东西。

下面是它凭什么做到。

### 它不编，它量

这个行业最不缺的就是「我觉得这样写更好」。所以库里有条死规矩：**一条经验想进来，先拿数据来。** 撑不住的，宁可删掉。

58.86 万条真实素材（Hell Grind 11.5 万 + Cully Hill Boys 47.3 万）摆在那儿，出现率、修订规律、分布，全都是量出来的。量不出来的，老老实实标「未验证」，不装。

举个具体的，你就明白这个区别有多要命。

真实创作者在处理参考图的时候，**45.4% 的人会一条条列出「要保留什么」，而只有 0.1% 的人会列「不要保留什么」**。

这个数字直接改写了它的做法。它现在会逼自己把「保留清单」写全——因为**你没写的那些，就是模型会自己发挥的那些**。你只说了「参考这张脸」，它就懂了：脸、发型、身材、每一件衣服、鞋、配饰，默认全都要。你没说不要背景，背景就会被带进来。

只凭直觉写 prompt 的时候，这一层往往就被跳过了。

### 它先去看真剧组是怎么写的

包里躺着 7,824 条真实生产 prompt，平均一条 1,622 词。写之前先检索一遍，学的是真实片场的写法——机位怎么标、光怎么描、镜头怎么动——不是网上那些 prompt 教学。

检索质量实测：首条命中 80%，前五条 100%，固定种子，你能自己复现。

### 镜头后面站着一个导演

最底下垫着 14 节导演工艺。一镜一个动机；光不是照明，光就是情绪；每个镜头都得有终点——是让观众松一口气，还是勾住他往下看，还是「看这里」，动笔前先想清楚。

所以出来的东西看起来是「拍的」，不是「生成的」。

### 不让角色换脸，靠的是图，不是嘴

这条完全是从数据里长出来的，不是拍脑袋定的。

真实素材里，**87.32% 带参考图**；**46.8% 带版本号**（`_v2`、`_v3`），最多的一个角色攒了 28 个版本。

结论很直白：**文本锚不住一张脸，图才能。**

所以机制是这样的：先用三面板设定图打底（正面全身 / 背面全身 / 特写），之后每一镜都去引用它。角色受伤了、淋湿了、换衣服了？**改设定图，出个新版本**——而不是在每一镜的视频 prompt 里重新描述一遍。

前者一次搞定。后者你写十遍它还是会飘。

### 一个镜头、一部短剧、一部电影，学一次就够

同一套规则，不用换脑子。

短剧多一层「镜间闭环」，每拍一镜走一圈。长片再往上叠五层状态栈——项目圣经 → 集圣经 → 场景卡 → 批次状态机 → 单镜，每层都有冻结点，防止你写到第 40 镜的时候，人设已经悄悄不是原来那个人了。

节奏也不是拍脑袋定的。137 场戏、42 个转场、14 种冲突模式的实测密度摆在那儿，拿它校准，不是拿通用编剧教材套。

### 换模型，只翻方言，思路不动

Seedance 是母语。你点名 Gemini Omni、可灵、Veo、Sora、Runway、海螺、即梦、Vidu、Wan、Pika，它会先把九件事问清楚——版本、方言、时长上限、参考图怎么吃、音频是不是同轨出、画幅、镜头词汇、语言——再老老实实翻语法。

翻译的是语法，不是想法。你不需要为新模型重新学一遍怎么当导演。

### 交给你之前，先过 12 道门

这一条不用多解释，12 项逐条对：模式、规格头、角色锚点、动作有没有终点、运镜有没有动机、光、三轨音频、负面约束够不够 5 条、风格锚、保真预算、镜末画像、序列链。

一门不过，打回重写。**你收到的都是过了闸的。**

### 想聊透了再做，就开个神仙会

这条是给人用的，不是给机器用的。

你说一句「先聊聊」或者「先别急着做」，它不会甩给你一句「请问您想要什么风格」——这种问题最烦人，因为你自己也不知道。它会直接开个会。

一次性给你五条**真的不一样**的方案，来自五个不同的位置。制片人关心这东西能不能被看完；编剧关心有没有戏核；导演关心拍出来长什么样；捣蛋鬼专门负责挑刺；还有一个人，始终替你盯着「你到底想要什么」。

一行一条，不给排序、不给推荐——**它不替你做决定。**

你回个编号，或者「①+③」，或者干脆「都不对，但②那个方向」，都算数。然后它把结果收成一张概念卡，直接往下走。

这里有条规矩挺狠：那个「捣蛋鬼」席位是强制的。**如果整轮里没有一条真质疑，这一轮算没干完，重来。**

为什么这么较真？因为 AI 最大的毛病从来不是不敢说，是**顺着你说**。

### 批量生产的时候，机器之间也要开会

短剧和长片模式下，这个默认开着；单镜头默认关。分这么细是有原因的——开会要花 token，为一条 10 秒的镜头开一场会不值当。想省就说一句「不开会」。

它补的是一个很具体的窟窿。

原来那 7 项自检，全都在「格式对不对」这一层。**没有任何一项有权否决一个故事层面的决定，也没有任何一个角色被授权去质疑骨架。** 4,154 组真实修订把这事证实了：创作者反复改的时候，69.7% 是在加长度、加约束，骨架只动 2–6%。**骨架从来没人碰，因为整个流程里没人管这个。**

三层会分工明确：提案会在 Step 3 之后跑一次，人物会在冒出新角色或绑定冲突时开，评审会在每批镜头交付前开。

流程是：各自独立提案 → 只递小纸条互评 → 一个统筹拍板 → 各自复述一遍 → 合成。

「只递小纸条」是认真的。互评阶段只传「哪一段、多严重、什么问题、一句话理由」，不传全文，也不给完整替代方案。因为研究者发现：**一旦把完整方案摊开交换，大家的想法会在一轮之内就趋同——损失发生在交换的那一刻。**

还有一条诚实底线。运行时按能力分三档：能真开出独立上下文的，算真开会；只能在一个上下文里轮流扮演的，交付物上必须写「独立性未完全保证」；连分角色都做不到的，直接标注「**本轮未经集体评审**」。

**开不了会就如实说明，比让交付物显得开过会要好。**

### 评审记录本身，就是一条能交出去的证据链

每条评审都带着角色、定位，和一条「可证伪的失败理由」——机器可读。

对上「先审后播」「审核会商」这类要求，这份记录可以直接拿来用。

所以说句实在话：**就算它的质量提升是边际的，光是「可审计」这一条，也可能足够构成采用它的理由。**

### 它是怎么走的

三张图看完全部信息流（SVG 源文件在 [docs/](docs)）：

![端到端信息流](docs/architecture-e2e.svg)
*从你的一句话进来，到成品出去的全过程。质检不合格会沿红色虚线打回重写。底部虚线框是开发期的测试台架，不参与日常运行。*

![短剧镜间闭环](docs/architecture-shot-loop.svg)
*短剧模式每拍一镜走一圈：先按节拍分账，再写这条 prompt，过连续性检查，你点头了才算数——只有你接受的镜头才进入正史。*

![长片五层状态栈](docs/architecture-longform.svg)
*拍长片（≥3 集 / ≥60 镜 / 电影）时往上叠五层状态栈：项目圣经 → 集圣经 → 场景卡 → 批次状态机 → 单镜，层层有冻结点，防止写着写着人设崩了。*

### 三种规模，三种交付

| 你要拍 | 怎么触发 | 你会拿到 |
|---|---|---|
| 一个镜头 | 说一条需求 | 一条能直接粘贴的 prompt（完整版 600-2000 词 / 快速版 80-300 词） |
| 一部短剧 | 说要多镜头 / 分镜 | 故事拆解 · 角色设定图 prompt · 连续性圣经 · 分镜表 · 镜间状态机 |
| 一部长片 | ≥3 集 / ≥60 镜 / 电影 | 五层状态栈 · 实测校准的集内节奏 · 风格先导批 · 跨集版本注册表 |

### 底下的数据

`references/` 和 `scripts/` 里的东西，没有一样是凭空写的，全是这批素材的产物。

| 资产 | 规模 |
|---|---|
| 检索语料 | **7,824 条**真实生产 prompt（金标 562 条，平均 1,622 词） |
| 原始采集 | **588,686 条**资产（Hell Grind 115,447 + Cully Hill Boys 473,239） |
| 角色 / 场景 / 道具设定卡 | **1,607 张**，共 4 万多条外观描述 |
| 参考元素注册表 | **1,391 条**（只留 `name` + `category`） |
| 真实修订聚类 | **4,154 组** |
| 真实图片 prompt | **61,554 条** |
| 故事层密度数据 | 137 场 · 42 个转场 · 14 种冲突 · 65 条道具动线 · 16 项幕结构 · 8 组运镜弧 |
| 规律库 | **22 份** reference 文档，共 3,051 行 |

### 手边的五个小工具

全是零依赖（纯 Python 标准库），跟着包一起发，不用装任何东西。

| 脚本 | 干什么 | 怎么跑 |
|---|---|---|
| `seedance_search.py` | 去 7,824 条真实范例里翻，自动剥掉源项目的版权内容 | `python3 scripts/seedance_search.py "<英文关键词>" 3` |
| `diagnose_prompt.py` | 诊断你自己手头的 prompt：哪里自相矛盾、缺了哪个段、缺了哪些约束 | `python3 scripts/diagnose_prompt.py my-prompt.txt` |
| `continuity_check.py` | 短剧交付前核对：镜号连不连、上一镜的结尾状态有没有接上下一镜的开头、锚点拼写一致吗 | `python3 scripts/continuity_check.py shots.md` |
| `validate_structure.py` | 结构防腐：关键约定有没有被误删、文档互引有没有变死链、有没有占位符混进主干 | `python3 scripts/validate_structure.py` |
| `eval_retrieval.py` | 检索质量评测，固定种子，可复现 | `python3 scripts/eval_retrieval.py` |

### 它对自己也上闸门

- **CI 门禁**（[.github/workflows/ci.yml](.github/workflows/ci.yml)）：8 步，push 和 PR 必跑——manifest 校验、依赖文件存在性、SKILL.md frontmatter、AGENTS.md 结构、检索冒烟、诊断器冒烟、结构防腐、install.sh 语法、README 双语完整性。
- **结构防腐**：`validate_structure.py` 用**行首锚定的正则**而不是子串匹配。因为子串会造假绿——`Step 5.5` 会被 `Step 5.5x` 满足，这个洞是故意灌故障测出来的。它还把一个真实翻车记录固化成了检查项：改完分流逻辑后，`AGENTS.md` 里留了一句自相矛盾的老话，当时靠人工 grep 才发现。
- **行为规格**：`tests/behavior-cases.json`，17 个用例、7 个类别。LLM 行为没法写断言，所以它的 `expected` 写的是自然语言验收条款，交给人或者另一个模型去判定。
- **渲染 A/B 回环**：`eval/render_loop/`，12 个用例 × 2 组 = 24 次渲染。评分只评「指令有没有被遵循」和「技术有没有缺陷」，**不评美学**；二元判定，不打分；评分表盲测，已验证不含组别字段。四条铁律写进了它的 README：金丝雀先行、成本上限先于调用、用例冻结、计划和观测物理分开存。

### 怎么用：它先问你一句「你到底要什么」

| 你说 | 你拿到 |
|---|---|
| 什么都没说 | 全套方案：简报 + 素材映射 + 连续性 + 可粘贴 prompt |
| 「只要提示词」 | 一个 `text` 代码块，别的没有 |
| 「只要脚本」 | 能开拍的脚本，不带 prompt 外壳 |
| 「为什么效果差」 | 只诊断，不擅自动你的东西 |
| 「按原结构改」 | 定点修改，改了哪告诉你 |

想体检一下自己手头的 prompt：

```bash
python3 scripts/diagnose_prompt.py my-prompt.txt
```

### 装到哪

```bash
./install.sh                          # 自动认出你的终端
./install.sh --target codex           # 指定装到哪
./install.sh --target repo --repo /path/to/your/project   # 装进某个项目
./install.sh --update                 # 更新已装版本
./install.sh --from-local <dir>       # 从本地目录装，不走 git clone
```

| 终端 | 装到哪 | 读哪个文件 |
|---|---|---|
| **Codex** | `~/.agents/skills/shortdrama-producer`（2026 spec，USER scope） | `AGENTS.md` |
| **Claude Code** | `~/.claude/skills/shortdrama-producer` | `SKILL.md` |
| **WorkBuddy** | `~/.workbuddy/skills/shortdrama-producer` | `SKILL.md` |
| **Cursor / Windsurf / Gemini CLI / Copilot** | `<你的项目>/.agents/skills/shortdrama-producer` | `AGENTS.md` |

两个不太容易被注意到、但踩过坑的细节：`--update` 遇到用 `--from-local` 装的副本会**重新同步**，而不是 `git pull`——那种副本没有 `.git`，不这样处理就永远只能手删；备份一律落在 `skills/` 的**上一层**（`skill-backups/`），因为宿主会扫 `skills/`，备份放里面会被当成第二个重复 skill 注册进去。

### 目录长这样

```
shortdrama-producer-agent/
├── AGENTS.md                 # 2026 跨终端标准定义（Codex/Cursor/Windsurf/Gemini/Copilot/Claude Code）
├── SKILL.md                  # skill 兼容层（Claude Code / WorkBuddy）
├── manifest.json             # 包元数据 + 依赖清单 + 数据规模（CI 校验）
├── agents/openai.yaml        # OpenAI / ChatGPT 侧元数据与调用策略
├── install.sh                # 跨终端安装 / 更新
├── scripts/                  # 5 个零依赖工具 + 7,824 条语料
├── references/               # 22 份规律库 + 设定卡 JSON + 参考注册表 + 故事层密度数据
├── docs/                     # 3 张架构图（SVG 源文件）
├── tests/behavior-cases.json # 17 条对话行为规格
├── eval/render_loop/         # 渲染 A/B 台架（开发期评测工具，不是运行时功能）
├── NOTICE.md                 # 语料来源、匿名化范围、第三方权利
└── .github/workflows/ci.yml  # 8 步门禁
```

### 几条底线

- **它不编。** 追溯不到统计数据的经验不进库；二手消息如实标注。
- **自主的意思是你不干技术活**，不是它从来不问。只问猜错代价大的事，一次问清，给选项，不烦你。
- **学写法，不抄内容。** 参考项目的角色、道具、世界观在黑名单里，绝不会出现在你的产出里。检索输出时会自动把锚点换成 `<<<CHARACTER_1>>>` 这类匿名标签，台词歌词原文一并剥掉。
- **能机械判定的事不投票。** 凡是 `continuity_check.py` 这类脚本能搞定的事，走硬约束，不进会议。

### 它不敢吹的地方

这个项目的卖点之一，是**不吹**。

- ⚠️ **成片质量还没经过真实渲染验证。** A/B 台架备好了，24 条 prompt 准备好了，金丝雀纪律立好了——但渲染还没跑，因为这台机器上没有任何 Seedance / 火山方舟 / Higgsfield 凭据。跑完之前，我们不对真实成片质量说一句大话。**管道就绪 ≠ 质量已验证。**
- ⚠️ **会议层的质量收益还没有 A/B 证据，实验是暂停状态。** 它在短剧和长片下默认开着，但这是**有意接受的取舍**：先上线拿真实使用数据，暂不为它单独跑 A/B。在实验出结果之前，任何对外材料里都别说它提升了质量。如果 A/B 显示连下尾指标都没改善，就应该把会议层砍掉，退回单主体 + 强化自检。
- 检索语料里，Hell Grind 是 0.9% 抽样，Cully Hill Boys 是去重后的全文件夹覆盖。
- 平台数据有一部分来自二手来源，已标注未验证。**真机 UI 永远比这个仓库大。**
- 部分设计依据来自**预印本**（比如那个 41.27% vs 86.36% 的数字），表述是「实验显示」而不是「已证实」。会议层那个 30% 的预算上限是**可调初始值**，不是实证结论。

### 自己验一遍

```bash
python3 scripts/validate_structure.py   # 结构有没有烂掉
python3 scripts/eval_retrieval.py       # 检索质量，固定种子可复现
python3 scripts/continuity_check.py     # 短剧批次连续性链核对
```

### 谢谢这些项目

这个项目站在别人的肩膀上：

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)**（MIT，by @iamemily2050）
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)**（MIT，by @slipknot0130）
- 语料来源项目的创作者们（Hell Grind / Cully Hill Boys 的公开资产）——匿名化范围见 [NOTICE.md](NOTICE.md)

### 许可证

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
语料来源与第三方权利：[NOTICE.md](NOTICE.md)

---

## English

**Just say it out loud. From one plain sentence to a shot-ready video prompt.**

You don't know how to write prompts. You shouldn't have to.

"A rainy night. A girl waiting outside a convenience store." That's all the detail it needs. Focal length, aspect ratio, lighting, negative constraints, whatever your platform actually allows — none of it is your problem. What comes back is a complete prompt you can paste straight into Seedance, Kling or Gemini Omni.

Why is it that good? Because every line in the library was measured across **588,686 real production assets**. Not "I feel this reads better" — "45.4% of real creators actually do it this way."

Runs on Claude Code · Codex · Cursor · Windsurf · Gemini CLI · GitHub Copilot · WorkBuddy.
It writes prompts and scripts. It never hits *Generate* for you, and it never burns your tokens.

**Current version v3.17.0** · Architecture diagrams in [docs/](docs)

### Get it running

```bash
git clone https://github.com/Eleven1111/shortdrama-producer-agent.git
cd shortdrama-producer-agent && ./install.sh
```

Restart your terminal, then describe it however you'd say it out loud:

```
A rainy night. A girl waiting outside a convenience store.
```

That's it. There genuinely is no second step.

### What it actually keeps you out of

The hard part of writing a video prompt isn't finding the words. It's not knowing when you're wrong.

Write "cinematic, 4k, masterpiece" and nobody stops you — it just does nothing. Your character looks right in shot one and has a different face by shot five, so you start over. You build a 60-second sequence only to learn the platform caps at 15.

All three get caught **before** generation. Not an apology afterwards — you simply never receive the broken version.

Here's how it manages that.

### It doesn't guess. It measures.

This field has no shortage of "I think this reads better." So the library has one hard rule: **an idea needs data before it ships.** If it can't be backed, it gets cut.

588,686 real assets sit behind it (115,447 from Hell Grind, 473,239 from Cully Hill Boys). Frequencies, revision patterns, distributions — all measured. Where it couldn't be measured, it says "unverified" instead of pretending.

A concrete example of why that matters.

Among real creators handling reference images, **45.4% enumerate what to keep, while only 0.1% list what not to inherit.**

That single number rewrote its behaviour. It now forces itself to write the keep-list out in full — because **whatever you don't write down is exactly what the model invents.** Say "use this face" and it understands the whole visible person: face, hair, build, every garment, shoes, accessories. Say nothing about the background and the background comes along for the ride.

Written on intuition alone, that layer usually gets skipped.

### It reads real crews before it writes

**7,824 real production prompts** ship inside the package, averaging 1,622 words each. It retrieves before generating, so what it learns is how actual sets write — camera position, light, movement — not how a blog post about prompts writes.

Measured retrieval: 80% at top-1, 100% at top-5. Fixed seed, so you can reproduce it.

### There's a director standing behind the camera

A 14-section craft layer sits underneath. One intention per shot. Light isn't illumination, light is emotion. Every shot needs an ending — a release, a hook to keep watching, a "look here" — and you decide which before you write.

Which is why the footage reads as *filmed* rather than *generated*.

### Faces don't drift, because images anchor them — not prose

This one grew entirely out of data. Nobody sat down and guessed it.

**87.32% of source assets carry reference images.** **46.8% carry version tags** (`_v2`, `_v3`), and one character accumulated 28 versions.

The conclusion is blunt: **text cannot anchor a face. Images can.**

So: a three-panel character sheet first (front full-body / back full-body / close-up), referenced by every shot after that. Character gets injured, soaked, changed? **Edit the sheet into a new version** — don't re-describe the change in each shot's video prompt.

The first approach works once. The second drifts even after you write it ten times.

### One shot, one short drama, one feature film — learn it once

Same rules throughout. No mental gear change.

Short drama adds a per-shot loop. Long-form stacks five layers on top — project bible → episode bible → scene card → batch state machine → shot — every layer with a freeze point, so that by shot 40 your character hasn't quietly become someone else.

The rhythm isn't guesswork either. 137 scenes, 42 transitions, 14 conflict types of measured density are sitting right there to calibrate against — not a generic screenwriting textbook.

### Switching models just switches dialect

Seedance is the native tongue. Name Gemini Omni, Kling, Veo, Sora, Runway, Hailuo, Jimeng, Vidu, Wan or Pika, and it settles nine things first — version, dialect, duration ceiling, how references are consumed, whether audio comes out in the same pass, ratio, camera vocabulary, language — then translates the grammar.

Grammar gets translated. Intent doesn't. You never have to relearn how to be a director for a new model.

### Twelve gates before it hands anything over

This one needs no explanation. Twelve items checked one by one: mode, spec header, character anchors, whether the action pays off, whether the camera move has a motive, light, three audio tracks, at least five negative constraints, style anchor, fidelity budget, ending profile, sequence chain.

Any single failure sends it back for a rewrite. **What reaches you already cleared the gate.**

### Want to think it through first? Hold a symposium.

This part is for humans, not for machines.

Say "let's talk it through first" and it won't fire back with *"what style are you after?"* — the most annoying question in the world, because you don't know either. It opens a session instead.

You get five options at once that are **genuinely different**, from five different seats. The producer cares whether anyone finishes watching. The writer cares whether there's a real dramatic core. The director cares what it will actually look like. The troublemaker exists purely to poke holes. And one seat always watches out for the only question that matters: *what do you actually want?*

One line each. No ranking, no recommendation — **it will not decide for you.**

Reply with a number, or "①+③", or even "none of these, but the direction of ②" — all of it counts. Then it collapses into a single concept card and gets to work.

One rule here is unusually strict: the troublemaker seat is mandatory. **A round with no genuine challenge counts as unfinished and gets reissued.**

Why so serious about it? Because the AI failure mode was never refusing to speak. It's **agreeing with you**.

### In batch production, the agents hold meetings too

On by default for short drama and long-form; off by default for a single shot. The split is deliberate — meetings cost tokens, and convening one for a 10-second shot isn't worth it. Say "no meeting" to switch it off.

It fills a very specific hole.

All 7 original self-checks lived in the format layer. **None of them could veto a story-level decision, and no role was authorised to question the skeleton.** 4,154 real revision clusters confirm the consequence: 69.7% of revisions add length and constraints, while the skeleton moves 2–6%. **Nobody touches the skeleton, because nothing in the pipeline owns it.**

Three meetings, clearly divided: a proposal meeting once after Step 3, a character meeting whenever a new character appears or an asset binding conflicts, and a review meeting before each batch of shots ships.

The flow: independent proposals → note-passing critique → one adjudicator rules → each writer restates it → synthesis.

"Note-passing" is literal. The critique round carries only *which passage, how severe, what kind of problem, one-line reason* — no full text, no complete alternative. Researchers found that once full solutions get exchanged, opinions converge **within a single round** — the loss happens at the moment of exchange.

And an honest floor: three runtime tiers. If it can spawn genuinely isolated contexts, that's a real meeting. If it can only role-play sequentially in one context, the deliverable must say "independence not fully guaranteed." If it can't separate roles at all, it gets labelled **"not collectively reviewed."**

**Saying plainly that no meeting happened beats making the deliverable look like one did.**

### The review log is itself a deliverable audit trail

Every critique carries a role, a target and a **falsifiable failure reason** — machine-readable.

Against "review before release" and "review consultation" requirements, that log is directly usable.

So, plainly: **even if the quality gain turns out marginal, auditability alone may be reason enough to adopt it.**

### How it flows

Three diagrams cover the whole information flow (SVG sources in [docs/](docs)):

![End-to-end information flow](docs/architecture-e2e.svg)
*From your one sentence to the finished output. QC failures loop back along the red dashed line. The dashed band at the bottom is the dev-time harness — not part of daily runs.*

![Short-drama per-shot loop](docs/architecture-shot-loop.svg)
*Short drama walks one loop per shot: split the beats, write the prompt, pass continuity checks, get your sign-off — only shots you accept become canon.*

![Long-form five-layer state stack](docs/architecture-longform.svg)
*For long-form (≥3 episodes / ≥60 shots / film), a five-layer stack goes on top: project bible → episode bible → scene card → batch state machine → shot. Each layer has a freeze point, so nobody's character falls apart halfway through.*

### Three scales, three deliveries

| You're making | Trigger | You get |
|---|---|---|
| One shot | a single request | one paste-ready prompt (full 600-2000 words / quick 80-300) |
| A short drama | multi-shot / storyboard | story breakdown · character-sheet prompts · continuity bible · shotlist · per-shot state machine |
| A long-form piece | ≥3 episodes / ≥60 shots / film | five-layer state stack · measured episode rhythm · style-pilot batch · cross-episode version registry |

### The data underneath

Nothing in `references/` or `scripts/` was written from thin air. All of it is a product of this corpus.

| Asset | Scale |
|---|---|
| Retrieval corpus | **7,824** real production prompts (562 gold, mean 1,622 words) |
| Raw collection | **588,686** assets (Hell Grind 115,447 + Cully Hill Boys 473,239) |
| Character / environment / prop cards | **1,607** cards, 40k+ appearance descriptions |
| Reference-element registry | **1,391** entries (`name` + `category` only) |
| Real revision clusters | **4,154** |
| Real image prompts | **61,554** |
| Story-layer density | 137 scenes · 42 transitions · 14 conflict types · 65 prop journeys · 16 act-structure points · 8 movement arcs |
| Rule library | **22** reference documents, 3,051 lines |

### Five small tools, all in the box

Zero dependencies (pure Python stdlib). They ship with the package; there's nothing to install.

| Script | Does | Run |
|---|---|---|
| `seedance_search.py` | Digs through 7,824 real examples, stripping source-project copyrighted content | `python3 scripts/seedance_search.py "<english keywords>" 3` |
| `diagnose_prompt.py` | Diagnoses a prompt you already have: contradictions, missing sections, missing constraints | `python3 scripts/diagnose_prompt.py my-prompt.txt` |
| `continuity_check.py` | Pre-delivery check: numbering, does shot N-1's ending state connect to shot N's opening, anchor spelling | `python3 scripts/continuity_check.py shots.md` |
| `validate_structure.py` | Anti-rot: contract phrases still present, cross-references not dead, no placeholders in the trunk | `python3 scripts/validate_structure.py` |
| `eval_retrieval.py` | Retrieval quality, fixed seed, reproducible | `python3 scripts/eval_retrieval.py` |

### It gates itself, too

- **CI** ([.github/workflows/ci.yml](.github/workflows/ci.yml)): eight steps, mandatory on push and PR — manifest, dependency existence, SKILL.md frontmatter, AGENTS.md structure, retrieval smoke, diagnoser smoke, anti-rot, install.sh syntax, README bilingual completeness.
- **Anti-rot**: `validate_structure.py` matches **line-anchored regexes rather than substrings**, because substrings produce false greens — `Step 5.5` is satisfied by `Step 5.5x`, and that hole was found by deliberately injecting a fault. It also fossilised a real incident into a check: after a routing change, `AGENTS.md` kept a contradictory stale sentence that only a manual grep caught.
- **Behaviour spec**: `tests/behavior-cases.json`, 17 cases across 7 categories. LLM behaviour can't be asserted, so `expected` is written as natural-language acceptance criteria for a human or another model to judge.
- **Render A/B loop**: `eval/render_loop/`, 12 cases × 2 arms = 24 renders. Grading covers instruction-following and technical defects only, **never aesthetics**; binary pass/fail/n/a, no numeric scale; the grading sheet is blind (verified to contain no arm field). Four rules are written into its README: canary first, cost ceiling before any call, cases frozen after preparation, and plan rows physically separated from observation rows.

### How to use it: it asks itself one question first — what do you actually want?

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

### Where it installs

```bash
./install.sh                          # finds your terminal automatically
./install.sh --target codex           # or pick one
./install.sh --target repo --repo /path/to/your/project   # install into a project
./install.sh --update                 # update an existing install
./install.sh --from-local <dir>       # copy from a local dir instead of git clone
```

| Terminal | Installs to | Reads |
|---|---|---|
| **Codex** | `~/.agents/skills/shortdrama-producer` (2026 spec, USER scope) | `AGENTS.md` |
| **Claude Code** | `~/.claude/skills/shortdrama-producer` | `SKILL.md` |
| **WorkBuddy** | `~/.workbuddy/skills/shortdrama-producer` | `SKILL.md` |
| **Cursor / Windsurf / Gemini CLI / Copilot** | `<your project>/.agents/skills/shortdrama-producer` | `AGENTS.md` |

Two easy-to-miss details, both learned the hard way: `--update` on a `--from-local` install **re-syncs** rather than running `git pull` (those copies have no `.git`, so otherwise they could only ever be deleted by hand); and backups always land one level **outside** `skills/` (`skill-backups/`), because the host scans that directory and would register the backup as a second, duplicate skill.

### What the tree looks like

```
shortdrama-producer-agent/
├── AGENTS.md                 # 2026 cross-tool standard (Codex/Cursor/Windsurf/Gemini/Copilot/Claude Code)
├── SKILL.md                  # skill-compatible layer (Claude Code / WorkBuddy)
├── manifest.json             # package metadata + dependencies + data scale (CI-validated)
├── agents/openai.yaml        # OpenAI / ChatGPT metadata and invocation policy
├── install.sh                # cross-terminal install / update
├── scripts/                  # 5 zero-dependency tools + the 7,824-doc corpus
├── references/               # 22 rule-library docs + card JSON + ref registry + story-layer density
├── docs/                     # 3 architecture diagrams (SVG sources)
├── tests/behavior-cases.json # 17 conversational behaviour specs
├── eval/render_loop/         # render A/B harness (dev-time evaluation, not a runtime feature)
├── NOTICE.md                 # corpus provenance, anonymisation scope, third-party rights
└── .github/workflows/ci.yml  # 8-step gate
```

### A few ground rules

- **It doesn't invent.** Advice that can't be traced to data doesn't ship. Second-hand figures are labelled.
- **Autonomy means you never do the technical work** — not that it never asks. It only asks when guessing wrong is expensive: concrete options, one round, then out of your way.
- **Learn the writing, never take the content.** Source-project characters, props and world settings are blocklisted from your output. Retrieval anonymises anchors into labels like `<<<CHARACTER_1>>>` and strips verbatim dialogue and lyrics.
- **Mechanically decidable problems don't get a vote.** Anything a script like `continuity_check.py` can settle goes through a hard constraint, not a meeting.

### Where it refuses to brag

Not bragging is one of this project's selling points.

- ⚠️ **Output quality is not yet validated against real renders.** The A/B harness is ready, 24 prompts are prepared, canary discipline is in place — but the renders haven't run, because there are no Seedance / Volcano Ark / Higgsfield credentials on this machine. Until they do, we make zero claims about real-world output quality. **A ready pipeline is not a verified quality claim.**
- ⚠️ **The meeting layer's quality gain has no A/B evidence, and that experiment is paused.** It ships on by default for short drama and long-form, but that's a deliberately accepted trade-off: get real usage data first rather than run a dedicated A/B now. Until results land, don't claim in any external material that it improves quality. If the A/B shows no improvement in the lower tail either, the layer should be dropped and the pipeline returned to single-subject plus hardened self-check.
- Hell Grind is sampled at 0.9%; Cully Hill Boys is cluster-deduplicated at full folder coverage.
- Some platform figures come from second-hand sources and are marked unverified. **The live product UI always outranks this repo.**
- Some design evidence comes from **preprints** (that 41.27% vs 86.36% figure, for instance), stated as "experiments show" rather than "proven". The meeting layer's 30% budget ceiling is a **tunable initial value**, not an empirical finding.

### Check it yourself

```bash
python3 scripts/validate_structure.py   # has the structure rotted?
python3 scripts/eval_retrieval.py       # retrieval quality, fixed seed
python3 scripts/continuity_check.py     # short-drama continuity chain check
```

### Thanks

This project stands on the shoulders of:

- **[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)** (MIT, by @iamemily2050)
- **[slipknot0130/Film-Production-Toolkit](https://github.com/slipknot0130/Film-Production-Toolkit)** (MIT, by @slipknot0130)
- The creators behind the source corpora (public Hell Grind / Cully Hill Boys assets) — anonymisation scope in [NOTICE.md](NOTICE.md)

### License

MIT License · Copyright (c) 2026 Eleven1111 · [LICENSE](LICENSE) ·
Corpus provenance and third-party rights: [NOTICE.md](NOTICE.md)
