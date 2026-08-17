#!/usr/bin/env python3
"""P1 渲染回环 · A/B 实验编排。

验证的假设：Step 5.5 的约束加固（来自 iteration-lessons.md）是否真的降低出片缺陷率。
  A 组 = 完整工作流（含 Step 5.5 约束）
  B 组 = 同一需求，跳过 Step 5.5

关键设计：**盲测**。产出的评分表里样本顺序被打乱且不含组别，组别映射单独存
`_blind_key.json`，只有 aggregate.py 才读它。评分者（人或模型）看不到组别。

用法：
  python3 run_ab.py --prepare              # 生成待填的 prompt 槽位（交给 agent 产出）
  python3 run_ab.py --render --backend dry # 走渲染（dry/manual/ark）
  python3 run_ab.py --sheet                # 生成盲测评分表
"""
import argparse, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
CASES = os.path.join(HERE, 'cases.json')
sys.path.insert(0, HERE)
from render_adapter import render, RenderError          # noqa: E402

RUBRIC_ITEMS = [
    'duration', 'shot_count', 'hard_cut_timecode', 'camera_move', 'lens_locked',
    'camera_relative_direction', 'axis_180', 'no_empty_first_frame', 'hold_final_frame',
    'character_count', 'hands_formed', 'identity_consistency', 'prop_consistency',
    'no_floating', 'no_smearing', 'no_look_at_lens', 'no_slow_motion',
    'no_onscreen_text', 'not_3d_render', 'diegetic_audio', 'shutter_cadence',
]


def load_cases():
    with open(CASES, encoding='utf-8') as f:
        return json.load(f)['cases']


def prepare():
    """产出 prompts.todo.json —— 每个用例两个空槽，由 agent 分别在「含/不含 Step 5.5」
    两种模式下填写。刻意不让本脚本调 LLM：prompt 必须由被测 agent 自己产出，
    否则测的就不是这个 agent。"""
    os.makedirs(OUT, exist_ok=True)
    todo = []
    for c in load_cases():
        for arm in ('A', 'B'):
            todo.append({
                'case_id': c['id'], 'arm': arm, 'mode': c['mode'],
                'shots': c.get('shots', 1), 'probes': c['probes'],
                'idea': c['idea'],
                'instruction': ('完整工作流，含 Step 5.5 约束加固'
                                if arm == 'A' else
                                '同一需求，跳过 Step 5.5，其余步骤相同'),
                'prompt': '',      # ← 由 agent 填写
            })
    path = os.path.join(OUT, 'prompts.todo.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(todo, f, ensure_ascii=False, indent=1)
    print('已生成 %d 个待填槽位 → %s' % (len(todo), path))
    print('下一步：让 agent 逐条填写 prompt 字段（A 组含 Step 5.5，B 组不含），然后 --render')


def do_render(backend, limit=None):
    path = os.path.join(OUT, 'prompts.todo.json')
    if not os.path.exists(path):
        sys.exit('缺 prompts.todo.json，先跑 --prepare')
    with open(path, encoding='utf-8') as f:
        todo = json.load(f)

    empty = [t for t in todo if not t['prompt'].strip()]
    if empty and backend != 'dry':
        sys.exit('有 %d 个槽位的 prompt 还没填，无法渲染（dry 模式可忽略）' % len(empty))

    results = []
    for i, t in enumerate(todo):
        if limit and i >= limit:
            break
        tag = '%s%s' % (t['case_id'], t['arm'])
        try:
            r = render(t['prompt'] or '(empty)', tag, OUT, backend=backend)
        except RenderError as e:
            r = {'job_id': tag, 'backend': backend, 'status': 'error', 'error': str(e)}
        r.update({'case_id': t['case_id'], 'arm': t['arm'], 'probes': t['probes']})
        results.append(r)
        print('  [%2d/%d] %-6s %-14s %s' % (i + 1, len(todo), tag, r['status'],
                                            r.get('note') or r.get('error') or ''))
    rp = os.path.join(OUT, 'render_results.json')
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    ok = sum(1 for r in results if r['status'] == 'ok')
    print('\n渲染登记 %d 条，成片可用 %d 条 → %s' % (len(results), ok, rp))


def sheet():
    """生成盲测评分表：打乱顺序、剥离组别；组别映射另存。"""
    rp = os.path.join(OUT, 'render_results.json')
    if not os.path.exists(rp):
        sys.exit('缺 render_results.json，先跑 --render')
    with open(rp, encoding='utf-8') as f:
        results = json.load(f)

    rows, key = [], {}
    rnd = random.Random(20260817)
    shuffled = results[:]
    rnd.shuffle(shuffled)
    for n, r in enumerate(shuffled, 1):
        sid = 'S%03d' % n
        key[sid] = {'case_id': r['case_id'], 'arm': r['arm'], 'job_id': r['job_id']}
        rows.append({
            'sample_id': sid,                  # 评分者只看到这个
            'video': r.get('video'),
            'probes': r.get('probes', []),     # 提示重点看哪几项，不泄露组别
            'scores': {k: '' for k in RUBRIC_ITEMS},   # pass / fail / n/a
            'grader': '', 'grader_type': '',   # human / vision_model / auto
            'notes': '',
        })
    sp = os.path.join(OUT, 'grading_sheet.json')
    kp = os.path.join(OUT, '_blind_key.json')
    with open(sp, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    with open(kp, 'w', encoding='utf-8') as f:
        json.dump(key, f, ensure_ascii=False, indent=1)
    print('盲测评分表 %d 条 → %s' % (len(rows), sp))
    print('组别映射（评分前不要看）→ %s' % kp)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare', action='store_true')
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--sheet', action='store_true')
    ap.add_argument('--backend', default='dry', choices=['dry', 'manual', 'ark'])
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    if a.prepare:
        prepare()
    elif a.render:
        do_render(a.backend, a.limit)
    elif a.sheet:
        sheet()
    else:
        ap.print_help()
