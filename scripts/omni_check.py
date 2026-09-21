#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""omni_check.py — Gemini Omni 方言交付前的确定性自检（零依赖）。

把 `references/model-adaptation.md` §7.3 / §7.4 的检查项落成机器判据。工艺层（运动配方 / 表演时序 /
光影语法）不在这里查 —— 这里只查**方言**：Omni 独有的规矩，Seedance 稿照搬过来必踩的那些。

用法：
  python3 omni_check.py <文件>              # 文件内含 1..N 条 prompt
  python3 omni_check.py <文件> --json
  cat p.txt | python3 omni_check.py

分条方式：文件里出现 `# shot N` / `===== SHOT N` / 单独一行 `---` 即视为新的一条 prompt；
都没有就把整份文件当一条。退出码：0 = 通过；1 = 有 error。

判据来源（每条对应 §7.4 的一行）：
  [E] 焦距/角度数值未删        —— 能力轴 8：多模型不认 mm 与度数
  [E] 画幅不是 16:9/9:16/1:1   —— Omni 只有三种画幅，21:9 不存在
  [E] 未声明单场景             —— 单场景强制；不写模型会自作主张叙事剪辑
  [E] 单次生成里写了 hard cut   —— 镜内不切；跨镜转场必须在生成之间做
  [E] 时长 / 时间码 >10s 且未规划 Extend —— 单次 ≤10s
  [E] 跨镜接续用自然语言祈使句   —— 独立生成之间无效，必须换末帧资产锚
  [E] 帧内文字与 No text overlays 互斥
  [W] 参数行未写 360p 预览      —— 成本纪律：参数行里要真写出 360p
  [W] seed 是相对说法或无 seed   —— 必须写死绝对数字
  [W] 负面清单超过 3 行          —— Omni 负面极简，其余转正面锁
