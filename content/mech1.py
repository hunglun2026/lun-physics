"""力學 1：單位與測量、向量、直線運動、二維運動（拋體與圓周）。"""
import math

from ._lib import Chapter, add, g, pi, c, prob

add(Chapter(
    id="units-measure", unit="mechanics", no=1, title="單位與測量",
    lead="物理量由「數字加單位」組成；學會換算、看量綱、抓有效位數，後面每一章的計算都靠這一章。",
    body=r"""
## 為什麼先談單位

物理在描述「量」，一個量一定是數字加單位，例如 $12\ \mathrm{m}$ 不是 $12$。單位寫錯，答案就錯，而且常常錯得很離譜。

國際單位制（SI）有七個基本單位，普通物理常用其中四個：

- 長度：公尺（m）
- 質量：公斤（kg）
- 時間：秒（s）
- 電流：安培（A）

其他單位都由它們組合而成，例如速度是 $\mathrm{m/s}$，力是 $\mathrm{kg\cdot m/s^2}$，我們稱它為牛頓（N）。

## 單位換算

換算的方法是乘以「等於 1 的分數」。要把 $90\ \mathrm{km/h}$ 換成 $\mathrm{m/s}$：

$$90\ \frac{\mathrm{km}}{\mathrm{h}}\times\frac{1000\ \mathrm{m}}{1\ \mathrm{km}}\times\frac{1\ \mathrm{h}}{3600\ \mathrm{s}}=25\ \frac{\mathrm{m}}{\mathrm{s}}$$

寫出每一個分數，你就不會把乘法和除法搞反。

> 記一個速成：$\mathrm{km/h}$ 除以 $3.6$ 就是 $\mathrm{m/s}$。

## 量綱分析

等號兩邊的量綱（長度 $L$、質量 $M$、時間 $T$ 的組合）一定要相同。用它可以檢查公式有沒有寫錯：位移 $x=\tfrac12 a t^2$，右邊是 $\dfrac{L}{T^2}\cdot T^2=L$，跟左邊一致，這個公式量綱合理。

>! 量綱對不代表公式對（係數 $\tfrac12$ 量綱檢查不出來），但量綱不對一定是錯的。

## 有效位數

測量結果只能到儀器的精度。計算時：

- 乘除：結果的有效位數取決於有效位數最少的那個數
- 加減：結果的小數位數取決於小數位數最少的那個數
- 中間過程多留一兩位，只在最後答案四捨五入

## 數量級估算

估算只求「差不多是幾位數」，例如一個人一生心跳約幾次。把問題拆成容易估的小塊再相乘，這叫費米估算。答案對到 10 倍以內就算成功。
""",
    problems=[
        prob(r"一輛車以 «v:3» km/h 行駛，速度是多少 m/s？", 108/3.6, "m/s",
             r"$«v» \times \dfrac{1000}{3600} = «ans»\ \mathrm{m/s}$", hint=r"除以 $3.6$。", v=108),
        prob(r"鐵的密度約 «d» g/cm³，換算成 kg/m³ 是多少？", 7.87*1000, "kg/m³",
             r"$1\ \mathrm{g/cm^3}=1000\ \mathrm{kg/m^3}$，所以 $«d»\times1000=«ans»\ \mathrm{kg/m^3}$。", d=7.87),
        prob(r"長方形長 «a» m、寬 «b» m（各量到小數第二位與第一位），面積用有效位數規則應寫成多少 m²？答案以兩位有效位數輸入。",
             2.8, "m²",
             r"$«a»\times«b»=«p»$，寬只有 2 位有效位數，所以結果取 2 位：$2.8\ \mathrm{m^2}$。", a=2.35, b=1.2, p=2.35*1.2),
        prob(r"一個人心跳每分鐘 «r» 次，活到 «y» 歲，一生心跳約幾次？（一年取 365 天）", 70*60*24*365*80, "次",
             r"$«r»\times60\times24\times365\times«y» = «ans»$ 次，約 $3\times10^9$。", r=70, y=80, tol=0.05),
        prob(r"一光年是光在真空中一年走的距離。取 $c=2.998\times10^8\ \mathrm{m/s}$、一年 $3.156\times10^7\ \mathrm{s}$，一光年約多少公尺？",
             2.998e8*3.156e7, "m",
             r"$c\times t = 2.998\times10^8\times3.156\times10^7 = «ans»\ \mathrm{m}$。"),
    ],
))

