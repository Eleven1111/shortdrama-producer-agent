# Seedance Short-Drama Producer Agent

**Turn a vague idea into a paste-ready Seedance 2.5 short-drama prompt — fully automated, cross-terminal.**

A self-contained agent package. The host agent (Claude Code / Codex / WorkBuddy / Cursor / Windsurf / Gemini CLI / GitHub Copilot) reads it, executes the production workflow end-to-end, and returns a finished prompt. **No LLM API to wire up, no external services, no Python packages** — the user just describes the idea.

> 把一句模糊的想法，变成可直接粘贴的 Seedance 2.5 短剧/视频 prompt——全自动、跨终端。宿主 Agent（Claude Code / Codex / WorkBuddy / Cursor / Windsurf / Gemini CLI / GitHub Copilot）读取本包后自动跑完整生产流程并交付成品。**无需接入任何 LLM API、无外部服务、零 Python 依赖**——用户只需描述想法。

---

## English

### What this is

| Artifact | Role |
|---|---|
| `AGENTS.md` | Core definition — the 2026 cross-terminal open standard (read by Codex / Cursor / Windsurf / Gemini CLI / GitHub Copilot / Claude Code). Contains the full autonomous workflow as system instructions. |
| `SKILL.md` | Compatibility layer — lets Claude Code / WorkBuddy load the same agent as a skill. Same content as `AGENTS.md`. |
| `agents/openai.yaml` | OpenAI metadata — UI name, description, invocation policy and tool deps for ChatGPT / Codex. |
| `scripts/seedance_search.py` | Zero-dependency BM25 retriever (pure Python stdlib). Retrieves real production examples. |
| `scripts/seedance_corpus.jsonl.gz` | 7,824 real Seedance production prompts (1,039 Hell Grind sampled + 6,785 Cully Hill Boys cluster representatives covering 937 folders), gold-tagged, copyright-stripped at query time. |
| `references/` | Writing guide (cross-project verified), prompt templates, sequence protocol, continuity bible, character card lexicon (1,607 cards), story-level patterns (3-act pacing, character journeys, prop journeys, beat transitions, conflict templates, movement arcs). |
| `install.sh` | One-command install / update for any supported terminal. |
| `manifest.json` | Package metadata (version, tags, dependencies). |

### Install

```bash
# one command, auto-detect terminals
./install.sh

# or target one terminal
./install.sh --target codex        # OpenAI Codex  -> $HOME/.agents/skills/shortdrama-producer
./install.sh --target claude       # Claude Code   -> $HOME/.claude/skills/shortdrama-producer
./install.sh --target workbuddy    # WorkBuddy     -> $HOME/.workbuddy/skills/shortdrama-producer
./install.sh --target repo --repo ~/myproject   # AGENTS.md-only terminals (Cursor/Windsurf/Gemini CLI/Copilot) -> <repo>/.agents/skills/

# update an existing install
./install.sh --update
```

After installing, **restart your terminal/agent** so the skill is discovered.

### Usage

Describe your idea in any language. The agent runs the whole workflow:

> "A girl walking through a rainy alley at night, holding a wet photograph, neon reflecting in puddles — moody."

1. **Parse intent** — single-shot (cinema / quick) or short-drama (multi-shot) mode
2. **Retrieve** — BM25 search over 7,824 real production examples (auto-runs the bundled script)
3. **Brief** — internal creative brief (subject / action / setting / mood / style anchor)
4. **Generate** — full Seedance prompt (SCENE CONTEXT → ACTIVE REFERENCES → OPTICS → ACTION → negatives → audio), 10 hard rules from verified corpus statistics
5. **Self-check** — 8-point quality gate; rewrite until passing
6. **Deliver** — paste-ready prompt + ≤3 short notes

**Short-drama mode** (say "short drama / storyboard / multi-shot") additionally produces: story breakdown → continuity bible → shotlist → per-shot prompts → state machine.

Manual retrieval (optional):

```bash
python3 scripts/seedance_search.py "police helicopter chasing a white Escalade at night" 3
```

### Data & provenance

| Item | Value |
|---|---|
| Retrieval corpus | 7,824 real production prompts (1,039 Hell Grind + 6,785 Cully Hill Boys) |
| Gold set | 562 (Seedance 2.5 "one-shot success" regenerations, `0 Regenerations` folder) |
| Source | Higgsfield public projects: "Hell Grind" (115,447 assets) + "Cully Hill Boys" (473,239 assets) |
| Character lexicon | 1,607 cards (character / environment / prop) with 40k+ appearance descriptions |
| Story patterns | 3-act pacing (Act 1 climax=0 → Act 4 climax=163), top-5 character journeys, props crossing up to 6 scenes, beat/transition distributions, 14 conflict templates |
| Retriever | Pure Python stdlib BM25 — no numpy, no embedding, no network at query time |
| Size | ~24 MB packaged |

### Boundaries

- Pure image prompts → decline; non-Seedance models → decline; rendering / API calls → decline
- IP / celebrity / likeness risk → warn, never infringe
- The corpus is a **style teacher, not content source** — never import source-project story, characters or props into user work (retriever strips copyrighted ACTIVE REFERENCES automatically)

