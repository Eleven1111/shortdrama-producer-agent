#!/usr/bin/env python3
"""P1 渲染回环 · 结果聚合。读盲测评分表 + 组别映射，出 A/B 对比。

只报效应量与方向，不做显著性声称 —— 12 对样本撑不起 p 值，硬报会是假精确。
若 A 组缺陷不降反升，照实输出：负面结果同样要回写。
"""
import json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')


def main():
    sp, kp = os.path.join(OUT, 'grading_sheet.json'), os.path.join(OUT, '_blind_key.json')
    for p in (sp, kp):
        if not os.path.exists(p):
            sys.exit('缺 %s' % p)
    rows = json.load(open(sp, encoding='utf-8'))
    key = json.load(open(kp, encoding='utf-8'))

    graded = [r for r in rows if any(v for v in r['scores'].values())]
    if not graded:
        sys.exit('评分表还是空的 —— 先完成评分再聚合')
    print('已评分 %d / %d 条' % (len(graded), len(rows)))
    gt = Counter(r.get('grader_type') or 'unspecified' for r in graded)
    print('评分方式：%s' % dict(gt))
    if 'unspecified' in gt:
        print('  ⚠ 有样本未标注评分方式 —— rubric 要求必须标注（人评/模型评/自动）')

    per_arm = defaultdict(lambda: {'n': 0, 'fail': 0, 'items': Counter(), 'na': 0})
    for r in graded:
        arm = key.get(r['sample_id'], {}).get('arm')
        if not arm:
            continue
        a = per_arm[arm]
        a['n'] += 1
        for item, v in r['scores'].items():
            v = (v or '').strip().lower()
            if v == 'fail':
                a['fail'] += 1
                a['items'][item] += 1
            elif v in ('n/a', 'na'):
                a['na'] += 1

    print('\n=== 主指标：每片缺陷数 ===')
    means = {}
    for arm in ('A', 'B'):
        a = per_arm.get(arm)
        if not a or not a['n']:
            print('  %s 组：无数据' % arm)
            continue
        means[arm] = a['fail'] / a['n']
        label = '含 Step 5.5' if arm == 'A' else '不含 Step 5.5'
        print('  %s 组（%-12s）n=%2d  缺陷 %3d  每片 %.2f' % (arm, label, a['n'], a['fail'], means[arm]))

    if len(means) == 2:
        d = means['B'] - means['A']
        if means['B']:
            print('\n  差值 %+.2f 缺陷/片（相对 %+.1f%%）' % (d, d / means['B'] * 100))
        verdict = ('Step 5.5 方向为正（A 组缺陷更少）' if d > 0 else
                   'Step 5.5 方向为负（A 组缺陷更多 —— 约束无效或有害，需回写）'
                   if d < 0 else 'A/B 无差异')
        print('  判定：%s' % verdict)
        print('  注：n=%d 对，只报方向与效应量，不做显著性声称。' % min(per_arm['A']['n'], per_arm['B']['n']))

    print('\n=== 分项 fail 次数（定位是哪条约束在起作用）===')
    items = set(per_arm['A']['items']) | set(per_arm['B']['items'])
    if items:
        print('  %-28s %6s %6s' % ('项', 'A', 'B'))
        for it in sorted(items, key=lambda x: -(per_arm['B']['items'][x] + per_arm['A']['items'][x])):
            print('  %-28s %6d %6d' % (it, per_arm['A']['items'][it], per_arm['B']['items'][it]))
    else:
        print('  （无 fail 记录）')

    rp = os.path.join(OUT, 'ab_summary.json')
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump({'per_arm': {k: {'n': v['n'], 'fail': v['fail'], 'na': v['na'],
                                   'items': dict(v['items'])} for k, v in per_arm.items()},
                   'mean_defects': means,
                   'grader_types': dict(gt)}, f, ensure_ascii=False, indent=1)
    print('\n已写 %s' % rp)


if __name__ == '__main__':
    main()