add(Chapter(
    id="vectors", unit="mechanics", no=2, title="向量",
    lead="有大小又有方向的量要用向量；會分解、會相加、會算內積外積，力學與電磁學都用得到。",
    body=r"""
## 純量與向量

只有大小的量是**純量**，例如質量、時間、溫度。有大小也有方向的量是**向量**，例如位移、速度、力。向量在文字裡用 $\vec{A}$ 表示，大小寫成 $|\vec{A}|$ 或 $A$。

## 分量

把向量投影到座標軸上，得到分量。大小為 $A$、與 $x$ 軸夾角 $\theta$ 的向量：

$$A_x = A\cos\theta,\qquad A_y = A\sin\theta$$

反過來，由分量求大小與方向：

$$A=\sqrt{A_x^2+A_y^2},\qquad \theta=\arctan\frac{A_y}{A_x}$$

>! 用 $\arctan$ 時要看分量的正負決定象限。計算機給出的角度只在 $-90^\circ$ 到 $90^\circ$ 之間。

## 向量相加

相加最可靠的方法是分量法：$x$ 分量加 $x$ 分量，$y$ 分量加 $y$ 分量。

$$\vec{C}=\vec{A}+\vec{B}\ \Rightarrow\ C_x=A_x+B_x,\quad C_y=A_y+B_y$$

## 內積（點積）

兩向量的內積得到一個純量，用來求「一個向量在另一個方向上有多少」，之後會用在功：

$$\vec{A}\cdot\vec{B}=AB\cos\theta=A_xB_x+A_yB_y+A_zB_z$$

兩向量垂直時內積為 $0$。

## 外積（叉積）

外積得到另一個向量，方向由右手定則決定，大小為：

$$|\vec{A}\times\vec{B}|=AB\sin\theta$$

之後的力矩、角動量、磁力都是外積。注意 $\vec{A}\times\vec{B}=-\vec{B}\times\vec{A}$，順序不能換。
""",
    problems=[
        prob(r"一個大小 «A» m 的位移，與 $x$ 軸夾 «t»°。它的 $x$ 分量是多少 m？", 10*math.cos(math.radians(30)), "m",
             r"$A_x=A\cos\theta=«A»\cos«t»^\circ=«ans»\ \mathrm{m}$。", A=10, t=30),
        prob(r"$\vec{A}=(3,4)$、$\vec{B}=(-1,2)$，求 $|\vec{A}+\vec{B}|$。", math.hypot(2, 6), "",
             r"$\vec{A}+\vec{B}=(2,6)$，大小 $=\sqrt{2^2+6^2}=«ans»$。"),
        prob(r"$\vec{A}+\vec{B}=(2,6)$，它與 $x$ 軸的夾角是幾度？", math.degrees(math.atan2(6, 2)), "度",
             r"$\theta=\arctan(6/2)=«ans»^\circ$，兩個分量都為正，在第一象限。"),
        prob(r"$\vec{A}=(2,3,1)$、$\vec{B}=(4,-1,2)$，求內積 $\vec{A}\cdot\vec{B}$。", 2*4 + 3*(-1) + 1*2, "",
             r"$2\times4+3\times(-1)+1\times2=«ans»$。"),
        prob(r"兩向量大小分別為 «A» 與 «B»，夾角 «t»°，求外積的大小。", 3*4*math.sin(math.radians(30)), "",
             r"$AB\sin\theta=«A»\times«B»\times\sin«t»^\circ=«ans»$。", A=3, B=4, t=30),
    ],
))

