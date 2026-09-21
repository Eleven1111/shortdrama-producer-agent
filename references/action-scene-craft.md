# 动作场景工艺库（Action Scene Craft）

> 来源：Higgsfield《The Trigger》（hitman × 战争闪回题材，seedance_2_5，5,429 jobs）动作类四场景 2,936 条 prompt 全量统计提炼。
> 与 `directorial-craft.md`（通用导演工艺）互补：本文件专注**枪战 / 追逃 / 搏斗 / 战争 / 威胁**类型场景。
> 配套数据：`story_level/conflict_patterns.json`（CHB chase/fight/shootout 样例）、`story_patterns.md`（冲突模式覆盖）。

## 0. 何时读

- 生成包含**开枪 / 搏斗 / 追逐 / 狙击 / 战争 / 暴力威胁**的镜头或场次时，必读 §3（暴力留白）+ §4（速度纪律）。
- 动作场一致性反复崩坏（换脸、换装、装备漂移）时，读 §2（法则分层）+ §8（装备锁）。
- 目标平台对暴力内容审核严格时，§3 是安全层的完整方案。

## 1. 数据画像（The Trigger 动作场景）

| 指标 | 数值 | 含义 |
|---|---|---|
| 动作场 prompt 均长 | 4,308–9,309 字符（中位 6,576） | 动作场 = 长列表式，比日常场长 2–4 倍 |
| 画幅 | 21:9 占 94.8% | 变形宽银幕是动作默认 |
| 参考图占比 | 53%–83% | 动作场更依赖外观锚定 |
| 否定短语密度 | 每条 10–30 个 `no X` | 否定清单是动作场的承重墙 |
| 秒级节拍 | 2,172 个时间拍 / 2,936 条 | 每条 prompt 都有 beat sheet |

## 2. 法则分层架构（Laws & Locks）——动作场的提示词骨架

CHB 的 `OPTICS/SCENE CONTEXT/ACTION` 是**分段**；动作场升级为**带优先级的法则块**。每块一个职责，块内声明裁决权：

```
【REFERENCES — RANKED】     参考图按优先级排序 + 裁决权声明
【<角色> LAW — HIGHEST PRIORITY】   该镜头最核心的一条表演/外观法则
【SILHOUETTE LAW — SECOND PRIORITY】次优先法则（藏与露，见 §7）
【FRAME】/【LIGHT】          镜头与光
【BEATS】                    秒级节拍表（§5）
【KIT OVERRIDE】             本场装备覆盖（§8）
ACTING TASK                  动机/目标/障碍/战术（§5）
物理 / 声音 / FORBIDDEN      物理合同 / 声音合同 / 否定清单（§9/§10/§11）
```

**优先级语法**（直接套用）：
- `【EYE LAW — HIGHEST PRIORITY】` / `【SILHOUETTE LAW — SECOND PRIORITY】`
- `IDENTITY (top priority): … If any instruction pulls a face off the reference, drop the instruction and keep the face.` —— 风格与身份冲突时，身份永远赢
- 参考图裁决权：`The asset decides the face. Scene text never overrides it.`（参考图管外貌身份，**不管**亮度与色调——后者由 prompt 的 LIGHT/GRADE 决定）

## 3. 暴力留白三件套（Implied Violence Doctrine）

Trigger 实测否定频次：`no blood` ×1,193、`no gore` ×715、`no muzzle flash` ×534、`no scope pov` ×894、`no reticle/crosshair` ×1,388（合计）。

三重动机：平台安全 + 反 AI 动作俗套（AI 最爱慢动作/瞄准镜 UI/枪口焰）+ 戏剧纪律。

| 手段 | 写法 | 例子 |
|---|---|---|
| ① 否定清单拦奇观 | FORBIDDEN 块集中列出 | `no blood, no gore, no muzzle flash, no scope POV, no reticle, no crosshair, no slow motion, no speed ramp` |
| ② 冲击转译为反应 | 写受击者的反应，不写弹道 | 眼睛的收缩、一次踉跄、手中物落地 |
| ③ 冲击转译为痕迹 | 事后状态独立成块 | `JACK'S WOUND`（166 次）：伤口是**连续性设定**（位置/深度/处理方式逐场锁死），不是画面奇观 |
| ④ "不作为"当节拍 | 负向动作独立成块 | `TERRENCE DOES NOT SHOOT`（116 次）：扣扳机的手比开枪更有戏 |

