"""力學 3：轉動、角動量、靜力平衡、萬有引力、流體。"""
import math

from ._lib import G, M_E, R_E, Chapter, add, g, pi, prob

add(Chapter(
    id="rotation", unit="mechanics", no=10, title="定軸轉動",
    lead="轉動的每個量都對應直線運動的一個量：角位移、角速度、角加速度、轉動慣量與力矩。",
    body=r"""
## 角量

物體繞固定軸轉動，用角度 $\theta$（單位弧度，rad）描述位置。

- 角速度 $\omega=\dfrac{d\theta}{dt}$，單位 rad/s
- 角加速度 $\alpha=\dfrac{d\omega}{dt}$，單位 rad/s²

$2\pi\ \mathrm{rad}=360^\circ$，轉速 $n$ rpm 換成角速度：$\omega=\dfrac{2\pi n}{60}$。

距轉軸 $r$ 處的線速率與切線加速度：$v=r\omega$，$a_t=r\alpha$。

## 與直線運動對照

角加速度固定時，公式與直線運動完全對應：

$$\omega=\omega_0+\alpha t,\qquad \theta=\omega_0t+\tfrac12\alpha t^2,\qquad \omega^2=\omega_0^2+2\alpha\theta$$

## 轉動慣量

轉動慣量 $I$ 是物體抗拒轉動變化的程度，扮演質量的角色：

$$I=\sum m_ir_i^2$$

質量離轉軸越遠，$I$ 越大。常見形狀（繞通過質心的軸）：

- 實心圓盤或圓柱：$I=\tfrac12MR^2$
- 薄圓環：$I=MR^2$
- 實心球：$I=\tfrac25MR^2$
- 細桿（繞中心）：$I=\tfrac1{12}ML^2$

## 力矩

力造成轉動的效果叫力矩：

$$\vec\tau=\vec r\times\vec F,\qquad |\tau|=rF\sin\phi$$

轉動的牛頓第二定律：

$$\sum\tau=I\alpha$$

>! 力矩要看力臂，也就是力的作用線到轉軸的垂直距離。力沿著轉軸方向推，力矩是 $0$。

## 轉動動能與滾動

$$K_{\text{rot}}=\tfrac12I\omega^2$$

不打滑的滾動 $v_{cm}=R\omega$，總動能 $=\tfrac12Mv_{cm}^2+\tfrac12I\omega^2$。所以同一個斜坡上，質量集中在中心的物體滾得快（分到轉動動能比較少）。
""",
    problems=[
        prob(r"轉速 «n» rpm，角速度是多少 rad/s？", 3000*2*pi/60, "rad/s", r"$\omega=\dfrac{2\pi n}{60}=\dfrac{2\pi\times«n»}{60}=«ans»\ \mathrm{rad/s}$。", n=3000),
        prob(r"飛輪從靜止開始，以 «a» rad/s² 的角加速度轉了 «t» s，轉過的角度是多少 rad？", 0.5*4*5**2, "rad", r"$\theta=\tfrac12\alpha t^2=\tfrac12\times«a»\times«t»^2=«ans»\ \mathrm{rad}$。", a=4, t=5),
        prob(r"質量 «M» kg、半徑 «R» m 的實心圓盤，繞中心軸的轉動慣量是多少 kg·m²？", 0.5*2*0.3**2, "kg·m²", r"$I=\tfrac12MR^2=\tfrac12\times«M»\times«R»^2=«ans»\ \mathrm{kg\cdot m^2}$。", M=2, R=0.3),
        prob(r"在距轉軸 «r» m 處施 «F» N 的垂直力，物體轉動慣量 «I» kg·m²，角加速度是多少 rad/s²？", 30*0.4/0.6, "rad/s²", r"$\tau=rF=«r»\times«F»=12\ \mathrm{N\cdot m}$，$\alpha=\tau/I=12/«I»=«ans»\ \mathrm{rad/s^2}$。", r=0.4, F=30, I=0.6),
        prob(r"實心圓柱從高 «h» m 的斜面靜止無滑動滾下，到底部質心速率是多少 m/s？", math.sqrt(4*g*2/3), "m/s",
             r"$Mgh=\tfrac12Mv^2+\tfrac12(\tfrac12MR^2)(v/R)^2=\tfrac34Mv^2$，所以 $v=\sqrt{\tfrac43gh}=\sqrt{\tfrac43\times9.8\times«h»}=«ans»\ \mathrm{m/s}$。", h=2),
    ],
))

