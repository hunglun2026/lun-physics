"""電磁學 1：庫侖定律、電場、高斯定律、電位、電容、電流與電阻、直流電路。"""
import math

from ._lib import G, Chapter, add, e, eps0, k_e, m_e, pi, prob

add(Chapter(
    id="charge-coulomb", unit="em", no=1, title="電荷與庫侖定律",
    lead="電荷有正負、守恆、而且量子化；兩個點電荷之間的力跟距離平方成反比，跟萬有引力同一個形狀。",
    body=r"""
## 電荷的性質

- 電荷有兩種：正與負。同性相斥，異性相吸
- **守恆**：孤立系統的總電荷不變，只能轉移，不會憑空產生
- **量子化**：電荷只能是基本電荷的整數倍：$e=1.602\times10^{-19}\ \mathrm C$。電子帶 $-e$，質子帶 $+e$

單位庫侖（C）很大，常用 $\mu\mathrm C=10^{-6}\ \mathrm C$、$\mathrm{nC}=10^{-9}\ \mathrm C$。

## 導體與絕緣體

導體（金屬）內有可自由移動的電子，絕緣體（塑膠、玻璃）沒有。靜電感應：把帶電體靠近導體，導體內的電荷會重新分布，所以帶電的梳子能吸起不帶電的小紙屑。

## 庫侖定律

兩個點電荷 $q_1$、$q_2$ 相距 $r$，力的大小：

$$F=k\frac{|q_1q_2|}{r^2},\qquad k=\frac1{4\pi\varepsilon_0}=8.988\times10^9\ \mathrm{N\cdot m^2/C^2}$$

沿兩電荷連線：同號相斥、異號相吸。$\varepsilon_0=8.854\times10^{-12}\ \mathrm{C^2/(N\cdot m^2)}$。

>! 電力和重力都是平方反比，但電力強太多了：兩個電子之間的電斥力是重力吸引力的約 $4\times10^{42}$ 倍。我們沒被電力撕裂，是因為物質整體幾乎是電中性的。

## 疊加原理

好幾個電荷同時作用在某個電荷上，合力是各個力的**向量**和，每個力都按庫侖定律單獨計算。共線時，先決定每個力的方向，再當正負號相加。
""",
    problems=[
        prob(r"兩個點電荷 «q1» μC 與 «q2» μC 相距 «r» m，彼此的力是多少 N？", k_e*2e-6*3e-6/0.1**2, "N", r"$F=k\dfrac{q_1q_2}{r^2}=8.988\times10^9\times\dfrac{«q1»\times10^{-6}\times«q2»\times10^{-6}}{«r»^2}=«ans»\ \mathrm N$。", q1=2, q2=3, r=0.1),
        prob(r"帶 «q» μC 負電的物體多了多少個電子？（$e=1.602\times10^{-19}\ \mathrm C$）", 1e-6/e, "個", r"$N=\dfrac{q}{e}=\dfrac{«q»\times10^{-6}}{1.602\times10^{-19}}=«ans»$。", q=1),
        prob(r"氫原子裡電子與質子相距 $r=5.29\times10^{-11}\ \mathrm m$，電吸引力是多少 N？", k_e*e*e/(5.29e-11)**2, "N", r"$F=\dfrac{ke^2}{r^2}=\dfrac{8.988\times10^9\times(1.602\times10^{-19})^2}{(5.29\times10^{-11})^2}=«ans»\ \mathrm N$。"),
        prob(r"兩個電子之間，電斥力是萬有引力的幾倍？（$G=6.674\times10^{-11}$、$m_e=9.109\times10^{-31}\ \mathrm{kg}$）", k_e*e**2/(G*m_e**2), "倍", r"兩者都與 $r^2$ 成反比，距離約掉：$\dfrac{ke^2}{Gm_e^2}=«ans»$。", tol=0.02),
        prob(r"兩個 «Q» μC 的正電荷相距 «d» m，在它們連線上距左邊 «x» m 處放一個 «q» μC 的正電荷，受到的合力大小是多少 N？", k_e*1e-6*3e-6*(1/0.1**2-1/0.3**2), "N",
             r"左邊的電荷推它向右：$F_1=\dfrac{kqQ}{«x»^2}$；右邊的電荷（距 $«d»-«x»=0.3$ m）推它向左。合力 $=kqQ\left(\dfrac1{«x»^2}-\dfrac1{0.3^2}\right)=«ans»\ \mathrm N$。", Q=3, d=0.4, x=0.1, q=1),
    ],
))