### License & update

MIT License · Copyright (c) 2026 Eleven1111.

Update: `git pull` in the source dir, then `./install.sh --update`, or per install: `git -C ~/.agents/skills/shortdrama-producer pull`.

---

## 中文

### 这是什么

| 文件 | 作用 |
|---|---|
| `AGENTS.md` | 核心定义——2026 跨终端开放标准（Codex / Cursor / Windsurf / Gemini CLI / GitHub Copilot / Claude Code 均读取），正文即完整自主工作流系统提示 |
| `SKILL.md` | 兼容层——Claude Code / WorkBuddy 按 skill 加载同一 Agent，内容与 AGENTS.md 同源 |
| `agents/openai.yaml` | OpenAI 元数据——ChatGPT / Codex 的 UI 名称、描述、调用策略与工具依赖声明 |
| `scripts/seedance_search.py` | 零依赖 BM25 检索器（纯 Python stdlib），检索真实生产范例 |
| `scripts/seedance_corpus.jsonl.gz` | 7,824 条真实 Seedance 生产 prompt（Hell Grind 1,039 采样 + Cully Hill Boys 6,785 cluster 去重代表，覆盖 937 个文件夹），含金标标签、检索时剥离版权内容 |
| `references/` | 写作规律库（跨项目验证）、模板、序列协议、连续性圣经、角色卡词典（1,607 张）、故事级模式（3 幕节奏/角色旅程/道具跨场/节拍转场/冲突模板/调度曲线） |
| `install.sh` | 一条命令安装/更新到任意支持的终端 |
| `manifest.json` | 包元数据（版本、标签、依赖） |

### 安装

```bash
# 一条命令，自动检测终端
./install.sh

# 或指定目标
./install.sh --target codex        # OpenAI Codex  -> $HOME/.agents/skills/shortdrama-producer
./install.sh --target claude       # Claude Code   -> $HOME/.claude/skills/shortdrama-producer
./install.sh --target workbuddy    # WorkBuddy     -> $HOME/.workbuddy/skills/shortdrama-producer
./install.sh --target repo --repo ~/myproject   # 仅 AGENTS.md 的终端（Cursor/Windsurf/Gemini CLI/Copilot）-> <repo>/.agents/skills/

# 更新已安装
./install.sh --update
```

安装后**重启终端/Agent** 以识别 skill。

### 使用方法

用任何语言描述你的想法，Agent 自动跑完整工作流：

> "想做一个雨夜女孩在巷子里拿着照片走的视频，要有氛围感"

1. **解析意图** — 单镜头（cinema / quick）或短剧（多镜头）模式
2. **检索** — 对 7,824 条真实生产范例做 BM25 检索（自动运行内置脚本）
3. **简报** — 内部生成创意简报（主体 / 动作 / 场景 / 氛围 / 风格锚）
4. **生成** — 完整 Seedance prompt（SCENE CONTEXT → ACTIVE REFERENCES → OPTICS → ACTION → 负面约束 → 音频），10 条硬规则来自语料统计
5. **质检** — 8 项自检，不过自动重写
6. **交付** — 可直接粘贴的 prompt + ≤3 条简短说明

**短剧模式**（说"短剧 / 分镜 / 多镜头"）自动追加：故事拆解 → 连续性圣经 → shotlist → 逐镜 prompt → 状态机。

手动检索（可选）：

```bash
python3 scripts/seedance_search.py "police helicopter chasing a white Escalade at night" 3
```

### 数据与出处

| 项 | 值 |
|---|---|
| 检索库 | 7,824 条真实生产 prompt（Hell Grind 1,039 + Cully Hill Boys 6,785） |
| 金标集 | 562 条（Seedance 2.5 "一次成型"重生成，`0 Regenerations` 文件夹） |
| 来源 | Higgsfield 公开项目："Hell Grind"（115,447 资产）+ "Cully Hill Boys"（473,239 资产） |
| 角色词典 | 1,607 张卡（角色/场景/道具）+ 4 万+ 条外观描述 |
| 故事模式 | 3 幕节奏（Act1 climax=0 → Act4 climax=163）、Top5 角色旅程、跨场道具（最多跨 6 场）、节拍/转场分布、14 种冲突模板 |
| 检索器 | 纯 Python stdlib BM25——无 numpy、无 embedding、查询时无网络 |
| 体积 | 打包约 24 MB |

### 边界

- 纯图像 prompt → 不做；非 Seedance 模型 → 不做；实际渲染/API 调用 → 不做
- IP / 名人 / 肖像风险 → 警告，绝不侵权
- 语料是**风格老师，不是内容源**——绝不把源项目的剧情、角色、道具搬进用户作品（检索器已自动剥离版权 ACTIVE REFERENCES 段）

### 许可证与更新

MIT License · Copyright (c) 2026 Eleven1111.

更新：源目录 `git pull` 后 `./install.sh --update`；或对每个安装 `git -C ~/.agents/skills/shortdrama-producer pull`。