add(Chapter(
    id="angular-momentum", unit="mechanics", no=11, title="角動量",
    lead="角動量是轉動版的動量；沒有外力矩時它守恆，溜冰選手收手轉得更快就是這個道理。",
    body=r"""
## 定義

質點的角動量：

$$\vec L=\vec r\times\vec p,\qquad |L|=mvr\sin\phi$$

繞定軸轉動的剛體：

$$L=I\omega$$

單位是 $\mathrm{kg\cdot m^2/s}$。

## 力矩改變角動量

$$\sum\vec\tau=\frac{d\vec L}{dt}$$

對照直線運動的 $\sum\vec F=d\vec p/dt$。力矩作用一段時間 $\Delta t$，角動量改變 $\tau\,\Delta t$（定軸、$\tau$ 固定時）。

## 角動量守恆

外力矩的總和為零時，角動量不變：

$$I_i\omega_i=I_f\omega_f$$

- 溜冰選手收攏手臂：$I$ 變小，$\omega$ 變大
- 跳水選手縮成一團翻轉，伸直入水
- 人跳上旋轉的圓盤：碰撞過程角動量守恆，不是動能守恆

>! 角動量守恆時，轉動動能通常不守恆。收手時選手作功，動能增加；人跳上圓盤是非彈性過程，動能減少。

## 為什麼行星軌道上近日點跑得快

太陽的引力指向太陽，對行星的力矩為零，所以角動量守恆：$mvr$ 固定，$r$ 小時 $v$ 大。這也等價於克卜勒第二定律（等面積定律）。

!sim mech-orbit

## 進動（了解即可）

陀螺的轉軸會繞鉛直軸慢慢轉動，這是力矩改變角動量的「方向」造成的：$d\vec L=\vec\tau\,dt$，所以 $\vec L$ 會往力矩的方向偏。
""",
    problems=[
        prob(r"轉動慣量 «I» kg·m² 的物體以 «w» rad/s 轉動，角動量是多少 kg·m²/s？", 0.5*10, "kg·m²/s", r"$L=I\omega=«I»\times«w»=«ans»$。", I=0.5, w=10),
        prob(r"溜冰選手手臂張開時 $I_1=«I1»\ \mathrm{kg\cdot m^2}$、角速度 «w1» rad/s，收攏手臂後 $I_2=«I2»\ \mathrm{kg\cdot m^2}$，新的角速度是多少 rad/s？", 4*2/1.6, "rad/s", r"$I_1\omega_1=I_2\omega_2\Rightarrow\omega_2=\dfrac{«I1»\times«w1»}{«I2»}=«ans»\ \mathrm{rad/s}$。", I1=4, w1=2, I2=1.6),
        prob(r"質量 «m» kg 的質點以 «v» m/s 的速率運動，運動方向與位置向量垂直，位置向量長 «r» m，角動量是多少 kg·m²/s？", 2*3*4, "kg·m²/s", r"$L=mvr\sin90^\circ=«m»\times«v»\times«r»=«ans»$。", m=2, v=3, r=4),
        prob(r"轉動慣量 «I» kg·m² 的靜止物體受到固定力矩 «tau» N·m 作用 «t» s，角速度變為多少 rad/s？", 5*3/2, "rad/s", r"$\tau t=\Delta L=I\omega\Rightarrow\omega=\dfrac{\tau t}{I}=\dfrac{«tau»\times«t»}{«I»}=«ans»\ \mathrm{rad/s}$。", I=2, tau=5, t=3),
        prob(r"轉動慣量 «I» kg·m² 的圓盤以 «w» rad/s 轉動，質量 «m» kg 的小孩輕輕跳上邊緣（半徑 «r» m），小孩原本靜止，之後的角速度是多少 rad/s？", 200*1.5/(200+30*2**2), "rad/s",
             r"$I\omega=(I+mr^2)\omega'$，$\omega'=\dfrac{«I»\times«w»}{«I»+«m»\times«r»^2}=«ans»\ \mathrm{rad/s}$。", I=200, w=1.5, m=30, r=2),
    ],
    sims=["mech-orbit"],
))

