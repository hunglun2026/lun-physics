"""熱學：溫度與熱、熱力學第一定律、氣體動力論、熱力學第二定律與熵。"""
import math

from ._lib import Chapter, R, add, k_B, prob

add(Chapter(
    id="temperature-heat", unit="thermo", no=1, title="溫度與熱",
    lead="溫度衡量分子平均動能，熱是因溫差而轉移的能量；膨脹、比熱、相變與熱傳導。",
    body=r"""
## 溫度

溫度計量的是物體冷熱程度，微觀上是分子平均動能的量度。常用刻度：

$$T_{\mathrm K}=T_{\mathrm C}+273.15,\qquad T_{\mathrm F}=\tfrac95T_{\mathrm C}+32$$

絕對溫度 $0\ \mathrm K$ 是理論下限。**熱力學公式裡的溫度一律用克耳文（K）。**

兩物體接觸一段時間後溫度相同，這叫熱平衡。若 A 與 B、B 與 C 各自達到熱平衡，則 A 與 C 也在熱平衡，這是熱力學第零定律，溫度計因此有意義。

## 熱膨脹

溫度升高，固體長度增加：

$$\Delta L=\alpha L_0\Delta T$$

$\alpha$ 是線膨脹係數，鋼約 $1.2\times10^{-5}\ \mathrm{K^{-1}}$。鐵軌與橋留伸縮縫就是為了這個。

## 熱與比熱

**熱** $Q$ 是因溫差而轉移的能量，單位焦耳（J）。溫度變化時吸收的熱：

$$Q=mc\,\Delta T$$

$c$ 是比熱，水 $c=4186\ \mathrm{J/(kg\cdot K)}$，是常見物質中很大的，所以水適合儲熱與冷卻。

## 相變

相變（熔化、汽化）時溫度不變，吸收的熱用來改變分子排列：

$$Q=mL$$

水的熔化熱 $L_f=3.34\times10^5\ \mathrm{J/kg}$，汽化熱 $L_v=2.26\times10^6\ \mathrm{J/kg}$。

>! 沸水加熱到水蒸氣時，溫度停在 100°C 不升高，加進去的熱全部用在汽化。

## 熱傳導

熱靠接觸從高溫處流向低溫處，單位時間的熱流：

$$\frac{Q}{t}=kA\frac{\Delta T}{L}$$

$k$ 是熱導率。金屬 $k$ 大（摸起來涼），泡棉 $k$ 小（保溫）。另外兩種傳熱方式是對流與輻射。

## 混合問題

高溫物體放的熱 $=$ 低溫物體吸的熱（沒有相變、不散失時）：$m_1c_1(T_1-T_f)=m_2c_2(T_f-T_2)$。
""",
    problems=[
        prob(r"氣溫 «T»°C 等於多少 K？", 25+273.15, "K", r"$T_K=T_C+273.15=«T»+273.15=«ans»\ \mathrm K$。", T=25),
        prob(r"鋼棒長 «L» m，$\alpha=1.2\times10^{-5}\ \mathrm{K^{-1}}$，溫度升高 «dT» K，長度增加多少 mm？", 1.2e-5*10*30*1000, "mm", r"$\Delta L=\alpha L_0\Delta T=1.2\times10^{-5}\times«L»\times«dT»=«ans»\ \mathrm{mm}$（先得 $3.6\times10^{-3}\ \mathrm m$）。", L=10, dT=30),
        prob(r"把 «m» kg 的水從 «T1»°C 加熱到 «T2»°C，需要多少 J？（$c=4186\ \mathrm{J/(kg\cdot K)}$）", 2*4186*60, "J", r"$Q=mc\Delta T=«m»\times4186\times(«T2»-«T1»)=«ans»\ \mathrm{J}$。", m=2, T1=20, T2=80),
        prob(r"使 «m» kg、0°C 的冰全部融成 0°C 的水，需要多少 J？（$L_f=3.34\times10^5\ \mathrm{J/kg}$）", 0.5*3.34e5, "J", r"$Q=mL_f=«m»\times3.34\times10^5=«ans»\ \mathrm{J}$。", m=0.5),
        prob(r"«m1» kg、«T1»°C 的水與 «m2» kg、«T2»°C 的水混合，達到熱平衡後溫度是多少°C？", (0.2*80+0.3*20)/0.5, "°C", r"同種液體比熱相同：$T_f=\dfrac{m_1T_1+m_2T_2}{m_1+m_2}=\dfrac{«m1»\times«T1»+«m2»\times«T2»}{«m1»+«m2»}=«ans»\ ^\circ\mathrm C$。", m1=0.2, T1=80, m2=0.3, T2=20),
    ],
))

