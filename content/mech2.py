"""力學 2：牛頓定律、牛頓定律的應用、功與動能、位能與能量守恆、動量與碰撞。"""
import math

from ._lib import Chapter, add, g, pi, prob

rad = math.radians

add(Chapter(
    id="newton-laws", unit="mechanics", no=5, title="牛頓運動定律",
    lead="力改變運動狀態：三條定律加上受力圖，是解決所有力學問題的起點。",
    body=r"""
## 三條定律

**第一定律（慣性）**：合力為零時，靜止的物體保持靜止，運動的物體保持等速直線運動。

**第二定律**：物體的加速度與合力成正比、與質量成反比，方向和合力相同：

$$\sum\vec F = m\vec a$$

力的單位是牛頓：$1\ \mathrm{N}=1\ \mathrm{kg\cdot m/s^2}$。

**第三定律（作用與反作用）**：A 對 B 施力，B 同時對 A 施一個大小相等、方向相反的力。

>! 作用力與反作用力作用在**不同的物體**上，所以不會互相抵消。分析一個物體時，只算「別人對它」的力。

## 質量與重量

質量 $m$ 是物體的慣性，到哪裡都一樣。重量是重力的大小：

$$W = mg$$

同一個人在月球質量不變，重量只剩約六分之一，因為月球表面 $g\approx1.62\ \mathrm{m/s^2}$。

## 解題標準流程

- 選一個研究對象，畫出**受力圖**（只畫別人對它的力）
- 選座標軸，把每個力分解成分量
- 每個軸分別寫 $\sum F=ma$
- 解聯立，最後檢查單位與方向合不合理

## 常見的力

- 重力 $mg$，向下
- 正向力 $N$，垂直接觸面，大小由方程式解出，不一定等於 $mg$
- 張力 $T$，沿繩子方向，繩子輕且不計摩擦時全繩相等
- 摩擦力 $f$，平行接觸面（下一章細談）

> 電梯加速向上時你覺得變重：體重計讀數是正向力 $N=m(g+a)$，不是你的重力變了。
""",
    problems=[
        prob(r"質量 «m» kg 的車以 «a» m/s² 加速，所需合力是多少 N？", 1500*2.0, "N", r"$F=ma=«m»\times«a»=«ans»\ \mathrm{N}$。", m=1500, a=2.0),
        prob(r"一個 «m» kg 的物體同時受到向東 «F1» N 與向北 «F2» N 的力，加速度大小是多少 m/s²？", math.hypot(30, 40)/5, "m/s²",
             r"合力 $=\sqrt{«F1»^2+«F2»^2}=50\ \mathrm{N}$，$a=F/m=50/«m»=«ans»\ \mathrm{m/s^2}$。", m=5, F1=30, F2=40),
        prob(r"一個人質量 «m» kg，在月球表面（$g=1.62\ \mathrm{m/s^2}$）的重量是多少 N？", 60*1.62, "N", r"$W=mg=«m»\times1.62=«ans»\ \mathrm{N}$。", m=60),
        prob(r"質量 «m» kg 的人站在電梯裡的體重計上，電梯以 «a» m/s² 加速向上，體重計讀數（正向力）是多少 N？取 $g=9.8$。", 70*(g+1.5), "N",
             r"向上為正：$N-mg=ma\Rightarrow N=m(g+a)=«m»\times(9.8+«a»)=«ans»\ \mathrm{N}$。", m=70, a=1.5),
        prob(r"光滑水平面上，用 «F» N 的水平力推 «m1» kg 與 «m2» kg 兩木塊（推 «m1» kg 那塊，兩塊接觸），«m2» kg 那塊受到的接觸力是多少 N？", 20*6/(4+6), "N",
             r"整體 $a=F/(m_1+m_2)=«F»/10=2\ \mathrm{m/s^2}$；對 «m2» kg 那塊：$N=m_2a=«m2»\times2=«ans»\ \mathrm{N}$。", F=20, m1=4, m2=6),
    ],
))