add(Chapter(
    id="electric-field", unit="em", no=2, title="電場",
    lead="電荷在周圍的空間製造電場，其他電荷放進去就受力；電場線畫出場的方向與強弱。",
    body=r"""
## 電場的定義

在空間某點放一個很小的正試探電荷 $q_0$，它受的力除以 $q_0$ 就是那一點的電場：

$$\vec E=\frac{\vec F}{q_0},\qquad \vec F=q\vec E$$

單位 N/C（等於 V/m）。正電荷受力方向與 $\vec E$ 同向，負電荷反向。

## 點電荷的電場

$$E=\frac{kQ}{r^2}$$

正電荷的場向外輻射，負電荷的場向內指。多個電荷的電場是各自電場的**向量和**。

!sim em-efield

## 電場線

- 從正電荷出發、止於負電荷
- 線上每一點的切線方向就是該點電場方向
- 線越密，電場越強
- 電場線不會相交（一點只有一個方向）

## 連續電荷分布

把帶電體切成很多小電荷 $dq$，每個貢獻 $dE=\dfrac{k\,dq}{r^2}$，再向量積分。例：電荷 $Q$ 均勻分布的圓環（半徑 $a$），在軸線上距圓心 $x$ 處：

$$E=\frac{kQx}{(a^2+x^2)^{3/2}}$$

## 電偶極

一對等量異號電荷 $\pm q$ 相距 $d$，偶極矩 $p=qd$。放在均勻電場中受力矩 $\tau=pE\sin\theta$，會轉到與場同向，水分子是偶極，所以微波爐能加熱水。

>! 電場是向量，疊加時要看方向。兩個等量異號電荷的連線中點，兩個場同方向、大小相加；兩個等量同號電荷的連線中點，兩個場方向相反、抵消為零。

## 帶電粒子在均勻電場中

力 $F=qE$ 固定，所以加速度固定 $a=\dfrac{qE}{m}$，運動就是等加速度（和拋體同一套數學）。電子槍、噴墨印表機都這樣偏轉電荷。
""",
    problems=[
        prob(r"點電荷 «q» nC 在距離 «r» m 處的電場大小是多少 N/C？", k_e*5e-9/0.3**2, "N/C", r"$E=\dfrac{kq}{r^2}=\dfrac{8.988\times10^9\times«q»\times10^{-9}}{«r»^2}=«ans»\ \mathrm{N/C}$。", q=5, r=0.3),
        prob(r"電子在 «E» N/C 的均勻電場中受力多大（N）？", e*1000, "N", r"$F=eE=1.602\times10^{-19}\times«E»=«ans»\ \mathrm N$。", E=1000),
        prob(r"電子在 «E» N/C 的電場中的加速度是多少 m/s²？（$m_e=9.109\times10^{-31}\ \mathrm{kg}$）", e*2000/m_e, "m/s²", r"$a=\dfrac{eE}{m_e}=\dfrac{1.602\times10^{-19}\times«E»}{9.109\times10^{-31}}=«ans»\ \mathrm{m/s^2}$。", E=2000),
        prob(r"$+«q»\ \mu\mathrm C$ 與 $-«q»\ \mu\mathrm C$ 兩個電荷相距 «d» m，連線中點的電場大小是多少 N/C？", 2*k_e*4e-6/0.1**2, "N/C", r"每個電荷在中點（距 $«d»/2=0.1$ m）的場 $=\dfrac{kq}{0.1^2}$，兩個場同方向，相加：$2\times\dfrac{8.988\times10^9\times«q»\times10^{-6}}{0.1^2}=«ans»\ \mathrm{N/C}$。", q=4, d=0.2),
        prob(r"電荷 «Q» nC 均勻分布的圓環，半徑 «a» m，軸線上距圓心 «x» m 處的電場是多少 N/C？", k_e*2e-9*0.1/(0.1**2+0.1**2)**1.5, "N/C", r"$E=\dfrac{kQx}{(a^2+x^2)^{3/2}}=\dfrac{8.988\times10^9\times«Q»\times10^{-9}\times«x»}{(«a»^2+«x»^2)^{3/2}}=«ans»\ \mathrm{N/C}$。", Q=2, a=0.1, x=0.1),
    ],
    sims=["em-efield"],
))

