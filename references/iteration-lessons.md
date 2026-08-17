# 迭代教训库 — 创作者在真实生产中反复补写的约束

来源：Cully Hill Boys 项目 404,887 条视频类资产，按 `cluster_hash` 聚成 6,300 组，
其中 **4,154 组存在首版→末版的实质改写**。本文件统计的是「创作者按时间顺序主动
补进去的内容」。

**这份数据能证明什么、不能证明什么**（重要，别越界解读）：

- 数据里**没有采纳/偏好标签** —— `is_favourite`、`published_at`、`review_status`
  全量扫描结果均为 0。所以**不能**说「后面的版本更好」。
- 能说的是更弱但可靠的一条：**创作者初稿漏掉、后来主动补上的东西，就是生产中
  必须写清楚的东西**。这对写 prompt 的人同样成立 —— 你的初稿大概率漏同样的项。

---

## 一、迭代的形状：不改骨架，只加约束

| 现象 | 实测 |
|---|---|
| 末版比首版**变长** | 2,897 组（**69.7%**） |
| 变短 | 706 组（17.0%） |
| 基本不变 | 551 组（13.3%） |
| 段落**新增/删除** | 各段仅 2–6% |
| 段落**显著扩写**（+30% 以上） | 见下 |

段落扩写率 TOP：

| 段落 | 扩写组占比 |
|---|---|
| POSITIVE CONSTRAINTS | **32.8%** |
| POSITIVE LOCKS | **31.0%** |
| ACTION TIMING | **28.5%** |
| SCENE CONTEXT | 21.6% |
| CHARACTER ACTING | 20.3% |
| LOCATION MAP | 19.8% |
| CAMERA | 19.6% |

> **结论**：真实生产里的迭代**几乎不动段落骨架**（增删只有 2–6%），而是往
> 约束段和时序段里持续加细节。两个「锁定」类段落扩写率最高（32.8% / 31.0%），
> 说明最大的痛点是**约束不足导致模型跑偏**，不是描述不够漂亮。
>
> 对 Agent 的直接含义：生成首版后，优先加固 POSITIVE CONSTRAINTS / POSITIVE
> LOCKS / ACTION TIMING，而不是重写 SCENE CONTEXT 的文采。

---

## 二、跨项目验证过的通用约束（可直接用）

在 **Hell Grind** 与 **Cully Hill Boys** 两个独立项目中都高频出现（按概念检索，
不是按措辞 —— 两个项目的措辞不同但概念一致）。百分比 = 出现该概念的文档占比。

| 约束概念 | Hell Grind | Cully Hill Boys | 写法示例 |
|---|---|---|---|
| **同期声 / 不要配乐** | 69.3% | 73.6% | `Diegetic sound only, no music.` |
| **禁止屏幕文字与水印** | 66.5% | 44.7% | `No on-screen text or watermark. No subtitles.` |
| **180° 快门节奏** | 49.4% | 26.3% | `Natural 180-degree shutter cadence.` |
| **硬切与时间码** | 20.0% | 55.1% | `0.0s–4.0s — SEG1. HARD CUT at 4.0s.` |
| **方位以镜头为准** | 13.3% | 9.9% | `All left/right = FROM CAMERA.` |

这五条在两个项目里都是主流写法，可作为**默认加进任何 Seedance prompt 的基线约束**。

---

## 三、单项目高频（有用，但未跨项目验证）

概念在一个项目里高频、另一个项目罕见。仍是真实生产经验，但**通用性未被数据证明** ——
用之前先判断是否契合当前片子的类型。

| 约束概念 | Hell Grind | Cully Hill Boys | 写法示例 |
|---|---|---|---|
| 非 3D 渲染 / 非游戏引擎风格 | **41.4%** | 3.0% | `NOT 3D render, NOT game engine, NOT cartoon.` |
| 镜头锁定、段内不变焦 | 4.3% | **39.8%** | `One lens locked per segment, no drift mid-shot.` |
| 无鱼眼 / 直线畸变校正 | 2.1% | **27.1%** | `Rectilinear, no fisheye.` |
| 首帧不得为空 | 0.3% | **18.5%** | `No empty frame. First frame occupied:` |
| 禁止演员看镜头 | 0.1% | **11.6%** | `No one looks into the lens.` |
| 物理真实、不漂浮 | 0.0% | **8.9%** | `Nothing floats. No floaty motion, no smearing.` |
| 禁止慢动作 | 3.0% | 7.2% | `No slow-motion.` |
| 180° 轴线一致 | 1.3% | 3.6% | `Camera stays one side of the 180° axis.` |
| 结尾定帧 | 0.1% | 3.3% | `Hold to the final frame.` |
| 手部结构正确 | 0.0% | 1.9% | `Hands fully formed, correct number of fingers.` |

> 注：最后两类（手部、漂浮）虽只在单项目出现，但属于公认的 AI 视频失效模式，
> 出现率低更可能是「另一个项目用了别的措辞」而非「不需要」。

---

## 四、项目专属设定 —— 禁止搬进用户作品

以下是源项目的世界观设定，在另一个项目中出现率为 **0.0%**。它们是本数据集的
「指纹」，混进用户 prompt 就是污染：

| 设定 | Hell Grind | Cully Hill Boys |
|---|---|---|
| `British spelling.` | 0.0% | 58.7% |
| `Nothing modern beyond 2011.`（年代限定） | 0.0% | 38.2% |
| `100% matches the reference.`（该项目的引用纪律） | 0.0% | 39.2% |
| 具体人物 / 地点 / 世界观（Vernon、grime crime-comedy 等） | — | — |

这两行同时是本次验证方法的**对照组**：它们被正确识别为单项目专属，说明上面
几张表的跨项目判定是可信的。

---

## 五、怎么用

1. 生成首版 prompt 后，**先补第二节的五条基线约束**（跨项目验证过）。
2. 若片子涉及多镜头，重点加固 `ACTION TIMING`（扩写率 28.5%）：给出秒级分段与
   HARD CUT 位置，而不是笼统的「几个镜头」。
3. 第三节按片型选用：写实题材优先「非 3D 渲染」「物理不漂浮」「手部正确」；
   多镜头连续场景优先「镜头锁定」「180° 轴线」「首帧非空」。
4. 第四节**永远不要出现**在交付给用户的 prompt 里。

---

*生成方式：`build_p4b_diff.py`（cluster 内首末版段落级 diff）+ `build_p4b_phrases.py`
（新增句归一化聚类）+ 概念级跨项目检索验证。全程确定性统计，无 LLM 推断。*
