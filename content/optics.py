"""光學：幾何光學、干涉、繞射。"""
import math

from ._lib import Chapter, add, pi, prob

deg = math.degrees
rad = math.radians

add(Chapter(
    id="geometric-optics", unit="optics", no=1, title="幾何光學",
    lead="光走直線、遇到界面會反射與折射；用反射定律、司乃耳定律與薄透鏡公式就能算成像。",
    body=r"""
## 光線模型

當障礙物比波長大很多時，可以把光當成沿直線前進的光線，忽略波動性。這就是幾何光學。

## 反射

入射角等於反射角（對法線量）。平面鏡成的像是虛像，大小相同，像距等於物距。

## 折射與司乃耳定律

光從折射率 $n_1$ 的介質進入 $n_2$：

$$n_1\sin\theta_1=n_2\sin\theta_2$$

$n=c/v$：介質中光速變慢，$n$ 越大光速越慢（水 1.33、玻璃約 1.5、鑽石 2.42）。進入較密介質（$n$ 變大）時光線偏向法線。折射時**頻率不變**，波長變為 $\lambda/n$。

## 全反射

從較密介質射向較疏介質（$n_1>n_2$）時，入射角超過臨界角，光完全反射回去：

$$\sin\theta_c=\frac{n_2}{n_1}$$

光纖通訊、稜鏡與鑽石的閃光都靠全反射。

## 薄透鏡

物距 $d_o$、像距 $d_i$、焦距 $f$ 的關係：

$$\frac1{d_o}+\frac1{d_i}=\frac1f,\qquad m=-\frac{d_i}{d_o}$$

!sim optics-lens

符號慣例：凸透鏡 $f>0$、凹透鏡 $f<0$；像在透鏡另一側（實像）$d_i>0$，同側（虛像）$d_i<0$；$m<0$ 表示倒立，$|m|>1$ 放大。

>! 物距小於焦距時，凸透鏡成正立放大的**虛像**（放大鏡）；這時算出的 $d_i$ 是負的，不是算錯。

## 球面鏡

凹面鏡 $f=R/2>0$，凸面鏡 $f<0$，使用同一組公式。汽車後照鏡用凸面鏡，視野大、像縮小。

## 色散

折射率隨波長稍有不同，所以稜鏡把白光分成彩虹。彩虹則是雨滴內的折射、反射再折射。
""",
    problems=[
        prob(r"光從空氣以 «t1»° 入射到折射率 «n» 的玻璃，折射角是幾度？", deg(math.asin(math.sin(rad(40))/1.5)), "度", r"$\sin\theta_2=\dfrac{n_1\sin\theta_1}{n_2}=\dfrac{\sin«t1»^\circ}{«n»}$，$\theta_2=«ans»^\circ$。", t1=40, n=1.5),
        prob(r"光從折射率 «n» 的水射向空氣，臨界角是幾度？", deg(math.asin(1/1.33)), "度", r"$\sin\theta_c=\dfrac{n_2}{n_1}=\dfrac1{«n»}$，$\theta_c=«ans»^\circ$。", n=1.33),
        prob(r"凸透鏡焦距 «f» m，物體在 «do» m 處，像距是多少 cm？", 100/(1/0.10-1/0.30)/100*100, "cm", r"$\dfrac1{d_i}=\dfrac1f-\dfrac1{d_o}=\dfrac1{«f»}-\dfrac1{«do»}$，$d_i=0.15\ \mathrm m=«ans»\ \mathrm{cm}$。", f=0.10, do=0.30),
        prob(r"同一個凸透鏡（$f=«f»$ m）、物距 «do» m，放大率 $m$ 是多少？（負號表示倒立）", -(1/(1/0.10-1/0.30))/0.30, "", r"$d_i=0.15\ \mathrm m$，$m=-\dfrac{d_i}{d_o}=-\dfrac{0.15}{«do»}=«ans»$，倒立縮小的實像。", f=0.10, do=0.30),
        prob(r"凹面鏡曲率半徑 «R» m，物體在 «do» m 處，像距是多少 cm？", 100/(1/(0.4/2)-1/0.5), "cm", r"$f=R/2=0.2\ \mathrm m$，$\dfrac1{d_i}=\dfrac1{0.2}-\dfrac1{«do»}$，$d_i=«ans»\ \mathrm{cm}$。", R=0.4, do=0.5),
    ],
    sims=["optics-lens"],
))