add(Chapter(
    id="newton-apps", unit="mechanics", no=6, title="摩擦、斜面與圓周運動",
    lead="把牛頓第二定律用到摩擦力、斜面和圓周軌道：重點是選對座標軸，以及記得向心力不是新的力。",
    body=r"""
## 摩擦力

接觸面之間的摩擦力平行於表面。

- 靜摩擦力：$f_s\le\mu_s N$。沒滑動時它隨外力改變，最大值是 $\mu_s N$
- 動摩擦力：$f_k=\mu_k N$，物體滑動時大小固定，方向與相對滑動方向相反

$\mu$ 沒有單位，通常 $\mu_k<\mu_s$。

>! 正向力 $N$ 不一定等於 $mg$。在斜面上、或被斜向拉著時，要用垂直接觸面的方程式去解。

## 斜面

沿斜面為 $x$ 軸、垂直斜面為 $y$ 軸，重力分解成：

$$mg\sin\theta\ (\text{沿斜面向下}),\qquad mg\cos\theta\ (\text{壓向斜面})$$

所以 $N=mg\cos\theta$，下滑加速度 $a=g(\sin\theta-\mu_k\cos\theta)$。

!sim mech-incline

## 等速圓周運動的受力

做圓周運動需要一個指向圓心的**合力**：

$$F_c = ma_c = \frac{mv^2}{r}$$

「向心力」只是合力指向圓心的那部分的名字，不是新的力。畫受力圖時不要另外畫一個「向心力」。

- 水平路面轉彎：向心力由靜摩擦力提供，最大速率 $v=\sqrt{\mu_s g r}$
- 傾斜彎道（不靠摩擦）：$\tan\theta=\dfrac{v^2}{rg}$
- 繩子拉著球在鉛直圓周運動：最高點 $T+mg=\dfrac{mv^2}{r}$
""",
    problems=[
        prob(r"一個 «m» kg 的箱子在水平地板上滑動，$\mu_k=«mu»$，動摩擦力是多少 N？取 $g=9.8$。", 0.3*20*g, "N", r"$f=\mu_k N=\mu_k mg=«mu»\times«m»\times9.8=«ans»\ \mathrm{N}$。", m=20, mu=0.3),
        prob(r"斜面傾角 «t»°，$\mu_k=«mu»$，物體下滑的加速度是多少 m/s²？", g*(math.sin(rad(30))-0.2*math.cos(rad(30))), "m/s²",
             r"$a=g(\sin\theta-\mu_k\cos\theta)=9.8(\sin«t»^\circ-«mu»\cos«t»^\circ)=«ans»\ \mathrm{m/s^2}$。", t=30, mu=0.2),
        prob(r"水平路面轉彎半徑 «r» m，$\mu_s=«mu»$，車子不打滑的最大速率是多少 m/s？", math.sqrt(0.6*g*50), "m/s",
             r"摩擦力提供向心力：$\mu_s mg=mv^2/r\Rightarrow v=\sqrt{\mu_s g r}=\sqrt{«mu»\times9.8\times«r»}=«ans»\ \mathrm{m/s}$。", r=50, mu=0.6),
        prob(r"半徑 «r» m 的傾斜彎道，要讓車以 «v» m/s 通過而不靠摩擦，傾角應為幾度？", math.degrees(math.atan(20**2/(100*g))), "度",
             r"$\tan\theta=\dfrac{v^2}{rg}=\dfrac{«v»^2}{«r»\times9.8}$，$\theta=«ans»^\circ$。", r=100, v=20),
        prob(r"光滑水平面上，用 «F» N 的力以與水平夾 «t»° 向上拉 «m» kg 的木塊，加速度是多少 m/s²？", 50*math.cos(rad(30))/10, "m/s²",
             r"水平分量 $F\cos\theta=«F»\cos«t»^\circ$，$a=F\cos\theta/m=«ans»\ \mathrm{m/s^2}$。", F=50, t=30, m=10),
    ],
    sims=["mech-incline"],
))