add(Chapter(
    id="equilibrium", unit="mechanics", no=12, title="靜力平衡與彈性",
    lead="物體保持靜止的條件是合力為零且合力矩為零；再加上固體受力後怎麼變形。",
    body=r"""
## 平衡的兩個條件

物體保持靜止（或等速）需要：

$$\sum\vec F=0\quad\text{且}\quad\sum\vec\tau=0$$

平面問題有三條方程式：$\sum F_x=0$、$\sum F_y=0$、$\sum\tau=0$（對任一點）。

## 解題技巧

- 力矩的轉軸可以選在**任何一點**，選在未知力的作用點，這個力的力矩就是 $0$，方程式變簡單
- 均勻物體的重力視為作用在質心（幾何中心）
- 支撐力、繩的張力、牆壁的反作用力都要畫進受力圖

>! 「物體不動」不代表只要合力為零。合力為零但力矩不為零，物體會轉起來。

## 質心

$$x_{cm}=\frac{\sum m_ix_i}{\sum m_i}$$

物體的支撐點在質心的正下方時才能穩定。

## 彈性

固體受力會變形。

- 應力（單位面積受力）：$\sigma=\dfrac FA$
- 應變（相對變形）：$\varepsilon=\dfrac{\Delta L}{L}$
- 楊氏模數：$E=\dfrac{\sigma}{\varepsilon}$，所以 $\Delta L=\dfrac{FL}{AE}$

在彈性限度內，應力與應變成正比（虎克定律的材料版）。超過限度就會永久變形，再超過就斷裂。

鋼的 $E\approx2.0\times10^{11}\ \mathrm{Pa}$，所以鋼很硬，拉一下幾乎不伸長。
""",
    problems=[
        prob(r"蹺蹺板兩側，一邊 «m1» kg 的小孩坐在距支點 «d1» m 處，另一邊 «m2» kg 的人要坐在距支點多少 m 才能平衡？", 40*2/50, "m", r"$m_1d_1=m_2d_2\Rightarrow d_2=\dfrac{«m1»\times«d1»}{«m2»}=«ans»\ \mathrm{m}$。", m1=40, d1=2, m2=50),
        prob(r"長 «L» m、質量 «M» kg 的均勻橫樑，兩端各有支撐。距左端 «x» m 處放一個 «W» kg 的物體，右端支撐力是多少 N？取 $g=9.8$。", (20*g*2+50*g*1)/4, "N",
             r"對左端取力矩：$N_R L=Mg\dfrac L2+Wg\,x\Rightarrow N_R=\dfrac{«M»\times9.8\times2+«W»\times9.8\times«x»}{«L»}=«ans»\ \mathrm{N}$。", L=4, M=20, x=1, W=50),
        prob(r"質量 «m» kg 的物體由兩條對稱的纜繩吊著，每條纜繩與水平夾 «t»°，每條纜繩的張力是多少 N？", 20*g/(2*math.sin(math.radians(30))), "N",
             r"鉛直方向：$2T\sin\theta=mg\Rightarrow T=\dfrac{mg}{2\sin\theta}=\dfrac{«m»\times9.8}{2\sin«t»^\circ}=«ans»\ \mathrm{N}$。", m=20, t=30),
        prob(r"鋼線長 «L» m、截面積 «A» m²，楊氏模數 $E=2.0\times10^{11}$ Pa，受 «F» N 拉力，伸長多少 mm？", 200*2/(1e-6*2e11)*1000, "mm",
             r"$\Delta L=\dfrac{FL}{AE}=\dfrac{«F»\times«L»}{«A»\times2.0\times10^{11}}=2.0\times10^{-3}\ \mathrm{m}=«ans»\ \mathrm{mm}$。", L=2, A=1e-6, F=200),
        prob(r"質量 «m1» kg 的質點在 $x=0$，質量 «m2» kg 的質點在 $x=«x2»$ m，質心在哪個位置（m）？", (2*0+3*5)/(2+3), "m", r"$x_{cm}=\dfrac{«m1»\times0+«m2»\times«x2»}{«m1»+«m2»}=«ans»\ \mathrm{m}$。", m1=2, m2=3, x2=5),
    ],
))

