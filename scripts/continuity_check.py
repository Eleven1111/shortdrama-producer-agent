#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""continuity_check.py — 短剧批次交付前的连续性链自动核对（零依赖）。

理念蒸馏自 Emily2040/seedance-2.0（MIT）的 continuity_chain_check.py（血缘引擎），
实现为本项目的轻量版：不引入 project-state JSON schema，直接解析我们序列协议的
三行序列头，在交付前机械捕获最易错的断链。

检查每镜的三行序列头、批次内的镜号和来源引用，以及相邻镜的结构化状态交接。
自然语言缺少重叠信号时只提示人工核对。显式时间跳跃允许状态变化。

用法：
  python3 scripts/continuity_check.py <shots.md>        # 逐镜文本或 md
  python3 scripts/continuity_check.py <shots.md> --json # 机器可读输出
退出码：0 = 通过；1 = 存在 error。警告不影响退出码。
"""
from __future__ import annotations
import argparse, json, re, sys

HEADER_SHOT = re.compile(r"^#\s*shot\s+(\d+)\s*/\s*(\d+)\s*\|(.*)$", re.IGNORECASE)
HEADER_FROM = re.compile(r"\bfrom\s+shot\s+(\d+)\b", re.IGNORECASE)
HEADER_START = re.compile(r"^#\s*start state\s*[:：]\s*(.*)$", re.IGNORECASE)
HEADER_END = re.compile(r"^#\s*end state\s*[:：]\s*(.*)$", re.IGNORECASE)
HEADER_CONTINUITY = re.compile(r"^#\s*(start|end) continuity\s*[:：]\s*(.*)$", re.IGNORECASE)
TIME_JUMP = re.compile(r"^(?:衔接|transition)\s*[:：]\s*(?:时间跳跃|time jump|time cut)(?:$|\s)", re.IGNORECASE)
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

def parse_continuity(raw: str) -> dict[str, str]:
    def unique_fields(pairs):
        values = {}
        for key, value in pairs:
            if key in values:
                raise ValueError(f"重复字段 {key}")
            if not key.strip() or not isinstance(value, str) or not value.strip():
                raise ValueError("字段和值都必须为非空字符串")
            values[key] = value
        return values

    fields = json.loads(raw, object_pairs_hook=unique_fields)
    if not isinstance(fields, dict) or not fields:
        raise ValueError("需要非空 JSON 对象")
    return fields


def parse_shots(text: str) -> list[dict]:
    shots: list[dict] = []
    cur: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        m = HEADER_SHOT.match(line)
        if m:
            fields = [field.strip() for field in m.group(3).split("|")]
            refs = HEADER_FROM.findall(m.group(3))
            cur = {
                "n": int(m.group(1)),
                "total": int(m.group(2)),
                "from": int(refs[0]) if refs else None,
                "time_jump": any(TIME_JUMP.match(field) for field in fields),
                "text": {},
                "continuity": {},
                "anchors": set(),
                "errors": ["序列头包含多个 from shot 引用"] if len(refs) > 1 else [],
            }
            shots.append(cur)
        if cur is None:
            continue
        cur["anchors"].update(a.strip() for a in ANCHOR.findall(line))
        for field, pattern in (("start", HEADER_START), ("end", HEADER_END)):
            if state := pattern.match(line):
                if field in cur["text"]:
                    cur["errors"].append(f"序列头重复 {field} state 行")
                cur["text"][field] = state.group(1).strip()
        if match := HEADER_CONTINUITY.match(line):
            field, raw_json = match.groups()
            field = field.lower()
            if field in cur["continuity"]:
                cur["errors"].append(f"序列头重复 {field} continuity 行")
            try:
                cur["continuity"][field] = parse_continuity(raw_json)
            except ValueError as exc:
                cur["continuity"][field] = {}
                cur["errors"].append(f"{field} continuity 格式错误: {exc}")
    return shots


def check(shots: list[dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    if not shots:
        return ["未找到任何序列头（# shot N / total | ...）"], warns

    declared_total = shots[0]["total"]
    if 0 < len(shots) < declared_total:
        warns.append(f"声明 total={declared_total}，本批解析到 {len(shots)} 镜"
                     "（跨批核对请带上前一批）")

    for shot in shots:
        n, total = shot["n"], shot["total"]
        errors.extend(f"镜 {n}: {error}" for error in shot["errors"])
        if not 1 <= n <= total:
            errors.append(f"镜 {n}: 镜号必须在 1..{total} 内")
        if total != declared_total:
            errors.append(f"镜 {n}: 声明 total={total}，与首镜的 {declared_total} 不一致")
        for field in ("start", "end"):
            if not shot["text"].get(field):
                errors.append(f"镜 {n}: 序列头缺 {field} state 行或内容为空")
        if shot["from"] is not None and (n == 1 or shot["from"] != n - 1):
            errors.append(f"镜 {n}: 衔接字段中的 from shot {shot['from']} 不是有效上一镜")

    for prev, cur in zip(shots, shots[1:]):
        if cur["n"] != prev["n"] + 1:
            errors.append(f"批次内镜号必须连续: {prev['n']} → {cur['n']}")
        if cur["time_jump"]:
            continue
        before = prev["continuity"].get("end", {})
        after = cur["continuity"].get("start", {})
        shared_fields = before.keys() & after.keys()
        for field in sorted(shared_fields):
            if before[field] != after[field]:
                errors.append(f"镜 {prev['n']} → {cur['n']}: {field} 状态冲突"
                              f"（{before[field]} → {after[field]}）")
        end, start = prev["text"].get("end"), cur["text"].get("start")
        if end and start and not shared_fields:
            prev_latin, prev_bi = content_signals(end)
            cur_latin, cur_bi = content_signals(start)
            if not (prev_latin & cur_latin) and len(prev_bi & cur_bi) < 2:
                warns.append(f"镜 {prev['n']} → {cur['n']}: 起止状态缺少共同内容词，请人工核对")

    canon: dict[str, tuple[int, str]] = {}
    for shot in shots:
        for anchor in sorted(shot["anchors"]):
            base = VERSION_SUFFIX.sub("", anchor)
            first_n, first_base = canon.setdefault(base.lower(), (shot["n"], base))
            if base != first_base:
                warns.append(f"锚点大小写漂移: 镜 {first_n} 用 `{first_base}`，"
                             f"镜 {shot['n']} 用 `{base}`")
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
            print("  批次镜号、序列头与可检查的交接字段均通过。")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
