"""把章節內容的簡易標記轉成 HTML，並把 $公式$ 交給 KaTeX 排版。

標記（寫在 content/*.py 的 body 字串裡）：
  ## 小標            → h2
  空行分段            → p
  $$ ... $$          → 獨立一行的公式（可跨行）
  $ ... $            → 行內公式
  - 項目              → 清單（連續的 - 行）
  > 文字              → 提示框；>! 文字 → 警示框（常見錯誤）
  !sim 名稱           → 嵌入互動模擬（public/js/sim/名稱.js）
  **粗體**  `代碼`    → strong / code
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "math.json"
MATH = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)

_cache: dict[str, str] = {}
_pending: dict[str, tuple[str, bool]] = {}


def _key(tex: str, display: bool) -> str:
    return hashlib.sha1((("D" if display else "I") + tex).encode()).hexdigest()


def load_cache() -> None:
    if CACHE.exists():
        _cache.update(json.loads(CACHE.read_text(encoding="utf-8")))


def flush_math() -> None:
    """把這次新出現的公式一次丟給 Node 排版（每個公式失敗就整個建置失敗，不放過語法錯）。"""
    todo = [(k, v) for k, v in _pending.items() if k not in _cache]
    if todo:
        payload = json.dumps([{"tex": t, "display": d} for _, (t, d) in todo])
        p = subprocess.run(["node", str(ROOT / "scripts" / "mathrender.mjs")], input=payload.encode("utf-8"),
                           capture_output=True, cwd=ROOT)
        if p.returncode != 0:
            sys.exit("公式排版失敗：\n" + p.stderr.decode("utf-8", "replace"))
        for (k, _), out in zip(todo, json.loads(p.stdout.decode("utf-8"))):
            _cache[k] = out
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(_cache, ensure_ascii=False), encoding="utf-8")


def _stash(text: str) -> tuple[str, list[str]]:
    """先把公式換成佔位符，避免被 HTML 跳脫與粗體規則弄壞；回傳 (文字, 佔位符對應的 key)。"""
    keys: list[str] = []

    def sub(m: re.Match) -> str:
        display = m.group(1) is not None
        tex = (m.group(1) if display else m.group(2)).strip()
        k = _key(tex, display)
        _pending[k] = (tex, display)
        keys.append(k)
        return f"\x00{len(keys) - 1}\x00"

    return MATH.sub(sub, text), keys


def _unstash(text: str, keys: list[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: _cache[keys[int(m.group(1))]], text)


def inline(text: str) -> str:
    """行內文字：公式＋粗體＋代碼，回傳 HTML 片段（要等 flush_math 之後才能 finish）。"""
    s, keys = _stash(text)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    _frag.append((s, keys))
    return f"\x01{len(_frag) - 1}\x01"


# 兩階段：先登記所有文字（收集公式），flush_math 後再 finish 成最終 HTML
_frag: list[tuple[str, list[str]]] = []


def finish(htmlish: str) -> str:
    def sub(m: re.Match) -> str:
        s, keys = _frag[int(m.group(1))]
        return _unstash(s, keys)

    return re.sub(r"\x01(\d+)\x01", sub, htmlish)


def body_to_html(body: str, sim_title=lambda n: n) -> str:
    """回傳含佔位符的 HTML，要經過 finish() 才完整。"""
    out: list[str] = []
    lines = body.strip("\n").split("\n")
    i = 0
    para: list[str] = []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush_para(); i += 1; continue
        if ln.startswith("$$"):  # 公式區塊：到下一個含 $$ 的行為止
            flush_para()
            buf = [ln]
            while buf[0].count("$$") < 2 and not any("$$" in b for b in buf[1:]):  # 單行 $$..$$ 直接收；否則收到下一個含 $$ 的行
                i += 1; buf.append(lines[i])
            out.append('<div class="eq">' + inline("\n".join(buf)) + "</div>")
            i += 1; continue
        if ln.startswith("## "):
            flush_para(); out.append("<h2>" + inline(ln[3:]) + "</h2>"); i += 1; continue
        if ln.startswith("!sim "):
            flush_para(); name = ln[5:].strip()
            out.append(f'<figure class="sim" data-sim="{html.escape(name)}"><div class="simbox" aria-live="polite">'
                       f'<noscript>這個互動模擬需要開啟 JavaScript。</noscript></div></figure>')
            i += 1; continue
        if ln.startswith("- "):
            flush_para(); items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("<li>" + inline(lines[i][2:]) + "</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if ln.startswith(">"):
            flush_para(); warn = ln.startswith(">!"); buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">!").strip()); i += 1
            cls = "warn" if warn else "tip"
            label = "常見錯誤" if warn else "重點"
            out.append(f'<aside class="{cls}"><b>{label}</b><p>' + inline(" ".join(buf)) + "</p></aside>")
            continue
        para.append(ln.strip()); i += 1
    flush_para()
    return "\n".join(out)
