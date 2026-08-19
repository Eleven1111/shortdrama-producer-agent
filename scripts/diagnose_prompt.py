#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断一段 Seedance prompt：缺什么、和真实生产比差在哪、有没有自相矛盾。

不是凭感觉点评。三类判据全部落在数据上：
  1. 段落覆盖 —— 对照 7,824 条真实生产 prompt 的段落出现率
  2. 约束覆盖 —— 对照 iteration-lessons.md（4,154 组真实修订统计出的加固项）
  3. 内部矛盾 —— 确定性规则，同一段 prompt 里互斥的指令

用法：
  python3 diagnose_prompt.py <prompt文件>
  cat prompt.txt | python3 diagnose_prompt.py
  python3 diagnose_prompt.py <prompt文件> --json
"""
import gzip, json, os, re, sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(_HERE, 'seedance_corpus.jsonl.gz')
SECTION_RE = re.compile(r'^([A-Z][A-Z0-9 &/\'()-]{3,44})\s*$', re.M)

# 真实生产中的段落出现率（全语料 7,824 条实测，见 README 的诊断基准说明）。
# 只对「高频且缺失代价明确」的段落报缺失 —— 出现率低的段落不缺不算问题。
SECTION_BASELINE = {
    'SCENE CONTEXT': (60.1, '没有场景与光的交代，模型自由发挥背景与影调'),
    'AUDIO': (55.0, '不写音频，模型会自行配乐或加旁白'),
    'LIGHTING': (54.7, '光是影调的唯一控制手段，缺了整体质感不可控'),
    'CAMERA': (48.2, '不写机位与运动，镜头语言随机'),
    'OPTICS': (46.1, '不写焦段/视角，景别与透视不可控'),
    'PHYSICS': (46.1, '不写物理，容易出现漂浮、拖影、违反重力'),
    'STYLE': (41.5, '没有风格锚，输出会退回通用 AI 质感'),
    'ACTION TIMING': (36.4, '多镜头/有事件时缺时序，节奏与硬切位置不可控'),
}

# Step 5.5 的加固项（来源 iteration-lessons.md，括号内为该项在真实修订中的证据强度）
CONSTRAINTS = {
    'diegetic_audio': (r'diegetic|no music|NO music|无配乐|同期声',
                       '同期声/禁配乐', '跨项目验证（HG 69.3% / CHB 73.6%）'),
    'no_onscreen_text': (r'no on-?screen text|no watermark|no subtitles|无字幕|无水印',
                         '禁屏幕文字与水印', '跨项目验证（66.5% / 44.7%）'),
    'shutter_cadence': (r'180[- ]degree shutter|180° shutter|shutter cadence',
                        '180° 快门节奏', '跨项目验证（49.4% / 26.3%）'),
    'hard_cut_timecode': (r'hard cut|HARD CUT|\d+(\.\d+)?s\s*[-–]\s*\d+(\.\d+)?s',
                          '硬切时间码', '跨项目验证（20.0% / 55.1%）· 仅多镜头适用'),
    'camera_relative': (r'from camera|FROM CAMERA|screen left|screen right',
                        '方位以镜头为准', '跨项目验证（13.3% / 9.9%）'),
    'not_3d_render': (r'not 3d render|NOT 3D render|no game[- ]engine|not cartoon',
                      '非 3D 渲染声明', '单项目高频（HG 41.4%）· 写实题材适用'),
    'lens_locked': (r'lens locked|no zoom|one lens per',
                    '段内锁定焦段', '单项目高频（CHB 39.8%）· 多镜头适用'),
    'no_fisheye': (r'rectilinear|no fisheye',
                   '直线畸变校正', '单项目高频（CHB 27.1%）'),
    'no_empty_first_frame': (r'no empty frame|first frame is occupied|first frame occupied',
                             '首帧非空', '单项目高频（CHB 18.5%）'),
    'no_look_at_lens': (r'look(s|ing)? (in)?to (the )?(lens|camera)|no one looks into',
                        '禁止看镜头', '单项目高频（CHB 11.6%）· 有演员时适用'),
    'no_floating': (r'nothing floats|no floaty|floaty motion',
                    '物体不漂浮', '单项目高频（CHB 8.9%）'),
    'hands_formed': (r'correct number of fingers|hands fully formed',
                     '手部解剖正确', '单项目（CHB 1.9%）· 公认失效模式，有手部特写时必加'),
}

# 否定短语 —— 检测「要求做 X」之前先把这些剥掉，避免 "no subtitles" 被读成要字幕
NEGATION_RE = re.compile(
    r'\b(?:no|without|avoid|never|not|omit|exclude)\b[\s:]*[\w\'\-]+(?:\s+[\w\'\-]+){0,3}'
    r'|(?:禁止|不要|不得|无)[一-鿿]{0,8}', re.I)

# 内部矛盾：A 侧在原文命中，B 侧在「剥掉否定后」的文本命中，才算冲突
CONTRADICTIONS = [
    (r'\bno music\b|diegetic sound only', r'\bbgm\b|background music|add music|配乐',
     '同时要求「无配乐」与「加配乐」'),
    (r'no slow-?motion', r'slow[- ]?motion|slow-mo|升格',
     '同时禁止与要求慢动作'),
    (r'\bstatic\b.{0,30}(camera|shot)|locked off|no camera move',
     r'\b(dolly|crane|pan|tilt|track(ing)?|push[- ]in|zoom)\b',
     '声明静止机位又要求运镜'),
    (r'no on-?screen text|no subtitles', r'\bsubtitle|caption|on-screen text|字幕',
     '同时禁止与要求字幕'),
    (r'one continuous shot|single (continuous )?take', r'hard cut|HARD CUT',
     '声明一镜到底又写了硬切'),
    (r'no zoom|lens locked', r'\bzoom (in|out)\b',
     '声明锁定焦段又要求变焦'),
]


def sections_of(text):
    return {m.group(1).strip() for m in SECTION_RE.finditer(text)}


def corpus_stats():
    """现算段落出现率；语料缺失时回落到内置基准。"""
    if not os.path.exists(CORPUS):
        return None
    try:
        n, hdr = 0, Counter()
        with gzip.open(CORPUS, 'rt', errors='replace') as f:
            for line in f:
                if not line.strip():
                    continue
                n += 1
                hdr.update(sections_of(json.loads(line)['prompt']))
        return {k: v / n * 100 for k, v in hdr.items()} if n else None
    except Exception:
        return None


def diagnose(text):
    secs = sections_of(text)
    live = corpus_stats()
    low = text.lower()
    multi_shot = bool(re.search(r'hard cut|seg\s*\d|shot \d+/', low))
    has_person = bool(re.search(r'<<<|character|man|woman|girl|boy|他|她', low))

    missing_sections = []
    for name, (rate, why) in SECTION_BASELINE.items():
        if name in secs:
            continue
        if name == 'ACTION TIMING' and not multi_shot:
            continue
        actual = live.get(name, rate) if live else rate
        missing_sections.append({'section': name, 'corpus_rate': round(actual, 1), 'why': why})
    missing_sections.sort(key=lambda x: -x['corpus_rate'])

    missing_constraints = []
    for key, (pat, label, evidence) in CONSTRAINTS.items():
        if re.search(pat, text, re.I):
            continue
        if key == 'hard_cut_timecode' and not multi_shot:
            continue
        if key in ('lens_locked',) and not multi_shot:
            continue
        if key in ('no_look_at_lens',) and not has_person:
            continue
        missing_constraints.append({'id': key, 'label': label, 'evidence': evidence})

    # 矛盾检测的「要求」侧必须在剥掉否定短语后的文本上匹配 —— 否则 "No subtitles"
    # 里的 subtitles 会被当成「要求字幕」，把每条合格的负面约束都误报成矛盾。
    positive = NEGATION_RE.sub(' ', text)
    conflicts = []
    for a, b, desc in CONTRADICTIONS:
        if re.search(a, text, re.I) and re.search(b, positive, re.I):
            conflicts.append(desc)

    spec = {
        'has_duration': bool(re.search(r'duration:\s*\d+', low)),
        'has_ratio': bool(re.search(r'aspect ratio', low)),
        'declared_duration': (lambda m: int(m.group(1)) if m else None)(
            re.search(r'duration:\s*(\d+)', low)),
    }
    warnings = []
    if not spec['has_duration']:
        warnings.append('缺 Duration 声明 —— 平台按默认时长走，节奏不可控')
    if not spec['has_ratio']:
        warnings.append('缺 Aspect ratio 声明')
    d = spec['declared_duration']
    if d and d > 15:
        warnings.append('声明 %ds：超过 Higgsfield Seedance 2.0 的 15s 上限；'
                        '2.5 可到 30s，Dreamina Long Video 可到 180s —— 确认平台与版本'
                        '（见 references/platform-capabilities.md）' % d)
    if len(text) < 300:
        warnings.append('全文不足 300 字符 —— 真实生产 prompt 中位约 9,000 字符，'
                        '控制力大概率不足')

    return {'length': len(text), 'sections_found': sorted(secs), 'multi_shot': multi_shot,
            'missing_sections': missing_sections, 'missing_constraints': missing_constraints,
            'contradictions': conflicts, 'spec': spec, 'warnings': warnings}


def render(r):
    out = ['# Prompt 诊断', '',
           '全文 %d 字符 · 识别到 %d 个段落 · %s' % (
               r['length'], len(r['sections_found']),
               '多镜头' if r['multi_shot'] else '单镜头'), '']
    if r['contradictions']:
        out += ['## ⛔ 内部矛盾（必须先解决）', '']
        out += ['- %s' % c for c in r['contradictions']] + ['']
    if r['warnings']:
        out += ['## ⚠ 规格问题', ''] + ['- %s' % w for w in r['warnings']] + ['']
    if r['missing_sections']:
        out += ['## 缺失的结构段（对照 7,824 条真实生产 prompt）', '',
                '| 段落 | 真实生产出现率 | 缺了会怎样 |', '|---|---|---|']
        out += ['| `%s` | %.1f%% | %s |' % (m['section'], m['corpus_rate'], m['why'])
                for m in r['missing_sections']]
        out += ['']
    if r['missing_constraints']:
        out += ['## 缺失的约束（对照 4,154 组真实修订）', '',
                '真实生产中 **69.7% 的修订是在加约束**，而不是改文采。以下是这条 prompt 还没写的：', '',
                '| 约束 | 证据强度 |', '|---|---|']
        out += ['| %s | %s |' % (m['label'], m['evidence']) for m in r['missing_constraints']]
        out += ['']
    if not (r['contradictions'] or r['missing_sections'] or r['missing_constraints'] or r['warnings']):
        out += ['结构、约束与规格均无明显缺口。若出片仍不理想，问题更可能在创意描述本身'
                '（动作是否具体、光是否可执行），而非 prompt 结构。', '']
    return '\n'.join(out)


def main():
    args = [a for a in sys.argv[1:] if a != '--json']
    as_json = '--json' in sys.argv[1:]
    if args:
        text = open(args[0], encoding='utf-8', errors='replace').read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print(__doc__)
        return 1
    if not text.strip():
        print('空输入')
        return 1
    r = diagnose(text)
    print(json.dumps(r, ensure_ascii=False, indent=1) if as_json else render(r))
    return 0


if __name__ == '__main__':
    sys.exit(main())
