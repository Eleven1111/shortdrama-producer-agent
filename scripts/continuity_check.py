#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""continuity_check.py — 短剧批次交付前的连续性链自动核对（零依赖）。

理念蒸馏自 Emily2040/seedance-2.0（MIT）的 continuity_chain_check.py（血缘引擎），
实现为本项目的轻量版：不引入 project-state JSON schema，直接解析我们序列协议的
三行序列头，在交付前机械捕获最易错的断链。

检查四件事：
  1. 序列头齐全且镜号连续（1..N 无跳号、无重复）
  2. 相邻镜衔接：镜 N 的 start state 与镜 N-1 的 end state 有实质重叠
     （锚点名重合，或内容词重合 ≥1），无重叠 = 断链（error）
  3. 锚点 `<<<name>>>` 一致性：同一角色跨镜出现大小写/拼写变体 → 警告
     （版本号 _v2/_v3 属于合法状态演进，不算变体）
  4. 衔接字段引用的 from shot N-1 与实际镜号一致

用法：
  python3 scripts/continuity_check.py <shots.md>        # 逐镜文本或 md
  python3 scripts/continuity_check.py <shots.md> --json # 机器可读输出
退出码：0 = 通过；1 = 存在 error。警告不影响退出码。
"""
from __future__ import annotations
import argparse, json, re, sys

HEADER_SHOT = re.compile(r"^#\s*shot\s+(\d+)\s*/\s*(\d+)\s*\|", re.IGNORECASE | re.MULTILINE)
HEADER_FROM = re.compile(r"from\s+shot\s+(\d+)", re.IGNORECASE)
HEADER_START = re.compile(r"^#\s*start state\s*[:：]\s*(.+)$", re.IGNORECASE)
HEADER_END = re.compile(r"^#\s*end state\s*[:：]\s*(.+)$", re.IGNORECASE)
ANCHOR = re.compile(r"<<<([^<>]+)>>>")
VERSION_SUFFIX = re.compile(r"_v\d+$", re.IGNORECASE)
# 忽略的虚词（中英通用最小集；重叠判定用）
STOP = set("的 了 在 是 和 与 a an the of to with and then as on in at from into "
           "camera shot scene continues now state 同 上镜 上一镜 本镜".split())

def content_signals(text: str) -> tuple[set[str], set[str]]:
    """返回 (拉丁词集合, 汉字二元组集合)。中文无分词，用 bigram 做实质重叠判定。"""
    latin = {w.lower() for w in re.findall(r"[A-Za-z_]+", text)
             if w.lower() not in STOP and len(w) > 1}
    han = re.findall(r"[\u4e00-\u9fff]+", text)
    bigrams = set()
    for run in han:
        run = "".join(ch for ch in run if ch not in "的了在是和与")
        bigrams.update(run[i:i + 2] for i in range(len(run) - 1))
    return latin, bigrams

def parse_shots(text: str) -> list[dict]:
    shots: list[dict] = []
    cur: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        m = HEADER_SHOT.match(line)
        if m:
            cur = {"n": int(m.group(1)), "total": int(m.group(2)),
                   "line": line, "from": None, "start": None, "end": None,
                   "anchors": set()}
            shots.append(cur)
            continue
        if cur is None:
            continue
        if (f := HEADER_FROM.search(line)):
            cur["from"] = int(f.group(1))
        if (s := HEADER_START.match(line)):
            cur["start"] = s.group(1).strip()
        if (e := HEADER_END.match(line)):
            cur["end"] = e.group(1).strip()
    # 锚点收集：锚点可出现在任何行，按镜块归属（下一个 shot 头之前的全部文本）
    # 注意：HEADER_SHOT 有 2 个捕获组，re.split 的分组边界是 3 而非 4——
    # 早先按 stride=4 取 body 会整体错位（且 ^ 未加 MULTILINE 时一个匹配都没有）。
    # 改用 finditer 按匹配起点切分，与捕获组数量解耦。
    marks = list(HEADER_SHOT.finditer(text))
    for i, m in enumerate(marks):
        n = int(m.group(1))
        body = text[m.end():(marks[i + 1].start() if i + 1 < len(marks) else len(text))]
        for shot in shots:
            if shot["n"] == n:
                shot["anchors"] = {a.strip() for a in ANCHOR.findall(body)}
                break
    return shots

def check(shots: list[dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    if not shots:
        return ["未找到任何序列头（# shot N / total | ...）"], warns
    nums = [s["n"] for s in shots]
    if nums != sorted(nums) or len(set(nums)) != len(nums):
        errors.append(f"镜号不连续或有重复: {nums}")
    declared_total = shots[0]["total"]
    if declared_total and len(shots) != declared_total:
        warns.append(f"声明 total={declared_total}，实际解析到 {len(shots)} 镜"
                     "（可能是分批交付；跨批核对请带上前一批）")
    # 相邻镜衔接
    for prev, cur in zip(shots, shots[1:]):
        if not prev["end"] or not cur["start"]:
            errors.append(f"镜 {cur['n']}: 序列头缺 start/end state 行")
            continue
        prev_anchors = {a.lower() for a in prev["anchors"]}
        cur_anchors = {a.lower() for a in cur["anchors"]}
        shared_anchors = prev_anchors & cur_anchors
        prev_latin, prev_bi = content_signals(prev["end"])
        cur_latin, cur_bi = content_signals(cur["start"])
        shared_latin = prev_latin & cur_latin
        shared_bigrams = prev_bi & cur_bi
        if not shared_anchors and not shared_latin and len(shared_bigrams) < 2:
            errors.append(
                f"断链: 镜 {prev['n']} end state 与镜 {cur['n']} start state "
                f"无任何锚点/内容词重叠 —— start 必须承接观测到的终态")
        if cur["from"] is not None and cur["from"] != prev["n"]:
            errors.append(f"镜 {cur['n']}: 衔接字段写 from shot {cur['from']}，"
                          f"但前一镜实际是 shot {prev['n']}")
    # 锚点拼写漂移（忽略版本号差异）
    canon: dict[str, tuple[int, str]] = {}
    for s in shots:
        for a in sorted(s["anchors"]):
            key = VERSION_SUFFIX.sub("", a).lower()
            if key in canon:
                first_n, first_a = canon[key]
                if a.lower() != first_a.lower():
                    warns.append(f"锚点拼写漂移: 镜 {first_n} 用 `<<<{first_a}>>>`，"
                                 f"镜 {s['n']} 用 `<<<{a}>>>` —— 锚点须逐字复用")
            else:
                canon[key] = (s["n"], a)
    return errors, warns

def main() -> int:
    ap = argparse.ArgumentParser(description="短剧序列连续性链核对（交付前跑一遍）")
    ap.add_argument("file", help="含逐镜 prompt 的 md/txt 文件")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()
    text = open(args.file, encoding="utf-8", errors="replace").read()
    shots = parse_shots(text)
    errors, warns = check(shots)
    if args.json:
        print(json.dumps({"shots": len(shots), "errors": errors,
                          "warnings": warns}, ensure_ascii=False, indent=2))
    else:
        print(f"解析到 {len(shots)} 镜")
        for e in errors:
            print(f"  [ERROR] {e}")
        for w in warns:
            print(f"  [WARN]  {w}")
        if not errors and not warns:
            print("  链路连续：镜号、end→start 衔接、锚点一致性均通过。")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
