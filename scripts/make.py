"""一鍵重建並驗證：建置 → 歡迎頁 → 切字型 → 歡迎頁 → 再建置（加預先載入）→ 歡迎頁 → 缺字檢查 → 簡體字掃描 → 內容測試 → 冒煙測試。
用法：python -X utf8 scripts/make.py [--no-smoke]
任何一步失敗就停下，離場碼 1。發布前一定要跑到全綠。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable, "-X", "utf8"]
STEPS = [
    ("建置", ["scripts/build.py"]),
    ("歡迎頁（第一次，字型切分要看它的字）", ["scripts/welcome-render.py"]),
    ("切字型", ["scripts/build-font.py"]),
    ("歡迎頁（字型更新後）", ["scripts/welcome-render.py"]),
    ("再建置（字型預先載入）", ["scripts/build.py"]),
    ("歡迎頁（帶最終 ?v=）", ["scripts/welcome-render.py"]),
    ("字型缺字檢查", ["scripts/build-font.py", "--check"]),
    ("簡體字掃描", ["scripts/check-simplified.py"]),
    ("內容驗算測試", ["tests/test_content.py"]),
]
if "--no-smoke" not in sys.argv:
    STEPS.append(("冒煙測試（真瀏覽器）", ["scripts/smoke.py"]))
    STEPS.append(("無障礙 axe（淺色與深色）", ["scripts/a11y.py"]))

for name, args in STEPS:
    print(f"\n== {name}")
    r = subprocess.run(PY + args, cwd=ROOT)
    if r.returncode:
        print(f"\n✗ 「{name}」失敗，停止")
        sys.exit(1)
print("\n全部通過")
