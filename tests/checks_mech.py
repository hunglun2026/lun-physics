"""力學各章的獨立驗算：只看題目「顯示出來的數字」（Problem.vals），用跟內容檔不同的寫法重算答案。
每一題都必須有一條；沒有就測試失敗。公式刻意寫成另一種形式（例：能量法對照運動學）。"""
from math import atan, atan2, cos, degrees, hypot, pi, radians, sin, sqrt

G = 9.8
GC, ME, RE = 6.674e-11, 5.972e24, 6.371e6  # 萬有引力常數、地球質量、地球半徑（獨立再寫一份）

CHECKS = {
    "units-measure": [
        lambda v: v["v"] / 3.6,
        lambda v: v["d"] * 1e3,
        lambda v: float(f"{v['a'] * v['b']:.2g}"),
        lambda v: v["r"] * 60 * 24 * 365 * v["y"],
        lambda v: 2.998e8 * 3.156e7,
    ],
    "vectors": [
        lambda v: v["A"] * cos(radians(v["t"])),
        lambda v: sqrt((3 - 1) ** 2 + (4 + 2) ** 2),
        lambda v: degrees(atan(6 / 2)),
        lambda v: sum(a * b for a, b in zip((2, 3, 1), (4, -1, 2))),
        lambda v: v["A"] * v["B"] * sin(radians(v["t"])),
    ],
    "motion-1d": [
        lambda v: v["v"] / v["t"] * v["t"] ** 2 / 2,           # a=v/t，x=½at²
        lambda v: v["v0"] ** 2 / (2 * v["a"]),
        lambda v: sqrt(2 * v["h"] / G),
        lambda v: (v["v0"] / G) * v["v0"] / 2,                # 上升時間 v0/g，平均速度 v0/2
        lambda v: v["v"] / (v["a"] / 2),
    ],
    "motion-2d": [
        lambda v: 2 * (v["v0"] * cos(radians(v["t"]))) * (v["v0"] * sin(radians(v["t"]))) / G,
        lambda v: (v["v0"] * sin(radians(v["t"]))) ** 2 / (2 * G),
        lambda v: v["v"] * sqrt(2 * v["h"] / G),
        lambda v: (2 * pi / v["T"]) ** 2 * v["r"],
        lambda v: sqrt(v["vb"] ** 2 + v["vr"] ** 2),
    ],
    "newton-laws": [
        lambda v: v["m"] * v["a"],
        lambda v: sqrt(v["F1"] ** 2 + v["F2"] ** 2) / v["m"],
        lambda v: v["m"] * 1.62,
        lambda v: v["m"] * G + v["m"] * v["a"],
        lambda v: v["m2"] * (v["F"] / (v["m1"] + v["m2"])),
    ],
    "newton-apps": [
        lambda v: v["mu"] * v["m"] * G,
        lambda v: G * sin(radians(v["t"])) - v["mu"] * G * cos(radians(v["t"])),
        lambda v: sqrt(v["mu"] * G * v["r"]),
        lambda v: degrees(atan2(v["v"] ** 2, v["r"] * G)),
        lambda v: v["F"] * cos(radians(v["t"])) / v["m"],
    ],
    "work-energy": [
        lambda v: v["F"] * v["d"] * cos(radians(v["t"])),
        lambda v: v["m"] * v["v"] ** 2 / 2,
        lambda v: v["m"] / 2 * (v["v2"] - v["v1"]) * (v["v2"] + v["v1"]),
        lambda v: v["k"] * v["x"] * v["x"] / 2,
        lambda v: v["m"] * G * v["h"] / v["t"],
    ],
    "potential-energy": [
        lambda v: v["m"] * G * v["h"],
        lambda v: sqrt(2 * G * v["h"]),
        lambda v: sqrt(v["k"] * v["x"] ** 2 / v["m"]),
        lambda v: sqrt(2 * G * (v["L"] - v["L"] * cos(radians(v["t"])))),
        lambda v: v["m"] * G * v["h"] - v["m"] * v["v"] ** 2 / 2,
    ],
    "momentum": [
        lambda v: v["m"] * v["v"],
        lambda v: v["F"] * v["t"],
        lambda v: v["m1"] * v["v"] / (v["m1"] + v["m2"]),
        lambda v: v["v"] * (2 * v["m1"]) / (v["m1"] + v["m2"]),
        lambda v: v["m"] * v["v"] / v["M"],
    ],
    "rotation": [
        lambda v: v["n"] / 60 * 2 * pi,
        lambda v: (v["a"] * v["t"]) / 2 * v["t"],               # ω=αt，平均角速度 ω/2
        lambda v: v["M"] * v["R"] ** 2 / 2,
        lambda v: v["F"] * v["r"] / v["I"],
        lambda v: sqrt(2 * G * v["h"] / 1.5),                   # 動能係數 1+½ 對照 4gh/3
    ],
    "angular-momentum": [
        lambda v: v["I"] * v["w"],
        lambda v: v["I1"] * v["w1"] / v["I2"],
        lambda v: v["m"] * v["v"] * v["r"],
        lambda v: (v["tau"] / v["I"]) * v["t"],                 # α=τ/I，ω=αt
        lambda v: v["I"] * v["w"] / (v["I"] + v["m"] * v["r"] ** 2),
    ],
    "equilibrium": [
        lambda v: v["m1"] * v["d1"] / v["m2"],
        lambda v: (v["M"] + v["W"]) * G - ((v["M"] * G * v["L"] / 2 + v["W"] * G * (v["L"] - v["x"])) / v["L"]),  # 總重減去左端支撐力
        lambda v: v["m"] * G / (2 * cos(radians(90 - v["t"]))),
        lambda v: v["F"] * v["L"] / (v["A"] * 2.0e11) * 1000,
        lambda v: v["m2"] * v["x2"] / (v["m1"] + v["m2"]),
    ],
    "gravitation": [
        lambda v: GC * ME * v["m"] / RE ** 2,
        lambda v: GC * ME / (RE + v["h"] * 1e3) ** 2,
        lambda v: sqrt(GC * ME / (RE + v["h"] * 1e3)),
        lambda v: 2 * pi / sqrt(GC * ME / v["r"] ** 3) / 3600,  # 用角速度算週期
        lambda v: sqrt(2 * (GC * ME / RE ** 2) * RE),            # sqrt(2gR)
    ],
    "fluids": [
        lambda v: 1000 * G * v["h"],
        lambda v: v["F1"] * v["A2"] / v["A1"],
        lambda v: 1000 * G * v["a"] ** 3,
        lambda v: v["rho"] / 1000,
        lambda v: 0.5 * 1000 * ((v["v1"] * (v["d1"] / v["d2"]) ** 2) ** 2 - v["v1"] ** 2),
    ],
}
