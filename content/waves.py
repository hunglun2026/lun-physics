"""振動與波：簡諧運動、波、聲音。"""
import math

from ._lib import Chapter, add, g, pi, prob

add(Chapter(
    id="shm", unit="waves", no=1, title="簡諧運動",
    lead="回復力與位移成正比的運動叫簡諧運動；彈簧與單擺都是它，能量在動能與位能之間來回。",
    body=r"""
## 什麼是簡諧運動

物體受的回復力與位移成正比、方向相反：$F=-kx$，運動就是簡諧運動。位移隨時間呈正弦變化：

$$x(t)=A\cos(\omega t+\phi)$$

- $A$：振幅，最大位移
- $\omega$：角頻率，$\omega=2\pi f=\dfrac{2\pi}{T}$
- $\phi$：初相位

速度 $v=-A\omega\sin(\omega t+\phi)$，加速度 $a=-\omega^2x$。最大速率 $v_{max}=A\omega$，最大加速度 $a_{max}=A\omega^2$。

## 彈簧振子

質量 $m$、彈力常數 $k$：

$$\omega=\sqrt{\frac km},\qquad T=2\pi\sqrt{\frac mk}$$

>! 週期與振幅無關，只由 $m$ 與 $k$ 決定。拉得更遠，走的路更長，但速度也更快，剛好抵消。

## 單擺（小角度）

$$T=2\pi\sqrt{\frac Lg}$$

只在擺角小（約 $15^\circ$ 以內）時成立；週期與擺錘質量無關。

!sim wave-shm

## 能量

彈簧振子的總能量固定：

$$E=\tfrac12kA^2=\tfrac12mv^2+\tfrac12kx^2$$

在最大位移處全是位能，通過平衡位置時全是動能。由此可得任一位置的速率：

$$v=\sqrt{\frac km\,(A^2-x^2)}$$

## 阻尼與共振

有摩擦時振幅會逐漸衰減（阻尼）。外力以接近系統自然頻率驅動時，振幅會變得很大，叫**共振**，例如推鞦韆、橋梁被風吹到共振而損壞。
""",
    problems=[
        prob(r"質量 «m» kg 的物體掛在 «k» N/m 的彈簧上，振動週期是多少 s？", 2*pi*math.sqrt(0.5/200), "s", r"$T=2\pi\sqrt{m/k}=2\pi\sqrt{«m»/«k»}=«ans»\ \mathrm{s}$。", m=0.5, k=200),
        prob(r"擺長 «L» m 的單擺（小角度），週期是多少 s？取 $g=9.8$。", 2*pi*math.sqrt(1.0/g), "s", r"$T=2\pi\sqrt{L/g}=2\pi\sqrt{«L»/9.8}=«ans»\ \mathrm{s}$。", L=1.0),
        prob(r"彈簧振子 $k=«k»\ \mathrm{N/m}$、$m=«m»\ \mathrm{kg}$，振幅 «A» m，最大速率是多少 m/s？", 0.1*math.sqrt(50/0.2), "m/s", r"$v_{max}=A\omega=A\sqrt{k/m}=«A»\sqrt{«k»/«m»}=«ans»\ \mathrm{m/s}$。", k=50, m=0.2, A=0.1),
        prob(r"彈簧振子 $k=«k»\ \mathrm{N/m}$，振幅 «A» m，總能量是多少 J？", 0.5*200*0.05**2, "J", r"$E=\tfrac12kA^2=\tfrac12\times«k»\times«A»^2=«ans»\ \mathrm{J}$。", k=200, A=0.05),
        prob(r"$k=«k»\ \mathrm{N/m}$、$m=«m»\ \mathrm{kg}$、振幅 «A» m 的振子，在位移 «x» m 處的速率是多少 m/s？", math.sqrt(100/1.0*(0.2**2-0.1**2)), "m/s", r"$v=\sqrt{\dfrac km(A^2-x^2)}=\sqrt{«k»/«m»\times(«A»^2-«x»^2)}=«ans»\ \mathrm{m/s}$。", k=100, m=1.0, A=0.2, x=0.1),
    ],
    sims=["wave-shm"],
))