add(Chapter(
    id="interference", unit="optics", no=2, title="干涉",
    lead="兩道同調光相遇時依相位相加：楊氏雙狹縫與薄膜干涉是光具有波動性的證據。",
    body=r"""
## 干涉的條件

兩列波疊加時依相位相加：同相增強（亮）、反相抵消（暗）。要看到穩定的干涉條紋，兩個光源要**同調**（相位差固定），通常用同一個光源分成兩束來達成。

相位差 $\phi$ 與路徑差 $\Delta$ 的關係：$\phi=\dfrac{2\pi\Delta}{\lambda}$。

- 亮紋（建設性）：$\Delta=m\lambda$，$m=0,\pm1,\pm2,\dots$
- 暗紋（破壞性）：$\Delta=(m+\tfrac12)\lambda$

## 楊氏雙狹縫

兩狹縫間距 $d$，光屏距離 $L\gg d$，到屏上某點的路徑差 $\Delta=d\sin\theta$：

$$d\sin\theta=m\lambda\quad(\text{亮紋})$$

小角度下，屏上相鄰亮紋的間距：

$$\Delta y=\frac{\lambda L}{d}$$

!sim optics-slit

波長越長、狹縫越近、屏越遠，條紋越寬。量出條紋間距就能測量光的波長。1801 年楊氏用這個實驗證明了光是波。

## 強度

兩束強度各為 $I_0$ 的光，合成強度 $I=4I_0\cos^2\dfrac{\phi}{2}$，亮處是單束的 4 倍，暗處是 0。能量沒有不見，只是重新分配。

## 薄膜干涉

肥皂泡、油膜的彩色來自薄膜上下兩個表面反射光的干涉。注意相位：

- 光由較疏介質射向較密介質反射時，有 $\pi$ 的相位跳變（相當於多走 $\lambda/2$）
- 由較密射向較疏反射則沒有

空氣中的肥皂膜（厚度 $t$、折射率 $n$）：上表面反射有跳變，下表面沒有，所以兩反射光增強的條件是 $2nt=(m+\tfrac12)\lambda$。

>! 薄膜很厚時看不到干涉色，因為厚度超過光的相干長度，而且各波長互相混合。

## 抗反射膜

鏡頭鍍上厚度 $\lambda/(4n)$ 的薄膜，使兩個反射光互相抵消，減少反射、增加透光量。
""",
    problems=[
        prob(r"雙狹縫間距 «d» mm、屏距 «L» m、光的波長 «lam» nm，亮紋間距是多少 mm？", 600e-9*1.5/0.3e-3*1000, "mm", r"$\Delta y=\dfrac{\lambda L}{d}=\dfrac{«lam»\times10^{-9}\times«L»}{«d»\times10^{-3}}=«ans»\ \mathrm{mm}$。", d=0.3, L=1.5, lam=600),
        prob(r"雙狹縫間距 «d» mm、波長 «lam» nm，第 «m» 級亮紋的角度是幾度？", deg(math.asin(2*500e-9/0.1e-3)), "度", r"$\sin\theta=\dfrac{m\lambda}{d}=\dfrac{«m»\times«lam»\times10^{-9}}{«d»\times10^{-3}}=0.01$，$\theta=«ans»^\circ$。", d=0.1, lam=500, m=2),
        prob(r"雙狹縫實驗中，條紋間距 «dy» mm、屏距 «L» m、狹縫間距 «d» mm，光的波長是多少 nm？", 2.0e-3*0.5e-3/2.0*1e9, "nm", r"$\lambda=\dfrac{d\,\Delta y}{L}=\dfrac{«d»\times10^{-3}\times«dy»\times10^{-3}}{«L»}=«ans»\times10^{-9}\ \mathrm m$。", dy=2.0, L=2.0, d=0.5),
        prob(r"空氣中的肥皂膜（$n=«n»$）要讓波長 «lam» nm 的反射光增強，最薄的厚度是多少 nm？", 550/(4*1.33), "nm", r"$2nt=\tfrac12\lambda\Rightarrow t=\dfrac{\lambda}{4n}=\dfrac{«lam»}{4\times«n»}=«ans»\ \mathrm{nm}$。", n=1.33, lam=550),
        prob(r"兩束波長 «lam» nm 的光，路徑差 «D» nm，相位差是多少 rad？", 2*pi*150/600, "rad", r"$\phi=\dfrac{2\pi\Delta}{\lambda}=\dfrac{2\pi\times«D»}{«lam»}=«ans»\ \mathrm{rad}$（$\pi/2$）。", lam=600, D=150),
    ],
    sims=["optics-slit"],
))