add(Chapter(
    id="first-law", unit="thermo", no=2, title="熱力學第一定律",
    lead="能量守恆套到熱現象：內能的改變等於吸收的熱減去對外作的功；理想氣體的四種基本過程。",
    body=r"""
## 理想氣體

氣體密度低、溫度遠高於液化點時，狀態方程式近似為：

$$PV=nRT$$

$n$ 是莫耳數，$R=8.314\ \mathrm{J/(mol\cdot K)}$，$T$ 用克耳文，$P$ 用帕。

## 氣體作功

氣體膨脹時對外作功：

$$W=\int P\,dV$$

在 $P$-$V$ 圖上，過程曲線下的面積就是功。壓力固定時 $W=P\Delta V$；體積不變時 $W=0$。

## 第一定律

$$\Delta U=Q-W$$

$Q$ 是系統**吸收**的熱，$W$ 是系統**對外所作**的功，$\Delta U$ 是內能增加量。

>! 符號慣例很容易搞混。看到題目先判斷：氣體是吸熱還是放熱？是膨脹（對外作功，$W>0$）還是被壓縮（$W<0$）？再代入。

理想氣體的內能只和溫度有關。單原子分子氣體 $U=\tfrac32nRT$。

## 四種基本過程

- **等容**：$\Delta V=0$，$W=0$，$Q=\Delta U=nC_V\Delta T$
- **等壓**：$W=P\Delta V$，$Q=nC_P\Delta T$
- **等溫**：$\Delta U=0$，$Q=W=nRT\ln\dfrac{V_2}{V_1}$
- **絕熱**：$Q=0$，$\Delta U=-W$，$PV^{\gamma}=$ 定值

!sim thermo-pv

莫耳比熱：單原子氣體 $C_V=\tfrac32R$，$C_P=C_V+R$；$\gamma=C_P/C_V$。

## 循環

氣體經過一圈回到原狀態，$\Delta U=0$，所以 $Q_{\text{淨}}=W_{\text{淨}}$，淨功是 $P$-$V$ 圖封閉曲線包圍的面積。順時針走是熱機。
""",
    problems=[
        prob(r"«n» mol 理想氣體，溫度 «T» K，體積 «V» m³，壓力是多少 Pa？", 2*R*300/0.05, "Pa", r"$P=\dfrac{nRT}{V}=\dfrac{«n»\times8.314\times«T»}{«V»}=«ans»\ \mathrm{Pa}$。", n=2, T=300, V=0.05),
        prob(r"氣體在固定壓力 «P» Pa 下體積增加 «dV» m³，對外作功多少 J？", 1e5*0.02, "J", r"$W=P\Delta V=«P»\times«dV»=«ans»\ \mathrm J$。", P=1e5, dV=0.02),
        prob(r"氣體吸收 «Q» J 的熱，同時對外作功 «W» J，內能增加多少 J？", 500-200, "J", r"$\Delta U=Q-W=«Q»-«W»=«ans»\ \mathrm J$。", Q=500, W=200),
        prob(r"«n» mol 理想氣體在 «T» K 等溫膨脹到原體積的 «r» 倍，對外作功多少 J？", 1*R*300*math.log(2), "J", r"$W=nRT\ln\dfrac{V_2}{V_1}=«n»\times8.314\times«T»\times\ln«r»=«ans»\ \mathrm J$。", n=1, T=300, r=2),
        prob(r"«n» mol 單原子理想氣體在體積不變下升溫 «dT» K，吸收多少 J 的熱？", 1.5*1*R*50, "J", r"$Q=nC_V\Delta T=«n»\times\tfrac32\times8.314\times«dT»=«ans»\ \mathrm J$。", n=1, dT=50),
    ],
    sims=["thermo-pv"],
))

