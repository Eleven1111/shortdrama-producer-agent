# 连续性锁块与静场工艺库（Continuity Locks & Quiet-Scene Craft）

> 来源：Higgsfield《The Trigger》5,429 jobs 非动作维度提炼（静场戏剧 / 字幕场景 / 角色资产工厂 / 中文 prompt 证据）。
> 与 `action-scene-craft.md`（动作场）、`continuity-bible.md`（跨场连续性文档）、`character_cards_visual.md`（角色卡库）互补。

## 0. 何时读

- 跨镜一致性反复崩坏（换脸/换光/换台词/文字乱加字）→ §1 锁块家族 + §2 参考图权限
- 安静场景（对话/等待/凝视/仪式感）表演空洞 → §3 微表演 + §4 声音合同
- 涉及**可读文字**的镜头（片头片尾/字幕卡/信件/屏幕/文件特写）→ §6 文字场景范式
- 需要批量生产角色/群演参考板 → §7 资产工厂
- 用户是中文创作者、或希望用中文写作 prompt → §8 中文范式

## 1. 锁块家族（Lock Blocks）——把连续性写进每条 prompt

`continuity-bible.md` 是**跨场文档**；锁块是**每条 prompt 内的强制条款**。生成每条 prompt 时，从 bible 摘取本场相关的 3–6 把锁写成具名块。

实测频次（The Trigger 全项目）：`KIT OVERRIDE` ×247、`BRIGHTNESS LOCK` ×128、`MOVEMENT LAW` ×87、`TEXT LOCK` ×84、`DIALOGUE LOCK` ×32、`LIGHT LOCK` ×32、`HEIGHT LOCK` ×29、`SCOPE LOCK` ×29、`FACE LOCK` ×28、`IDENT` ×125。

**锁块写法公式**：

```
<名> LOCK — <一句话说明为什么这是本场最重要的事>。
<正向描述：具体到米 / 度 / 毫米 / 张数>。
<never 否定串：封死所有漂移方向>。
```

实测样板（SCENE 02，32 个 job 100% 遵循）：

```
HEIGHT LOCK — THIS IS THE MOST IMPORTANT THING IN THE SHOT. …we look DOWN onto
the ROOF of the car… This is never a street-level view, never eye-level with
anyone… and equally never a straight-down bird's eye.

SCOPE LOCK: …ONE LOCKED MAGNIFICATION for the whole scene: the scope never
zooms, never changes magnification, never racks focus, never punches in.

LIGHT LOCK — BACKLIGHT ONLY. …NOTHING LIGHTS THEM FROM THE FRONT. …no key
light, no fill, no bounce off the pavement…

DIALOGUE LOCK: NOBODY SPEAKS IN THIS WHOLE SCENE. No lines, no shouting, no
whispering, no mouthing of words, no voice-over.
```

常用锁速查：

| 锁 | 管什么 | 写法要点 |
|---|---|---|
| FACE LOCK | 面容 | 指向参考图 + "The asset decides the face" |
| LIGHT LOCK | 光位 | 唯一光源方位 + 正面禁光清单 |
| DIALOGUE LOCK | 台词 | 全场说话人数与内容，或"无人说话" |
| HEIGHT/GEOGRAPHY LOCK | 空间 | 楼层/高度角/门窗方位，具体到度和米 |
| BRIGHTNESS LOCK | 亮度 | 逐场锁定曝光水平，防跨镜忽亮忽暗 |
| TEXT LOCK | 文字 | 白名单式锁死画内文字（见 §6） |
| KIT OVERRIDE | 装备 | 单场覆盖全局设定，只写差异项 |
| MOVEMENT LAW | 运动 | 什么能动、什么永远不动 |

## 2. 参考图权限分层

> `参考图只控制外貌、服装与场景身份，不控制画面亮度与色调。`

- 参考图管"**是什么**"（身份/外观/空间身份），prompt 管"**怎么样**"（光/色/运动/表演）。
- 多参考图时按优先级排序（RANKED），并声明冲突裁决权：`The asset decides the face. Scene text never overrides it.`
- 参考图不出现时（见 §7 资产工厂），靠纯文本超长约束文档替代其职能。

## 3. 静场微表演（LIVING PERFORMANCE）

安静场景的表演工程——"什么都没发生"也要写出来：

- **首帧声明**：`FIRST FRAME & STAGING` 独立块——开画第一帧的姿态/构图/视线方向（实测 ×47）
- **微动作清单**：呼吸起伏一次、手指轻叩、窗外虚化行人经过、杯子热气细丝——每条都是可见的"活着"证据
- **眨眼纪律**：自然眨眼节奏；`最后一拍才停止眨眼`——用眨眼停止标记情绪节点
- **表演四件套**（`GOAL / OBSTACLE / TACTIC / 动机`）不分动静场通用：动机→目标（可拍动词）→障碍（具体阻力）→战术（逐拍进 BEATS）
- **反呆滞安全线**：`目光始终投入任务，绝不僵死呆滞、绝不空洞发直`
- **收尾三连**：停住一拍 → 画面定格 → 切黑

## 4. 声音合同（静场版）

- **把"无音乐"写成剧情设定**（模型更难违反）：`这家店按店规禁止播放音乐:墙上贴着一块手写告示，老板从不开音响……整段视频里一秒钟的音乐都不存在`
- **底噪逐项清单**：咖啡机蒸汽、后厨油声、听不清的低语、门铃、椅子拖动、风扇低频——给"安静"一个可执行的声音配方
- **收束设计**：`最后四秒只剩底噪与他一次极慢的呼气`——用声音做节拍器
- 台词条款：唯一台词 + `全程不说话，嘴唇静止`

