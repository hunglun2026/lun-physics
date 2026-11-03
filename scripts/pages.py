"""頁面樣板：每個函式回傳完整 HTML 字串。頁面不含內嵌腳本與內嵌樣式（符合 CSP）。"""
from __future__ import annotations

import html
import json
import re

SITE = "普通物理"
URL = "https://physics.hunglun.com"
PRELOAD = ""  # build.py 依 public/fonts 裡第 0 包字型檔名設定（預先載入，不用等 CSS 解析完才開始抓字型）
V = "1"  # CSS／JS 的 ?v=，改了要全站一起升（scripts/build.py 讀 VERSION 檔）


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def shell(title: str, desc: str, body: str, path: str, ver: str = V, jsonld: dict | None = None, js: str = "site") -> str:
    full = f"{title}｜{SITE}" if title != SITE else f"{SITE}｜大學普通物理免費學習站"
    extra = "" if js == "site" else f'<script src="/js/{js}.js?v={ver}" defer></script>'
    cur_help = ' aria-current="page"' if path == "/help" else ""
    cur_about = ' aria-current="page"' if path == "/about" else ""
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
<meta name="theme-color" content="#faf8f3">
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
<a class="brand" href="/home"><img class="mark" src="/img/logo-192.webp" width="34" height="34" alt=""><span>{SITE}</span></a>
<nav aria-label="主選單"><a href="/home#units">全部單元</a><a href="/help"{cur_help}>怎麼用</a><a href="/about"{cur_about}>授權與出處</a></nav>
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
    # 本章目錄：幫每個 <h2> 加 id，頂端放一排跳轉鈕（長章節不用一直往下捲）
    heads: list[str] = []

    def add_id(m):
        heads.append(m.group(1))
        return f'<h2 id="s{len(heads)}">{m.group(1)}</h2>'
    body_html = re.sub(r"<h2>(.*?)</h2>", add_id, body_html)
    toc_items = "".join(f'<li><a href="#s{i}">{re.sub("<[^>]+>", "", h)}</a></li>' for i, h in enumerate(heads, 1))
    toc = f'<ul class="toc" aria-label="本章目錄">{toc_items}<li><a href="#pt">練習題</a></li></ul>'
    nx = (f'<a class="btn" href="/c/{nxt.id}">下一章：{esc(nxt.title)}</a>' if nxt else '<a class="btn" href="/home">回首頁看全部單元</a>')
    n = len(ch.problems)
    body = f"""<nav class="crumb" aria-label="目前位置"><a href="/home">首頁</a> › <a href="/home#u-{ch.unit}">{esc(unit_name)}</a></nav>
<article class="chapter" data-unit="{ch.unit}" data-ch="{ch.id}" data-nprob="{len(ch.problems)}">
<p class="kicker">{esc(unit_name)}　第 {ch.no} 章</p>
<h1>{esc(ch.title)}</h1>
<p class="lead">{esc(ch.lead)}</p>
{toc}
{body_html}
<section class="practice" aria-labelledby="pt"><h2 id="pt">練習題</h2>
<p class="muted">每題輸入數值答案，系統容許約 {int(round(ch.problems[0].tol * 100)) if ch.problems else 2}% 誤差。卡住時先看提示，最後再看解答。</p>
<div class="pprog"><span id="pcount">已答對 0 / {n} 題</span><span class="bar" aria-hidden="true"><i id="pbar"></i></span></div>
{probs_html}
<div class="cta" id="cta" hidden><p><b>這章的題目全部答對了。</b></p><div class="row">{nx}</div></div>
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
    cards, jumps = [], []
    allch = [c for cs in chapters_by_unit.values() for c in cs]
    n_prob = sum(len(c.problems) for c in allch)
    n_sim = len({ln[5:].strip() for c in allch for ln in c.body.splitlines() if ln.startswith("!sim ")})
    for uid, uname, udesc in units:
        chs = chapters_by_unit.get(uid, [])
        if not chs:
            continue
        li = "".join(f'<li><a href="/c/{c.id}" data-ch="{c.id}"><span class="no">{c.no}</span>'
                     f'<span class="tt">{esc(c.title)}</span><span class="ck" aria-hidden="true"></span></a></li>' for c in chs)
        jumps.append(f'<li data-unit="{uid}"><a href="#u-{uid}">{esc(uname)}　{len(chs)} 章</a></li>')
        cards.append(f'<section class="unit" data-unit="{uid}" id="u-{uid}"><div class="unit-h"><h2>{esc(uname)}</h2>'
                     f'<span class="upg" data-total="{len(chs)}">共 {len(chs)} 章</span></div><p class="muted">{esc(udesc)}</p><ol class="chlist">{li}</ol></section>')
    first = chapters_by_unit["mechanics"][0].id
    body = f"""<section class="hero">