## 4. 速度纪律（Speed Discipline）

Trigger 动作签名：**静止→全速的零过渡**。

> `AND THEN, WITH NO WARNING AT ALL, HE MOVES — straight out of stillness into full speed. No wind-up, no preparation beat, no inhale before it.`

规则：
1. 爆发前一帧必须是完全静止；禁止预备拍（`no wind-up, no preparation beat, no inhale`）
2. 禁慢动作与变速：`no slow motion`（×990）、`no speed ramp`（×460）——写实动作片语法
3. 需要专门控制节奏时开 `SPEED` 独立块，只写速度要求，不混入动作描述

## 5. 动作节拍表（Beat Sheet + 硬切时间轴）

秒级节拍是动作场标配（`0.0–1.5s — …`），多镜头场加硬切标记（`3.5秒切`）：

```
镜头1——0.0至3.5秒——背影中远景，构图完全锁死。他只是坐着……什么也没发生。
3.5秒切
镜头2——3.5至5.9秒——桌面特写，极浅景深……
```

- **景别轮换模板**（Trigger SCENE 01 实测：7 镜头 22.5s，每镜景别与角度都不同）：背影中远景 → 桌面特写 → 顶视俯拍 → 低角推镜 → 侧后近景 → 微距 → 中景
- 表演内核四件套（`ACTING TASK`，×1,845）：

```
动机：他为什么在这
目标：这场他要完成什么（动词，可拍）
障碍：什么在拦（可拍的具体阻力）
战术：他具体怎么做（逐拍写进 BEATS）
安全线：目光始终投入任务，绝不僵死呆滞（反 AI 呆滞眼神）
```

## 6. 眼睛表演法则（EYE LAW）

动作决断时刻（发现目标 / 决定开枪 / 认出仇人），表演全部收进眼睛，四步可读：

1. `HE SEES` — 视线锁定一个具体点并停住
2. `HE MEASURES IT` — 微小快速眼动：扫一条线、回来、落定（在工作，不是做梦）
3. `HE KNOWS` — 眼睛微微睁大：上睑抬 2–3 毫米、瞳孔放大；禁止恐怖片瞪视、禁止眼白全露
4. `IT IS NOT HIS OWN LIFE` — 一瞬瞟向身边人再回目标（恐惧属于她，不属于他）

配套否定：`The mouth, brows, jaw and nostrils stay out of it. The FACE is quiet — the EYES are loud.`

## 7. 藏与露（Concealment Cinematography）

威胁在暗处时，**不给看**是最强的张力工具（`SILHOUETTE LAW`）：

- 人物 = 纯黑剪影：`Pure black, 100% unlit, not one feature, no eye, no cheek, no skin tone`
- 武器永不越界：`its muzzle and suppressor never crossing the sill`
- 画面 90–95% 纯黑，唯一亮部是窗外/门口的亮矩形
- 零成本适用于：狙击手、埋伏、门后的人、电话另一端的杀手

## 8. 装备真实感与 KIT OVERRIDE（Tactical Authenticity）

军/警/战术题材防装备漂移：

```
MILITARY AUTHENTICITY (mandatory): every soldier wears a tactical combat helmet
(fabric cover, NVG bracket) AND ballistic goggles — no exceptions. Desert-tan
coyote camo, plate carrier, gloves, caked with sweat and dust, worn not
costume-like. All long guns are sand-coloured; the only black w[eapon is X].
```

- 装备 = 清单式硬约束（品类 + 颜色 + 磨损状态 + 负向锁定）
- 质感关键词：`worn not costume-like`（穿过，不是戏服）
- 单场要换装/缴械时开 `KIT OVERRIDE`：只写**覆盖项**，其余继承全局 `KIT`

## 9. 声音替代冲击（Sound Replaces Impact）