add(Chapter(
    id="gauss", unit="em", no=3, title="高斯定律",
    lead="穿過封閉曲面的電通量，只由面內包圍的電荷決定；遇到對稱的電荷分布，用它比直接積分快很多。",
    body=r"""
## 電通量

電場穿過一個面的通量：

$$\Phi_E=\int\vec E\cdot d\vec A$$

均勻電場穿過面積 $A$、法線與電場夾角 $\theta$ 的平面：$\Phi=EA\cos\theta$。通量可想成「穿過這個面的電場線條數」。

## 高斯定律

穿過任何封閉曲面（高斯面）的總通量，只看面內包圍的電荷：

$$\oint\vec E\cdot d\vec A=\frac{Q_{\text{enc}}}{\varepsilon_0}$$

面外的電荷對總通量沒有貢獻（進去的線又出來）。

## 怎麼用

高斯定律永遠成立，但要用它算出 $E$，需要電荷分布有高度對稱，才能選一個「$E$ 在面上大小固定、方向垂直或平行面」的高斯面：

- **球對稱**：選同心球面，$E\cdot4\pi r^2=\dfrac{Q_{\text{enc}}}{\varepsilon_0}$
- **無限長線**（線密度 $\lambda$）：選同軸圓柱，$E=\dfrac{\lambda}{2\pi\varepsilon_0r}$
- **無限大平面**（面密度 $\sigma$）：$E=\dfrac{\sigma}{2\varepsilon_0}$，與距離無關

## 導體

靜電平衡時：

- 導體內部電場為零
- 多餘電荷全部在表面
- 表面外緊鄰處電場垂直表面，大小 $E=\dfrac{\sigma}{\varepsilon_0}$

>! 帶電的導體球殼，內部沒有電場，這叫靜電屏蔽。汽車與飛機的金屬外殼讓雷擊時車內的人安全，同樣是這個原因。

## 均勻帶電的絕緣球

總電荷 $Q$、半徑 $R$：球外 $E=\dfrac{kQ}{r^2}$（等同電荷集中在球心）；球內 $E=\dfrac{kQr}{R^3}$，與 $r$ 成正比。
""",
    problems=[
        prob(r"一個封閉曲面包圍了 «Q» nC 的電荷，穿過它的總電通量是多少 N·m²/C？", 3e-9/eps0, "N·m²/C", r"$\Phi=\dfrac{Q}{\varepsilon_0}=\dfrac{«Q»\times10^{-9}}{8.854\times10^{-12}}=«ans»$。", Q=3),
        prob(r"無限大帶電平面，面電荷密度 «s» μC/m²，電場大小是多少 N/C？", 2e-6/(2*eps0), "N/C", r"$E=\dfrac{\sigma}{2\varepsilon_0}=\dfrac{«s»\times10^{-6}}{2\times8.854\times10^{-12}}=«ans»\ \mathrm{N/C}$。", s=2),
        prob(r"無限長帶電線，線電荷密度 «l» nC/m，在距離 «r» m 處的電場是多少 N/C？", 3e-9/(2*pi*eps0*0.5), "N/C", r"$E=\dfrac{\lambda}{2\pi\varepsilon_0r}=\dfrac{«l»\times10^{-9}}{2\pi\times8.854\times10^{-12}\times«r»}=«ans»\ \mathrm{N/C}$。", l=3, r=0.5),
        prob(r"半徑 «R» m 的導體球帶電 «Q» nC，球面外緊鄰處的電場是多少 N/C？", k_e*5e-9/0.1**2, "N/C", r"球外等同電荷集中在球心：$E=\dfrac{kQ}{R^2}=\dfrac{8.988\times10^9\times«Q»\times10^{-9}}{«R»^2}=«ans»\ \mathrm{N/C}$。", R=0.1, Q=5),
        prob(r"均勻帶電的絕緣球，$Q=«Q»$ nC、半徑 «R» m，球內距中心 «r» m 處的電場是多少 N/C？", k_e*8e-9*0.1/0.2**3, "N/C", r"高斯面內只包圍 $Q(r/R)^3$ 的電荷：$E=\dfrac{kQr}{R^3}=\dfrac{8.988\times10^9\times«Q»\times10^{-9}\times«r»}{«R»^3}=«ans»\ \mathrm{N/C}$。", Q=8, R=0.2, r=0.1),
    ],
))

