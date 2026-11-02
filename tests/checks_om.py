"""光學與近代物理的獨立驗算（只看題目顯示的數字，用不同寫法重算）。"""
from math import asin, degrees, floor, log, pi, radians, sin, sqrt

HC = 1239.84  # eV·nm


def gam(b):
    return 1 / sqrt(1 - b * b)


CHECKS = {
    "geometric-optics": [
        lambda v: degrees(asin(sin(radians(v["t1"])) / v["n"])),
        lambda v: degrees(asin(1 / v["n"])),
        lambda v: v["f"] * v["do"] / (v["do"] - v["f"]) * 100,
        lambda v: -v["f"] / (v["do"] - v["f"]),
        lambda v: (v["R"] / 2) * v["do"] / (v["do"] - v["R"] / 2) * 100,
    ],
    "interference": [
        lambda v: v["lam"] * 1e-9 * v["L"] / (v["d"] * 1e-3) * 1e3,
        lambda v: degrees(asin(v["m"] * v["lam"] * 1e-9 / (v["d"] * 1e-3))),
        lambda v: v["d"] * 1e-3 * v["dy"] * 1e-3 / v["L"] * 1e9,
        lambda v: v["lam"] / (4 * v["n"]),
        lambda v: 2 * pi * v["D"] / v["lam"],
    ],
    "diffraction": [
        lambda v: 2 * v["lam"] * 1e-9 * v["L"] / (v["a"] * 1e-3) * 1e3,
        lambda v: degrees(asin(v["lam"] * 1e-9 * v["N"] * 1e3)),
        lambda v: floor((1 / (v["N"] * 1e3)) / (v["lam"] * 1e-9)),
        lambda v: 1.22 * v["lam"] * 1e-9 / v["D"],
        lambda v: degrees(asin(v["lam"] / (2 * v["d"]))),
    ],
    "relativity": [
        lambda v: gam(v["b"]),
        lambda v: v["t0"] * gam(v["b"]),
        lambda v: v["L0"] / gam(v["b"]),
        lambda v: 9.109e-31 * (2.998e8) ** 2 / 1.602e-19 / 1e6,
        lambda v: (gam(v["b"]) - 1) * 0.511,
    ],
    "photons": [
        lambda v: HC / v["lam"],
        lambda v: HC / v["lam"] - v["phi"],
        lambda v: HC / v["phi"],
        lambda v: 6.626e-34 / (v["lam"] * 1e-9),
        lambda v: 2.898e-3 / v["T"] * 1e9,
    ],
    "matter-waves-atom": [
        lambda v: 1.2264 / sqrt(v["V"]),
        lambda v: -13.6 / v["n"] ** 2,
        lambda v: HC / (13.6 * (1 / 4 - 1 / 9)),
        lambda v: 1.0546e-34 / (2 * v["dx"] * 1e-9),
        lambda v: v["n"] * v["n"] * 0.0529,
    ],
    "nuclear": [
        lambda v: 1.2 * v["A"] ** (1 / 3),
        lambda v: v["dm"] * 931.5,
        lambda v: 0.5 ** (v["t"] / v["T"]),
        lambda v: log(2) / v["T"] * v["N"],
        lambda v: log(1 / v["f"]) / log(2) * 5730,
    ],
}