add(Chapter(
    id="gravitation", unit="mechanics", no=13, title="萬有引力",
    lead="任何兩個質量之間都有引力；從蘋果落地到衛星軌道、克卜勒三定律，都是同一條定律。",
    body=r"""
## 牛頓萬有引力定律

兩個質點之間的引力大小：

$$F=\frac{GMm}{r^2}$$

$G=6.674\times10^{-11}\ \mathrm{N\cdot m^2/kg^2}$。力是相吸的，且互為作用與反作用。

本章用地球質量 $M_E=5.972\times10^{24}\ \mathrm{kg}$、半徑 $R_E=6.371\times10^6\ \mathrm{m}$。

## 重力加速度

在離地心 $r$ 處，$g(r)=\dfrac{GM_E}{r^2}$。在地表 $r=R_E$，$g\approx9.8\ \mathrm{m/s^2}$。高度越高，$g$ 越小，但在近地軌道（約 400 km）仍有約 $8.7\ \mathrm{m/s^2}$。

>! 太空站上的人「無重力」不是因為那裡沒有引力，而是太空站與人一起繞地球自由落下，沒有東西把人頂在地板上。

## 圓軌道

引力提供向心力：$\dfrac{GMm}{r^2}=\dfrac{mv^2}{r}$，所以：

$$v=\sqrt{\frac{GM}{r}},\qquad T=2\pi\sqrt{\frac{r^3}{GM}}$$

## 克卜勒三定律

- 行星軌道是橢圓，太陽在一個焦點
- 行星與太陽的連線在相同時間掃過相同面積（角動量守恆）
- 週期的平方與半長軸的立方成正比：$T^2\propto a^3$

## 重力位能與脫離速度

引力位能（零點在無窮遠）：

$$U=-\frac{GMm}{r}$$

總能量 $E=K+U<0$ 是被束縛的軌道。要脫離地球，總能量至少為 $0$：

$$\tfrac12mv^2=\frac{GMm}{R}\ \Rightarrow\ v_{esc}=\sqrt{\frac{2GM}{R}}\approx11.2\ \mathrm{km/s}$$
""",
    problems=[
        prob(r"質量 «m» kg 的人站在地表，地球對他的引力是多少 N？（用本章的 $G$、$M_E$、$R_E$）", G*M_E*70/R_E**2, "N", r"$F=\dfrac{GM_Em}{R_E^2}=\dfrac{6.674\times10^{-11}\times5.972\times10^{24}\times«m»}{(6.371\times10^6)^2}=«ans»\ \mathrm{N}$。", m=70),
        prob(r"高度 «h» km 處的重力加速度是多少 m/s²？", G*M_E/(R_E+400e3)**2, "m/s²", r"$g=\dfrac{GM_E}{(R_E+h)^2}=\dfrac{GM_E}{(6.371\times10^6+«h»\times10^3)^2}=«ans»\ \mathrm{m/s^2}$。", h=400),
        prob(r"高度 «h» km 的圓軌道，衛星速率是多少 m/s？", math.sqrt(G*M_E/(R_E+400e3)), "m/s", r"$v=\sqrt{\dfrac{GM_E}{R_E+h}}=«ans»\ \mathrm{m/s}$（約 $7.7\ \mathrm{km/s}$）。", h=400),
        prob(r"軌道半徑 «r» m（距地心）的衛星，繞地球一圈要幾小時？", 2*pi*math.sqrt(4.22e7**3/(G*M_E))/3600, "小時", r"$T=2\pi\sqrt{\dfrac{r^3}{GM_E}}=«T»\ \mathrm{s}=«ans»\ \mathrm{h}$，接近 24 小時，這就是同步衛星。", r=4.22e7, T=2*pi*math.sqrt(4.22e7**3/(G*M_E))),
        prob(r"地球的脫離速度是多少 m/s？", math.sqrt(2*G*M_E/R_E), "m/s", r"$v_{esc}=\sqrt{\dfrac{2GM_E}{R_E}}=«ans»\ \mathrm{m/s}$。"),
    ],
))

