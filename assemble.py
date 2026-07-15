#!/usr/bin/env python3
"""把 _frag/*.html 拼进 index.html 的 <!--INSERT:x--> 占位。
幂等：用 <!--INSERT:x-->...<!--END:x--> 包裹注入内容，可反复重跑。"""
import re, pathlib, sys

HERE = pathlib.Path(__file__).parent
INDEX = HERE / "index.html"
FRAG = HERE / "_frag"

# 占位名 -> fragment 文件
MAP = {
    "onboarding": "onboarding.html",
    "trends":     "trends.html",
    "ai":         "ai.html",
    "events":     "events_a.html",
    "events2":    "events_b.html",
    "evidence":   "evidence.html",
    "profile":    "profile.html",
    "more":       "more_a.html",
    "more2":      "more_b.html",
    "watch":      "watch.html",
}

html = INDEX.read_text(encoding="utf-8")
missing = []
for key, fname in MAP.items():
    fp = FRAG / fname
    if not fp.exists():
        missing.append(fname)
        content = f"<!-- MISSING frag: {fname} -->"
    else:
        content = fp.read_text(encoding="utf-8").strip()
    block = f"<!--INSERT:{key}-->\n{content}\n<!--END:{key}-->"
    # 已注入过 -> 替换整段；否则替换裸标记
    pat_done = re.compile(r"<!--INSERT:%s-->.*?<!--END:%s-->" % (re.escape(key), re.escape(key)), re.S)
    if pat_done.search(html):
        html = pat_done.sub(lambda m: block, html)
    else:
        html = html.replace(f"<!--INSERT:{key}-->", block)

INDEX.write_text(html, encoding="utf-8")
print("assembled. missing frags:", missing if missing else "none")