"""
from __future__ import annotations
import argparse, gzip, json, pathlib, re, sys

SPLIT = re.compile(r"^(?:#\s*shot\b.*|={3,}\s*SHOT\b.*|-{3,})\s*$", re.I | re.M)

NUMERIC_OPTICS = [
    (re.compile(r"\b\d+(?:\.\d+)?\s?mm\b", re.I), "焦距数值（mm）"),
    (re.compile(r"\d+(?:\.\d+)?\s?°"), "角度数值（°）"),
    (re.compile(r"\bf/\d(?:\.\d+)?\b", re.I), "光圈数值（f/N）"),
]
RATIOS = ("16:9", "9:16", "1:1")
SINGLE_SCENE = re.compile(r"single continuous shot|no scene cuts|one unbroken scene", re.I)
HARD_CUT = re.compile(r"hard cut", re.I)
TIMECODE = re.compile(r"\[(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*s\]")
DURATION = re.compile(r"duration:\s*(\d+(?:\.\d+)?)", re.I)
SEED_ABS = re.compile(r"\bseed\s*[:=]?\s*(\d{3,})", re.I)
SEED_REL = re.compile(r"same seed|seed as the others?|the same seed|identical seed", re.I)
EXTEND_PLAN = re.compile(r"\bextend\b", re.I)
NEG_LINE = re.compile(r"^No\s+[A-Z].*\.\s*$", re.M)
NO_TEXT_OVERLAY = re.compile(r"no text overlays|no text overlay", re.I)
WANTS_TEXT = re.compile(
    r"\blegible\b|\breads\s+[\"“]|sign reading|lettering visible|"
    r"visible text|renders the words|the words .{0,20}read", re.I)
REL_CONTINUITY = re.compile(
    r"must match shot\s*\d|same as shot\s*\d|identical to shot\s*\d|"
    r"matches shot\s*\d|repeats the .{0,30}of shot\s*\d|"
    r"the colour must match|in the same acoustic space as shot", re.I)
END_FRAME_ANCHOR = re.compile(r"final frame of the (?:previous|preceding) shot|image_\d+\.png is the final frame", re.I)
PREVIEW_360 = re.compile(r"360p", re.I)
DIALOGUE_COLON = re.compile(r"says\s*:", re.I)
QUOTED_DIALOGUE = re.compile(r"\bsays\s*[\"“]|\basks\s*[\"“]|[\"“][^\"”]{3,}[\"”]\s*(?:says|asks)")


def split_prompts(text: str):
    parts = [p.strip() for p in SPLIT.split(text)]
    parts = [p for p in parts if p and len(p) > 60]
    return parts or ([text.strip()] if text.strip() else [])


def check_one(text: str):
    err, warn, ok = [], [], []

    for rx, label in NUMERIC_OPTICS:
        m = rx.search(text)
        if m:
            err.append(f"{label}未删：`{m.group(0)}` —— 能力轴 8，多模型不认数值，改写效果"
                       f"（`medium shot, eye-level` / `shallow depth of field`）")
    if not err or not any("焦距" in e or "角度" in e for e in err):
        ok.append("参数数值已清")

    if "21:9" in text or "2.39" in text:
        err.append("画幅 21:9 在 Omni 不存在 —— 改成 16:9 / 9:16 / 1:1，并重查原本靠宽画幅成立的调度")
    if not any(r in text for r in RATIOS):
        warn.append("正文没声明画幅（16:9 / 9:16 / 1:1 三选一）")
    else:
        ok.append("画幅在 Omni 支持集合内")

    if not SINGLE_SCENE.search(text):
        err.append("未声明单场景 —— 必须写明 `single continuous shot` / `no scene cuts`，"
                   "否则 Omni 会自作主张叙事剪辑")
    else:
        ok.append("单场景强制已声明")

    if HARD_CUT.search(text):
        err.append("单次生成里写了 `hard cut` —— Omni 镜内不切；跨镜转场必须在生成之间做"
                   "（多镜拼接或剪辑台），或用时间码语法做镜内节奏")

    d = DURATION.search(text)
    tc = [float(b) for _, b in TIMECODE.findall(text)]
    span = max(tc) if tc else (float(d.group(1)) if d else None)
    if span is not None and span > 10 and not EXTEND_PLAN.search(text):
        err.append(f"单次生成跨度 {span:.1f}s > 10s 且未规划 Extend —— 拆两镜，或用 Extend 链"
                   f"（每次 +10s，总长 ≤40s；注意 Extend 会改接最后几帧）")
    elif span is not None:
        ok.append(f"时长 {span:.1f}s ≤ 10s")

    if REL_CONTINUITY.search(text):
        m = REL_CONTINUITY.search(text)
        err.append(f"跨镜接续用了自然语言祈使句（`{m.group(0)}`）—— 独立生成之间无效。"
                   f"改成末帧资产锚：把上一镜末帧截存为 image_N.png，正文写 "
                   f"`image_N.png is the final frame of the previous shot`")
    if END_FRAME_ANCHOR.search(text):
        ok.append("跨镜接续走末帧资产锚")

    if NO_TEXT_OVERLAY.search(text) and WANTS_TEXT.search(text):
        err.append("帧内可读文字与 `No text overlays` 互斥 —— 二选一：删掉 No text overlays，"
                   "改成范围化正向锁（`the sign is the only text in frame`）；"
                   "同批里任何一镜漏改都会重现")

    if not PREVIEW_360.search(text):
        warn.append("正文没写 360p —— 成本纪律要求参数行里真的写出 `Preview at 360p`，"
                    "只在交付说明里提不算")
    else:
        ok.append("360p 预览已写进正文")

    if SEED_REL.search(text):
        warn.append("seed 是无锚点的相对锁（`same seed` 之类）—— 每次生成是独立会话，"
                    "必须写死绝对数字：`Seed 481923`")
    elif not SEED_ABS.search(text):
        warn.append("未写 seed —— 跨镜一致性双锁缺一半（逐字复用角色描述 + 绝对 seed）")
    else:
        ok.append("绝对 seed 已写")

    negs = NEG_LINE.findall(text)
    if len(negs) > 3:
        warn.append(f"负面清单 {len(negs)} 行 > 3 —— Omni 负面极简，其余负面转正面锁")
    elif negs:
        ok.append(f"负面 {len(negs)} 行（极简）")

    if QUOTED_DIALOGUE.search(text) and not DIALOGUE_COLON.search(text):
        warn.append("对白疑似带引号 —— Omni 用冒号引出：`A woman says: My name is Clara.`"
                    "（引号会诱发模型把话渲染成字幕）")

    return err, warn, ok


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemini Omni 方言自检（交付前跑一遍）")
    ap.add_argument("file", nargs="?", help="含 1..N 条 prompt 的文件；缺省读 stdin")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    a = ap.parse_args()
    if a.file:
        text = pathlib.Path(a.file).read_text(encoding="utf-8", errors="replace")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print(__doc__)
        return 1
    prompts = split_prompts(text)
    if not prompts:
        print("空输入")
        return 1

    report, total_e = [], 0
    for i, p in enumerate(prompts, 1):
        err, warn, ok = check_one(p)
        total_e += len(err)
        report.append({"n": i, "errors": err, "warnings": warn, "passed": ok})

    if a.json:
        print(json.dumps({"prompts": len(prompts), "errors": total_e, "report": report},
                         ensure_ascii=False, indent=2))
        return 1 if total_e else 0

    print(f"解析到 {len(prompts)} 条 prompt\n")
    for r in report:
        head = r["errors"][0][:46] if r["errors"] else (r["warnings"][0][:46] if r["warnings"] else "通过")
        print(f"-- prompt {r['n']} · {len(r['errors'])} error / {len(r['warnings'])} warn · {head}")
        for e in r["errors"]:
            print(f"   [ERROR] {e}")
        for w in r["warnings"]:
            print(f"   [WARN]  {w}")
        print()
    if not total_e:
        print("Omni 方言自检通过：数值已清、画幅合法、单场景已声明、时长 ≤10s、"
              "接续走资产锚、无帧内文字冲突。")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main())