add(Chapter(
    id="potential", unit="em", no=4, title="電位與電位能",
    lead="電位是每單位電荷的位能，是純量；用它解題常比算電場向量輕鬆。",
    body=r"""
## 電位能與電位

靜電力是保守力，可以定義電位能 $U$。兩個點電荷相距 $r$：

$$U=\frac{kq_1q_2}{r}$$

同號為正（要作功才能拉近），異號為負（束縛）。電位（電壓）是單位電荷的電位能：

$$V=\frac Uq,\qquad \Delta V=V_b-V_a=-\int_a^b\vec E\cdot d\vec l$$

單位伏特：$1\ \mathrm V=1\ \mathrm{J/C}$。

## 點電荷的電位

$$V=\frac{kQ}{r}\quad(\text{零點在無窮遠})$$

多個電荷的電位是各自電位的**代數和**（純量，不用管方向），這是用電位的最大好處。

## 能量守恆與電子伏特

電荷 $q$ 穿過電位差 $\Delta V$，動能改變：$\Delta K=-q\Delta V$。電子由靜止被加速通過 $V$ 伏特，獲得動能 $eV$。能量單位**電子伏特**：$1\ \mathrm{eV}=1.602\times10^{-19}\ \mathrm J$。

## 電場與電位的關係

$$E_x=-\frac{dV}{dx}$$

電場指向電位下降最快的方向。均勻電場中 $\Delta V=Ed$。

## 等位面

電位相等的點連成等位面。電場永遠垂直等位面；沿著等位面移動電荷，電場不作功。導體表面是等位面，導體內部各點電位相同。

>! 電位是 $0$ 的地方，電場不一定是 $0$；電場是 $0$ 的地方，電位也不一定是 $0$。例如電偶極的中垂線上電位為 $0$，但有電場。電位看的是「高度」，電場看的是「坡度」。
""",
    problems=[
        prob(r"點電荷 «q» nC 在距離 «r» m 處的電位是多少 V？", k_e*2e-9/0.3, "V", r"$V=\dfrac{kq}{r}=\dfrac{8.988\times10^9\times«q»\times10^{-9}}{«r»}=«ans»\ \mathrm V$。", q=2, r=0.3),
        prob(r"把 «q» μC 的電荷移過 «dV» V 的電位差，作功多少 J？", 1e-6*12, "J", r"$W=q\Delta V=«q»\times10^{-6}\times«dV»=«ans»\ \mathrm J$。", q=1, dV=12),
        prob(r"電子由靜止被 «V» V 的電位差加速，最後速率是多少 m/s？", math.sqrt(2*e*500/m_e), "m/s", r"$eV=\tfrac12mv^2\Rightarrow v=\sqrt{\dfrac{2eV}{m_e}}=\sqrt{\dfrac{2\times1.602\times10^{-19}\times«V»}{9.109\times10^{-31}}}=«ans»\ \mathrm{m/s}$。", V=500),
        prob(r"均勻電場 «E» V/m，沿電場方向相距 «d» m 的兩點，電位差是多少 V？", 500*0.04, "V", r"$\Delta V=Ed=«E»\times«d»=«ans»\ \mathrm V$。", E=500, d=0.04),
        prob(r"$+«q1»\ \mu\mathrm C$ 與 $-«q2»\ \mu\mathrm C$ 兩個點電荷相距 «r» m，系統的電位能是多少 J？", k_e*3e-6*(-2e-6)/0.5, "J", r"$U=\dfrac{kq_1q_2}{r}=\dfrac{8.988\times10^9\times«q1»\times10^{-6}\times(-«q2»\times10^{-6})}{«r»}=«ans»\ \mathrm J$，是負的，表示互相吸引、被束縛。", q1=3, q2=2, r=0.5),
    ],
))

