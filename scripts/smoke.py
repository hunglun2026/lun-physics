"""冒煙測試：用無頭 Chromium 真的走一遍使用者會做的事（本機伺服器會套用 public/_headers，所以 CSP 擋到東西會變成錯誤）。

檢查：每頁（桌機 1280／手機 390）的 JS 錯誤與 CSP 違規、失敗請求、橫向溢出、壞圖；
      章節頁：互動模擬有畫出來、答對／答錯的回饋、進度寫入 localStorage、首頁顯示已讀、回報對話框能開、公式有排版。
用法：python -X utf8 scripts/smoke.py [--only 章節id] [--shots 資料夾]
離場碼：0 全過｜1 有問題
"""
from __future__ import annotations

import functools
import http.server
import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"


def header_rules() -> list[tuple[str, dict]]:
    rules, cur = [], None
    for ln in (PUB / "_headers").read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if not ln.startswith((" ", "\t")):
            cur = (ln.strip(), {}); rules.append(cur)
        else:
            k, _, v = ln.strip().partition(":"); cur[1][k.strip()] = v.strip()
    return rules


class Handler(http.server.SimpleHTTPRequestHandler):
    rules = header_rules()

    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0]
        if p.endswith("/"):
            p += "index.html"
        elif "." not in p.rsplit("/", 1)[-1]:
            p += ".html"
        return str(PUB / p.lstrip("/"))

    def end_headers(self):
        path = self.path.split("?")[0]
        for pat, hs in self.rules:
            if pat == "/*" or (pat.endswith("/*") and path.startswith(pat[:-1])):
                for k, v in hs.items():
                    self.send_header(k, v)
        super().end_headers()

    def do_POST(self):  # /report 在本機回成功（Worker 另外測）
        self.send_response(200); self.send_header("content-type", "application/json"); self.end_headers(); self.wfile.write(b'{"ok":true}')

    def log_message(self, *a):
        pass


def serve() -> tuple[http.server.ThreadingHTTPServer, str]:
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def main() -> int:
    from playwright.sync_api import sync_playwright

    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    chapters = json.loads((PUB / "data" / "chapters.json").read_text(encoding="utf-8"))
    pages = ["/", "/help", "/about", "/privacy"] + [f"/c/{c['id']}" for c in chapters if not only or c["id"] == only]
    srv, base = serve()
    bad: list[str] = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for vname, vp in (("桌機", {"width": 1280, "height": 800}), ("手機", {"width": 390, "height": 844})):
            ctx = br.new_context(viewport=vp)
            for path in pages:
                pg = ctx.new_page(); errs: list[str] = []
                pg.on("console", lambda m, e=errs: e.append("console:" + m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda x, e=errs: e.append("pageerror:" + str(x)))
                pg.on("requestfailed", lambda r, e=errs: e.append("requestfailed:" + r.url[-60:]))
                pg.on("response", lambda r, e=errs: e.append(f"http{r.status}:" + r.url[-60:]) if r.status >= 400 else None)
                pg.goto(base + path, wait_until="networkidle")
                if path.startswith("/c/"):
                    pg.wait_for_timeout(400)
                    n_sim = pg.locator("figure.sim").count()
                    if n_sim and pg.locator("figure.sim canvas").count() != n_sim:
                        errs.append(f"模擬沒畫出來（{pg.locator('figure.sim canvas').count()}/{n_sim}）")
                    if pg.locator(".katex").count() == 0:
                        errs.append("沒有公式被排版")
                    if pg.locator(".katex-error").count():
                        errs.append("公式排版錯誤")
                m = pg.evaluate("() => ({ov: document.documentElement.scrollWidth > innerWidth + 2, bi: [...document.images].filter(i=>i.complete&&i.naturalWidth===0).length})")
                if m["ov"]:
                    errs.append("橫向溢出")
                if m["bi"]:
                    errs.append("壞圖")
                if shots and vname == "桌機" and (path in ("/", "/c/motion-2d") or only):
                    pg.screenshot(path=str(shots / ((path.strip("/").replace("/", "_") or "home") + f"-{vname}.png")), full_page=True)
                if errs:
                    bad.append(f"{vname} {path}: " + "; ".join(errs[:4]))
                pg.close()
            ctx.close()

        # 功能流程（桌機）：答題 → 進度 → 首頁已讀 → 回報對話框
        ctx = br.new_context(viewport={"width": 1280, "height": 800}); pg = ctx.new_page()
        pg.goto(base + "/", wait_until="networkidle"); pg.wait_for_timeout(300)
        nfont = pg.evaluate("() => [...document.fonts].filter(f => f.family.includes('PhysSans') && f.status === 'loaded').length")
        if nfont < 1:
            bad.append("功能：自架中文字型 PhysSans 沒有載入（會退回系統字型）")
        first = chapters[0]["id"] if not only else only
        pg.goto(f"{base}/c/{first}", wait_until="networkidle")
        prob = pg.locator(".prob").first
        ans = float(prob.get_attribute("data-ans"))
        prob.locator(".ans").fill(str(ans * 1.5 if ans else 99)); prob.locator("[data-act=check]").click()
        if "ok" in (prob.locator(".res").get_attribute("class") or ""):
            bad.append("功能：錯誤答案被判對")
        prob.locator(".ans").fill(repr(ans)); prob.locator("[data-act=check]").click()
        if "答對" not in prob.locator(".res").inner_text():
            bad.append("功能：標準答案沒被判對")
        saved = pg.evaluate("() => JSON.parse(localStorage.getItem('phys.progress.v1')||'{}')")
        if first not in saved or 0 not in saved[first].get("solved", []):
            bad.append("功能：答對沒有寫進進度")
        pg.locator("#doneBtn").click()
        pg.goto(base + "/", wait_until="networkidle")
        if not pg.locator(f"a[data-ch={first}].done").count():
            bad.append("功能：首頁沒顯示已讀")
        pg.goto(f"{base}/c/{first}", wait_until="networkidle")
        pg.locator("[data-report]").first.click()
        if not pg.locator("#reportDlg").evaluate("d => d.open"):
            bad.append("功能：回報對話框沒開")
        pg.locator("#reportText").fill("測試回報，請忽略"); pg.locator("#reportSend").click(); pg.wait_for_timeout(300)
        if "已收到" not in pg.locator("#reportMsg").inner_text():
            bad.append("功能：回報送出沒成功訊息")
        br.close()
    srv.shutdown()
    print(f"檢查 {len(pages)} 頁 × 桌機／手機 + 功能流程")
    for b in bad:
        print("  ✗", b)
    print("全部通過" if not bad else f"{len(bad)} 項問題")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