add(Chapter(
    id="motion-1d", unit="mechanics", no=3, title="直線運動",
    lead="位置、速度、加速度三者的關係，以及等加速度運動的四條公式，自由落體是它最重要的例子。",
    body=r"""
## 位置、速度、加速度

物體沿一條直線運動時，用位置 $x(t)$ 描述。

- 平均速度：$\bar v=\dfrac{\Delta x}{\Delta t}$
- 瞬時速度：$v=\dfrac{dx}{dt}$，也就是位置對時間的斜率
- 加速度：$a=\dfrac{dv}{dt}$，也就是速度對時間的斜率

>! 速度（velocity）有方向、可正可負；速率（speed）是速度的大小，永遠不為負。位移和路徑長也不同：繞操場一圈，位移是 $0$。

## 等加速度運動

加速度固定時，這四條公式涵蓋所有情況：

$$v = v_0 + at$$
$$x - x_0 = v_0 t + \tfrac12 a t^2$$
$$v^2 = v_0^2 + 2a(x-x_0)$$
$$x - x_0 = \tfrac12 (v_0+v)\,t$$

解題時先列出已知量，看哪一條公式剛好缺你不需要的那個量，就用那一條。

## 自由落體

忽略空氣阻力時，所有物體的加速度都是 $g=9.8\ \mathrm{m/s^2}$，向下。取向上為正時 $a=-g$。物體往上丟到最高點時速度為 $0$，但加速度仍是 $-g$。

!sim mech-motion1d

## 讀圖

- $x$-$t$ 圖的斜率是速度
- $v$-$t$ 圖的斜率是加速度，曲線下的面積是位移
""",
    problems=[
        prob(r"車子從靜止起步，«t» s 內加速到 «v» m/s，求這段時間內行駛的距離（m）。", 0.5*27*6, "m",
             r"等加速度：$x=\tfrac12(v_0+v)t=\tfrac12(0+«v»)\times«t»=«ans»\ \mathrm{m}$。", v=27, t=6),
        prob(r"車子以 «v0» m/s 行駛，緊急煞車的加速度大小為 «a» m/s²，求停下前滑行的距離（m）。", 20**2/(2*5), "m",
             r"$v^2=v_0^2-2ad$，$v=0$，所以 $d=\dfrac{v_0^2}{2a}=\dfrac{«v0»^2}{2\times«a»}=«ans»\ \mathrm{m}$。", v0=20, a=5),
        prob(r"物體從 «h» m 高處自由落下，落地需要幾秒？取 $g=9.8\ \mathrm{m/s^2}$。", math.sqrt(2*45/g), "s",
             r"$h=\tfrac12 g t^2\Rightarrow t=\sqrt{2h/g}=\sqrt{2\times«h»/9.8}=«ans»\ \mathrm{s}$。", h=45),
        prob(r"以 «v0» m/s 的初速向上拋球，球能升到多高（m）？取 $g=9.8$。", 15**2/(2*g), "m",
             r"最高點 $v=0$：$0=v_0^2-2gh\Rightarrow h=\dfrac{v_0^2}{2g}=\dfrac{«v0»^2}{2\times9.8}=«ans»\ \mathrm{m}$。", v0=15),
        prob(r"甲以 «v» m/s 等速前進，乙在同地點同時由靜止出發，加速度 «a» m/s²。乙經過幾秒追上甲？", 2*10/2, "s",
             r"追上時位置相同：$vt=\tfrac12 a t^2\Rightarrow t=\dfrac{2v}{a}=\dfrac{2\times«v»}{«a»}=«ans»\ \mathrm{s}$。", v=10, a=2),
    ],
    sims=["mech-motion1d"],
))