add(Chapter(
    id="kinetic-theory", unit="thermo", no=3, title="氣體動力論",
    lead="把氣體看成大量亂跑的分子：壓力是撞牆的平均效果，溫度是平均動能，巨觀公式由此推出。",
    body=r"""
## 基本想法

氣體是大量分子的集合。每個分子不斷碰撞，速度各不相同。我們只看**平均**：壓力是分子撞擊器壁的平均力，溫度反映平均動能。

## 壓力與溫度

由分子對器壁的衝量可得：

$$PV=\tfrac13Nm\overline{v^2}$$

與 $PV=NkT$ 比較（$k=1.381\times10^{-23}\ \mathrm{J/K}$ 是波茲曼常數），得到每個分子的平均平移動能：

$$\overline{K}=\tfrac12m\overline{v^2}=\tfrac32kT$$

這說明溫度的意義：溫度正比於分子平均動能，與分子種類無關。

## 方均根速率

$$v_{rms}=\sqrt{\overline{v^2}}=\sqrt{\frac{3kT}{m}}=\sqrt{\frac{3RT}{M}}$$

$M$ 是莫耳質量（kg/mol）。同溫度下，分子越輕跑得越快：氦比氮快。

>! $v_{rms}$ 是統計平均，不是每個分子的速度。氣體中有的分子很慢、有的很快，分布稱為馬克士威與波茲曼的速率分布。

!sim thermo-gas

## 均分定理與比熱

每個二次方的自由度，每個分子平均分到 $\tfrac12kT$。

- 單原子分子：3 個平移自由度，$U=\tfrac32nRT$，$C_V=\tfrac32R$
- 雙原子分子（室溫）：加上 2 個轉動，$U=\tfrac52nRT$，$C_V=\tfrac52R$

這和量測的氣體比熱吻合；溫度很高時振動也啟動，比熱再增加。

## 平均自由徑

分子連續兩次碰撞之間走的平均距離：$\lambda=\dfrac{1}{\sqrt2\,\pi d^2(N/V)}$。常溫常壓下約 $10^{-7}\ \mathrm m$，只比分子大小大幾百倍。
""",
    problems=[
        prob(r"溫度 «T» K 時，氣體分子的平均平移動能是多少 J？（$k=1.381\times10^{-23}\ \mathrm{J/K}$）", 1.5*k_B*300, "J", r"$\overline K=\tfrac32kT=\tfrac32\times1.381\times10^{-23}\times«T»=«ans»\ \mathrm J$。", T=300),
        prob(r"氮氣（莫耳質量 $M=0.028\ \mathrm{kg/mol}$）在 «T» K 時的方均根速率是多少 m/s？", math.sqrt(3*R*300/0.028), "m/s", r"$v_{rms}=\sqrt{\dfrac{3RT}{M}}=\sqrt{\dfrac{3\times8.314\times«T»}{0.028}}=«ans»\ \mathrm{m/s}$。", T=300),
        prob(r"氦氣（$M=0.004\ \mathrm{kg/mol}$）在 «T» K 時的方均根速率是多少 m/s？", math.sqrt(3*R*300/0.004), "m/s", r"$v_{rms}=\sqrt{\dfrac{3RT}{M}}=\sqrt{\dfrac{3\times8.314\times«T»}{0.004}}=«ans»\ \mathrm{m/s}$，比氮快。", T=300),
        prob(r"«n» mol 單原子理想氣體在 «T» K 時的內能是多少 J？", 1.5*2*R*300, "J", r"$U=\tfrac32nRT=\tfrac32\times«n»\times8.314\times«T»=«ans»\ \mathrm J$。", n=2, T=300),
        prob(r"雙原子氣體（室溫）的定容莫耳比熱 $C_V$ 是多少 J/(mol·K)？", 2.5*R, "J/(mol·K)", r"$C_V=\tfrac52R=\tfrac52\times8.314=«ans»$。"),
    ],
    sims=["thermo-gas"],
))

