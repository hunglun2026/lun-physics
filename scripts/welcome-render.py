"""產生歡迎頁（public/index.html 與 css/welcome*.css、js/welcome.js），用全系列共用的產生器 supereduweb/runner/welcome.py。

設定在 project.yaml 的「歡迎頁」區塊。結果提交進 public/；CI 只跑 build.py，不跑這支（公開 repo 沒有 supereduweb），
所以 build.py 不碰歡迎頁的檔案，改歡迎頁內容或字型後要跑 scripts/make.py 重產。
用法：python -X utf8 scripts/welcome-render.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT.parent / "supereduweb" / "runner"))

import build  # noqa: E402
import engine as E  # noqa: E402
import welcome as W  # noqa: E402


def main() -> int:
    conf = E.load_yaml(ROOT / "project.yaml")
    conf["網域"] = conf.get("網域") or "physics.hunglun.com"
    res = W.render(ROOT, conf, [], "physics", v=build.asset_version())
    print("歡迎頁已產生：" + "、".join(res["wrote"]))
    if res["missing_logo"]:
        print(f"找不到 logo：{res['settings']['logo']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