add(Chapter(
    id="waves", unit="waves", no=2, title="波動",
    lead="波傳遞的是能量與擾動，不是物質；波速、頻率、波長的關係，加上疊加與駐波。",
    body=r"""
## 橫波與縱波

- 橫波：介質振動方向垂直傳播方向（繩波、光波）
- 縱波：介質振動方向平行傳播方向（聲波、彈簧上的疏密波）

波傳遞能量，介質本身只在原地附近振動。

## 波的基本關係

週期波的波長 $\lambda$、頻率 $f$、波速 $v$：

$$v=f\lambda$$

波速由**介質**決定，頻率由**波源**決定。波從一種介質進入另一種，頻率不變，波速與波長改變。

弦上橫波的速度：

$$v=\sqrt{\frac{T}{\mu}}$$

$T$ 是張力，$\mu$ 是線密度（單位長度質量）。繃得越緊、越輕，波跑得越快。

## 正弦波

沿 $+x$ 方向行進的波：

$$y(x,t)=A\sin(kx-\omega t)$$

波數 $k=\dfrac{2\pi}{\lambda}$，角頻率 $\omega=2\pi f$，波速 $v=\dfrac{\omega}{k}$。

## 疊加與干涉

兩個波相遇時，位移直接相加（疊加原理），之後各自繼續前進。同相相加變強（建設性干涉），反相相消（破壞性干涉）。

!sim wave-superpos

## 駐波

兩端固定的弦上，反向行進的兩個波疊加成駐波。只有特定頻率能存在：

$$f_n=\frac{nv}{2L},\qquad n=1,2,3,\dots$$

$n=1$ 是基頻，其餘是泛音。腹點振動最大，節點完全不動。

>! 駐波看起來「不傳播」，但它是由兩個行進波疊成的，能量在腹點之間來回，不會穿過節點。
""",
    problems=[
        prob(r"頻率 «f» Hz 的波，波長 «lam» m，波速是多少 m/s？", 440*0.78, "m/s", r"$v=f\lambda=«f»\times«lam»=«ans»\ \mathrm{m/s}$。", f=440, lam=0.78),
        prob(r"弦的張力 «T» N、線密度 «mu» kg/m，弦上波速是多少 m/s？", math.sqrt(100/0.01), "m/s", r"$v=\sqrt{T/\mu}=\sqrt{«T»/«mu»}=«ans»\ \mathrm{m/s}$。", T=100, mu=0.01),
        prob(r"長 «L» m 兩端固定的弦，波速 «v» m/s，基頻是多少 Hz？", 100/(2*0.65), "Hz", r"$f_1=\dfrac{v}{2L}=\dfrac{«v»}{2\times«L»}=«ans»\ \mathrm{Hz}$。", L=0.65, v=100),
        prob(r"波長 «lam» m 的波，波數 $k$ 是多少 rad/m？", 2*pi/0.5, "rad/m", r"$k=\dfrac{2\pi}{\lambda}=\dfrac{2\pi}{«lam»}=«ans»\ \mathrm{rad/m}$。", lam=0.5),
        prob(r"長 «L» m 兩端固定的弦，波速 «v» m/s，第三諧音（$n=3$）的頻率是多少 Hz？", 3*240/(2*1.2), "Hz", r"$f_3=\dfrac{3v}{2L}=\dfrac{3\times«v»}{2\times«L»}=«ans»\ \mathrm{Hz}$。", L=1.2, v=240),
    ],
    sims=["wave-superpos"],
))

add(Chapter(
    id="sound", unit="waves", no=3, title="聲音",
    lead="聲音是空氣中的縱波：怎麼量它的大小、都卜勒效應為什麼讓警笛變調、管子裡的共鳴。",
    body=r"""
## 聲速

聲波靠介質傳播，真空中沒有聲音。空氣中聲速隨溫度上升：

$$v\approx331+0.6\,T_{\mathrm C}\ \ (\mathrm{m/s})$$

20°C 約 $343\ \mathrm{m/s}$。固體與液體中更快（水約 $1500\ \mathrm{m/s}$）。

## 強度與分貝

強度是單位面積的功率：$I=\dfrac PA$。點聲源向四面八方均勻發聲：$I=\dfrac{P}{4\pi r^2}$，距離加倍，強度變成 $\tfrac14$。

人耳對強度是對數反應，所以用分貝（dB）：

$$\beta=10\log_{10}\frac{I}{I_0},\qquad I_0=10^{-12}\ \mathrm{W/m^2}$$

強度變 10 倍，增加 10 dB；變 2 倍，約增加 3 dB。

>! 兩個 60 dB 的聲音加在一起不是 120 dB，而是約 63 dB，因為要先把強度相加，再轉成分貝。

## 都卜勒效應

波源與觀察者有相對運動時，聽到的頻率改變。聲源以 $v_s$ 靠近靜止的觀察者：

$$f'=f\,\frac{v}{v-v_s}$$

遠離時分母改成 $v+v_s$。觀察者以 $v_o$ 靠近靜止聲源：$f'=f\dfrac{v+v_o}{v}$。靠近時音調變高，遠離時變低。

## 拍

兩個頻率很接近的聲音疊加，會聽到忽大忽小的「拍」，拍頻是兩頻率之差：

$$f_{\text{拍}}=|f_1-f_2|$$

調樂器時，拍頻越慢越準。

## 管內駐波

- 兩端開口的管（開管）：$f_n=\dfrac{nv}{2L}$，$n=1,2,3,\dots$
- 一端封閉的管（閉管）：$f_n=\dfrac{nv}{4L}$，$n=1,3,5,\dots$（只有奇數倍）
""",
    problems=[
        prob(r"氣溫 «T»°C 時空氣中的聲速約是多少 m/s？（用 $v=331+0.6T$）", 331+0.6*25, "m/s", r"$v=331+0.6\times«T»=«ans»\ \mathrm{m/s}$。", T=25),
        prob(r"聲音強度 «I» W/m²，聲音強度級是多少 dB？（$I_0=10^{-12}\ \mathrm{W/m^2}$）", 10*math.log10(1e-6/1e-12), "dB", r"$\beta=10\log_{10}(I/I_0)=10\log_{10}(«I»/10^{-12})=«ans»\ \mathrm{dB}$。", I=1e-6),
        prob(r"救護車以 «vs» m/s 迎面接近靜止的你，警笛頻率 «f» Hz，聲速 «v» m/s，你聽到的頻率是多少 Hz？", 500*343/(343-30), "Hz", r"$f'=f\dfrac{v}{v-v_s}=«f»\times\dfrac{«v»}{«v»-«vs»}=«ans»\ \mathrm{Hz}$。", vs=30, f=500, v=343),
        prob(r"兩個音叉頻率 «f1» Hz 與 «f2» Hz 同時發聲，每秒聽到幾次拍？", 444-440, "次", r"$f_{\text{拍}}=|f_1-f_2|=|«f1»-«f2»|=«ans»$。", f1=440, f2=444),
        prob(r"長 «L» m 的開管，聲速 «v» m/s，基頻是多少 Hz？", 343/(2*0.5), "Hz", r"$f_1=\dfrac{v}{2L}=\dfrac{«v»}{2\times«L»}=«ans»\ \mathrm{Hz}$。", L=0.5, v=343),
    ],
))