add(Chapter(
    id="work-energy", unit="mechanics", no=7, title="功與動能",
    lead="功是力在位移方向上的累積；功等於動能的改變，這個定理常比直接用牛頓定律更省力。",
    body=r"""
## 功

固定的力 $\vec F$ 作用在發生位移 $\vec d$ 的物體上，所作的功是兩向量的內積：

$$W=\vec F\cdot\vec d=Fd\cos\theta$$

單位是焦耳：$1\ \mathrm{J}=1\ \mathrm{N\cdot m}$。

- 力與位移同向：$W>0$，力讓物體加速
- 力與位移反向（如摩擦力）：$W<0$
- 力與位移垂直（如圓周運動的向心力、斜面的正向力）：$W=0$

力隨位置變化時，功是 $F$-$x$ 圖下的面積：$W=\int F\,dx$。

## 彈簧的力與功

虎克定律：彈簧力 $F=-kx$，$k$ 是彈力常數。把彈簧從平衡位置拉伸（或壓縮）$x$，外力作的功為：

$$W=\tfrac12 k x^2$$

## 動能與功能定理

質量 $m$、速率 $v$ 的物體動能：

$$K=\tfrac12 mv^2$$

**功能定理**：合力對物體所作的總功等於動能的變化。

$$W_{\text{net}}=\Delta K=\tfrac12mv_f^2-\tfrac12mv_i^2$$

>! 動能與方向無關，永遠是正的；功能定理裡要算的是**合力**的功，或把每個力的功都加起來。

## 功率

做功的快慢：平均功率 $P=\dfrac{W}{t}$，瞬時功率 $P=\vec F\cdot\vec v$。單位是瓦特：$1\ \mathrm{W}=1\ \mathrm{J/s}$。
""",
    problems=[
        prob(r"用 «F» N 的力沿與位移夾 «t»° 的方向拉箱子前進 «d» m，這個力作功多少 J？", 50*10*math.cos(rad(60)), "J", r"$W=Fd\cos\theta=«F»\times«d»\times\cos«t»^\circ=«ans»\ \mathrm{J}$。", F=50, d=10, t=60),
        prob(r"質量 «m» kg 的車以 «v» m/s 行駛，動能是多少 J？", 0.5*1200*20**2, "J", r"$K=\tfrac12mv^2=\tfrac12\times«m»\times«v»^2=«ans»\ \mathrm{J}$。", m=1200, v=20),
        prob(r"質量 «m» kg 的車速度由 «v1» m/s 增加到 «v2» m/s，合力共作功多少 J？", 0.5*1000*(20**2-10**2), "J", r"$W=\tfrac12m(v_2^2-v_1^2)=\tfrac12\times«m»\times(«v2»^2-«v1»^2)=«ans»\ \mathrm{J}$。", m=1000, v1=10, v2=20),
        prob(r"彈力常數 «k» N/m 的彈簧，從原長拉長 «x» m，外力作功多少 J？", 0.5*200*0.3**2, "J", r"$W=\tfrac12kx^2=\tfrac12\times«k»\times«x»^2=«ans»\ \mathrm{J}$。", k=200, x=0.3),
        prob(r"把 «m» kg 的物體以等速舉高 «h» m，費時 «t» s，需要的平均功率是多少 W？取 $g=9.8$。", 60*g*5/10, "W", r"$P=\dfrac{mgh}{t}=\dfrac{«m»\times9.8\times«h»}{«t»}=«ans»\ \mathrm{W}$。", m=60, h=5, t=10),
    ],
))

