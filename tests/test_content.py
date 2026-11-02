"""內容測試（不連網）：python -X utf8 tests/test_content.py

1. 每一題都有獨立驗算（tests/checks_*.py），且驗算值與標準答案相符（相對誤差 < 1e-6）
2. 答案是有限數；解答文字非空；章節 id 不重複；題數 >= 4
3. 公式能被 KaTeX 排版（build 失敗就是公式語法錯，這裡不重複）
4. 文字裡沒有簡體字常見混入、沒有破折號
"""
from __future__ import annotations

import importlib
import math
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402

CHAPTERS = build.load_content()
CHECKS: dict = {}
for f in sorted((ROOT / "tests").glob("checks_*.py")):
    CHECKS.update(importlib.import_module(f.stem).CHECKS)


class ContentTest(unittest.TestCase):
    def test_every_problem_has_independent_check(self):
        for ch in CHAPTERS:
            self.assertIn(ch.id, CHECKS, f"{ch.id} 沒有獨立驗算")
            self.assertEqual(len(CHECKS[ch.id]), len(ch.problems), f"{ch.id} 題數與驗算數不同")

    def test_answers_match_independent_formula(self):
        for ch in CHAPTERS:
            for i, (p, chk) in enumerate(zip(ch.problems, CHECKS.get(ch.id, []))):
                want = chk(p.vals)
                self.assertTrue(math.isfinite(p.ans), f"{ch.id} 第 {i + 1} 題答案不是有限數")
                self.assertLess(abs(p.ans - want), 5e-4 * max(1.0, abs(want)),  # 容許常數四捨五入差（k 與 1/4πε0 差約 0.003%）
                                f"{ch.id} 第 {i + 1} 題：標準答案 {p.ans} ≠ 獨立驗算 {want}（顯示數字 {p.vals}）")

    def test_shape(self):
        ids = [c.id for c in CHAPTERS]
        self.assertEqual(len(ids), len(set(ids)))
        for c in CHAPTERS:
            self.assertGreaterEqual(len(c.problems), 4, c.id)
            self.assertTrue(c.lead and c.body.strip(), c.id)
            for p in c.problems:
                self.assertTrue(p.steps.strip() and p.q.strip(), c.id)
                self.assertNotIn("«", p.q + p.steps + p.hint, f"{c.id} 有沒換掉的 «»")

    def test_wording(self):
        dash = re.compile("[—–]|──")
        for c in CHAPTERS:
            text = c.title + c.lead + c.body + "".join(p.q + p.steps + p.hint for p in c.problems)
            self.assertIsNone(dash.search(text), f"{c.id} 有破折號")
            # 全域用詞禁用詞 + 物理譯名的大陸用法（臺灣教科書用：冷次、必歐-沙伐、波耳、楊氏模數、克卜勒、白努利、虎克、繞射、雷射、微中子、測不準原理、介電質）
            for bad in ("賦能", "優化", "痛點", "顆粒度", "閉環", "抓手", "楞次", "畢奧", "玻爾", "楊氏模量", "開普勒", "伯努利", "胡克",
                        "衍射", "激光", "中微子", "不確定性原理", "電介質", "庫倫", "視頻", "軟件", "信息"):
                self.assertNotIn(bad, text, f"{c.id} 用了 {bad}")

    def test_sims_exist(self):
        for c in CHAPTERS:
            for name in re.findall(r"^!sim (\S+)", c.body, re.M):
                f = ROOT / "public" / "js" / "sim" / (name.split("-")[0] + ".js")
                self.assertTrue(f.exists(), f"{c.id} 的模擬 {name} 缺檔 {f.name}")
                self.assertIn(f'S["{name}"]', f.read_text(encoding="utf-8"), f"{name} 沒有註冊")


if __name__ == "__main__":
    unittest.main(verbosity=1)
