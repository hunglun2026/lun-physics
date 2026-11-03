"""無障礙檢查（axe-core，WCAG 2.1 AA＋best-practice）：全站每頁 × 淺色／深色，用本機伺服器，bypass_csp 只為了注入 axe。
axe.min.js 借官網專案的那份（company/hunglun2026/sitemap/axe.min.js，用相對位置找）。有違規離場碼 1。
用法：python -X utf8 scripts/a11y.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import smoke  # noqa: E402

AXE = ROOT.parent.parent / "company" / "hunglun2026" / "sitemap" / "axe.min.js"


def main() -> int:
    from playwright.sync_api import sync_playwright

    if not AXE.exists():
        print("找不到 axe.min.js（官網專案的 sitemap/axe.min.js），略過", file=sys.stderr)
        return 0
    axe = AXE.read_text(encoding="utf-8")
    ids = [c["id"] for c in json.loads((ROOT / "public/data/chapters.json").read_text(encoding="utf-8"))]
    pages = ["/", "/about", "/help", "/privacy"] + [f"/c/{i}" for i in ids]
    srv, base = smoke.serve()
    bad: dict = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for scheme in ("light", "dark"):
            pg = br.new_context(viewport={"width": 1280, "height": 900}, color_scheme=scheme, bypass_csp=True).new_page()
            for u in pages:
                pg.goto(base + u, wait_until="load")
                pg.wait_for_timeout(250)
                pg.add_script_tag(content=axe)
                r = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa','best-practice']})")
                for v in r["violations"]:
                    bad.setdefault((v["id"], v["impact"]), []).append(f"{scheme}{u}: " + v["nodes"][0]["html"][:60])
        br.close()
    srv.shutdown()
    print(f"axe 檢查 {len(pages)} 頁 × 淺色／深色：", "0 項違規" if not bad else f"{len(bad)} 類違規")
    for k, w in bad.items():
        print(" ", k, len(w), w[:3])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
