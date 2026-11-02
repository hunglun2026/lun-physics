"""頁面樣板：每個函式回傳完整 HTML 字串。頁面不含內嵌腳本與內嵌樣式（符合 CSP）。"""
from __future__ import annotations

import html
import json

SITE = "普通物理"
URL = "https://physics.hunglun.com"
PRELOAD = ""  # build.py 依 public/fonts 裡第 0 包字型檔名設定（預先載入，不用等 CSS 解析完才開始抓字型）
V = "1"  # CSS／JS 的 ?v=，改了要全站一起升（scripts/build.py 讀 VERSION 檔）


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def shell(title: str, desc: str, body: str, path: str, ver: str = V, jsonld: dict | None = None, js: str = "site") -> str:
    full = f"{title}｜{SITE}" if title != SITE else f"{SITE}｜大學普通物理免費學習站"
    extra = "" if js == "site" else f'<script src="/js/{js}.js?v={ver}" defer></script>'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}{path}">
<meta property="og:image" content="{URL}/img/logo.webp">
<meta name="theme-color" content="#16325c">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{PRELOAD}
<link rel="stylesheet" href="/css/katex.css?v={ver}">
<link rel="stylesheet" href="/css/style.css?v={ver}">
{ld}
</head>
<body>
<a class="skip" href="#main">跳到內容</a>
<header class="top"><div class="wrap">
<a class="brand" href="/"><img class="mark" src="/img/logo-192.webp" width="34" height="34" alt=""><span>{SITE}</span></a>
<nav aria-label="主選單"><a href="/#units">全部單元</a><a href="/help">怎麼用</a><a href="/about">授權與出處</a></nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer class="foot"><div class="wrap">
<p>內容由本站原創撰寫，公式與題目答案皆經程式驗算。覺得哪裡有錯，請按頁面下方的「回報錯誤」。</p>
<p><a href="/about">授權與出處</a>　<a href="/privacy">隱私</a>　<a href="/help">怎麼用</a>　<button type="button" class="linkbtn" data-report>回報錯誤</button></p>
</div></footer>
<dialog id="reportDlg" aria-labelledby="rdT"><form method="dialog" id="reportForm">
<h2 id="rdT">回報錯誤</h2>
<p class="muted">不需要姓名與聯絡方式。請寫清楚哪一題或哪一句有問題。</p>
<label class="sr" for="reportText">說明</label>
<textarea id="reportText" maxlength="500" rows="5" required placeholder="例：第 3 題答案應該是 …"></textarea>
<p id="reportMsg" class="muted" role="status"></p>
<div class="row"><button type="button" class="btn ghost" id="reportCancel">取消</button><button type="submit" class="btn" id="reportSend">送出</button></div>
</form></dialog>
<script src="/js/site.js?v={ver}" defer></script>
{extra}
</body>
</html>
"""


def chapter_page(ch, unit_name: str, body_html: str, probs_html: str, prev, nxt, refs_html: str, ver: str) -> str:
    nav = '<nav class="pnav" aria-label="上一章與下一章">'
    nav += f'<a class="prev" href="/c/{prev.id}"><small>上一章</small>{esc(prev.title)}</a>' if prev else "<span></span>"
    nav += f'<a class="next" href="/c/{nxt.id}"><small>下一章</small>{esc(nxt.title)}</a>' if nxt else "<span></span>"
    nav += "</nav>"
    body = f"""<nav class="crumb" aria-label="目前位置"><a href="/">首頁</a> › <a href="/#u-{ch.unit}">{esc(unit_name)}</a></nav>
