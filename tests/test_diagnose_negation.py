#!/usr/bin/env python3
"""diagnose_prompt.py 中文否定剥离的回归测试。

用法： python3 tests/test_diagnose_negation.py   （全过退出 0）
背景：2026-10-21 实测「无提示笑点的音效或配乐」「没有字幕」被误报成矛盾。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
from diagnose_prompt import diagnose

MUSIC, SUBS = '同时要求「无配乐」与「加配乐」', '同时禁止与要求字幕'
CASES = [  # (文本, 预期出现的矛盾, 说明)
    ('Diegetic sound only, no music. 无提示笑点的音效或配乐。', set(), '长否定句不误报'),
    ('No subtitles. 画面里没有字幕。', set(), '「没有」算否定'),
    ('Diegetic sound only, no music. 无罐头笑声、配乐。', set(), '顿号列举仍在否定内'),
    ('Diegetic sound only, no music. 结尾加配乐。', {MUSIC}, '正控：真矛盾必须报'),
    ('No subtitles. 不要停顿，加字幕。', {SUBS}, '正控：否定不跨逗号'),
    ('No subtitles. 只有环境声。', set(), '空对照'),
]

fail = 0
for text, want, why in CASES:
    got = set(diagnose(text)['contradictions']) & {MUSIC, SUBS}
    ok = got == want
    fail += not ok
    print('%s  %s  got=%s' % ('PASS' if ok else 'FAIL', why, sorted(got)))
sys.exit(1 if fail else 0)
