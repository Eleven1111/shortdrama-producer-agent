# Prompt 模板库（两档）

> 所有模板满足 `seedance-writing-guide.md` 的 10 条硬规则。cinema 档默认；quick 档用于快速出片。

---

## 档位 A：cinema（电影级长版，600–2,000 词）

### 结构骨架（按序拼装）

```
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.

Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: <导演A> × <导演B>.
Lighting: <布光方式> — <光质细节>, atmospheric haze throughout.
Color: <分级或配色>.

<<<角色1>>> — <体型/发型/肤色/服装逐件/饰品>. CHARACTER REF — appearance only.
<<<角色2>>> [image1] — <外观锁定>.
<<<道具>>> — <外观/材质/位置>.

Location — <<<环境>>>: <建筑结构/材质/破损细节/光照方向/时间/大气>.

ONE CONTINUOUS <镜头类型> <焦距>mm lens, camera <机位高度>, <角度>, <运动>.
<动作序列：主语+动词+细节（面部表情/肢体/与环境的交互）>.

<氛围段：情绪词 + 光线/色调>.
audio: <环境音>; SFX only, no music.

Acting: Hollywood — <表演细节>.
Physics: <物理约束>.
no <AI感项>, no <物理错误项>, never <镜头失控项>, <一致性锁定项>.
```

### 拼装规则
- 每个 `<>` 都必须填实，不填空位。
- 角色 ≥1 个；场景段必写；镜头段三件套必写；负面约束 ≥5 条。
- 若简报不含道具/参考图，删对应段，不留占位。

### 示例（基于真实语料形态重构，非原文复制）

```
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.

Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: Emmanuel Lubezki × Roger Deakins.
Lighting: Natural light only — soft diffused overcast daylight, gentle rim light, atmospheric haze throughout.
Color: desaturated silver, cool tones; one warm accent in the frame.

<<<red_girl>>> — small slim figure, short dark hair, pale skin, round face. Wears a red knit sweater
over a white collar, dark pleated skirt, black stockings. CHARACTER REF — appearance only.

Location — <<<old_street>>>: narrow rain-wet asphalt street, low brick walls, distant neon sign glow,
cool blue hour light, light rain and mist in the air.

ONE CONTINUOUS LOW-ANGLE WIDE SHOT, 35mm lens, camera at knee height, tilted slightly upward,
slow push-in with subtle handheld drift. The girl walks toward the camera, turns her head slightly,
eyes catching the neon reflection, breath visible in the cold air.

Mood: lonely, atmospheric, quietly tense.
audio: distant traffic, soft rain, a faint neon hum; SFX only, no music.

Acting: Hollywood — micro-pauses before the turn, precise eye-line, wet living eyes with catch-lights.
Physics: real weight on every step, correct contact shadows, rain drips reacting to movement.
no 3D render, no floating props, no identity drift, never locked off on a tripod, no subtitles.
```

---

## 档位 B：quick（快速短版，80–300 词）

### 结构骨架（紧凑四段）

```
[规格一句话] — [风格锚一句话] — [氛围一句话]

[角色1] <<<name>>> — 外观一句话（含服装/关键特征）.
[场景] — 一句话（地点+光+大气）.

[镜头+动作] — 机位/焦距/运动 + 一句话动作，含微表情。

audio: 一句话音效; 负面约束 2-3 条（no X, no Y, never Z）.
```

### 示例

```
15s, 21:9, one continuous shot. Cinematic realism, Deakins-style natural light. Tense, rainy, intimate.

<<<red_girl>>> — girl in red sweater, dark hair, pale face, walking alone.
Old street — rain-wet asphalt, blue hour, mist, distant neon.

Slow push-in 35mm, handheld drift — she stops, turns, looks at camera with a quiet sad glance.
audio: rain and distant traffic; SFX only, no music. no 3D render, no floating props, no subtitles.
```

### quick 档取舍
- 只保留：角色一句、场景一句、镜头+动作一句、音频+负面约束。
- 丢弃：表演指导段、物理段、色彩分段（并入风格锚一句话）。
- 用户后续说"再细一点" → 升级为 cinema 档重写。

---

## 档位切换规则

