"""產生整個網站：content/*.py → public/*.html、sitemap、llms.txt、data/chapters.json。

用法：python -X utf8 scripts/build.py
  - 公式用 Node 的 KaTeX 排版（建置時），網站只載入 KaTeX 的 CSS 與字型
  - CSS／JS 的 ?v= 用檔案內容雜湊，內容一變網址就變，不用手動升版
"""
from __future__ import annotations

import hashlib
import importlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import pages as P  # noqa: E402
import render as R  # noqa: E402
from content import _lib as L  # noqa: E402

PUB = ROOT / "public"
# 每章的「延伸閱讀」：只放外部連結，不收錄對方內容（OpenStax 是 CC BY-NC-SA 且禁止 AI 攝取，本站內容全是原創，沒有用它）。
UNIT_REFS = {
    "mechanics": ("OpenStax University Physics 第 1 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-1/pages/preface"),
    "waves": ("OpenStax University Physics 第 1 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-1/pages/preface"),
    "thermo": ("OpenStax University Physics 第 2 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-2/pages/preface"),
    "em": ("OpenStax University Physics 第 2 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-2/pages/preface"),
    "optics": ("OpenStax University Physics 第 3 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-3/pages/preface"),
    "modern": ("OpenStax University Physics 第 3 冊（英文、免費）", "https://openstax.org/books/university-physics-volume-3/pages/preface"),
}


def load_content() -> list[L.Chapter]:
    for f in sorted((ROOT / "content").glob("[a-z]*.py")):  # _lib.py 不載入
        importlib.import_module(f"content.{f.stem}")
    order = {u[0]: i for i, u in enumerate(L.UNITS)}
    chs = sorted(L.REGISTRY, key=lambda c: (order[c.unit], c.no))
    ids = [c.id for c in chs]
    assert len(ids) == len(set(ids)), "章節 id 重複"
    for i, c in enumerate(chs, 1):
        c.no = i  # 全站連續編號
    return chs


def asset_version() -> str:
    h = hashlib.sha1()
    for f in sorted(list((PUB / "css").glob("*.css")) + list((PUB / "js").rglob("*.js"))):
        h.update(f.read_bytes())
    return h.hexdigest()[:8]


def copy_katex() -> None:
    """KaTeX 的 CSS 與 woff2 字型複製到 public（舊格式 woff／ttf 不要，現代瀏覽器都吃 woff2）。"""
    src = ROOT / "node_modules" / "katex" / "dist"
    out = PUB / "fonts" / "katex"
    out.mkdir(parents=True, exist_ok=True)
    for f in (src / "fonts").glob("*.woff2"):
        shutil.copy(f, out / f.name)
    css = (src / "katex.min.css").read_text(encoding="utf-8")
    css = re.sub(r",url\(fonts/[^)]+\.(?:woff|ttf)\) format\(\"(?:woff|truetype)\"\)", "", css)
    css = css.replace("url(fonts/", "url(/fonts/katex/")
    (PUB / "css" / "katex.css").write_text(css, encoding="utf-8", newline="\n")


def collect(chs: list[L.Chapter]):
    """第一階段：登記所有文字（收集公式）。"""
    rendered = {}
    for c in chs:
        body = R.body_to_html(c.body)
        probs = []
        for i, p in enumerate(c.problems):
            probs.append((R.inline(p.q), R.body_to_html(p.steps)))
        refs = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in (c.refs or [UNIT_REFS[c.unit]]))
        rendered[c.id] = (body, probs, refs)
    return rendered


