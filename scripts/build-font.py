"""產生自架中文字型子集 public/fonts/phys-sans-<包>-<雜湊>.woff2（Noto Sans TC，SIL OFL 1.1）。

做法與 lun-zoo 的 build-font.py 相同：拆包，瀏覽器靠 @font-face 的 unicode-range 只下載畫面上真的出現的字所在的那包。
  第 0 包＝首頁／說明頁／全部 JS（含模擬裡的文字）用到的字（每頁都會用到，會預先載入）
  之後＝各章講解與題目的字，依出現次數排，每包約 400 字
KaTeX 排出來的公式（.katex 裡面）用 KaTeX 自己的字型，不算進中文字型。
用法：
  python scripts/build-font.py          重新切字型並寫入 public/css/style.css 的 FONTS 區塊（之後要再跑一次 build.py 把預先載入標籤放進頁面）
  python scripts/build-font.py --check  檢查網站文字有沒有字不在任何一包裡（有就離場碼 1）
來源字型沿用 tools/web-design 的快取（~/.cache/web-design/fonts/），不用重新下載。
"""
import hashlib
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / "tools" / "web-design"))  # ClaudeOnly/tools/web-design（用相對位置，三台磁碟代號不同也能跑）
from webdesign import fonts  # noqa: E402

PUB = ROOT / "public"
FONTS = PUB / "fonts"
CSS = PUB / "css" / "style.css"
CHUNK = 400
EMOJI = re.compile("[←-⯿〰〽㊗㊙\U0001f000-\U0001faff️‍⃣]")
VOID = {"br", "img", "input", "meta", "link", "hr", "wbr", "source"}


class TextOnly(HTMLParser):
    """取出頁面文字，略過 .katex 整個子樹（公式用 KaTeX 的字型）與 <script type=application/ld+json> 以外的腳本標籤內容。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.skip_at = None
        self.out: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.depth += 1
        cls = dict(attrs).get("class") or ""
        if self.skip_at is None and "katex" in cls.split():
            self.skip_at = self.depth
        for k, v in attrs:  # placeholder、aria-label、alt 等也會顯示
            if k in ("placeholder", "aria-label", "alt", "title", "content") and v:
                self.out.append(v)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip_at is not None and self.depth == self.skip_at:
            self.skip_at = None
        self.depth -= 1

    def handle_data(self, data):
        if self.skip_at is None:
            self.out.append(data)


def page_text(path: Path) -> str:
    p = TextOnly()
    p.feed(path.read_text(encoding="utf-8"))
    return "".join(p.out)


def keep(text: str) -> set:
    return {c for c in text if ord(c) >= 0x20 and c not in "\r\n\t�" and not EMOJI.match(c)}


def groups():
    """回傳 (第 0 包的字集合, {章節頁: 字集合})。"""
    ui = ""
    for name in ("index", "home", "about", "help", "privacy"):
        f = PUB / f"{name}.html"
        if f.exists():
            ui += page_text(f)
    for f in (PUB / "js").rglob("*.js"):
        ui += f.read_text(encoding="utf-8")
    ui += CSS.read_text(encoding="utf-8").split("/* FONTS:END */")[-1]
    ui += "".join(chr(c) for c in range(0x20, 0x7F))
    chap = {f: page_text(f) for f in sorted((PUB / "c").glob("*.html"))}
    return keep(ui), chap


def chunks() -> list:
    first, chap = groups()
    freq: dict = {}
    for t in chap.values():
        for c in t:
            freq[c] = freq.get(c, 0) + 1
    rest = {c for t in chap.values() for c in keep(t)} - first
    ordered = sorted(rest, key=lambda c: (-freq.get(c, 0), c))
    packs = [ordered[i:i + CHUNK] for i in range(0, len(ordered), CHUNK)]
    if len(packs) > 1 and len(packs[-1]) < CHUNK // 4:
        last = packs.pop()  # 先 pop 再加：原本 packs[-2] += packs.pop() 在剩兩包時會索引超出範圍
        packs[-1] += last
    return ["".join(sorted(first))] + ["".join(sorted(p)) for p in packs]


def ranges(chars: str) -> str:
    cps = sorted({ord(c) for c in chars})
    parts, start = [], cps[0]
    for prev, cur in zip(cps, cps[1:] + [None]):
        if cur != prev + 1:
            parts.append(f"U+{start:X}" if start == prev else f"U+{start:X}-{prev:X}")
            start = cur
    return ",".join(parts)


def main() -> int:
    if "--check" in sys.argv:
        from fontTools.ttLib import TTFont

        cmap: set = set()
        for f in FONTS.glob("phys-sans-*.woff2"):
            cmap |= set(TTFont(f).getBestCmap())
        first, chap = groups()
        need = first | {c for t in chap.values() for c in keep(t)}
        missing = sorted(c for c in need if ord(c) not in cmap)
        print(f"字型 {len(list(FONTS.glob('phys-sans-*.woff2')))} 包共 {len(cmap)} 字；網站用到 {len(need)} 字；缺 {len(missing)} 字")
        if missing:
            print("缺字：", "".join(missing))
        return 1 if missing else 0

    FONTS.mkdir(parents=True, exist_ok=True)
    for old in FONTS.glob("phys-sans*.woff2"):
        old.unlink()
    faces, total = [], 0
    for i, chars in enumerate(chunks()):
        blob = fonts.subset_woff2("sans", chars)
        name = f"phys-sans-{i}-{hashlib.sha1(blob).hexdigest()[:8]}.woff2"
        (FONTS / name).write_bytes(blob)
        total += len(blob)
        faces.append('@font-face{font-family:"PhysSans";src:url("/fonts/%s") format("woff2");font-weight:400 800;font-display:swap;unicode-range:%s}' % (name, ranges(chars)))
        print(f"第 {i} 包：{len(chars)} 字，{len(blob) / 1024:.0f} KB → {name}")
    css = CSS.read_text(encoding="utf-8")
    a, b = css.index("/* FONTS:BEGIN"), css.index("/* FONTS:END */")
    CSS.write_text(css[:a] + "/* FONTS:BEGIN 由 scripts/build-font.py 產生，不要手改 */\n" + "\n".join(faces) + "\n" + css[b:], encoding="utf-8", newline="\n")
    lic = fonts.cache_dir() / "OFL-LICENSE.txt"
    if lic.exists():
        shutil.copy(lic, FONTS / "LICENSE-OFL.txt")
    print(f"共 {len(faces)} 包 {total / 1024:.0f} KB；已更新 style.css。接著重跑 scripts/build.py（會加上預先載入標籤與新的 ?v=）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
