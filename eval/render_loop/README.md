# P1 渲染回环

验证一件到目前为止**零证据**的事：agent 产出的 prompt，真实出片效果到底如何。

在此之前所有质量判断都停在 prompt 文本层（结构齐不齐、约束够不够），从未与
Seedance 的实际出片对齐过。**没有这一环，「商用级」永远是 UNVERIFIED。**

## 这不是 agent 的功能

agent 的运行时边界不变 —— 它仍然只产出 prompt，不调渲染 API（见 SKILL.md / AGENTS.md
的 Boundaries）。本目录是**开发期评测工具**，给维护者验证质量用。

## 首个实验：Step 5.5 到底有没有用

`references/iteration-lessons.md` 的约束是从 4,154 组真实修订里统计出来的，
但「创作者反复补它」不等于「补了出片更好」。A/B 直接测：

| 组 | 内容 |
|---|---|
| **A** | 完整工作流，含 Step 5.5 约束加固 |
| **B** | 同一需求，跳过 Step 5.5，其余相同 |

12 用例 × 2 组 = 24 次渲染。用例见 `cases.json`，每个带 `probes` 字段标明该用例
重点探测哪几条约束。

## 流程

```bash
python3 run_ab.py --prepare                 # 1. 生成 24 个待填槽位
#    2. 让 agent 逐条填 prompt 字段（A 组走完 Step 5.5，B 组跳过）
python3 run_ab.py --render --backend manual # 3. 渲染
python3 run_ab.py --sheet                   # 4. 生成盲测评分表
#    5. 按 rubric.md 评分（评分者看不到组别）
python3 aggregate.py                        # 6. 还原组别并聚合
```

第 2 步刻意不由脚本调 LLM —— prompt 必须由**被测 agent 自己**产出，否则测的不是它。

## 三种渲染后端

| backend | 说明 |
|---|---|
| `dry` | 不调 API，只验证管道结构。**默认**。 |
| `manual` | 脚本导出 prompt 到 `out/prompts/`，人工在平台渲染后把成片放回 `out/videos/<job_id>.mp4`。慢，但不需要 API 凭据。 |
| `ark` | 火山方舟 Seedance，需 `ARK_API_KEY`。**会消耗付费额度**，调用前须获得额度所有者明确同意。 |

适配层刻意不含任何绕过鉴权的路径。没有凭据就用 `manual`。

## 评分为什么这样设计

见 `rubric.md`。三个要点：

1. **只评指令遵循 + 技术缺陷，不评美学** —— 美学主观、跨评分者不一致、无法归因到
   某条 prompt 改动，放进 A/B 只会制造噪音。
2. **二元判定**（pass/fail/n/a），不用 1–5 分制 —— 模糊分数会把美学偏好混进来。
3. **盲测** —— 评分表打乱顺序且不含组别（已验证：`grading_sheet.json` 无 `arm`/
   `case_id` 字段），映射单独存 `_blind_key.json`，只有 `aggregate.py` 读。

## 已验证到哪一步

- ✅ 管道结构：`--prepare` → `--render --backend dry` → `--sheet` 全程跑通，24 槽位齐。
- ✅ 盲测有效：评分表确认不含组别字段。
- ✅ 聚合算术：用构造数据（A=2 缺陷/片、B=5 缺陷/片）验证，输出差值 +3.00、
  相对 +60.0%、方向判定与分项定位均正确。自测数据已清除，评分表为空。
- ❌ **真实渲染未跑** —— 本机无任何 Seedance / 火山方舟 / Higgsfield 凭据。
  这一步需要额度所有者提供凭据或走 `manual`。

在真实渲染跑完之前，**不要宣称这个 agent 达到了商用级**。管道就绪 ≠ 质量已验证。
