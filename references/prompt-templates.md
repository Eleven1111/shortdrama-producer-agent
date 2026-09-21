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
- 序列头 **必须是 3 个独立行**，放在 prompt 正文前，且 `start state` / `end state` 的
  前缀逐字固定（`# start state:` / `# end state:`）——`continuity_check.py` 的
  `HEADER_START/HEADER_END` 是**行首锚定**解析：把三者挤在一行（`# shot 1/2 | … | start: X | end: Y`）
  会让每一镜都报 `序列头缺 start/end state 行`（ERROR，退出码 1），是格式陷阱不是内容缺陷。
  含 `from shot N-1` 的衔接字段同样要留在第一行。
- 衔接方式三选：延续（默认）/ 时间跳跃 / 转场特写（见 sequence-protocol.md）。
- 同一批 ≤6 镜；批次间先更新状态机再产出下一批。
- 每镜带一致性负面约束：`no identity drift, characters identical across every cut`。

### 短剧示例（2 镜，示意衔接写法）

```
# shot 1 / 2 | 场 1 | 衔接: —
# start state: 女孩站在巷口
# end state: 她弯腰捡起湿透的照片
Duration: 15 seconds. Aspect ratio: 21:9. One continuous shot.
Style: 8K IMAX. Photorealistic — no 3D render. Cinematography: Lubezki × Deakins.
<<<red_girl>>> — small slim figure, short dark hair, pale skin, red knit sweater, dark pleated skirt... CHARACTER REF — appearance only.
Location — <<<old_street>>>: rain-wet asphalt, blue hour, mist, distant neon.
ONE CONTINUOUS LOW-ANGLE WIDE SHOT, 35mm lens, slow push-in, handheld drift.
She walks toward the camera, stops, crouches, picks up a soaked photograph from the puddle.
audio: rain, distant traffic; SFX only, no music.
no 3D render, no floating props, no identity drift, no subtitles.

# shot 2 / 2 | 场 1 | 衔接: 延续 from shot 1
# start state: 她握着照片起身
# end state: 她抬头看向巷口灯光
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

---

## 必读踩坑：段头必须独立成行

`scripts/diagnose_prompt.py` 的段头识别正则是 `^([A-Z][A-Z0-9 &/'()-]{3,44})\s*$`（`re.M`）——
**要求该行只有大写段头本身，行内不能再有内容。**

| 写法 | 诊断器 | 后果 |
|---|---|---|
| `STYLE — Photorealistic live-action...` | ✗ 认不出 | 该段报"缺失" |
| `Lighting: soft overcast...` | ✗ 认不出（大小写不符） | 该段报"缺失" |
| `STYLE`<br>`Photorealistic live-action...` | ✓ | 正常 |

实测后果：整条 prompt 只有 `ACTIVE REFERENCES` 被识别，其余 8 个基准段头
（`SCENE CONTEXT` `OPTICS` `CAMERA` `LIGHTING` `PHYSICS` `AUDIO` `ACTION TIMING` `STYLE`）
全部被报成"缺失"——而 prompt 本身其实写得没问题。**这是格式陷阱，不是内容缺陷，别去改内容。**

**spec header 陷阱（2026-09-15 实测）**：含 SEG 硬切的多段 prompt，规格行不要照抄
`One continuous shot.` —— 会触发诊断器的 ⛔ 内部矛盾「声明一镜到底又写了硬切」。
改写为与内容一致的声明：`Five shots, four hard cuts.` / `Multi-shot montage — six shots, five hard cuts.`
/ `Three shots, two hard cuts.`；只有真·一镜到底（段间是连续运镜、无硬切词）才保留 `One continuous shot.`

**单镜 prompt 的假「多镜头」误判（2026-09-18 实测）**：把一个批次文件逐镜拆开、单独丢给
`diagnose_prompt.py` 时，序列头 `# shot 1 / 4 | …` 会命中诊断器的 `multi_shot` 判据
（`shot \d+/`），于是每一镜都被判成「多镜头」，并因此索要 `hard_cut_timecode` 约束——
**而这一镜本身是真·一镜到底，根本不存在硬切。这是判据的假阳性，不是内容缺陷。**
两种解法：
- ✅ 推荐：把动作段里的时间码写成**无空格**形式 `3.5s–8.0s`（正则 `\d+(\.\d+)?s\s*[-–]\s*\d+(\.\d+)?s` 命中），
  既如实交代时序，又满足约束检测。
- ❌ 不要为了过检测而往单镜 prompt 里塞 `hard cut` 字样 —— 那会与 `One continuous shot.`
  构成**真**矛盾，把假阳性升级成真报错。
另外：`LIGHTING` 段在语料里出现率 47.8%，别把布光并进 `STYLE` 一句话带过——2D/动漫媒介下
`LIGHTING` 写"画出来的光"（固定光源、双色 cel 阴影、光斑形状），照样过段头识别。

推荐段序（与语料 8-12 段结构化范式一致）：

```
STYLE / LIGHTING / SCENE CONTEXT / ACTIVE REFERENCES /
OPTICS / CAMERA / ACTION TIMING（含 SEG 与 HARD CUT 时间码）/
MOOD / CHARACTER ACTING / PHYSICS / AUDIO / NEGATIVE
```

`OPTICS` 与 `CAMERA` 段可写成**分镜索引**（`SEG 1 — 29° (≈85 mm) medium close. SEG 2 — 84° (≈24 mm) extreme wide.`），
把逐段的详细机位句留在 `ACTION TIMING` 的 SEG 段落里——索引+细节分层，不重复。

## 交付形态（用户既定偏好）

短剧交付默认产出 **单文件、零外部依赖的可复制 HTML**：每个 prompt 配一个 copy 按钮，
另配一个 copy-all 按钮；prompt 正文放在 `<pre>` 里，用 `textContent` 复制（避免 `<<<` 被 HTML 转义吃掉）。
再附一份纯文本 `*_all_prompts.txt` 便于整包粘贴。

交付前跑三步验证（缺一不可）：

1. **格式门**：`python3 scripts/diagnose_prompt.py <每一镜>` —— 确认段头被识别、无内部矛盾；
2. **链路门**：`python3 scripts/continuity_check.py <整批>` —— 确认 `end→start` 无断链、锚点无拼写漂移；
3. **渲染门**：用 jsdom 渲染 HTML，断言脚本无报错、prompt 块数与按钮数正确、锚点转义后完整还原
   （`<<<name>>>` 必须能在 `textContent` 里读回）。

截图验证时若 playwright 报 `Executable doesn't exist`，直接复用本机浏览器：
`chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'})`。
