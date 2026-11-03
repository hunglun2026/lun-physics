"""電磁學補充：馬克士威方程組與物質磁性（排在電磁波之前）。"""
import math

from ._lib import Chapter, add, c, e, eps0, k_e, mu0, pi, prob

add(Chapter(
    id="maxwell-magnetism", unit="em", no=12.5, title="馬克士威方程組與物質磁性",
    lead="四條方程式收納整個電磁學；其中一條補上「變化的電場也會產生磁場」，電磁波因此成立。物質放進磁場，則依原子的磁矩分成順磁、反磁與鐵磁。",
    body=r"""
## 前面學過的四個定律

到這裡，電與磁的規律已經有四條：

- **電的高斯定律**：電荷是電場線的起點與終點，$\oint\vec E\cdot d\vec A=\dfrac{Q}{\varepsilon_0}$
- **磁的高斯定律**：磁場線一定是封閉的圈，沒有單獨的磁荷（磁單極），$\oint\vec B\cdot d\vec A=0$
- **法拉第定律**：變化的磁通量產生電場，$\oint\vec E\cdot d\vec\ell=-\dfrac{d\Phi_B}{dt}$
- **安培定律**：電流產生磁場，$\oint\vec B\cdot d\vec\ell=\mu_0 I$

前三條沒問題，第四條有一個漏洞。

## 安培定律的漏洞

幫電容器充電時，導線有電流，但兩片板之間是真空，沒有電荷在跑。用「圍住導線的圈」算安培定律，得到 $\mu_0I$；改用「穿過兩板之間的鼓形曲面」來算，穿過的電流是 0。同一個圈算出兩個答案，定律矛盾。

馬克士威（1865）的解法：兩板之間雖然沒有電流，但**電場正在變化**，把它當成一種電流，叫**位移電流**：

$$I_d=\varepsilon_0\frac{d\Phi_E}{dt}$$

充電時，板間電場隨電荷增加而變強，算出來的 $I_d$ 剛好等於導線裡的電流 $I$，矛盾消失。

## 馬克士威方程組

把安培定律補上位移電流，就得到完整的四條：

$$\oint\vec E\cdot d\vec A=\frac{Q}{\varepsilon_0}\qquad\oint\vec B\cdot d\vec A=0$$

$$\oint\vec E\cdot d\vec\ell=-\frac{d\Phi_B}{dt}\qquad\oint\vec B\cdot d\vec\ell=\mu_0I+\mu_0\varepsilon_0\frac{d\Phi_E}{dt}$$

> 變化的磁場產生電場（法拉第），變化的電場產生磁場（馬克士威的補充）。兩者互相接力，不需要電荷或導線也能在空間中傳下去，這就是電磁波。

## 光就是電磁波

從這組方程式可以推出波速：

$$c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}=\frac{1}{\sqrt{4\pi\times10^{-7}\times8.854\times10^{-12}}}\approx2.998\times10^8\ \mathrm{m/s}$$

這個數字完全等於實驗量到的光速。馬克士威因此推斷光是電磁波，之後赫茲（1887）用實驗做出了無線電波，證實預言。下一章就是電磁波的性質。

>! 位移電流不是電荷在移動，名字容易誤導。它是「變化的電場」產生磁場的效果，量值上可以和真正的電流相比。

## 物質的磁性

把物質放進磁場，原子裡的電子有兩種磁矩來源：軌道運動與自旋。電子自旋的磁矩大小約等於一個**波耳磁子**：

$$\mu_B=\frac{e\hbar}{2m_e}=9.274\times10^{-24}\ \mathrm{J/T}=5.788\times10^{-5}\ \mathrm{eV/T}$$

依原子磁矩的表現，分成三類：

- **反磁性**：所有物質都有。外加磁場時，電子軌道產生反向的小磁場，物質被微弱地排斥。水、銅、金都是；效果極小，相對磁導率約 $1-10^{-5}$。超導體是理想的反磁體，把磁場完全擠出去
- **順磁性**：原子本身有磁矩（有未配對電子），平常方向亂，外加磁場時稍微排向同一方向，被微弱吸引，相對磁導率約 $1+10^{-5}$。鋁、氧氣是
- **鐵磁性**：鐵、鈷、鎳。相鄰原子磁矩彼此鎖定同方向，形成許多小區塊（磁域），外加磁場時磁域整個轉向，磁化很強，相對磁導率可到數百至數萬

## 磁化與磁導率

線性磁性材料放進螺線管，總磁場是真空時的 $\kappa_m$ 倍（相對磁導率）：

$$B=\kappa_m\mu_0nI$$

也可以看成「外加的場 $\mu_0nI$」加上「材料自己產生的磁化部分 $\mu_0M$」，$M$ 是單位體積的磁矩（磁化強度）。

鐵磁物質的磁化與外加場不成正比，而且有**磁滯**：磁場降回零時，材料仍保留磁性。磁滯迴圈寬的是永久磁鐵材料，窄的適合變壓器鐵芯。溫度高過**居里溫度**（鐵約 1043 K）時，磁域被熱運動打亂，鐵磁性消失，變成順磁。
""",
    problems=[
        prob(r"平行板電容器面積 $A=«A»\ \mathrm{m^2}$、板距 $d=«d»$ mm，兩板電壓以 $«dVdt»\ \mathrm{V/s}$ 的速率上升。板間的位移電流是多少 μA？", 8.854e-12 * 0.010 / 1e-3 * 1e6 * 1e6, "μA",
             r"板間電場 $E=V/d$，$\dfrac{dE}{dt}=\dfrac{dV/dt}{d}$，$I_d=\varepsilon_0A\dfrac{dE}{dt}=8.854\times10^{-12}\times«A»\times\dfrac{«dVdt»}{«d»\times10^{-3}}=«ans»\ \mu\mathrm A$。",
             hint=r"位移電流 $I_d=\varepsilon_0\,d\Phi_E/dt$，$\Phi_E=EA$。", A=0.010, d=1.0, dVdt=1e6),
        prob(r"已知光速 $c=2.998\times10^8\ \mathrm{m/s}$、$\varepsilon_0=8.854\times10^{-12}\ \mathrm{F/m}$，由 $c=1/\sqrt{\mu_0\varepsilon_0}$ 求 $\mu_0$ 是多少 μH/m？（$1\ \mu\mathrm{H/m}=10^{-6}\ \mathrm{H/m}$）", 1 / (8.854e-12 * 2.998e8 ** 2) * 1e6, "μH/m",
             r"$\mu_0=\dfrac1{\varepsilon_0c^2}=\dfrac{1}{8.854\times10^{-12}\times(2.998\times10^8)^2}=«ans:4»\times10^{-6}\ \mathrm{H/m}$。"),
        prob(r"圓形平行板電容器的板半徑 $R=«R»$ cm，以 $I=«I»$ A 的電流充電。板間電場的變化率是多少 V/(m·s)？", 2.0 / (8.854e-12 * pi * 0.05 ** 2), "V/(m·s)",
             r"$E=\dfrac{\sigma}{\varepsilon_0}=\dfrac{Q}{\varepsilon_0A}$，所以 $\dfrac{dE}{dt}=\dfrac{I}{\varepsilon_0\pi R^2}=\dfrac{«I»}{8.854\times10^{-12}\times\pi\times(«R»\times10^{-2})^2}=«ans:4»\ \mathrm{V/(m\cdot s)}$。",
             R=5.0, I=2.0),
        prob(r"電子自旋磁矩約為 1 個波耳磁子（$5.788\times10^{-5}\ \mathrm{eV/T}$）。放在 $B=«B»$ T 的磁場中，自旋與磁場平行和反平行的兩個狀態，能量差是多少 μeV？", 2 * 9.274e-24 * 1.0 / 1.602e-19 * 1e6, "μeV",
             r"磁位能 $U=-\mu B\cos\theta$，平行是 $-\mu_BB$，反平行是 $+\mu_BB$，差 $\Delta E=2\mu_BB=2\times\dfrac{9.274\times10^{-24}\times«B»}{1.602\times10^{-19}}=«ans»\ \mu\mathrm{eV}$。", B=1.0),
        prob(r"螺線管每公尺 $«n»$ 匝、電流 $«I»$ A，內部塞滿相對磁導率 $\kappa_m=«km»$ 的鐵芯（當作線性材料）。管內磁場是多少 T？", mu0 * 500 * 1000 * 0.50, "T",
             r"$B=\kappa_m\mu_0nI=«km»\times4\pi\times10^{-7}\times«n»\times«I»=«ans»\ \mathrm T$。", n=1000, I=0.50, km=500),
    ],
))