add(Chapter(
    id="potential-energy", unit="mechanics", no=8, title="位能與能量守恆",
    lead="只有保守力作功時，動能加位能的總和不變；把摩擦等耗散的能量算進去，能量守恆永遠成立。",
    body=r"""
## 保守力與位能

如果一個力對物體所作的功只看起點和終點、與路徑無關，這個力是**保守力**（重力、彈簧力、靜電力）。對保守力可以定義位能 $U$，使得 $W_{\text{保守力}}=-\Delta U$。

- 重力位能：$U_g=mgh$（$h$ 是相對於選定零點的高度，只有**差**才有意義）
- 彈性位能：$U_s=\tfrac12kx^2$

摩擦力與空氣阻力是**非保守力**：它們把機械能變成熱。

## 力學能守恆

只有保守力作功時：

$$K_i+U_i=K_f+U_f$$

解題時選一個位能零點，寫出起點與終點的總能量，令它們相等。

## 有非保守力時

$$K_i+U_i+W_{\text{非保守}}=K_f+U_f$$

摩擦力作負功，損失的機械能 $=|f|\cdot d$，變成熱能。**總能量**（含熱能）永遠守恆。

>! 能量守恆只告訴你速率，不告訴你方向或時間。若題目問時間或力，通常還要回到牛頓定律。

## 位能曲線

從位能曲線 $U(x)$ 可以讀出力：$F=-\dfrac{dU}{dx}$。曲線的谷底是穩定平衡點，山頂是不穩定平衡點。

## 為什麼好用

能量是純量，不用管路徑形狀。雲霄飛車從高度 $h$ 靜止滑下，到底部的速率只由 $h$ 決定：$v=\sqrt{2gh}$，軌道彎成什麼樣都一樣。
""",
    problems=[
        prob(r"質量 «m» kg 的物體在地面上方 «h» m，重力位能是多少 J？（地面為零點，$g=9.8$）", 2*g*15, "J", r"$U=mgh=«m»\times9.8\times«h»=«ans»\ \mathrm{J}$。", m=2, h=15),
        prob(r"雲霄飛車從靜止開始，從高 «h» m 處無摩擦滑下，到達底部的速率是多少 m/s？", math.sqrt(2*g*30), "m/s", r"$mgh=\tfrac12mv^2\Rightarrow v=\sqrt{2gh}=\sqrt{2\times9.8\times«h»}=«ans»\ \mathrm{m/s}$。", h=30),
        prob(r"彈力常數 «k» N/m 的彈簧壓縮 «x» m，把 «m» kg 的木塊水平彈出（光滑），離開彈簧時的速率是多少 m/s？", 0.1*math.sqrt(400/0.05), "m/s",
             r"$\tfrac12kx^2=\tfrac12mv^2\Rightarrow v=x\sqrt{k/m}=«x»\sqrt{«k»/«m»}=«ans»\ \mathrm{m/s}$。", k=400, x=0.1, m=0.05),
        prob(r"擺長 «L» m 的單擺，從與鉛直夾 «t»° 處靜止釋放，擺到最低點的速率是多少 m/s？", math.sqrt(2*g*1.5*(1-math.cos(rad(60)))), "m/s",
             r"下降高度 $h=L(1-\cos\theta)=«L»(1-\cos«t»^\circ)$，$v=\sqrt{2gh}=«ans»\ \mathrm{m/s}$。", L=1.5, t=60),
        prob(r"質量 «m» kg 的物體從 «h» m 高的斜面頂端靜止滑下，到底部速率為 «v» m/s，摩擦力損失了多少 J 的機械能？取 $g=9.8$。", 2*g*3 - 0.5*2*6**2, "J",
             r"損失 $=mgh-\tfrac12mv^2=«m»\times9.8\times«h»-\tfrac12\times«m»\times«v»^2=«ans»\ \mathrm{J}$。", m=2, h=3, v=6),
    ],
))

