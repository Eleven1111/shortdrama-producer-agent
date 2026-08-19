# 第三方声明 · Third-party notice

## 独立项目

本项目是独立的社区工具，**与 ByteDance、Dreamina／即梦、Seedance、Higgsfield 均无
关联，未获其背书或赞助**。上述平台名称、商标、文档与服务行为的权利归各自所有者。

This is an independent community project, **not affiliated with, endorsed by, or sponsored
by ByteDance, Dreamina, Seedance, or Higgsfield**. Platform names, trademarks,
documentation, and service behaviour remain the property of their respective owners.

## 数据来源

`scripts/seedance_corpus.jsonl.gz`、`references/iteration-lessons.md`、
`references/reference-image-protocol.md`、`references/character_cards_visual.*`、
`references/reference_registry.json`、`references/story_level/*` 中的统计结论与写法规律，
来自对 Higgsfield 平台上两个**公开可访问**项目页面的资产采集与分析：

| 项目 | 采集量 |
|---|---|
| Hell Grind | 115,447 条资产 |
| Cully Hill Boys | 473,239 条资产 |

采集只经由公开页面，未使用平台账号凭据，未调用其生成接口，未消耗他人额度。

## 语料里究竟存了什么（请如实理解）

**语料 `seedance_corpus.jsonl.gz`（7,824 条）保存的是源项目 prompt 的原始文本**，
包含其原有的锚点标识与描写。这一点不做含糊表述。

匿名化发生在**检索输出环节**（`scripts/seedance_search.py` 的 `strip_copyright`），
每次检索交给模型的文本会：

- 把资产锚点替换为 `<<<CHARACTER_1>>>` / `<<<PROP_2>>>` 等匿名标签；
- 把正文中出现的源项目角色专名一并匿名化；
- 按内容特征剥离台词与歌词原文，仅保留时间码结构。

已从仓库中**移除且不再分发**的内容：源项目创作者的账号标识（`user_*`）与素材直链
（CloudFront URL）。`references/reference_registry.json` 只保留 `name` 与 `category`
两个字段。

## 用途与边界

这些数据在本项目中的用途是**方法论研究**：统计真实生产中的结构写法、约束习惯与修订
方向，用以指导 Agent 生成**用户自己的**内容。

Agent 的运行规则明确禁止把源项目的故事、角色、道具或世界观设定搬进用户产出
（见 `references/iteration-lessons.md` §4 的黑名单、`references/reference-image-protocol.md`
的边界章节，以及 `AGENTS.md` / `SKILL.md` 的 Boundaries）。
`character_cards_visual.*` 是**写法教材，不是素材库**。

## 平台能力信息

`references/platform-capabilities.md` 中标注为 `[官方]` `[报道]` `[未验证]` 的条目，
是对公开文档与公开报道的独立整理与归纳，非原文转载。**运行时 UI 与本仓库冲突时，
一律以平台当前 UI 为准。**

## 权利主张与联系

若你是上述项目的权利人，认为本仓库的任何内容超出了合理的研究与互操作范围，请通过
GitHub Issue 联系，我们会及时移除或调整相关内容。

If you hold rights to any referenced material and believe its inclusion here exceeds
reasonable research or interoperability use, please open a GitHub issue and it will be
removed or adjusted promptly.

## 本项目自身的许可

本仓库的代码与文档以 MIT 许可发布，见 [LICENSE](LICENSE)。该许可适用于本项目的原创
部分，**不构成对上述第三方素材的任何权利授予**。