add(Chapter(
    id="capacitance", unit="em", no=5, title="電容",
    lead="電容器儲存電荷與電能；平行板電容器、串並聯、加上介電質，是電路裡最常見的零件。",
    body=r"""
## 電容

兩個導體分別帶 $+Q$、$-Q$，之間的電位差 $V$ 與 $Q$ 成正比：

$$C=\frac QV$$

單位法拉（F），常用 $\mu\mathrm F=10^{-6}\ \mathrm F$、$\mathrm{nF}$、$\mathrm{pF}$。

## 平行板電容器

面積 $A$、間距 $d$：

$$C=\frac{\varepsilon_0A}{d}$$

電容只由幾何形狀決定，與 $Q$、$V$ 無關。

## 串聯與並聯

- **並聯**：電壓相同，電荷相加：$C_{eq}=C_1+C_2+\cdots$
- **串聯**：電荷相同，電壓相加：$\dfrac1{C_{eq}}=\dfrac1{C_1}+\dfrac1{C_2}+\cdots$

>! 電容的串並聯公式跟電阻**剛好相反**。電容並聯是直接相加，串聯才是倒數相加。

## 儲存的能量

$$U=\tfrac12QV=\tfrac12CV^2=\frac{Q^2}{2C}$$

能量儲存在電場中，能量密度 $u=\tfrac12\varepsilon_0E^2$。相機閃光燈與電擊器就是電容快速放電。

## 介電質

兩板之間塞入絕緣材料（介電質），分子極化產生反向電場，使同樣電荷下電壓降低：

$$C=\kappa C_0$$

$\kappa$ 是介電常數（空氣約 1，紙約 3，水約 80）。

- **接著電池**（電壓固定）插入介電質：$C$ 增加為 $\kappa$ 倍，電荷增加 $\kappa$ 倍
- **充電後斷開電池**（電荷固定）插入：電壓變成 $\dfrac V\kappa$
""",
    problems=[
        prob(r"平行板電容器面積 «A» m²、間距 «d» mm，電容是多少 pF？", eps0*0.02/1e-3*1e12, "pF", r"$C=\dfrac{\varepsilon_0A}{d}=\dfrac{8.854\times10^{-12}\times«A»}{«d»\times10^{-3}}=«ans»\ \mathrm{pF}$。", A=0.02, d=1),
        prob(r"«C» μF 的電容器接上 «V» V 電池，儲存的電荷是多少 μC？", 10*12, "μC", r"$Q=CV=«C»\times«V»=«ans»\ \mu\mathrm C$。", C=10, V=12),
        prob(r"«C» μF 的電容器充電到 «V» V，儲存的能量是多少 J？", 0.5*10e-6*12**2, "J", r"$U=\tfrac12CV^2=\tfrac12\times«C»\times10^{-6}\times«V»^2=«ans»\ \mathrm J$。", C=10, V=12),
        prob(r"«C1» μF 與 «C2» μF 的電容器串聯，等效電容是多少 μF？", 1/(1/2+1/3), "μF", r"$\dfrac1{C_{eq}}=\dfrac1{«C1»}+\dfrac1{«C2»}\Rightarrow C_{eq}=\dfrac{«C1»\times«C2»}{«C1»+«C2»}=«ans»\ \mu\mathrm F$。", C1=2, C2=3),
        prob(r"電容器充電到 «V» V 後與電池斷開，再塞入 $\kappa=«k»$ 的介電質，電壓變成多少 V？", 12/4, "V", r"電荷不變，$C$ 變成 $\kappa$ 倍，所以 $V'=V/\kappa=«V»/«k»=«ans»\ \mathrm V$。", V=12, k=4),
    ],
))