add(Chapter(
    id="motion-2d", unit="mechanics", no=4, title="二維運動與拋體",
    lead="把二維運動拆成互不干擾的水平與鉛直兩個一維運動，就能處理拋體；再加上等速圓周運動與相對運動。",
    body=r"""
## 二維運動的核心想法

位置、速度、加速度都變成向量。最重要的觀念是：$x$ 方向和 $y$ 方向的運動可以**分開算**，兩邊只共用同一個時間 $t$。

## 拋體運動

忽略空氣阻力，只受重力。以初速 $v_0$、仰角 $\theta$ 拋出：

- 水平方向（等速）：$v_x=v_0\cos\theta$，$x=v_0\cos\theta\cdot t$
- 鉛直方向（加速度 $-g$）：$v_y=v_0\sin\theta-gt$，$y=v_0\sin\theta\cdot t-\tfrac12 g t^2$

由此可得兩個常用結果（落回同一高度時）：

$$H=\frac{v_0^2\sin^2\theta}{2g}\ (\text{最大高度}),\qquad R=\frac{v_0^2\sin 2\theta}{g}\ (\text{水平射程})$$

!sim mech-projectile

>! 在最高點，鉛直速度是 $0$，但水平速度不是 $0$。速度的水平分量從頭到尾都不變。

射程在 $\theta=45^\circ$ 最大，而 $\theta$ 與 $90^\circ-\theta$ 的射程相同。

## 等速圓周運動

速率固定但方向一直在變，所以有加速度，方向指向圓心，稱為向心加速度：

$$a_c=\frac{v^2}{r}=\frac{4\pi^2 r}{T^2}$$

## 相對速度

「對地面的速度」等於「對移動參考系的速度」加上「該參考系對地面的速度」：$\vec v_{\text{對地}}=\vec v_{\text{對水}}+\vec v_{\text{水對地}}$。向量要用分量法相加。
""",
    problems=[
        prob(r"以 «v0» m/s、仰角 «t»° 拋出，落回同一高度，水平射程是多少 m？取 $g=9.8$。", 20**2*math.sin(math.radians(60))/g, "m",
             r"$R=\dfrac{v_0^2\sin2\theta}{g}=\dfrac{«v0»^2\sin(2\times«t»^\circ)}{9.8}=«ans»\ \mathrm{m}$。", v0=20, t=30),
        prob(r"以 «v0» m/s、仰角 «t»° 拋出，最大高度是多少 m？", (20*math.sin(math.radians(53)))**2/(2*g), "m",
             r"$v_{0y}=«v0»\sin«t»^\circ$，$H=\dfrac{v_{0y}^2}{2g}=«ans»\ \mathrm{m}$。", v0=20, t=53),
        prob(r"從 «h» m 高的懸崖以 «v» m/s 水平射出，水平飛行多遠（m）？取 $g=9.8$。", 15*math.sqrt(2*80/g), "m",
             r"落地時間 $t=\sqrt{2h/g}=\sqrt{2\times«h»/9.8}=«tt»\ \mathrm{s}$，水平距離 $x=vt=«v»\times«tt»=«ans»\ \mathrm{m}$。",
             h=80, v=15, tt=math.sqrt(2*80/g)),
        prob(r"半徑 «r» m 的圓周，繞一圈需 «T» s，等速率，向心加速度是多少 m/s²？", 4*pi**2*0.5/2**2, "m/s²",
             r"$a_c=\dfrac{4\pi^2 r}{T^2}=\dfrac{4\pi^2\times«r»}{«T»^2}=«ans»\ \mathrm{m/s^2}$。", r=0.5, T=2),
        prob(r"船以相對水 «vb» m/s 的速率垂直河岸划行，河水流速 «vr» m/s，船相對岸的速率是多少 m/s？", math.hypot(4, 3), "m/s",
             r"兩個垂直分量：$\sqrt{«vb»^2+«vr»^2}=«ans»\ \mathrm{m/s}$。", vb=4, vr=3),
    ],
    sims=["mech-projectile"],
))
