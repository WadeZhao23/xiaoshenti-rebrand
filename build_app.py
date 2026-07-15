#!/usr/bin/env python3
"""构建可交互 App 版 index.html：shell.html + sprite(取自 gallery.html) + 各屏模板(_frag/*.html)。
每个 <article data-screen=key> → <template data-screen=key ...>inner</template>，路由按 key 克隆渲染。
watch.html 是 <figure> 非 article，交互版不含手表屏（跳过）。"""
import re, pathlib

HERE = pathlib.Path(__file__).parent
FRAG = HERE / "_frag"

shell = (HERE / "shell.html").read_text(encoding="utf-8")
gallery = (HERE / "gallery.html").read_text(encoding="utf-8")

# 1) sprite
m = re.search(r'<svg width="0" height="0".*?</svg>', gallery, re.S)
sprite = m.group(0) if m else ""

# 2) 屏模板
ART = re.compile(r'<article\b([^>]*)>(.*?)</article>', re.S)
def attr(tag, name):
    mm = re.search(name + r'="([^"]*)"', tag)
    return mm.group(1) if mm else ""

FILES = ['brand.html','today.html','onboarding.html','trends.html','ai.html',
         'events_a.html','events_b.html','evidence.html','profile.html','more_a.html','more_b.html']

templates, keys, warns = [], [], []
for f in FILES:
    fp = FRAG / f
    if not fp.exists():
        warns.append('missing:' + f); continue
    html = fp.read_text(encoding="utf-8")
    n = 0
    for mt in ART.finditer(html):
        tag, inner = mt.group(1), mt.group(2)
        key = attr(tag, 'data-screen')
        if not key:
            warns.append(f + ':article-without-data-screen'); continue
        tab = attr(tag, 'data-tab') or 'none'
        nav = attr(tag, 'data-nav') or 'none'
        theme = attr(tag, 'data-theme') or 'light'
        templates.append(
            f'<template data-screen="{key}" data-tab="{tab}" data-nav="{nav}" data-theme="{theme}">{inner}</template>')
        keys.append(key); n += 1
    if n == 0:
        warns.append('no-articles:' + f)

out = shell.replace('<!--SPRITE-->', sprite).replace('<!--SCREENS-->', '\n'.join(templates))
(HERE / "index.html").write_text(out, encoding="utf-8")
print(f"built index.html · {len(templates)} screens")
print("keys:", ", ".join(keys))
if warns: print("warnings:", warns)
