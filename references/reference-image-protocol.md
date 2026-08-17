# 参考图协议 — 跨镜头一致性的真正机制

纯文本描述锚不住角色。同一段外观文字连写十遍，Seedance 每一镜仍会漂。
源项目 473,239 条资产里，**87.32% 带 `reference_elements`** —— 一致性是靠**参考图**
锁定的，文本锚点 `<<<name>>>` 只是指向那张图的指针。

本协议讲怎么产出这些图的 prompt，以及怎么接回视频 prompt。

## 一、什么时候需要设定图

| 情况 | 要不要 |
|---|---|
| 单镜头、角色只出现一次 | **不需要** —— 直接写外观描述即可 |
| 多镜头 / 短剧，同一角色跨镜出现 | **需要** —— 否则必然身份漂移 |
| 关键道具跨场景出现 | 需要 |
| 场景需要反复回到同一地点 | 需要 |

## 二、三面板设定图（主流格式）

源数据中 `three-panel` 出现 4,556 次、`character sheet` 3,007 次、
`full-body front` / `full-body back` 各约 1,790 次 —— 这是最成熟的做法。

标准构成：**正面全身 + 背面全身 + 面部特写**（有时加后脑视角）。

```
Full-length three-panel character sheet on a seamless neutral mid-grey studio backdrop.
Left: full-body FRONT view. Centre: full-body BACK view. Right: close-up portrait.

<角色外观：身高体型 / 发型发色 / 肤质 / 逐件服装 / identifying marks>

Even soft studio lighting, photoreal, no stylisation. Identical identity, proportions
and clothing across all three panels. Neutral pose, arms relaxed at sides.

Negative prompt: changed character design, different faces between panels, stylised,
cartoon, illustration, text, watermark, inconsistent clothing.
```

要点（全部来自真实生产 prompt）：
- **seamless neutral mid-grey backdrop** —— 中性灰底，不干扰后续抠取与打光
- **even soft lighting** —— 平光，把光留给视频镜头去打
- 明确写 `identical identity across all panels`，否则三面板会各画各的
- 外观必须逐件写清（参照 `character_cards_visual.md` 的颗粒度）

## 三、状态演进：改设定图，不要改视频 prompt

**这是最容易做错的一步。** 角色在剧情中受伤、变脏、湿身、换装时，不要在每个镜头的
视频 prompt 里补描述 —— 那样每镜的措辞都会漂。正确做法是**编辑设定图，产生新版本**。

数据佐证：363 个角色资产里 **46.8% 带版本号 `_vN`**、23.1% 带场景号 `_sN`；24 个角色
存在多版本，最多的一个有 **28 版**，命名里直接带着状态（`..._s84_v2_wet`、`..._v2_desloped`）。

编辑设定图的 prompt 模板：

```
Edit the attached <角色> character sheet. <要加的状态变化，具体到部位与材质>.
Add it consistently across ALL panels (front full-body, back full-body, close-up face).

Do NOT change his pose, framing, clothing, <已有的其他状态> — only add <本次变化>.
Match the same soft even lighting and neutral grey background.
COLOUR GRADE — match the reference image EXACTLY 1:1.
Keep everything else unchanged.

Negative prompt: changed character design, different pose, altered framing, <本次不该出现的>
```

三条硬规则：
1. **`consistently across ALL panels`** —— 漏写这句，三个面板的状态会不一致，等于毁了设定图。
2. **逐项列出「不要改」的东西**（pose / framing / 服装 / 已有伤口）—— 只说「只加沙子」不够。
3. **`COLOUR GRADE — match EXACTLY 1:1`** —— 否则新版本与旧版本调色不一致，同一场戏里跨镜会跳。

## 四、命名与接回视频

设定图产出后，按源项目的命名法登记，再在视频 prompt 里用锚点引用：

```
char_<剧集缩写>_<角色名>_v<版本>          # char_NR_mei_v3      角色第 3 版设定图
char_<剧集缩写>_<角色名>_s<场景>_v<版本>   # char_NR_mei_s12_v2   第 12 场专用状态（如淋湿）
prop_<剧集缩写>_<道具名>_v<版本>
loc_<剧集缩写>_<地点名>
```

视频 prompt 里：

```
ACTIVE REFERENCES
<<<char_NR_mei_v3>>>, <<<prop_NR_umbrella_v1>>>, <<<loc_NR_convenience_store>>>
```

- 一个镜头引用哪一版，取决于该镜头在剧情中的**状态时点** —— 受伤后的镜头引用受伤版。
- 锚点名在整部片子里**逐字复用**，不要改写（写进连续性圣经，见 `continuity-bible.md`）。

## 五、与视频工作流的衔接

短剧模式下的正确顺序：

1. 故事拆解 → 确定有哪些跨镜角色/道具/地点（`story-breakdown.md`）
2. **为每个跨镜元素产出设定图 prompt**（本协议第二节）
3. 有状态变化的，产出编辑版设定图 prompt（第三节）
4. 连续性圣经登记锚点名与版本（`continuity-bible.md`）
5. 逐镜视频 prompt，`ACTIVE REFERENCES` 引用对应版本

交付给用户时要说清：设定图 prompt 需要先在图像模型（Seedream / Nano Banana 等）跑出图，
把图上传为参考素材后，视频 prompt 里的锚点才会生效。

## 边界

- 本协议只处理**服务于视频一致性**的参考图。用户要的是纯图像创作（海报、插画、
  单张作品）→ 仍然拒绝，那不是本 Agent 的职责。
- 不要把源项目的角色/道具设定原样搬给用户 —— `character_cards_visual.md` 是写法教材，
  不是素材库。

---

*数据来源：Cully Hill Boys 61,554 条图像模型 prompt（设定图类 10,712 条 / 编辑精修类
21,572 条）与 1,391 个 reference_elements 资产的命名结构。*