add(Chapter(
    id="momentum", unit="mechanics", no=9, title="動量與碰撞",
    lead="沒有外力時總動量不變：碰撞、爆炸、反衝都靠它解；再區分彈性與非彈性碰撞的能量。",
    body=r"""
## 動量與衝量

動量是向量：

$$\vec p=m\vec v$$

牛頓第二定律的更一般形式是 $\vec F_{\text{net}}=\dfrac{d\vec p}{dt}$。力在一段時間內的累積叫**衝量**，等於動量的改變：

$$\vec J=\int\vec F\,dt=\vec F_{\text{avg}}\Delta t=\Delta\vec p$$

同樣的動量改變，拉長作用時間可以減小力，這就是安全氣囊與軟墊的原理。

## 動量守恆

一個系統不受外力（或外力的總和為零），總動量不變：

$$m_1\vec v_{1i}+m_2\vec v_{2i}=m_1\vec v_{1f}+m_2\vec v_{2f}$$

碰撞時間極短、內力遠大於外力，所以碰撞前後動量近似守恆。

## 碰撞的種類

- **彈性碰撞**：動量守恆，動能也守恆
- **非彈性碰撞**：動量守恆，動能減少
- **完全非彈性碰撞**：兩物體黏在一起，動能損失最多：$v_f=\dfrac{m_1v_{1i}+m_2v_{2i}}{m_1+m_2}$

一維彈性碰撞，若 $m_2$ 原本靜止：

$$v_{1f}=\frac{m_1-m_2}{m_1+m_2}v_{1i},\qquad v_{2f}=\frac{2m_1}{m_1+m_2}v_{1i}$$

!sim mech-collide

>! 動量守恆永遠成立，動能守恆只在彈性碰撞成立。不要在非彈性碰撞裡把動能也寫成守恆。

## 質心

質點系統的質心 $\vec r_{cm}=\dfrac{\sum m_i\vec r_i}{\sum m_i}$。沒有外力時，質心的速度不變，不論內部怎麼爆炸或碰撞。
""",
    problems=[
        prob(r"質量 «m» kg 的棒球以 «v» m/s 飛行，動量大小是多少 kg·m/s？", 0.145*40, "kg·m/s", r"$p=mv=«m»\times«v»=«ans»\ \mathrm{kg\cdot m/s}$。", m=0.145, v=40),
        prob(r"球棒對球施以平均 «F» N 的力，作用 «t» s，衝量是多少 N·s？", 800*0.02, "N·s", r"$J=F\Delta t=«F»\times«t»=«ans»\ \mathrm{N\cdot s}$。", F=800, t=0.02),
        prob(r"質量 «m1» kg 的車以 «v» m/s 撞上靜止的 «m2» kg 車並黏在一起，碰後速率是多少 m/s？", 1000*15/(1000+1500), "m/s",
             r"$v_f=\dfrac{m_1v}{m_1+m_2}=\dfrac{«m1»\times«v»}{«m1»+«m2»}=«ans»\ \mathrm{m/s}$。", m1=1000, m2=1500, v=15),
        prob(r"質量 «m1» kg、速率 «v» m/s 的球與靜止的 «m2» kg 球作一維彈性碰撞，被撞球碰後速率是多少 m/s？", 2*2*6/(2+4), "m/s",
             r"$v_{2f}=\dfrac{2m_1}{m_1+m_2}v=\dfrac{2\times«m1»}{«m1»+«m2»}\times«v»=«ans»\ \mathrm{m/s}$。", m1=2, m2=4, v=6),
        prob(r"冰面上質量 «M» kg 的人原本靜止，把 «m» kg 的球以 «v» m/s 水平丟出，人反向滑動的速率是多少 m/s？", 2*10/80, "m/s",
             r"動量守恆：$0=mv-Mu\Rightarrow u=\dfrac{mv}{M}=\dfrac{«m»\times«v»}{«M»}=«ans»\ \mathrm{m/s}$。", M=80, m=2, v=10),
    ],
    sims=["mech-collide"],
))