def main() -> int:
    R.load_cache()
    chs = load_content()
    copy_katex()
    first = sorted((PUB / "fonts").glob("phys-sans-0-*.woff2"))
    P.PRELOAD = f'<link rel="preload" as="font" type="font/woff2" href="/fonts/{first[0].name}" crossorigin>' if first else ""
    rendered = collect(chs)
    static = {
        "about": P_about(), "help": P_help(), "privacy": P_privacy(),
    }
    R.flush_math()
    ver = asset_version()
    by_unit: dict[str, list] = {}
    for c in chs:
        by_unit.setdefault(c.unit, []).append(c)
    uname = {u[0]: u[1] for u in L.UNITS}

    (PUB / "c").mkdir(exist_ok=True)
    for old in (PUB / "c").glob("*.html"):
        old.unlink()
    for i, c in enumerate(chs):
        body, probs, refs = rendered[c.id]
        ph = "".join(P.problem_html(k, p, R.finish(q), R.finish(s)) for k, (p, (q, s)) in enumerate(zip(c.problems, probs)))
        refs_html = (f'<section class="refs"><h2>延伸閱讀</h2><p class="muted">以下是外部網站的連結，內容不收錄在本站。</p><ul>{refs}</ul></section>' if refs else "")
        prev = chs[i - 1] if i else None
        nxt = chs[i + 1] if i + 1 < len(chs) else None
        page = P.chapter_page(c, uname[c.unit], R.finish(body), ph, prev, nxt, refs_html, ver)
        (PUB / "c" / f"{c.id}.html").write_text(page, encoding="utf-8", newline="\n")

    (PUB / "index.html").write_text(P.home_page(L.UNITS, by_unit, len(chs), ver), encoding="utf-8", newline="\n")
    for name, (title, desc, inner) in static.items():
        (PUB / f"{name}.html").write_text(P.simple_page(title, desc, f"/{name}", R.finish(inner), ver), encoding="utf-8", newline="\n")

    (PUB / "data").mkdir(exist_ok=True)
    index = [{"id": c.id, "no": c.no, "unit": c.unit, "title": c.title, "lead": c.lead, "n": len(c.problems)} for c in chs]
    (PUB / "data" / "chapters.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")

    urls = ["/", "/help", "/about", "/privacy"] + [f"/c/{c.id}" for c in chs]
    sm = "".join(f"<url><loc>{P.URL}{u}</loc></url>" for u in urls)  # 不放 lastmod：每天不同會讓 CI 的「public 與原始內容一致」檢查失敗
    (PUB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8", newline="\n")
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {P.URL}/sitemap.xml\n", encoding="utf-8", newline="\n")
    llms = [f"# 普通物理\n\n> 免費、免註冊的繁體中文大學普通物理自學站，{len(chs)} 章，每章有講解、互動模擬與附解答的練習題。\n"]
    for uid, un, ud in L.UNITS:
        if uid in by_unit:
            llms.append(f"\n## {un}\n" + "".join(f"- [{c.title}]({P.URL}/c/{c.id}): {c.lead}\n" for c in by_unit[uid]))
    (PUB / "llms.txt").write_text("".join(llms), encoding="utf-8", newline="\n")
    n_prob = sum(len(c.problems) for c in chs)
    print(f"完成：{len(chs)} 章、{n_prob} 題、?v={ver}")
    return 0


# 靜態說明頁（內容短，放在這裡；回傳 (標題, 描述, 內文 HTML 含佔位符)）
def P_about():
    return ("授權與出處", "本站內容的授權、資料來源與外部連結說明。", R.body_to_html("""
## 本站內容

講解、例題與練習題由本站原創撰寫，不改寫自任何受授權限制的教科書。物理定律與公式本身是科學事實；數值常數取自 CODATA 與 NIST 公布的推薦值。

## 練習題怎麼確保答案對

每一題的答案都是由程式用題目的數字算出來的，不是手打。另外有一組獨立的測試，只看題目顯示的數字，用不同的公式寫法再算一次，兩邊不一致就不能發布。測試只能抓到「題目與答案對不上」和「算式寫錯」，抓不到「觀念講錯」，所以仍歡迎你回報。

## 外部連結

「延伸閱讀」會連到其他網站（例如 OpenStax）。這些只是連結，本站沒有收錄、改寫或參考它們的內容，它們的授權條款以各自網站為準。

## 回報錯誤

每一頁下方都有「回報錯誤」，不需要姓名與聯絡方式。

## 製作

鴻綸科技　hunglun.com"""))


def P_help():
    return ("怎麼用", "章節結構、練習題輸入方式、進度儲存方式。", R.body_to_html("""
## 每一章的結構

- 白話講解，先講直覺再講公式
- 互動模擬：拖動滑桿，看數字怎麼影響結果
- 練習題：輸入數值答案按「檢查」，系統容許約 2% 的誤差
- 提示與解答：卡住先看提示，最後再看解答

## 輸入答案

直接輸入數字就好，不用寫單位，單位已經顯示在輸入框旁邊。很大或很小的數可以用科學記號，例如 `3.2e5` 代表 $3.2\\times10^5$。

## 進度

「標記這章讀完」和答對的題目，只存在你這台裝置的瀏覽器裡，不會上傳。換裝置或清除瀏覽器資料就會歸零。

## 單位與常數

全站重力加速度取 $g = 9.8\\ \\mathrm{m/s^2}$，其他常數用 CODATA 推薦值，並在題目裡寫明。"""))


def P_privacy():
    return ("隱私", "本站不收集個人資料。", R.body_to_html("""
## 我們收集什麼

沒有帳號、沒有追蹤廣告。學習進度只存在你的瀏覽器本機。

## 回報錯誤

你送出的回報只包含你寫的說明和當時的頁面網址，不含姓名、聯絡方式。為了擋大量灌送，伺服器會短暫記錄來源連線的送出次數，十分鐘後自動消失。"""))


if __name__ == "__main__":
    sys.exit(main())