<article class="chapter" data-ch="{ch.id}" data-nprob="{len(ch.problems)}">
<p class="kicker">{esc(unit_name)}　第 {ch.no} 章</p>
<h1>{esc(ch.title)}</h1>
<p class="lead">{esc(ch.lead)}</p>
{body_html}
<section class="practice" aria-labelledby="pt"><h2 id="pt">練習題</h2>
<p class="muted">每題輸入數值答案，系統容許約 {int(round(ch.problems[0].tol * 100)) if ch.problems else 2}% 誤差。卡住時先看提示，最後再看解答。</p>
{probs_html}
</section>
{refs_html}
<div class="actions"><button class="btn" id="doneBtn" type="button" aria-pressed="false">標記這章讀完</button>
<button class="btn ghost" data-report type="button">回報這頁的錯誤</button></div>
{nav}
</article>"""
    desc = f"{ch.title}：{ch.lead}"
    ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": ch.title, "description": ch.lead,
          "inLanguage": "zh-Hant", "learningResourceType": "lesson", "educationalLevel": "大學普通物理",
          "isAccessibleForFree": True, "url": f"{URL}/c/{ch.id}"}
    return shell(ch.title, desc, body, f"/c/{ch.id}", ver, ld, js="chapter")


def problem_html(i: int, p, q_html: str, steps_html: str) -> str:
    hint = f'<details class="hint"><summary>提示</summary><p>{p.hint}</p></details>' if p.hint else ""
    return f"""<div class="prob" data-i="{i}" data-ans="{p.ans:.10g}" data-tol="{p.tol}">
<p class="pq"><span class="qn">{i + 1}</span><span class="qt">{q_html}</span></p>
<div class="row"><label class="sr" for="a{i}">第 {i + 1} 題答案</label>
<input id="a{i}" class="ans" inputmode="decimal" autocomplete="off" placeholder="答案數值"><span class="uu">{esc(p.unit)}</span>
<button class="btn" type="button" data-act="check">檢查</button></div>
<p class="res" role="status"></p>
{hint}
<details class="sol"><summary>看解答</summary><div class="steps">{steps_html}</div></details>
</div>"""


def home_page(units, chapters_by_unit, total: int, ver: str) -> str:
    cards = []
    for uid, uname, udesc in units:
        chs = chapters_by_unit.get(uid, [])
        if not chs:
            continue
        li = "".join(f'<li><a href="/c/{c.id}" data-ch="{c.id}"><span class="no">{c.no}</span>'
                     f'<span class="tt">{esc(c.title)}</span><span class="ck" aria-hidden="true"></span></a></li>' for c in chs)
        cards.append(f'<section class="unit" id="u-{uid}"><h2>{esc(uname)}</h2><p class="muted">{esc(udesc)}</p><ol class="chlist">{li}</ol></section>')
    body = f"""<section class="hero">
<p class="kicker">免費、免註冊、不放廣告</p>
<h1>大學普通物理，<br>從零看懂，自己算得出來</h1>
<p class="lead">{total} 個章節，涵蓋力學、波、熱學、電磁、光學與近代物理。每章有白話講解、互動模擬和附解答的練習題，答案都經程式驗算。</p>
<div class="stats"><div><b>{total}</b><span>章</span></div><div><b id="doneN">0</b><span>章已讀完</span></div><div><b>0</b><span>元</span></div></div>
<div class="row"><a class="btn" href="/c/{chapters_by_unit['mechanics'][0].id}">從第一章開始</a><a class="btn ghost" href="#units">看全部單元</a></div>
<p class="muted small">進度只存在你這台裝置的瀏覽器裡，不上傳。</p>
</section>
<div class="search"><label class="sr" for="q">搜尋章節</label><input id="q" type="search" placeholder="搜尋章節，例如：牛頓、電容、干涉" autocomplete="off"><p id="qn" class="muted" role="status"></p></div>
<div id="units" class="units">{''.join(cards)}</div>"""
    ld = {"@context": "https://schema.org", "@type": "Course", "name": "大學普通物理", "inLanguage": "zh-Hant",
          "description": "涵蓋力學、波、熱學、電磁、光學與近代物理的免費繁體中文自學課程",
          "isAccessibleForFree": True, "provider": {"@type": "Organization", "name": "鴻綸科技", "url": "https://hunglun.com"}}
    return shell(SITE, f"{total} 章免費大學普通物理，白話講解、互動模擬、附解答練習題，免註冊。", body, "/", ver, ld, js="home")


def simple_page(title: str, desc: str, path: str, inner: str, ver: str) -> str:
    return shell(title, desc, f'<article class="doc"><h1>{esc(title)}</h1>{inner}</article>', path, ver)