add(Chapter(
    id="second-law", unit="thermo", no=4, title="熱力學第二定律與熵",
    lead="第一定律說能量守恆，第二定律說過程的方向：熱不會自動從冷處流向熱處，熱機效率有上限。",
    body=r"""
## 方向性

打破的杯子不會自己拼回去，熱咖啡不會自己變得更燙。能量守恆（第一定律）允許這些事發生，但自然界不這樣走。第二定律描述這個方向。

**克耳文敘述**：不可能把一個熱源的熱完全變成功而不留下其他影響。
**克勞修斯敘述**：熱不會自發地從低溫物體流向高溫物體。

## 熱機

熱機從高溫熱源吸熱 $Q_H$，對外作功 $W$，剩下的熱 $Q_C$ 排到低溫熱源：$W=Q_H-Q_C$。效率：

$$e=\frac{W}{Q_H}=1-\frac{Q_C}{Q_H}$$

效率不可能是 100%，因為一定要排熱。

## 卡諾熱機

在兩個溫度 $T_H$、$T_C$ 之間運作的熱機，效率有一個上限，由可逆的卡諾循環（兩個等溫加兩個絕熱）達到：

$$e_{\text{卡諾}}=1-\frac{T_C}{T_H}\quad(T\text{ 用 K})$$

!sim thermo-carnot

>! 想提高效率，要提高 $T_H$ 或降低 $T_C$。真實熱機都不可逆，一定低於卡諾效率。

## 冷氣與冷凍機

冷凍機反方向，作功 $W$ 把熱從低溫處抽到高溫處。性能係數（COP）：

$$\text{COP}=\frac{Q_C}{W},\qquad\text{理想：}\ \frac{T_C}{T_H-T_C}$$

## 熵

熵 $S$ 是無序度的量度。可逆過程中：

$$\Delta S=\int\frac{dQ}{T}$$

等溫過程 $\Delta S=\dfrac QT$。

**熵增原理**：孤立系統的總熵永不減少。可逆過程不變，不可逆過程增加。第二定律的另一種說法：宇宙的熵不斷增加。

>! 局部的熵可以減少（冰箱內部變冷、生物變有序），代價是別處熵增加更多，總和還是增加。
""",
    problems=[
        prob(r"熱機吸熱 «QH» J，排熱 «QC» J，效率是多少？（輸入 0 到 1 的小數）", 1-500/800, "", r"$e=1-\dfrac{Q_C}{Q_H}=1-\dfrac{«QC»}{«QH»}=«ans»$。", QH=800, QC=500),
        prob(r"高溫熱源 «TH» K、低溫熱源 «TC» K，卡諾熱機的效率是多少？（輸入 0 到 1 的小數）", 1-300/500, "", r"$e=1-\dfrac{T_C}{T_H}=1-\dfrac{«TC»}{«TH»}=«ans»$。", TH=500, TC=300),
        prob(r"卡諾熱機在 «TH» K 與 «TC» K 之間運作，從高溫熱源吸熱 «QH» J，最多能作功多少 J？", 1000*(1-300/500), "J", r"$W=eQ_H=\left(1-\dfrac{«TC»}{«TH»}\right)\times«QH»=«ans»\ \mathrm J$。", TH=500, TC=300, QH=1000),
        prob(r"使 «m» kg、0°C（273.15 K）的冰可逆地融化成 0°C 的水，熵增加多少 J/K？（$L_f=3.34\times10^5\ \mathrm{J/kg}$）", 1*3.34e5/273.15, "J/K", r"$\Delta S=\dfrac{Q}{T}=\dfrac{mL_f}{T}=\dfrac{«m»\times3.34\times10^5}{273.15}=«ans»\ \mathrm{J/K}$。", m=1),
        prob(r"理想冷凍機把熱從 «TC» K 抽到 «TH» K，性能係數 COP 是多少？", 260/(300-260), "", r"$\text{COP}=\dfrac{T_C}{T_H-T_C}=\dfrac{«TC»}{«TH»-«TC»}=«ans»$。", TC=260, TH=300),
    ],
    sims=["thermo-carnot"],
))
