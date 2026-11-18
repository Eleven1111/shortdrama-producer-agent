#!/usr/bin/env python3
"""按相同用例聚合完整的盲测 A/B 评分，报告效应量与方向。"""

import json
import os
import sys
from collections import Counter, defaultdict

from run_ab import OUT, RUBRIC_ITEMS

ARMS = ('A', 'B')
SCORE_VALUES = {'pass', 'fail', 'n/a'}


def complete_scores(row):
    scores = row.get('scores', {})
    if not isinstance(scores, dict) or scores.keys() != set(RUBRIC_ITEMS):
        return None
    normalized = {
        item: value.strip().lower() if isinstance(value, str) else ''
        for item, value in scores.items()
    }
    if set(normalized.values()) <= SCORE_VALUES and any(
        value != 'n/a' for value in normalized.values()
    ):
        return normalized
    return None


def collect_pairs(rows, key):
    by_sample = {row['sample_id']: row for row in rows}
    if len(by_sample) != len(rows) or by_sample.keys() - key.keys():
        sys.exit('评分表含重复样本或未登记样本')

    by_case = defaultdict(dict)
    for sample_id, entry in key.items():
        case_id, arm = entry['case_id'], entry['arm']
        if arm not in ARMS or arm in by_case[case_id]:
            sys.exit('盲测映射含未知组别或重复槽位')
        by_case[case_id][arm] = sample_id

    pairs = []
    incomplete = {}
    for case_id, slots in sorted(by_case.items()):
        reasons = {}
        usable = {}
        for arm in ARMS:
            sample_id = slots.get(arm)
            row = by_sample.get(sample_id)
            if sample_id is None:
                reasons[arm] = '缺组别槽位'
            elif row is None:
                reasons[arm] = '缺评分行'
            elif not row.get('video') or not os.path.isfile(os.path.join(OUT, row['video'])):
                reasons[arm] = '缺成片'
            else:
                scores = complete_scores(row)
                if scores is None:
                    reasons[arm] = '评分缺项、值无效或全部不适用'
                else:
                    usable[arm] = (row, scores)

        if not reasons:
            _, a_scores = usable['A']
            _, b_scores = usable['B']
            if any((a_scores[item] == 'n/a') != (b_scores[item] == 'n/a')
                   for item in RUBRIC_ITEMS):
                reasons['pair'] = 'A/B 适用项不一致'

        if reasons:
            incomplete[case_id] = reasons
        else:
            pairs.append(usable)
    return pairs, incomplete


def main():
    sp = os.path.join(OUT, 'grading_sheet.json')
    kp = os.path.join(OUT, '_blind_key.json')
    for path in (sp, kp):
        if not os.path.exists(path):
            sys.exit('缺 %s' % path)
    with open(sp, encoding='utf-8') as f:
        rows = json.load(f)
    with open(kp, encoding='utf-8') as f:
        key = json.load(f)

    pairs, incomplete = collect_pairs(rows, key)
    print('完整配对 %d / %d 个已登记用例' % (len(pairs), len(pairs) + len(incomplete)))
    for case_id, reasons in incomplete.items():
        print('  %s: %s' % (case_id, '，'.join('%s %s' % item for item in reasons.items())))

    per_arm = {}
    means = {}
    graders = Counter()
    if pairs:
        print('\n=== 主指标：每片缺陷数 ===')
        for arm in ARMS:
            failures = Counter()
            applicable = Counter()
            for pair in pairs:
                row, scores = pair[arm]
                graders[row.get('grader_type') or 'unspecified'] += 1
                failures.update(item for item, value in scores.items() if value == 'fail')
                applicable.update(item for item, value in scores.items() if value != 'n/a')
            total = sum(failures.values())
            per_arm[arm] = {
                'n': len(pairs), 'fail': total,
                'na': len(pairs) * len(RUBRIC_ITEMS) - sum(applicable.values()),
                'items': dict(failures), 'applicable': dict(applicable),
            }
            means[arm] = total / len(pairs)
            label = '含 Step 5.5' if arm == 'A' else '不含 Step 5.5'
            print('  %s 组（%s）缺陷 %d，每片 %.2f' % (arm, label, total, means[arm]))

        delta = means['B'] - means['A']
        print('  差值 %+.2f 缺陷/片（B − A）' % delta)
        if means['B']:
            print('  相对差值 %+.1f%%' % (delta / means['B'] * 100))
        print('  评分方式：%s' % dict(graders))
        if 'unspecified' in graders:
            print('  ⚠ 有样本未标注评分方式')
        print('\n=== 分项失败次数 / 适用样本 ===')
        for item in RUBRIC_ITEMS:
            count = per_arm['A']['applicable'].get(item, 0)
            if count:
                print('  %-28s A %d/%d  B %d/%d' % (
                    item, per_arm['A']['items'].get(item, 0), count,
                    per_arm['B']['items'].get(item, 0), count,
                ))
    else:
        print('等待同一用例的 A/B 成片与完整评分')

    result = {
        'pair_count': len(pairs),
        'incomplete_cases': incomplete,
        'per_arm': per_arm,
        'mean_defects': means,
        'grader_types': dict(graders),
    }
    rp = os.path.join(OUT, 'ab_summary.json')
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('\n已写 %s' % rp)


if __name__ == '__main__':
    main()
