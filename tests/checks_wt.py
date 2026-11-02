"""振動與波、熱學的獨立驗算（只看題目顯示的數字，用不同寫法重算）。"""
from math import log, log10, pi, sqrt

G = 9.8
R = 8.314

CHECKS = {
    "shm": [
        lambda v: 2 * pi / sqrt(v["k"] / v["m"]),
        lambda v: 2 * pi / sqrt(G / v["L"]),
        lambda v: v["A"] * sqrt(v["k"] / v["m"]),
        lambda v: v["k"] * v["A"] ** 2 / 2,
        lambda v: sqrt((v["k"] * v["A"] ** 2 / 2 - v["k"] * v["x"] ** 2 / 2) * 2 / v["m"]),  # 用能量差反推速率
    ],
    "waves": [
        lambda v: v["f"] * v["lam"],
        lambda v: sqrt(v["T"] / v["mu"]),
        lambda v: v["v"] / (2 * v["L"]),
        lambda v: 2 * pi / v["lam"],
        lambda v: 3 * (v["v"] / (2 * v["L"])),
    ],
    "sound": [
        lambda v: 331 + 0.6 * v["T"],
        lambda v: 10 * log10(v["I"] / 1e-12),
        lambda v: v["f"] / (1 - v["vs"] / v["v"]),
        lambda v: abs(v["f1"] - v["f2"]),
        lambda v: v["v"] / (2 * v["L"]),
    ],
    "temperature-heat": [
        lambda v: v["T"] + 273.15,
        lambda v: 1.2e-5 * v["L"] * v["dT"] * 1000,
        lambda v: v["m"] * 4186 * (v["T2"] - v["T1"]),
        lambda v: v["m"] * 3.34e5,
        lambda v: v["T1"] - v["m2"] * (v["T1"] - v["T2"]) / (v["m1"] + v["m2"]),
    ],
    "first-law": [
        lambda v: v["n"] * R * v["T"] / v["V"],
        lambda v: v["P"] * v["dV"],
        lambda v: v["Q"] - v["W"],
        lambda v: v["n"] * R * v["T"] * log(v["r"]),
        lambda v: v["n"] * (3 / 2 * R) * v["dT"],
    ],
    "kinetic-theory": [
        lambda v: 3 / 2 * 1.381e-23 * v["T"],
        lambda v: sqrt(3 * R * v["T"] / 0.028),
        lambda v: sqrt(3 * R * v["T"] / 0.004),
        lambda v: 3 / 2 * v["n"] * R * v["T"],
        lambda v: 5 / 2 * R,
    ],
    "second-law": [
        lambda v: (v["QH"] - v["QC"]) / v["QH"],
        lambda v: (v["TH"] - v["TC"]) / v["TH"],
        lambda v: v["QH"] * (v["TH"] - v["TC"]) / v["TH"],
        lambda v: v["m"] * 3.34e5 / 273.15,
        lambda v: v["TC"] / (v["TH"] - v["TC"]),
    ],
}