- **实景音效合同**（`SOUND`，×1,539）：先列"能听到什么"（环境底噪清单），再写唯一台词，最后 `无旁白，无额外台词`
- 全片无音乐是 Trigger 最高频约束（`no music` ×2,536）——写实动作片靠静默制造压迫；可学 Trigger 把"无音乐"写成**剧情设定**（店规禁音乐、墙上贴告示），让模型更难违反
- 冲击力全部转译为声音细节：落杯闷响、纸张脆响、一次极慢呼气；距离感用"隔着一层水般发闷"

## 10. 道具微物理合同（Prop Physics）

动作场最容易崩的是道具物理。逐项写"物理合同"：状态定义 + 全程不变声明 + 否定清单：

```
纸和封面之间没有任何粘连：不吸附、不剥离、不拉丝、不产生胶感。
封面翻开一次到位，不来回摆动，不重复开合。
派完整稳定、不掉渣、不塌、不裂；整段视频里派一直保持这个样子。
```

枪械专项：后坐（recoil ×387）、抛壳（shell casing）、上膛、保险、收枪入套（holster ×281）各自单列一条物理预期。

## 11. FORBIDDEN 块架构（否定清单）

否定不是散落在正文，而是**结尾集中一块 + 分类**（×1,706）：

| 分类 | 高频项 |
|---|---|
| 音乐 | no music, no score, no soundtrack, no melody, no beat, no rhythm |
| 血腥 | no blood, no gore, no wound(特写), no muzzle flash |
| 炫技镜语 | no slow motion, no speed ramp, no zoom, no whip transition, no lens flare, no starbursts, no light streaks |
| UI/水印 | no reticle, no crosshair, no subtitles, no numbers, no watermark |
| 风格污染 | no anime, no costume look, no cold grade |

写作要点：FORBIDDEN 放 prompt 末尾；正文关键位置可对**最易违反的 1–2 项**复述一次（Trigger 的"第一条规矩"模式：正文用剧情设定讲一次，结尾 FORBIDDEN 再列一次）。

## 12. 移植模板（Trigger 骨架 → 本 Agent 用法）

动作/枪战场可直接套用的骨架（与 `prompt-templates.md` 的 ACTION TIMING 兼容：BEATS 即 ACTION TIMING 的 SEG 展开）：

```
【REFERENCES — RANKED】<<<anchor>>> 按优先级 + "The asset decides the face."
【<核心> LAW — HIGHEST PRIORITY】本镜头最关键的一条（表演/外观/物理）
【FRAME】镜头：焦段/机位/运动（写实动作：锁定或机械缓移；手持需写 "handheld, alive"）
【LIGHT】光：单一动机光源 + 否定炫技
【BEATS】0.0–Xs — … （每拍一个可见动作；硬切标 "X秒切"）
ACTING TASK：动机/目标/障碍/战术 + 安全线（反呆滞）
物理：关键道具逐项合同（含枪械后坐/抛壳）
声音：实景音效清单 + 唯一台词 + 无旁白
FORBIDDEN：分类否定清单（音乐/血腥/炫技/UI/风格污染）
```

分级适配：
- **单镜头 vlog 动作**（10s）：只保留 LAW + BEATS + FORBIDDEN 三块，其余压缩进正文
- **多镜头短剧动作场**（15s/镜）：全骨架；跨镜一致性靠 RANKED references + KIT OVERRIDE
- **非写实风格**（动漫/儿童）：§3 否定清单替换为该风格的红线（见 `directorial-craft.md` §14）

## 13. 红线速查（动作场自检）

- [ ] 爆发动作前一帧完全静止，无预备拍
- [ ] 无 slow motion / speed ramp / muzzle flash / scope POV / reticle
- [ ] 血与伤只在 FORBIDDEN 或 wound 连续性块中，不在画面里当奇观
- [ ] 冲击 = 反应 + 声音 + 事后痕迹，三者至少占二
- [ ] 决断时刻表演在眼睛里（四步之一），脸部其他器官静止
- [ ] 威胁在暗处 → 剪影法则，武器不越入亮区
- [ ] 装备清单式锁死 + `worn not costume-like`
- [ ] 无音乐（或写成剧情设定）；声音合同有底噪清单
- [ ] 关键道具物理合同（不粘连/不掉渣/不塌裂）
- [ ] FORBIDDEN 集中收尾 + 最易违反项正文复述一次
