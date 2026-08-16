# shortdrama-producer · 跨终端通用 Agent 包

把用户一句模糊的想法，变成**可直接粘贴的 Seedance 短剧/视频 prompt**——全自动，跨终端可用。

## 这是什么

一个**自包含的 Agent 包**（不是只绑定某家终端）：
- `AGENTS.md` — **2026 跨终端 Agent 标准**（Codex / Cursor / Windsurf / Gemini CLI / GitHub Copilot / Claude Code 都读）
- `SKILL.md` — skill 兼容层（Claude Code / WorkBuddy 按 skill 加载）
- `scripts/` — 零依赖检索器 + 4,348 条真实生产范例（纯 Python stdlib，任何终端有 `python3` 就能跑）
- `references/` — 写作规律 / 模板 / 序列协议

**为什么跨终端**：AGENTS.md 是 2026 年开放 Agent 标准（Codex/Cursor/Windsurf/Gemini CLI/Copilot 均读取），SKILL.md 覆盖 Claude Code/WorkBuddy；检索脚本零依赖；资源全部打包在本目录。任意终端「复制 → 用」，无需改代码。

## 安装（任一终端）

```bash
# Codex（个人级）
mkdir -p ~/.codex/skills && cp -r shortdrama-producer-agent ~/.codex/skills/shortdrama-producer

# Claude Code
mkdir -p ~/.claude/skills && cp -r shortdrama-producer-agent ~/.claude/skills/shortdrama-producer

# WorkBuddy
mkdir -p ~/.workbuddy/skills && cp -r shortdrama-producer-agent ~/.workbuddy/skills/shortdrama-producer

# Cursor / Windsurf / Gemini CLI / Copilot：把 AGENTS.md 放入项目或全局 agents 目录
```

## 使用（所有终端一致）

> "想做一个雨夜女孩在巷子里拿着照片走的视频，要有氛围感"

Agent 自动：① 解析意图（单镜头/短剧）→ ② 检索真实范例 → ③ 生成简报 → ④ 生成 prompt（10 条硬规则）→ ⑤ 质检（8 项，不过自动重写）→ ⑥ 交付。

短剧模式（说"短剧/分镜/多镜头"）自动补：故事拆解 → 连续性圣经 → shotlist → 逐镜 prompt → 状态机。

## 手动调用检索（可选）

```bash
python3 scripts/seedance_search.py "police helicopter chasing a white Escalade at night" 3
```

## 数据

| 项 | 值 |
|---|---|
| 检索库 | 4,348 条真实生产范例（金标 562 + 采样） |
| 来源 | Higgsfield "Cully Hill Boys" 473,239 资产 |
| 脚本 | 纯 Python stdlib，无 numpy/无 embedding 依赖 |
| 体积 | 打包 18MB |

## 版权

Copyright (c) 2026 Eleven1111 · MIT License