add(Chapter(
    id="diffraction", unit="optics", no=3, title="繞射",
    lead="光通過窄縫會散開：單縫決定中央亮紋有多寬，光柵把光譜分得很開，繞射也決定鏡頭解析度的極限。",
    body=r"""
## 什麼是繞射

波遇到與波長相近的障礙或開口，會繞過邊緣散開，不再是直線傳播。聲音能繞過牆角傳進房間、光通過小孔在屏上形成條紋，都是繞射。

## 單狹縫

寬度 $a$ 的狹縫，屏上出現中央一條寬亮紋，兩側是較暗的亮紋。暗紋位置：

$$a\sin\theta=m\lambda,\quad m=\pm1,\pm2,\dots$$

中央亮紋的全寬（小角度，屏距 $L$）：

$$w=\frac{2\lambda L}{a}$$

**縫越窄，繞射越嚴重，條紋越寬。**

>! 注意單縫公式的 $m$ 是**暗紋**條件，雙縫公式的 $m$ 是**亮紋**條件，兩者很容易搞混。實際的雙縫圖樣是兩者相乘：雙縫干涉的細條紋被單縫繞射的包絡罩住。

## 繞射光柵

很多條等間距狹縫（間距 $d$）。亮紋又細又亮，位置：

$$d\sin\theta=m\lambda,\quad m=0,\pm1,\pm2,\dots$$

不同波長的亮紋在不同角度，所以光柵可以把光分開成光譜，是光譜儀的核心。光柵的條數越多，亮紋越細，分辨能力越強。光碟表面的彩虹色就是一個光柵。

能看到的最高級次 $m_{max}$ 受限於 $\sin\theta\le1$：$m_{max}=\left\lfloor\dfrac d\lambda\right\rfloor$。

## 圓孔與解析度

圓孔（直徑 $D$）的繞射使點光源的像變成一個亮斑，角半徑：

$$\theta=1.22\frac{\lambda}{D}$$

瑞利準則：兩個點光源的角距離至少要等於這個值才能分辨。這就是望遠鏡、顯微鏡與人眼解析度的極限，口徑越大、波長越短，解析度越好。

## X 光繞射

X 射線波長約 $0.1\ \mathrm{nm}$，與晶體中原子間距相近，晶體是天然的三維光柵。布拉格條件：

$$2d\sin\theta=m\lambda$$

DNA 的雙螺旋結構就是由 X 光繞射的照片推出來的。
""",
    problems=[
        prob(r"單縫寬 «a» mm、波長 «lam» nm、屏距 «L» m，中央亮紋全寬是多少 mm？", 2*500e-9*2/0.1e-3*1000, "mm", r"$w=\dfrac{2\lambda L}{a}=\dfrac{2\times«lam»\times10^{-9}\times«L»}{«a»\times10^{-3}}=«ans»\ \mathrm{mm}$。", a=0.1, lam=500, L=2),
        prob(r"光柵每 mm 有 «N» 條刻線，波長 «lam» nm 的光，第一級亮紋的角度是幾度？", deg(math.asin(600e-9*500e3)), "度", r"$d=1/«N»\ \mathrm{mm}=2\times10^{-6}\ \mathrm m$，$\sin\theta=\dfrac\lambda d=«lam»\times10^{-9}\times«N»\times10^3=0.3$，$\theta=«ans»^\circ$。", N=500, lam=600),
        prob(r"同一個光柵（每 mm «N» 條）與 «lam» nm 的光，最多能看到第幾級亮紋？", 3, "級", r"$m_{max}=\lfloor d/\lambda\rfloor=\lfloor1/0.3\rfloor=«ans»$。", N=500, lam=600),
        prob(r"望遠鏡口徑 «D» m、觀測波長 «lam» nm，瑞利解析角是多少 rad？", 1.22*550e-9/0.1, "rad", r"$\theta=1.22\dfrac\lambda D=1.22\times\dfrac{«lam»\times10^{-9}}{«D»}=«ans»\ \mathrm{rad}$。", D=0.1, lam=550),
        prob(r"X 光波長 «lam» nm 打在晶面間距 «d» nm 的晶體上，第一級布拉格反射的角度是幾度？", deg(math.asin(0.154/(2*0.2))), "度", r"$\sin\theta=\dfrac{m\lambda}{2d}=\dfrac{«lam»}{2\times«d»}=0.385$，$\theta=«ans»^\circ$。", lam=0.154, d=0.2),
    ],
))
