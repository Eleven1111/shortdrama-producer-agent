# 反渣词库与措辞修复（Anti-Slop Lexicon）

> 蒸馏自 MIT 协议的 [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)（Skill OS v6.7）
> `anti-slop-lexicon.md`（Emily2040/seedance-2.0） 与 `references/vocab/{en,zh}.md`，概念级萃取、按本项目红线裁剪。
> 源仓库自身声明：这是**编辑启发式，不是实测规则**——词法匹配不等于该词在上下文中有害。
> 定位：本文件是 Step 5 自检「No AI-flavored filler」的**执行标准**，用于质检与修复，
> 不是创作时的枷锁。与本工艺库冲突时，工艺库裁决优先（例：源词表含 24mm/50mm 焦距写法，
> 本项目跨模型红线禁写焦距数值——按红线执行，见 §5）。

## 1. 六类渣词（质检线索，不是自动删除规则）

先看这个词在当前 brief 里的**角色**，再决定动不动它：

| 类 | 长相 | 条件修复 |
|---|---|---|
| 空评价词 | `cinematic, epic, stunning, beautiful, dramatic` | 保留有用的风格/情绪线索；只澄清它背后**没决定的事**（史诗=物理规模还是情感筹码？） |
| 图像模型借词 | `8K, masterpiece, award-winning, trending, Unreal Engine, RAW` | 区分三种角色：交付要求（走参数，不进正文）/ 渲染风格意图 / 无支撑吹捧（删） |
| 标签沙拉 | 逗号关键词堆，关系不明 | 把已有的主体、动作、时序**连成关系**；已无歧义的简洁列表可保留 |
| 负面渣词 | `no blur, no artifacts, no extra fingers` | 模糊的负面口号改写成**期望状态**；必要的显式排除与保留边界一律保留 |
| 形容词堆叠 | `gorgeous, breathtaking, mesmerizing sunset` | 删掉不新增意图的重复；保留情绪目标与有效区分 |
| 氛围感后缀 | `电影感 · atmosférico · vibey` | 语境里解释；保留情绪线索，必要时澄清它想表达的具体样子 |

## 2. 高频词裁决表（保留意图，澄清缺口）

| 待审词 | 要保留 / 要澄清 |
|---|---|
| cinematic | 保留"电影语言"意图；只在 brief 留白处澄清景别、节奏或光 |
| epic | 保留雄心；澄清是物理规模、情感筹码还是别的强度 |
| dynamic | 澄清**什么在变**；刻意锁定的机位不许因此加运镜 |
| dramatic | 保留张力/表演要求；不自动加阴影、静默或镜头压迫 |
| beautiful | 保留审美偏好；澄清到色彩、材质、构图或表演 |
| magical | 保留奇幻/惊奇方向；粒子和辉光只是可选实现 |
| professional | 澄清该类型的制作标准；产品台面光不是万能解 |
| 8K / hyper-detailed | 交付要求移出正文、走支持参数；不支持就声明缺口，**不悄悄降级** |
| masterpiece / award-winning | 无支撑的结果主张删；真实的参考角色与具体要求保留 |
| atmosphere of mystery | 保留"什么该不确定"；先用于现有场景，再考虑遮蔽物/雾/暗 |

## 3. 不过度矫正（三条刹车）

1. **有用的标签保留**：noir / documentary / ultra-realistic 描述的是选定的样子，不是渣词。
2. **可观察细节是消歧手段，不是逐词过滤测试**：一个锁死机位也可以服务高能场面。
3. **澄清 ≠ 重新提交**：改措辞不授权再烧一次生成；分辨率/时长等交付要求原样保留并声明归属。

## 4. 中英措辞对照精选（替换"形容词"为"可拍摄的决定"）

写作时从右列取词，质检时把左列修成右列。完整精神：每个词都要么锁定身份、要么决定画面、要么声明来源。

| 功能 | 中文 | English |
|---|---|---|
| 运镜 | 缓慢推镜（推动认知，非炫技） | slow push-in |
| 运镜 | 镜头后拉揭示空间（有动机的 reveal） | pull back to reveal the space |
| 运镜 | 固定中景（人脸/对白的稳） | locked medium shot |
| 运镜 | 手持镜头，轻微呼吸晃动（受控纪录感） | handheld with slight breathing sway |
| 景别 | 大面积负空间，孤独感 | large negative space, isolation |
| 景别 | 前景虚化遮挡 | subject seen past foreground blur |
| 光 | 柔和侧逆光 | soft side backlight |
| 光 | 左侧暖色实用灯（来源+方向） | warm practical light from the left |
| 光 | 冷色月光轮廓光（不写 moody） | cool moonlight rim |
| 光 | 潮湿地面反射霓虹（反射即光源） | wet asphalt reflecting neon |
| 动作 | 缓慢转头并停住（有终点的表演拍） | a slow head turn that stops |
| 动作 | 衣料随动作自然摆动 | fabric moves naturally with action |
| 动作 | 脚步带动薄雾扩散（环境回应主体） | fog parts around the footsteps |
| VFX | 金色粒子升起后消散（来源+路径+终点） | gold particles rise, catch backlight, dissipate |
| 音频 | 无配乐，仅低环境声 | no music, low ambience only |
| 对白 | 对白期间镜头固定 | locked camera during dialogue |