add(Chapter(
    id="fluids", unit="mechanics", no=14, title="流體",
    lead="靜止流體的壓力隨深度增加，浮力等於排開流體的重；流動時，流速越快壓力越小。",
    body=r"""
## 密度與壓力

密度 $\rho=\dfrac mV$，水約 $1000\ \mathrm{kg/m^3}$。壓力是單位面積受的垂直力：

$$P=\frac FA,\qquad 1\ \mathrm{Pa}=1\ \mathrm{N/m^2}$$

大氣壓約 $1.01\times10^5\ \mathrm{Pa}$。

## 靜止流體的壓力

流體內深度 $h$ 處的壓力：

$$P=P_0+\rho gh$$

$\rho gh$ 叫錶壓（比大氣壓多出來的部分）。壓力只跟**深度**有關，跟容器形狀無關。

**帕斯卡原理**：施在密閉流體上的壓力會原封不動傳到各處。油壓千斤頂利用它：$\dfrac{F_1}{A_1}=\dfrac{F_2}{A_2}$，小力在小面積換成大力在大面積。

## 浮力

浮力等於物體排開流體的重量（阿基米德原理）：

$$F_B=\rho_{\text{流體}}\,V_{\text{排開}}\,g$$

浮在水面的物體，浮力等於自身重量，所以浸入體積的比例是 $\dfrac{V_{\text{浸}}}{V}=\dfrac{\rho_{\text{物}}}{\rho_{\text{流體}}}$。

>! 浮力的大小只看排開的流體體積，不看物體多重。同樣大小的鐵塊與木塊全浸在水中時，浮力相同。

## 流體的流動

理想流體（不可壓縮、無黏滯）：

- **連續方程式**：$A_1v_1=A_2v_2$，管子變細流速變快
- **白努利方程式**：沿流線 $P+\tfrac12\rho v^2+\rho gy=\text{定值}$

白努利說明：同一高度，流速越快壓力越小。這就是飛機機翼產生升力、噴霧器吸水的原因。
""",
    problems=[
        prob(r"水下 «h» m 深處的錶壓是多少 Pa？水的密度取 $1000\ \mathrm{kg/m^3}$，$g=9.8$。", 1000*g*10, "Pa", r"$P=\rho gh=1000\times9.8\times«h»=«ans»\ \mathrm{Pa}$。", h=10),
        prob(r"油壓千斤頂小活塞面積 «A1» m²、大活塞面積 «A2» m²。小活塞上施 «F1» N，大活塞能舉起多大的力（N）？", 200*0.5/0.01, "N", r"$F_2=F_1\dfrac{A_2}{A_1}=«F1»\times\dfrac{«A2»}{«A1»}=«ans»\ \mathrm{N}$。", A1=0.01, A2=0.5, F1=200),
        prob(r"邊長 «a» m 的立方體完全浸沒在水中，受到的浮力是多少 N？", 1000*g*0.2**3, "N", r"$F_B=\rho gV=1000\times9.8\times«a»^3=«ans»\ \mathrm{N}$。", a=0.2),
        prob(r"密度 «rho» kg/m³ 的木塊浮在水面（水 $1000\ \mathrm{kg/m^3}$），體積有多少比例浸在水裡？（輸入 0 到 1 的小數）", 600/1000, "", r"浮力等於重量：$\dfrac{V_{\text{浸}}}{V}=\dfrac{\rho_{\text{木}}}{\rho_{\text{水}}}=\dfrac{«rho»}{1000}=«ans»$。", rho=600),
        prob(r"水管內徑從 «d1» cm 縮到 «d2» cm，粗的地方流速 «v1» m/s，細的地方比粗的地方壓力小多少 Pa？（水 $1000\ \mathrm{kg/m^3}$）", 0.5*1000*((2*(10/5)**2)**2-2**2), "Pa",
             r"連續方程式：$v_2=v_1(d_1/d_2)^2=«v1»\times(«d1»/«d2»)^2=8\ \mathrm{m/s}$；白努利：$\Delta P=\tfrac12\rho(v_2^2-v_1^2)=\tfrac12\times1000\times(64-4)=«ans»\ \mathrm{Pa}$。", d1=10, d2=5, v1=2),
    ],
))
