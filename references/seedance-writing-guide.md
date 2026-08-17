# Seedance Short-Drama Prompt Writing Rules (Cross-Project Verified)

> 来源：Higgsfield「Hell Grind」101,854 seedance_2_0 +「Cully Hill Boys」404,432 seedance_2_0，**两份独立大样本交叉验证**。
> 验证：2026-08-16。数据规模：HG ≈ 1.3M 视频任务，CHB ≈ 6M 视频任务。

## 一、跨项目一致参数基线（**通用可信，无需多解释**）

| 参数 | HG (Hell Grind) | CHB (Cully Hill Boys) | 结论 |
|---|---|---|---|
| **aspect_ratio** | 21:9 = 89% (78/88) | 21:9 = 98% (98k/100k) | 21:9 是 Higgsfield 短剧默认，16:9 用于特殊段落 |
| **duration** | 15s = 66% (58/88) | 15s = 49% (49k/100k) | 15s 是绝对主流；6-12s 用于节奏快的过渡 |
| **generate_audio** | True = 100% | True = 94% | 几乎全开音频 |
| **镜头 mm Top2** | 35mm / 85mm | 35mm / 85mm | 两个项目镜头体系高度同源 |
| **风格锚 Top2** | Lubezki / Deakins | Lubezki / Deakins | **跨项目绝对共识**：这是 Higgsfield 生态通用标准 |
| **运镜高频** | handheld / pan / locked / tilt | pan / locked / handheld / static | 三项 handheld + pan + locked 都进 Top5 |
| **角色锚规范** | `<<<UUID>>>` + name 解析 | `<<<UUID>>>` | 跨项目统一使用角色锚引用系统 |
| **写作范式** | 44 段破折号段流（更长更碎片化） | OPTICS/SCENE/ACTION 分段（更结构化） | **范式不同**——HG 更长、CHB 更模板化 |

## 二、跨项目两条范式的差异（**值得 Agent 区分**）

| 维度 | HG 范式 | CHB 范式 |
|---|---|---|
| 段落数/条 | 44 段（极碎片化） | 8-12 段（结构化） |
| 平均长度 | 同级（≈ 13k ch） | 同级 |
| 显式分段标题 | 弱（`—` 破折号） | 强（`OPTICS` `SCENE CONTEXT` `ACTION`） |
| **适用场景** | 短篇独立剧 / 行为密集 / 对白繁多 | 电影化叙事 / 摄影感强 / 多镜头连贯 |

**Agent 选范式提示**：
- 用户说"短片 / 一镜到底 / 动作密集" → HG 范式
- 用户说"电影 / 分镜 / 摄影感" → CHB 范式
- 不明确时 → 默认 CHB（结构化更通用）

## 三、镜头语言基线（两份数据共同证据）

- **度数为基调**：HG 写作例 `45° wide`, `180° ultra wide`；CHB 写作例 `47°(≈50mm)`, `29°(≈85mm)`, `84°(≈24mm)`——视角度数比 mm 更通用
- **mm 高频**：35mm、85mm、50mm（CHB）/35mm、85mm、50mm（HG）——**完全一致**
- **核心运镜**：handheld（律动）/ pan / locked（静止对照）/ tilt / static / dolly / push-in

## 四、风格锚标准库（**通用可信**）

跨项目 TOP5 导演引用（HG 60+ / CHB 20k+ 量级）：
- **Lubezki**（自然光 / 长镜头 / 重情绪）
- **Deakins**（精确打光 / 冷峻 / 史诗级）
- **Refn**（霓虹 / 高饱和 / 风格化）
- **Wright**（动作喜剧 / 节奏感）
- **Scorsese**（动态 / 戏剧张力）

## 五、负面约束四大功能（CHB 总结）

1. **反 3D 化**：`no 3D render`, `no CGI`, `no game engine`
2. **反身份漂移**：`same face on every frame`, `no identity drift`
3. **反机位僵化**：`never locked off on tripod`, `no static surveillance`
4. **反 AI 腔**：`no AI artifacts`, `no float`, `no subtitle`

每条 prompt 平均含 ~5-8 条否定约束（HG 38.6 个否定词/条；CHB 类似）。

## 六、节奏与长度基线

- 单条 prompt 长度：平均 **12,730 字符**（HG）/ **12,118 字符**（CHB），**几乎相同**
- 段落数：HG 44 / CHB 8-12
- 角色锚引用频率：~27 次/条

## 七、镜头段写法示例（CHB 风格，可作 Agent 模板）

```
OPTICS and CAMERA
<<<director>>> lens, <<<director>>> lighting. <<<lens_mm/degree>>>, <<<shot_type>>>.
Duration: <<<duration>> seconds. Aspect ratio: <<<21:9>>>. One continuous <<<move>> shot.

<<— additional spec paragraphs —>>
```

## 八、检索优先级（BM25 跨项目语料）

`seedance_corpus.jsonl.gz` 现合并 HG 1039（采样）+ CHB 6785（cluster 去重代表，覆盖 937 folder）= 7824 docs。检索时优先：
1. 用户场景词命中范例
2. 同 project 优先（HG 检索召回时 HG 项目本身优先）
3. 金标（CHB 562）始终保留优先召回

---

## 附：数据规模与置信度

| 项目 | 视频任务 | 抽样式本 | 风格锚验证样本 | 置信度 |
|---|---|---|---|---|
| Hell Grind (HG) | 101,854 | 88 (本月) / 30k (历史报告) | 116 | 高 |
| Cully Hill Boys (CHB) | 404,432 | 100k | 多 | 极高 |

跨项目一致性结论 = 两份独立数据相互印证，是种子级的事实。