## 5. 与本项目红线的关系（冲突时按红线）

- **焦距数值禁写**（47° 度数写法仅限 Seedance 原生方言）——源词表的 `24mm wide spatial feel` /
  `50mm natural portrait perspective` 在本项目内一律改写为空间感受描述（wide spatial feel /
  natural portrait perspective），不携带数值。
- 抽象词该不该删，最终由 `directorial-craft.md` 的"一镜一动机"裁决：能回答
  "because the intention is X" 的风格词全部保留；回答不了的按 §1 分类修复。
- 与语料校准的关系：词表决定"最低水质"，OPTICS 密度与分段布局（Step 2 检索）决定"形态安全区"，二者叠加使用。

## 6. 质检接法

- 单镜头：Step 5 自检命中"AI 腔填充"→ 按 §1 分类 → §2 裁决 → §4 替换。
- 短剧：每镜交付前过一遍 §1（短 prompt 更容易标签沙拉，长 prompt 更容易形容词堆叠）。
- `diagnosis-only` 模式：`diagnose_prompt.py` 的词法报告以本文件为解释依据，逐条给"保留/澄清/替换"三选一结论，不自动重写。

## 7. 题材级禁区（Genre Stock-Solution Refusals）

> 蒸馏自 Emily2040/seedance-2.0（MIT）directing-engine-genre-library.md 的 `stock solution refused` 字段——33 个题材范例中每个题材"最俗套但最常见"的第一反应。**这些不是通用红线，是题材专属的 AI 味**：命中即视为该题材的 stock solution，除非 brief 明确要求。

| 题材 | 禁区（第一反应黑名单） |
|---|---|
| 短剧 | 尖叫反应 · 闪帧字幕插入 · 硬切光线突变 · 音效惊吓点 · 本镜内交代后果 |
| 动漫/2D 热血 | 尖叫变身 · 扩散能量球 · 环绕碎石 · 摄影镜头语言（见 directorial-craft §14） |
| 动作/追逐 | 速度斜坡（speed ramp）· 不可能的甩镜 · 随机碰撞蒙太奇 · 中途变屏幕方向 |
| 恐怖/悬疑 | 怪物揭示 · jump cut · 反应特写 · 配乐惊吓弦 |
| 对白双人文戏 | 反派狞笑 · 荷兰角 · 指控式台词 · 音乐惊刺 |
| 喜剧 | 反应变焦 · 旁观者切镜 · 罐头笑声 · 音乐提示笑点 |
| 儿童/幼儿内容 | 五彩纸屑 · 夸张反应 · 镜头旋转 · 童谣提示 · 不可能的泡泡雨 |
| 口播/带货 | 疯狂跳切 · 悬浮 UI 图形 · 魔法变换 · 重复 CTA |
| 旅行 vlog | 无人机环绕 · 张开双臂背影 · 旅行口号 · 加速地标蒙太奇 |
| 美妆/时尚 | 风扇吹发 · 闪切摆姿 · 环绕机位 · 无名奢华表面 |
| 怀旧/回忆 | 棕褐色滤镜 · 假胶片烧帧 · 煽情配乐 · 慢镜拥抱 · 解说旁白 |
| 纪录片采访 | 鸡汤配乐 · B-roll 蒙太奇 · 催泪特写 · 行业口号 |
| 自然/动物 | 追逐 · 慢镜跃起 · 交响奇观 · 捕食者揭示 · 人类反应切镜 |
| 宠物 | 拟人微笑 · 萌系旁白 · 八音盒配乐 · 换装 · 夸张歪头 |
| 科幻 | 全息蜂群 · 警报声 · 旋转机位 · 喊出式解说 · 一次性全揭示 |
| 奇幻/史诗 | 旋转符文 · 漂浮粒子场 · 天空光柱 · 胜利姿势 · 命运旁白 |
| 怀旧系万能禁令 | **sepia wash / fake film burn / sentimental score** 三件套在一切"回忆"题材默认拒绝 |

用法：Step 1 确定题材后，把对应行的禁区关键词并入该镜 negative constraints（≥5 条的红线基数之外的题材加项）；Step 5 质检时正文若出现禁区手段，回问一句"brief 明确要了吗"。

---
*来源：Emily2040/seedance-2.0（MIT）anti-slop-lexicon.md + vocab/en.md + vocab/zh.md，2026-09-11 萃取。*