## 5. 道具微物理合同 + 叙事道具

每个关键道具三件套：**状态定义 + 全程不变声明 + 否定清单**：

```
液面平整、落杯时晃动一次即止；派完整稳定、不掉渣、不塌、不裂；
纸和封面之间没有任何粘连：不吸附、不剥离、不拉丝、不产生胶感。
```

**prop-as-plot-device**：核心叙事装置值得为它单开生成文件夹反复打磨（实测：一张载有暗杀订单的账单夹，独立子文件夹 ×52 条，贯穿全片 6 场）。识别标准：删掉这个道具剧情是否崩——崩，就给它建资产级打磨流程。

## 6. 文字与字幕场景范式（CREDITS 语法）

涉及可读文字的镜头（片头片尾/字幕卡/信件/文件/屏幕），否定词密度全场最高（68/条）——文字场景最怕模型乱加字：

- **文字白名单**：`TEXT LOCK` / `THE ONLY WORDS THAT EXIST IN THIS SHOT ARE <逐字列出>` ——画内只允许出现列出的字
- **可读性法则**：`THE CAMERA IS LOCKED WHENEVER TEXT IS READABLE` ——文字可读时摄影机静止
- **运动立法**：`MOVEMENT LAW` ——什么时候能移、移到哪停
- **分页组织**：文字内容多时按 `PAGE 1…PAGE N` 分页，每页独立成块（实测一部片尾 7 页 ×110 条）
- 中文场景同构：`画内只出现以下文字，其余全是空白` + 逐字列出 + `没有别的字、没有店名、没有logo、没有水印`

## 7. 角色资产工厂（Casting Sheet 范式）

角色参考板是**纯文本超长 prompt** 生成的（实测角色卡 196 条：均长 10,608 字符、否定词 86/条、仅 6% 带参考图；最长 26,201 字符）：

```
Photorealistic full-length CASTING AND WARDROBE REFERENCE SHEET…
FIFTEEN fighters…ONE SINGLE STRAIGHT ROW…ALL FACING THE CAMERA DEAD-ON,
FRONT VIEW ONLY…every figure FULL LENGTH, nothing cropped…

BODY RULE — ABSOLUTE: EVERY MAN IS LEAN AND HARD…ABSOLUTELY NOBODY IS FAT:
no bellies, no gut… and equally nobody bodybuilt or gym-inflated.

The hostility is DIFFERENT ON EVERY FACE and never a mask: one openly furious,
one flat and dead-eyed, one coldly contemptuous, one stony and patient…
```

要点：
- **双向体型否定**：禁胖 + 禁健美（两个方向都要封）
- **差异化人格清单**：`DIFFERENT ON EVERY FACE` + 逐个列举具体变体——批量生成防"千人一面"
- **工厂流水线**：批量生成参考板 → 挑选 → 全片引用（实测主角 JACK 332 条 / TERRENCE 265 条的生成复购）
- 与 `character_cards_visual.md` 衔接：该库提供卡片写法语料；本节提供**批量生产模板**（多人一板 + 全身 + 正面 + 影棚均匀光）

## 8. 中文 prompt 范式（第三语料证据）

HG / CHB 语料全为英文；The Trigger 补上了关键证据——**Seedance 接受整段中文长 prompt**：

| 场景 | 中文 prompt 占比 | 均长 |
|---|---|---|
| SCENE 01（咖啡馆静场戏） | **78%** | 4,337 字符 |
| SCENE 03 | 31% | 4,618 字符 |
| PROJECT ROOT | 14% | 7,506 字符 |

**中英混排范式**（可直接套用）：
- 正文（场景/表演/物理/声音）整段中文
- 台词保留英文引号原文：`画外女声带着笑意:"Your check."`
- 否定关键词可英文混排：`no music, no score, no soundtrack…`（也可全中文：`没有音乐、没有配乐…`，实测两者都成立）
- 镜头术语可中文（`顶视俯拍、荷兰角约12度、构图锁死`），无需硬翻英文

对本 Agent 的意义：中文用户可全程中文写作 prompt；台词按目标语言放引号内；不必为"模型要英文"而翻译——把翻译时间还给内容。

## 9. 数据画像

| 场景 | jobs | 均长 | 中文占比 | 参考图 | 否定词/条 |
|---|---|---|---|---|---|
| SCENE 01 静场+暗杀 | 443 | 4,337 | 78% | 56% | 11.3 |
| SCENE 02 锁块样板场 | 32 | 7,844 | 0% | 100% | 48.3 |
| SCENE 05 字幕场景 | 341 | 6,836 | 0% | 63% | **68.4** |
| ASSETS/Characters 角色卡 | 196 | **10,608** | 0% | 6% | **86.0** |

## 10. 红线速查

- [ ] 每条 prompt 从 bible 摘 3–6 把锁写成具名 LOCK 块（正向具体 + never 串）
- [ ] 参考图权限声明：管身份不管光色；多图按优先级 + 裁决权
- [ ] 静场有 FIRST FRAME 首帧声明 + 微动作清单 + 眨眼节点
- [ ] "无音乐"尽量写成剧情设定；底噪逐项列；收束有声设计
- [ ] 关键道具三件套（状态/不变/否定）；叙事装置道具走资产级打磨
- [ ] 画内可读文字 = 白名单逐字锁 + 可读时摄影机静止
- [ ] 批量角色板：双向体型否定 + 差异化人格逐个列
- [ ] 中文写作可用；台词引号保留目标语言
