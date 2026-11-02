"""電磁學的獨立驗算（只看題目顯示的數字，常數另外抄一份、用不同寫法重算）。"""
from math import cos, exp, hypot, pi, radians, sqrt

K, E0, QE, ME, GG = 8.988e9, 8.854e-12, 1.602e-19, 9.109e-31, 6.674e-11
MU0 = 4e-7 * pi

CHECKS = {
    "charge-coulomb": [
        lambda v: K * v["q1"] * v["q2"] * 1e-12 / v["r"] ** 2,
        lambda v: v["q"] * 1e-6 / QE,
        lambda v: K * QE ** 2 / (5.29e-11) ** 2,
        lambda v: (K / GG) * (QE / ME) ** 2,
        lambda v: K * v["q"] * v["Q"] * 1e-12 * (1 / v["x"] ** 2 - 1 / (v["d"] - v["x"]) ** 2),
    ],
    "electric-field": [
        lambda v: K * v["q"] * 1e-9 / v["r"] ** 2,
        lambda v: QE * v["E"],
        lambda v: QE * v["E"] / ME,
        lambda v: 2 * K * v["q"] * 1e-6 / (v["d"] / 2) ** 2,
        lambda v: K * v["Q"] * 1e-9 * v["x"] / (v["a"] ** 2 + v["x"] ** 2) ** 1.5,
    ],
    "gauss": [
        lambda v: v["Q"] * 1e-9 / E0,
        lambda v: v["s"] * 1e-6 / (2 * E0),
        lambda v: v["l"] * 1e-9 / (2 * pi * E0 * v["r"]),
        lambda v: v["Q"] * 1e-9 / (4 * pi * E0 * v["R"] ** 2),
        lambda v: v["Q"] * 1e-9 * (v["r"] / v["R"]) ** 3 / (4 * pi * E0 * v["r"] ** 2),   # 高斯面內只包圍一部分電荷
    ],
    "potential": [
        lambda v: v["q"] * 1e-9 / (4 * pi * E0 * v["r"]),
        lambda v: v["q"] * 1e-6 * v["dV"],
        lambda v: sqrt(2 * QE * v["V"] / ME),
        lambda v: v["E"] * v["d"],
        lambda v: v["q1"] * 1e-6 * (-v["q2"] * 1e-6) / (4 * pi * E0 * v["r"]),
    ],
    "capacitance": [
        lambda v: E0 * v["A"] / (v["d"] * 1e-3) * 1e12,
        lambda v: v["C"] * v["V"],
        lambda v: (v["C"] * 1e-6 * v["V"]) ** 2 / (2 * v["C"] * 1e-6),   # Q²/2C
        lambda v: v["C1"] * v["C2"] / (v["C1"] + v["C2"]),
        lambda v: v["V"] / v["k"],
    ],
    "current-resistance": [
        lambda v: v["I"] * v["t"] * 60,
        lambda v: 1.68e-8 * v["L"] / v["A"],
        lambda v: v["V"] / v["R"],
        lambda v: (v["V"] / v["R"]) * v["V"],    # 先算電流再 P=IV
        lambda v: v["P"] * v["t"],
    ],
    "dc-circuits": [
        lambda v: v["V"] / (v["R1"] + v["R2"]),
        lambda v: 1 / (1 / v["R1"] + 1 / v["R2"]),
        lambda v: v["E"] * v["R"] / (v["R"] + v["r"]),
        lambda v: (v["E"] / (v["R1"] + 1 / (1 / v["R2"] + 1 / v["R3"]))) * v["R3"] / (v["R2"] + v["R3"]),   # 電流分配
        lambda v: v["E"] * (1 - exp(-(v["R"] * 1e3 * v["C"] * 1e-6) / (v["R"] * 1e3 * v["C"] * 1e-6))),
    ],
    "magnetic-force": [
        lambda v: QE * v["v"] * v["B"],
        lambda v: v["v"] / (QE * v["B"] / ME) * 100,            # r = v/ω，ω=qB/m
        lambda v: v["I"] * v["L"] * v["B"],
        lambda v: (QE * v["B"] / 1.673e-27) / (2 * pi),
        lambda v: v["N"] * v["I"] * v["A"] * v["B"],
    ],
    "magnetic-sources": [
        lambda v: 2e-7 * v["I"] / v["r"],
        lambda v: 2e-7 * pi * v["N"] * v["I"] / v["R"],
        lambda v: 4e-7 * pi * v["n"] * v["I"],
        lambda v: 2e-7 * v["I1"] * v["I2"] / v["d"],
        lambda v: 2 * 2e-7 * v["I"] / (v["d"] / 2),
    ],
    "induction": [
        lambda v: v["B"] * v["A"] * cos(radians(v["t"])),
        lambda v: v["N"] * v["f1"] / v["dt"],
        lambda v: v["B"] * v["L"] * v["v"],
        lambda v: (v["B"] * v["L"] * v["v"] / v["R"]) * v["B"] * v["L"],
        lambda v: v["N"] * v["B"] * v["A"] * v["w"],
    ],
    "inductance": [
        lambda v: v["L"] * v["r"],
        lambda v: v["L"] * v["I"] * v["I"] / 2,
        lambda v: v["L"] / v["R"] * 1000,
        lambda v: (1 / sqrt(v["L"] * 1e-3 * v["C"] * 1e-9)) / (2 * pi),
        lambda v: MU0 * v["N"] ** 2 * v["A"] / v["l"] * 1000,
    ],
    "ac-circuits": [
        lambda v: v["Vm"] * 0.7071067811865476,
        lambda v: 2 * pi * v["f"] * v["L"],
        lambda v: 1 / (2 * pi * v["f"] * v["C"] * 1e-6),
        lambda v: hypot(v["R"], v["XL"] - v["XC"]),
        lambda v: (1 / sqrt(v["L"] * v["C"] * 1e-6)) / (2 * pi),
    ],
    "em-waves": [
        lambda v: 2.998e8,
        lambda v: 2.998e8 / (v["f"] * 1e6),
        lambda v: v["E0"] / 2.998e8,
        lambda v: v["E0"] ** 2 / (2 * MU0 * 2.998e8),           # 用 μ0 寫的等價式
        lambda v: v["I0"] * cos(radians(v["t"])) ** 2,
    ],
}