- 默认 cinema；用户说「快/短/预览/先看看」→ quick。
- quick 出片后用户要正式版 → 基于同一简报直接升 cinema（不重新澄清）。
- 一次会话内角色/场景锚定复用，不重复定义。

---

## 档位 C：短剧模式（shotlist 分镜表 + 连续镜头）

> 短剧模式的全部 prompt 满足 10 条硬规则，另加序列协议（sequence-protocol.md）与连续性圣经（continuity-bible.md）约束。

### 结构骨架（短剧交付顺序）

```
### 短剧大纲（story-breakdown.md 产物）
<故事目标/结局/节拍/场/镜头预算>

### 连续性圣经（continuity-bible.md 产物）
<<<角色>>> — <剧集级外观定义> ...（每角色一段）
<<<场景>>> — <场景圣经> ...
<<<道具>>> — <道具圣经> ...

### Shotlist 分镜表
| shot | 场 | 镜头类型 | 机位/焦距/运动 | 内容一句话 | 衔接 |
|---|---|---|---|---|---|
| 1 | 1 | wide | 35mm, knee-high, push-in | 女孩走进巷口 | — |
| 2 | 1 | close-up | 85mm, eye-level, static | 她发现照片 | 延续 |
| ... | | | | | |

### 连续 Prompt（每条独立可粘贴，按 sequence-protocol 逐镜产出）
# shot 1 / total | 场 1 | 衔接: — | start: ... | end: ...
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.
Style: ...
<<<角色>>> — <引用连续性圣经，不改写> ...
Location — <<<场景>>>: <引用场景圣经> ...
ONE CONTINUOUS <镜头类型> <焦距>mm, camera <机位>, <运动>.
<动作> ...
audio: ...
no identity drift, characters identical across every cut, no floating props, no subtitles.

# shot 2 / total | 场 1 | 衔接: 延续 from shot 1 | start: <shot1 end> | end: ...
<同圣经引用 + 新镜头/新动作 + 承接上一镜结尾>
```

### 逐镜规则
- 每镜 prompt 复用圣经定义（拷贝不改写），只更新该镜的镜头/动作/衔接段。
- 序列头 3 行（shot N/total | 衔接 | start/end state）放在 prompt 正文前。
- 衔接方式三选：延续（默认）/ 时间跳跃 / 转场特写（见 sequence-protocol.md）。
- 同一批 ≤6 镜；批次间先更新状态机再产出下一批。
- 每镜带一致性负面约束：`no identity drift, characters identical across every cut`。

### 短剧示例（2 镜，示意衔接写法）

```
# shot 1 / 2 | 场 1 | 衔接: — | start: 女孩站在巷口 | end: 她弯腰捡起湿透的照片
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.
Style: 8K IMAX. Photorealistic — no 3D render. Cinematography: Lubezki × Deakins.
<<<red_girl>>> — small slim figure, short dark hair, pale skin, red knit sweater, dark pleated skirt... CHARACTER REF — appearance only.
Location — <<<old_street>>>: rain-wet asphalt, blue hour, mist, distant neon.
ONE CONTINUOUS LOW-ANGLE WIDE SHOT, 35mm lens, slow push-in, handheld drift.
She walks toward the camera, stops, crouches, picks up a soaked photograph from the puddle.
audio: rain, distant traffic; SFX only, no music.
no 3D render, no floating props, no identity drift, no subtitles.

# shot 2 / 2 | 场 1 | 衔接: 延续 from shot 1 | start: 她握着照片起身 | end: 她抬头看向巷口灯光
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.
Style: 8K IMAX. Photorealistic — no 3D render. Cinematography: Lubezki × Deakins.
<<<red_girl>>> — <同 shot 1 引用，不重写> ...
Location — <<<old_street>>>: <同场景圣经> ...
ONE CONTINUOUS CLOSE-UP, 85mm lens, eye-level, slow tilt up from photo to her face.
Her eyes widen, breath catches, she looks up toward the distant streetlight at the alley mouth.
audio: rain softens, a faint hum; SFX only, no music.
no identity drift, characters identical across every cut, no floating props, no subtitles.
```

### 档位切换（短剧内）
- 默认每镜 cinema 档；用户说"快点" → 每镜 quick 档（80-300 词），但圣经与序列头保留。
- 用户只要其中一镜 → 单独交付该镜（含序列头，标注衔接来源）。