<p class="pill">免費、免註冊、不放廣告</p>
<h1>大學普通物理，<br>從零看懂，自己算得出來</h1>
<p class="lead">用白話把觀念講清楚，拖一拖模擬看結果怎麼變，再用練習題確認自己真的會了。</p>
<div class="row"><a class="btn" id="start" href="/c/{first}">從第一章開始</a><a class="btn ghost" href="#units">看全部單元</a><a class="btn ghost" href="/help">怎麼用</a></div>
<ul class="facts"><li><b>{total}</b> 章</li><li><b>{n_prob}</b> 題附解答</li><li><b>{n_sim}</b> 個互動模擬</li><li><b id="doneN">0</b> 章已讀完</li></ul>
<p class="muted small">進度只存在你這台裝置的瀏覽器裡，不上傳。</p>
</section>
<section class="sec" aria-labelledby="how"><h2 id="how">每一章都這樣走</h2>
<ol class="cards">
<li class="card"><span class="n">1</span><h3>讀講解</h3><p>先講直覺，再給公式。重點與容易犯的錯會用色塊標出來。</p></li>
<li class="card"><span class="n">2</span><h3>玩模擬</h3><p>拖動滑桿，看數字變了結果怎麼跟著變，比背公式更快有感覺。</p></li>
<li class="card"><span class="n">3</span><h3>做練習題</h3><p>輸入數字按「檢查」，卡住先看提示，最後再看完整解答。</p></li>
</ol></section>
<section class="sec" aria-labelledby="who"><h2 id="who">你現在是哪一種？</h2>
<ul class="cards">
<li><a class="card" href="/c/{first}"><h3>完全新手</h3><p>從力學第一章「單位與測量」開始，一章接一章最穩。</p></a></li>
<li><a class="card" href="#units"><h3>想補某一個單元</h3><p>直接從下面挑單元與章節；也可以用搜尋框打關鍵字。</p></a></li>
<li><a class="card" href="/help"><h3>第一次來，想先看操作</h3><p>三分鐘看完怎麼輸入答案、怎麼玩模擬、進度存在哪。</p></a></li>
</ul></section>
<div class="search"><label class="sr" for="q">搜尋章節</label><input id="q" type="search" placeholder="搜尋章節，例如：牛頓、電容、干涉" autocomplete="off"><p id="qn" class="muted" role="status"></p></div>
<ul class="jump" aria-label="跳到單元">{''.join(jumps)}</ul>
<div id="units" class="units">{''.join(cards)}</div>"""
    ld = {"@context": "https://schema.org", "@type": "Course", "name": "大學普通物理", "inLanguage": "zh-Hant",
          "description": "涵蓋力學、波、熱學、電磁、光學與近代物理的免費繁體中文自學課程",
          "isAccessibleForFree": True, "provider": {"@type": "Organization", "name": "鴻綸科技", "url": "https://hunglun.com"}}
    return shell(SITE, f"{total} 章免費大學普通物理，白話講解、互動模擬、附解答練習題，免註冊。", body, "/home", ver, ld, js="home")


def simple_page(title: str, desc: str, path: str, inner: str, ver: str) -> str:
    return shell(title, desc, f'<article class="doc"><h1>{esc(title)}</h1>{inner}</article>', path, ver)
