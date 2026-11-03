"""補充章節的獨立驗算（只看題目顯示的數字，用不同寫法重算）。"""
from math import cos, exp, pi, sin, sqrt

HC = 1239.84  # eV·nm


def simpson(f, a, b, n=2000):
    """數值積分（Simpson），用來獨立驗證機率積分的解析結果。"""
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


CHECKS = {
    "maxwell-magnetism": [
        # 位移電流：I_d = ε0·A·dE/dt，另用電容 C=ε0A/d 的路線：I = C·dV/dt
        lambda v: 8.854e-12 * v["A"] / (v["d"] * 1e-3) * v["dVdt"] * 1e6,
        # μ0 = 4π×10^-7（已知值）換成 μH/m
        lambda v: 4 * pi * 1e-7 * 1e6,
        # dE/dt 改用庫倫常數：ε0 = 1/(4πk)，dE/dt = 4kI/R²
        lambda v: 4 * 8.988e9 * v["I"] / (v["R"] * 1e-2) ** 2,
        # 波耳磁子用 5.788e-5 eV/T
        lambda v: 2 * 5.788e-5 * v["B"] * 1e6,
        # B = μ0(nI + M)，M=(κ-1)nI
        lambda v: 4 * pi * 1e-7 * (v["n"] * v["I"] + (v["km"] - 1) * v["n"] * v["I"]),
    ],
    "quantum-mechanics": [
        lambda v: 0.376 / v["L"] ** 2,
        lambda v: HC / (0.376 / v["L"] ** 2 * (v["ni"] ** 2 - v["nf"] ** 2)),
        # 機率：直接對 |ψ|² 做數值積分（L=1）
        lambda v: simpson(lambda x: 2 * sin(pi * x) ** 2, 1 / 3, 2 / 3),
        # κ 用 ħ²/2m = 0.0381 eV·nm²
        lambda v: exp(-2 * sqrt(v["dU"] / 0.0381) * v["L"]),
        lambda v: 4.1357e-15 * v["f"] / 2,  # hf/2，h 用 eV·s
    ],
    "solids": [
        lambda v: HC / v["Eg"],
        lambda v: HC / v["Eg"],
        lambda v: 0.0381 * (3 * pi ** 2 * v["n"] * 1e-27) ** (2 / 3),  # ħ²/2m = 0.0381 eV·nm²，n 換成 nm^-3，結果 eV
        lambda v: 1 / (1 / (v["n"] * 1.602e-19 * v["mu"])),  # σ = 1/ρ，ρ = 1/(neμ)
        lambda v: exp(v["Eg"] / (2 * 8.617e-5 * v["T1"]) - v["Eg"] / (2 * 8.617e-5 * v["T2"])),
    ],
    "particles-cosmology": [
        lambda v: v["H0"] * v["d"],
        lambda v: 977.8 / v["H0"] * 10,  # 1/H0 = 977.8/H0 Gyr（H0 單位 km/s/Mpc），×10 變億年
        lambda v: v["lam"] / 656.3 - 1,
        lambda v: 2.4263e-12 * 1e12,  # 康普頓波長 h/(m_e c)
        lambda v: 1.98645e-25 / (4.965114 * 1.380649e-23 * v["T"]) * 1e3,  # 另用 hc/(4.965kT)
    ],
}