add(Chapter(
    id="current-resistance", unit="em", no=6, title="電流與電阻",
    lead="電流是電荷的流動；歐姆定律與電阻率說明導線怎麼限制電流，電功率說明能量去了哪裡。",
    body=r"""
## 電流

單位時間通過截面的電荷：

$$I=\frac{dq}{dt}$$

單位安培：$1\ \mathrm A=1\ \mathrm{C/s}$。電流方向規定為**正電荷移動的方向**，所以金屬中電子流動的方向和電流方向相反。

金屬內電子的漂移速度其實很慢（約 $10^{-4}\ \mathrm{m/s}$），開關一按燈就亮，是因為整條導線裡的電場幾乎瞬間建立，每個電子同時被推動。

## 電阻與歐姆定律

$$V=IR$$

單位歐姆（$\Omega$）。電阻由材料與形狀決定：

$$R=\rho\frac LA$$

$\rho$ 是電阻率（銅 $1.68\times10^{-8}\ \Omega\cdot\mathrm m$）。越長越粗：電阻與長度成正比，與截面積成反比。

>! 歐姆定律是「某些材料」的性質（歐姆性材料，$R$ 固定）。二極體、燈泡的燈絲都不遵守，$V$-$I$ 圖不是直線。公式 $R=V/I$ 對任何材料都能算出某一瞬間的電阻值。

## 溫度的影響

金屬溫度升高，電阻增加；半導體相反，溫度升高電阻降低。超導體在臨界溫度以下電阻為零。

## 電功率

電流通過電阻消耗電能轉成熱：

$$P=IV=I^2R=\frac{V^2}{R}$$

單位瓦特。電費的「度」就是 $\mathrm{kWh}$（千瓦小時）：$1\ \mathrm{kWh}=3.6\times10^6\ \mathrm J$。

## 電動勢

電池靠化學能把電荷從低電位推到高電位，維持電流。電池不接外電路時的電壓叫電動勢 $\mathcal E$，接上電路後端電壓略低（見下一章內電阻）。
""",
    problems=[
        prob(r"電流 «I» A 流過導線 «t» 分鐘，通過的總電荷是多少 C？", 2.5*10*60, "C", r"$q=It=«I»\times(«t»\times60)=«ans»\ \mathrm C$。", I=2.5, t=10),
        prob(r"銅線（$\rho=1.68\times10^{-8}\ \Omega\cdot\mathrm m$）長 «L» m、截面積 «A» m²，電阻是多少 Ω？", 1.68e-8*10/1e-6, "Ω", r"$R=\rho\dfrac LA=\dfrac{1.68\times10^{-8}\times«L»}{«A»}=«ans»\ \Omega$。", L=10, A=1e-6),
        prob(r"電阻 «R» Ω 接在 «V» V 電壓上，電流是多少 A？", 12/48, "A", r"$I=\dfrac VR=\dfrac{«V»}{«R»}=«ans»\ \mathrm A$。", V=12, R=48),
        prob(r"電熱器接 «V» V、電阻 «R» Ω，功率是多少 W？", 120**2/10, "W", r"$P=\dfrac{V^2}{R}=\dfrac{«V»^2}{«R»}=«ans»\ \mathrm W$。", V=120, R=10),
        prob(r"功率 «P» kW 的冷氣開 «t» 小時，用了多少度電（kWh）？", 1.5*2, "kWh", r"$E=Pt=«P»\times«t»=«ans»\ \mathrm{kWh}$。", P=1.5, t=2),
    ],
))

