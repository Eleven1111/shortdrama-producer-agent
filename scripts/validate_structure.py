#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""结构防腐校验 —— 挡住文档在后续编辑中悄悄退化。

不测行为（LLM 行为测不了），只测三件确定性的事：
  1. 关键契约短语还在不在 —— 工作流步骤、分流规则、边界声明被误删时 CI 变红
  2. 文档间的相互引用有没有变成死链
  3. 有没有 TODO/FIXME 之类的占位符混进主干

背景：本仓库的 references 有 18 个文件互相引用，工作流步骤分散在 SKILL.md 与
AGENTS.md 两处且必须保持一致。历史上真实发生过：改完 P2 后 AGENTS.md 残留了与新
分流表矛盾的旧句，靠人工 grep 才发现。这个脚本就是把那次人工检查固化下来。

用法： python3 scripts/validate_structure.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 关键契约：删掉任何一条都意味着某个能力静默消失。
# 值是正则，**不是子串** —— 子串匹配挡不住改名：`Step 5.5` 会被 `Step 5.5x` 满足，
# 这个假绿是故障注入测出来的。工作流步骤一律用行首标题锚定。
REQUIRED_PHRASES = {
    'SKILL.md': [
        (r'(?m)^#+ Step 0 —', '输出模式选择（diagnosis/revision 入口）'),
        (r'(?m)^#+ Step 1\.5 —', '平台能力检查'),
        (r'(?m)^#+ Step 4\.6 —', '参考图设定表'),
        (r'(?m)^#+ Step 5\.5 —', '约束加固（iteration-lessons）'),
        (r'option-style questions', '新手选项式追问'),
        (r'3 concrete directions', '零信息兜底'),
        (r'`references/platform-capabilities\.md`', '平台能力引用'),
        (r'`references/iteration-lessons\.md`', '迭代教训引用'),
        (r'`references/reference-image-protocol\.md`', '参考图协议引用'),
        (r'`references/output-modes\.md`', '输出模式引用'),
    ],
    'AGENTS.md': [
        (r'(?m)^#+ Step 0 —', '输出模式选择'),
        (r'(?m)^#+ Step 1\.5 —', '平台能力检查'),
        (r'(?m)^#+ Step 4\.6 —', '参考图设定表'),
        (r'(?m)^#+ Step 5\.5 —', '约束加固'),
        (r'option-style questions', '新手选项式追问'),
        (r'3 concrete directions', '零信息兜底'),
        (r'`references/platform-capabilities\.md`', '平台能力引用'),
        (r'`references/output-modes\.md`', '输出模式引用'),
    ],
    'references/clarification-protocol.md': [
        (r'(?m)^#+ .*选项式追问', '选项式追问章节'),
        (r'(?m)^#+ .*零信息兜底', '零信息兜底章节'),
        (r'只问「猜错了代价高」的维度', '提问原则'),
    ],
    'references/iteration-lessons.md': [
        (r'69\.7%', '修订变长的实测比例'),
        (r'POSITIVE CONSTRAINTS', '最高扩写段'),
        (r'禁止搬进用户作品', '项目专属黑名单'),
    ],
    'references/platform-capabilities.md': [
        (r'\[实证\]', '证据分级'),
        (r'\[未验证\]', '证据分级'),
        (r'以 UI 为准', '快照过期防护'),
    ],
    'references/reference-image-protocol.md': [
        (r'三面板', '设定图格式'),
        (r'consistently across ALL panels', '编辑设定图的硬规则'),
    ],
}

# 两个入口必须同时具备的步骤（防止只改一处导致跨终端行为不一致）
MIRRORED_STEPS = [(r'(?m)^#+ Step 0 —', 'Step 0'), (r'(?m)^#+ Step 1\.5 —', 'Step 1.5'),
                  (r'(?m)^#+ Step 4\.6 —', 'Step 4.6'), (r'(?m)^#+ Step 5\.5 —', 'Step 5.5')]

PLACEHOLDER_RE = re.compile(r'\b(TODO|TBD|FIXME|XXX)\b')
MD_LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
# 本仓库更常用反引号引用而非 markdown 链接，两种都要查
BACKTICK_PATH_RE = re.compile(r'`((?:references|scripts|eval)/[A-Za-z0-9_./-]+\.(?:md|py|json|gz))`')


def check_required(errors):
    for rel, phrases in REQUIRED_PHRASES.items():
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            errors.append('缺文件: %s' % rel)
            continue
        text = open(path, encoding='utf-8').read()
        for pattern, why in phrases:
            if not re.search(pattern, text):
                errors.append('%s 丢失关键契约（%s）' % (rel, why))


def check_mirrored(errors):
    try:
        skill = open(os.path.join(ROOT, 'SKILL.md'), encoding='utf-8').read()
        agents = open(os.path.join(ROOT, 'AGENTS.md'), encoding='utf-8').read()
    except OSError as e:
        errors.append('读取入口文件失败: %s' % e)
        return
    for pattern, label in MIRRORED_STEPS:
        a, b = bool(re.search(pattern, skill)), bool(re.search(pattern, agents))
        if a != b:
            errors.append('%s 只存在于 %s —— 两个入口的工作流必须一致'
                          % (label, 'SKILL.md' if a else 'AGENTS.md'))


def check_links(errors):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', 'out')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            text = open(path, encoding='utf-8', errors='replace').read()
            targets = set()
            for t in MD_LINK_RE.findall(text):
                t = t.strip().split('#', 1)[0]
                if t and '://' not in t and not t.startswith('#'):
                    targets.add((t, os.path.dirname(path)))
            for t in BACKTICK_PATH_RE.findall(text):
                targets.add((t, ROOT))          # 反引号路径一律相对仓库根
            for t, base in targets:
                if not os.path.exists(os.path.join(base, t)):
                    errors.append('死链: %s -> %s' % (rel, t))


def check_placeholders(errors):
    for sub in ('SKILL.md', 'AGENTS.md', 'README.md'):
        p = os.path.join(ROOT, sub)
        if os.path.isfile(p):
            m = PLACEHOLDER_RE.search(open(p, encoding='utf-8').read())
            if m:
                errors.append('%s 含占位符 %s' % (sub, m.group(0)))
    refs = os.path.join(ROOT, 'references')
    if os.path.isdir(refs):
        for fn in sorted(os.listdir(refs)):
            if fn.endswith('.md'):
                m = PLACEHOLDER_RE.search(open(os.path.join(refs, fn), encoding='utf-8').read())
                if m:
                    errors.append('references/%s 含占位符 %s' % (fn, m.group(0)))


def check_manifest_coverage(errors):
    """manifest 声明的文件要存在；references 下的 .md 也不该有漏登记的孤儿。"""
    try:
        m = json.load(open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        errors.append('manifest.json 解析失败: %s' % e)
        return
    declared = set(m.get('dependencies', {}).get('references', []))
    for fn in sorted(os.listdir(os.path.join(ROOT, 'references'))):
        if not fn.endswith('.md'):
            continue
        rel = 'references/%s' % fn
        if rel not in declared and not fn.startswith('character_cards'):
            errors.append('孤儿文件（未登记进 manifest）: %s' % rel)


def main():
    errors = []
    check_required(errors)
    check_mirrored(errors)
    check_links(errors)
    check_placeholders(errors)
    check_manifest_coverage(errors)
    if errors:
        print('结构校验失败：')
        for e in errors:
            print('  - %s' % e)
        return 1
    print('结构校验通过：关键契约、双入口一致性、文档链接、占位符、manifest 覆盖均正常。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
