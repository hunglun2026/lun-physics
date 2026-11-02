"""內容共用工具：章節與習題的資料結構、數字格式。

習題的答案一律由 Python 算出來（不是手打數字），解答文字用 f-string 帶入算出的值，
所以題目改了數字、答案跟著變；tests/test_content.py 還會用另一組獨立公式再算一次。
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

g = 9.8  # m/s²，全站統一
G = 6.674e-11
k_e = 8.988e9
eps0 = 8.854e-12
mu0 = 4e-7 * math.pi
c = 2.998e8
h = 6.626e-34
e = 1.602e-19
m_e = 9.109e-31
m_p = 1.673e-27
k_B = 1.381e-23
N_A = 6.022e23
R = 8.314
sigma = 5.670e-8
pi = math.pi
M_E = 5.972e24  # 地球質量 kg
R_E = 6.371e6  # 地球平均半徑 m
M_sun = 1.989e30
AU = 1.496e11


def sig(x, n: int = 3) -> str:
    """數字轉 LaTeX 片段（不含 $）：有效位數 n 位，很大很小用科學記號，整數不補 .0。"""
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    s = f"{x:.{n}g}"
    if "e" in s:
        m, ex = s.split("e")
        return f"{m}\\times10^{{{int(ex)}}}"
    return s


def T(x, n: int = 3) -> str:
    """行內公式用的數字：回傳 `$...$` 包好的字串。"""
    return f"${sig(x, n)}$"


def fill(text: str, **v) -> str:
    """把文字裡的 «名稱» 或 «名稱:位數» 換成算好的數字（LaTeX 片段，要放在 $...$ 裡）。"""
    def sub(m):
        name, _, n = m.group(1).partition(":")
        return sig(v[name], int(n) if n else 3)
    return re.sub(r"«([^»]+)»", sub, text)


def prob(q: str, ans: float, unit: str, steps: str, /, hint: str = "", tol: float = 0.02, **v) -> "Problem":
    """建一題：q、steps、hint 裡的 «x» 用 v 帶入，«ans» 是標準答案。"""
    if callable(ans):  # 答案可寫成 lambda **v：直接用題目顯示的數字算，不會打岔
        ans = ans(**v)
    shown = dict(v)
    v = {**v, "ans": ans}
    return Problem(fill(q, **v), float(ans), unit, fill(steps, **v), tol, fill(hint, **v), shown)


@dataclass
class Problem:
    q: str            # 題目（可含 $公式$）
    ans: float        # 標準答案（數值，SI 或題目指定單位）
    unit: str         # 顯示用單位（純文字，例 m/s、N·m）
    steps: str        # 解答步驟（可含 $公式$、換行 = 分段）
    tol: float = 0.02  # 相對誤差容許；ans 為 0 時用絕對誤差 0.02
    hint: str = ""
    vals: dict = field(default_factory=dict)  # 題目顯示用的數字（tests 用獨立公式從這裡重算答案）


@dataclass
class Chapter:
    id: str
    unit: str
    no: int
    title: str
    lead: str
    body: str
    problems: list[Problem] = field(default_factory=list)
    sims: list[str] = field(default_factory=list)
    refs: list[tuple[str, str]] = field(default_factory=list)  # (顯示文字, 外部延伸閱讀網址)


UNITS = [
    ("mechanics", "力學", "運動、力、能量、動量、轉動、重力、流體"),
    ("waves", "振動與波", "簡諧運動、波、聲音"),
    ("thermo", "熱學", "溫度、熱力學定律、氣體、熵"),
    ("em", "電磁學", "電場、電位、電路、磁場、感應、電磁波"),
    ("optics", "光學", "幾何光學、干涉、繞射"),
    ("modern", "近代物理", "相對論、量子、原子、原子核"),
]

REGISTRY: list[Chapter] = []


def add(ch: Chapter) -> Chapter:
    REGISTRY.append(ch)
    return ch