add(Chapter(
    id="dc-circuits", unit="em", no=7, title="直流電路",
    lead="電阻的串並聯、克希何夫定律、電池內電阻，以及電容充放電的時間常數。",
    body=r"""
## 電阻的串並聯

- **串聯**：電流相同，電壓相加：$R_{eq}=R_1+R_2+\cdots$
- **並聯**：電壓相同，電流相加：$\dfrac1{R_{eq}}=\dfrac1{R_1}+\dfrac1{R_2}+\cdots$

並聯後的總電阻比最小的那個還小。兩個電阻並聯可用 $R_{eq}=\dfrac{R_1R_2}{R_1+R_2}$。

## 電池的內電阻

真實電池有內電阻 $r$，接上負載 $R$ 時：

$$I=\frac{\mathcal E}{R+r},\qquad V_{\text{端}}=\mathcal E-Ir$$

電流越大，端電壓掉得越多；這就是手電筒電池快沒電時變暗的原因之一。

## 克希何夫定律

複雜電路用兩條規則：

- **節點定律**（電荷守恆）：流進一個節點的電流總和等於流出的總和
- **迴路定律**（能量守恆）：沿封閉迴路繞一圈，電位變化的總和為零

用法：標每段電流的假設方向，沿迴路走時遇到電阻順電流方向是 $-IR$、逆著是 $+IR$；經過電池由負到正是 $+\mathcal E$。算出來的電流若是負的，代表實際方向相反。

>! 算出負電流不是算錯。它只是告訴你當初假設的方向猜反了。

## RC 電路

電容器經電阻充電，電壓指數增加：

$$V_C(t)=\mathcal E\left(1-e^{-t/\tau}\right),\qquad\tau=RC$$

放電則 $V_C(t)=V_0e^{-t/\tau}$。經過一個 $\tau$，充電到約 $63\%$，放電剩約 $37\%$。時間常數越大，變化越慢。

!sim em-rc

## 安全

通過人體的電流才是危險的：約 $1\ \mathrm{mA}$ 就感覺到，$10\ \mathrm{mA}$ 以上肌肉無法放開，$100\ \mathrm{mA}$ 可能致命。乾燥皮膚電阻高，潮濕時小很多，所以濕手摸電器更危險。
""",
    problems=[
        prob(r"«R1» Ω 與 «R2» Ω 串聯後接在 «V» V 電源上，電流是多少 A？", 20/(4+6), "A", r"$I=\dfrac{V}{R_1+R_2}=\dfrac{«V»}{«R1»+«R2»}=«ans»\ \mathrm A$。", R1=4, R2=6, V=20),
        prob(r"«R1» Ω 與 «R2» Ω 並聯，等效電阻是多少 Ω？", 6*3/(6+3), "Ω", r"$R_{eq}=\dfrac{R_1R_2}{R_1+R_2}=\dfrac{«R1»\times«R2»}{«R1»+«R2»}=«ans»\ \Omega$。", R1=6, R2=3),
        prob(r"電池電動勢 «E» V、內電阻 «r» Ω，接上 «R» Ω 的電阻，端電壓是多少 V？", 12-12/(5.5+0.5)*0.5, "V", r"$I=\dfrac{\mathcal E}{R+r}=\dfrac{«E»}{«R»+«r»}=2\ \mathrm A$，$V=\mathcal E-Ir=«E»-2\times«r»=«ans»\ \mathrm V$。", E=12, r=0.5, R=5.5),
        prob(r"電源 «E» V，串聯 $R_1=«R1»\ \Omega$，再接 $R_2=«R2»\ \Omega$ 與 $R_3=«R3»\ \Omega$ 的並聯組。通過 $R_2$ 的電流是多少 A？", 22/(10+20*30/50)*(20*30/50)/20, "A",
             r"並聯組 $=\dfrac{«R2»\times«R3»}{«R2»+«R3»}=12\ \Omega$，總電阻 $22\ \Omega$，總電流 $1\ \mathrm A$，並聯組電壓 $12\ \mathrm V$，所以 $I_2=12/«R2»=«ans»\ \mathrm A$。", E=22, R1=10, R2=20, R3=30),
        prob(r"RC 電路 $R=«R»\ \mathrm{k\Omega}$、$C=«C»\ \mu\mathrm F$、電池 «E» V，開始充電後經過一個時間常數，電容電壓是多少 V？", 12*(1-math.exp(-1)), "V", r"$V_C=\mathcal E(1-e^{-1})=«E»\times0.632=«ans»\ \mathrm V$（此時 $\tau=RC=10\ \mathrm{ms}$）。", R=2, C=5, E=12),
    ],
    sims=["em-rc"],
))
