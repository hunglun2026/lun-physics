"""電磁學 2：磁力、磁場來源、電磁感應、電感、交流電路、電磁波。"""
import math

from ._lib import Chapter, add, c, e, eps0, m_e, m_p, mu0, pi, prob

add(Chapter(
    id="magnetic-force", unit="em", no=8, title="磁場與磁力",
    lead="磁場只對運動中的電荷施力，而且力永遠垂直速度，所以只轉彎、不加速；電流與載流線圈也受磁力。",
    body=r"""
## 磁場與磁力

磁場 $\vec B$ 的單位是特斯拉（T）。運動電荷 $q$ 在磁場中受力：

$$\vec F=q\vec v\times\vec B,\qquad F=qvB\sin\theta$$

方向用右手定則（正電荷）：四指由 $\vec v$ 轉向 $\vec B$，拇指是力的方向；負電荷則反向。

>! 磁力永遠垂直於速度，所以**不作功**，只改變方向，不改變速率。靜止的電荷不受磁力。

## 在磁場中做圓周運動

速度垂直磁場時，磁力就是向心力：$qvB=\dfrac{mv^2}{r}$，所以：

$$r=\frac{mv}{qB},\qquad f=\frac{qB}{2\pi m}$$

迴旋頻率 $f$ 與速率、半徑無關，迴旋加速器靠這個性質重複加速粒子。質譜儀用半徑 $r\propto m$ 分辨不同質量的離子。

!sim em-bfield

## 電流受的力

長度 $L$ 的直導線通過電流 $I$，在磁場中受力：

$$\vec F=I\vec L\times\vec B,\qquad F=ILB\sin\theta$$

## 載流線圈的力矩

$N$ 匝、面積 $A$、電流 $I$ 的線圈放在均勻磁場中，磁矩 $\mu=NIA$，力矩：

$$\tau=NIAB\sin\theta$$

$\theta$ 是線圈法線與磁場的夾角。馬達就靠這個力矩轉動，電流表也是（線圈受力矩，被彈簧拉住，偏轉角度正比於電流）。

## 霍爾效應（了解即可）

載流導體放在垂直磁場裡，載子被偏向一側，兩側產生霍爾電壓，可用來判斷載子的正負號與測磁場。

## 為什麼磁力不作功卻能工作

馬達能作功是因為電流變化時，感應電動勢、電場力提供能量，磁力只是中間的「轉接」，把電能轉成機械能。
""",
    problems=[
        prob(r"質子以 «v» m/s 的速率垂直射入 «B» T 的磁場，受到的力是多少 N？", e*3e6*0.5, "N", r"$F=qvB=1.602\times10^{-19}\times«v»\times«B»=«ans»\ \mathrm N$。", v=3e6, B=0.5),
        prob(r"電子以 «v» m/s 的速率垂直射入 «B» T 的磁場，圓周運動半徑是多少 cm？", m_e*2e6/(e*1e-3)*100, "cm", r"$r=\dfrac{mv}{qB}=\dfrac{9.109\times10^{-31}\times«v»}{1.602\times10^{-19}\times«B»}=«r»\ \mathrm m=«ans»\ \mathrm{cm}$。", v=2e6, B=1e-3, r=m_e*2e6/(e*1e-3)),
        prob(r"長 «L» m 的導線通過 «I» A 的電流，垂直放在 «B» T 的磁場中，受力是多少 N？", 4*0.5*0.2, "N", r"$F=ILB=«I»\times«L»\times«B»=«ans»\ \mathrm N$。", L=0.5, I=4, B=0.2),
        prob(r"質子在 «B» T 的磁場中的迴旋頻率是多少 Hz？（$m_p=1.673\times10^{-27}\ \mathrm{kg}$）", e*1.5/(2*pi*m_p), "Hz", r"$f=\dfrac{qB}{2\pi m}=\dfrac{1.602\times10^{-19}\times«B»}{2\pi\times1.673\times10^{-27}}=«ans»\ \mathrm{Hz}$。", B=1.5),
        prob(r"線圈 «N» 匝、面積 «A» m²、電流 «I» A，法線垂直於 «B» T 的磁場（$\sin\theta=1$），力矩是多少 N·m？", 100*0.5*0.01*0.3, "N·m", r"$\tau=NIAB=«N»\times«I»\times«A»\times«B»=«ans»\ \mathrm{N\cdot m}$。", N=100, I=0.5, A=0.01, B=0.3),
    ],
    sims=["em-bfield"],
))

add(Chapter(
    id="magnetic-sources", unit="em", no=9, title="磁場的來源",
    lead="電流產生磁場；長直導線、圓環、螺線管的磁場公式，加上安培定律與平行導線之間的力。",
    body=r"""
## 電流產生磁場

1820 年厄斯特發現通電導線會讓指南針偏轉：電流周圍有磁場。方向用右手定則：拇指指電流方向，四指彎曲的方向就是磁場繞導線的方向。

真空磁導率 $\mu_0=4\pi\times10^{-7}\ \mathrm{T\cdot m/A}$。

## 必歐-沙伐定律

小段電流 $I\,d\vec l$ 在距離 $r$ 處的磁場：

$$d\vec B=\frac{\mu_0}{4\pi}\frac{I\,d\vec l\times\hat r}{r^2}$$

把全部電流段積分，就得到下面的結果。

## 常用的結果

- **長直導線**，距離 $r$：$B=\dfrac{\mu_0I}{2\pi r}$
- **圓形線圈**中心（半徑 $R$、$N$ 匝）：$B=\dfrac{\mu_0NI}{2R}$
- **長螺線管**內部（每公尺 $n$ 匝）：$B=\mu_0nI$，內部均勻，外部近似為零

## 安培定律

沿任一封閉路徑的環流，由穿過它的電流決定：

$$\oint\vec B\cdot d\vec l=\mu_0I_{\text{enc}}$$

它在電流分布對稱時很好用（像高斯定律對電場），長直導線與螺線管的公式都可以這樣推出。

## 平行導線之間的力

導線 1 的磁場作用在導線 2 上，每單位長度的力：

$$\frac FL=\frac{\mu_0I_1I_2}{2\pi d}$$

**同向電流相吸，反向電流相斥。** 國際單位制曾經用這個力定義 1 安培。

>! 電場線有起點與終點（電荷），磁場線永遠是封閉的圈。目前沒有找到單獨的磁單極，這等價於 $\oint\vec B\cdot d\vec A=0$。

## 物質的磁性

磁性來自電子的軌道與自旋磁矩。鐵、鈷、鎳是鐵磁性（磁矩排整齊，能被磁化）；大多數物質磁性很弱。
""",
    problems=[
        prob(r"長直導線通過 «I» A，距導線 «r» m 處的磁場是多少 T？", mu0*10/(2*pi*0.05), "T", r"$B=\dfrac{\mu_0I}{2\pi r}=\dfrac{4\pi\times10^{-7}\times«I»}{2\pi\times«r»}=«ans»\ \mathrm T$。", I=10, r=0.05),
        prob(r"圓形線圈半徑 «R» m、«N» 匝、通過 «I» A，圓心的磁場是多少 T？", mu0*20*2/(2*0.1), "T", r"$B=\dfrac{\mu_0NI}{2R}=\dfrac{4\pi\times10^{-7}\times«N»\times«I»}{2\times«R»}=«ans»\ \mathrm T$。", R=0.1, N=20, I=2),
        prob(r"螺線管每公尺 «n» 匝，電流 «I» A，內部磁場是多少 T？", mu0*1000*2, "T", r"$B=\mu_0nI=4\pi\times10^{-7}\times«n»\times«I»=«ans»\ \mathrm T$。", n=1000, I=2),
        prob(r"兩條平行長導線相距 «d» m，電流分別為 «I1» A 與 «I2» A，每公尺受力是多少 N/m？", mu0*20*30/(2*pi*0.02), "N/m", r"$\dfrac FL=\dfrac{\mu_0I_1I_2}{2\pi d}=\dfrac{4\pi\times10^{-7}\times«I1»\times«I2»}{2\pi\times«d»}=«ans»\ \mathrm{N/m}$。", d=0.02, I1=20, I2=30),
        prob(r"兩條平行導線相距 «d» m，各通過 «I» A 的**反向**電流，兩線正中點的磁場是多少 T？", 2*mu0*5/(2*pi*0.05), "T", r"中點距每條導線 $«d»/2=0.05$ m，每條線的場 $\dfrac{\mu_0I}{2\pi\times0.05}$；反向電流在中點產生同方向的場，相加：$2\times\dfrac{4\pi\times10^{-7}\times«I»}{2\pi\times0.05}=«ans»\ \mathrm T$。", d=0.1, I=5),
    ],
))

add(Chapter(
    id="induction", unit="em", no=10, title="電磁感應",
    lead="磁通量改變就產生電動勢：發電機、變壓器、感應爐的原理，以及冷次定律決定方向。",
    body=r"""
## 磁通量

通過面積的磁場「量」：

$$\Phi_B=\int\vec B\cdot d\vec A=BA\cos\theta$$

單位韋伯（Wb）：$1\ \mathrm{Wb}=1\ \mathrm{T\cdot m^2}$。

## 法拉第定律

迴路中磁通量改變，就產生感應電動勢：

$$\mathcal E=-N\frac{d\Phi_B}{dt}$$

任何能使 $\Phi=BA\cos\theta$ 改變的方式都有效：改變 $B$、改變 $A$、或改變角度 $\theta$。

## 冷次定律

那個負號的意思：**感應電流的方向，總是要抵抗造成它的磁通量變化。**

- 磁鐵 N 極靠近線圈，通量增加，線圈產生反向磁場去抵抗（互相排斥）
- 磁鐵遠離，通量減少，線圈產生同向磁場去挽留（互相吸引）

這是能量守恆的必然：若感應電流是幫忙而非抵抗，能量就憑空產生了。

>! 感應電動勢只看磁通量的**變化率**，不看磁通量本身有多大。穩定的強磁場穿過線圈，不會產生感應電流。

## 動生電動勢

長 $L$ 的導體棒以速度 $v$ 垂直切割磁場：

$$\mathcal E=BLv$$

接上電阻 $R$ 後電流 $I=\dfrac{BLv}{R}$，磁場對棒施一個阻力 $F=BIL=\dfrac{B^2L^2v}{R}$，要維持等速必須外加同樣大的力，外力作的功就轉成電能。

## 發電機

線圈在磁場中以角速度 $\omega$ 旋轉，$\theta=\omega t$：

$$\mathcal E=NBA\omega\sin\omega t$$

這是交流電的來源，峰值正比於轉速與磁場。

!sim em-gen

## 變壓器

兩個線圈共用鐵芯，初級電壓 $V_1$（$N_1$ 匝）與次級 $V_2$（$N_2$ 匝）：$\dfrac{V_2}{V_1}=\dfrac{N_2}{N_1}$。只能用在交流（磁通量要變化），理想變壓器功率不變，升壓必降流，所以輸電用高壓以減少 $I^2R$ 的損耗。
""",
    problems=[
        prob(r"磁場 «B» T 穿過面積 «A» m² 的線圈，磁場與線圈法線夾 «t»°，磁通量是多少 Wb？", 0.4*0.05*math.cos(math.radians(60)), "Wb", r"$\Phi=BA\cos\theta=«B»\times«A»\times\cos«t»^\circ=«ans»\ \mathrm{Wb}$。", B=0.4, A=0.05, t=60),
        prob(r"«N» 匝線圈的磁通量在 «dt» s 內從 «f1» Wb 降為 0，感應電動勢大小是多少 V？", 50*0.02/0.1, "V", r"$\mathcal E=N\dfrac{|\Delta\Phi|}{\Delta t}=«N»\times\dfrac{«f1»}{«dt»}=«ans»\ \mathrm V$。", N=50, f1=0.02, dt=0.1),
        prob(r"導體棒長 «L» m，以 «v» m/s 垂直切割 «B» T 的磁場，兩端電動勢是多少 V？", 0.5*0.4*3, "V", r"$\mathcal E=BLv=«B»\times«L»\times«v»=«ans»\ \mathrm V$。", B=0.5, L=0.4, v=3),
        prob(r"上題的導體棒接在總電阻 «R» Ω 的迴路中，要維持等速 «v» m/s 需要的外力是多少 N？（$B=«B»$ T，$L=«L»$ m）", 0.5**2*0.4**2*3/2, "N", r"$F=\dfrac{B^2L^2v}{R}=\dfrac{«B»^2\times«L»^2\times«v»}{«R»}=«ans»\ \mathrm N$。", R=2, v=3, B=0.5, L=0.4),
        prob(r"發電機線圈 «N» 匝、面積 «A» m²、磁場 «B» T、角速度 «w» rad/s，輸出電動勢的峰值是多少 V？", 200*0.1*0.02*120, "V", r"$\mathcal E_{max}=NBA\omega=«N»\times«B»\times«A»\times«w»=«ans»\ \mathrm V$。", N=200, B=0.1, A=0.02, w=120),
    ],
    sims=["em-gen"],
))

add(Chapter(
    id="inductance", unit="em", no=11, title="電感",
    lead="線圈反抗電流的變化；電感把能量儲存在磁場中，和電阻、電容組成 RL、LC 電路。",
    body=r"""
## 自感

線圈中的電流改變，會使自己的磁通量改變，產生反抗這個變化的電動勢：

$$\mathcal E=-L\frac{dI}{dt}$$

$L$ 是電感，單位亨利（H）：$1\ \mathrm H=1\ \mathrm{V\cdot s/A}$。電感的大小為 $L=\dfrac{N\Phi}{I}$。

螺線管（長 $l$、截面積 $A$、$N$ 匝）：

$$L=\frac{\mu_0N^2A}{l}$$

>! 電感反抗的是電流的**變化**，不是電流本身。電流穩定時，理想電感的電壓是零，像一條導線；試圖突然切斷電流時，$dI/dt$ 很大，會產生很高的電壓（所以拔插頭會看到火花）。

## 磁場儲存的能量

$$U=\tfrac12LI^2$$

與電容的 $\tfrac12CV^2$ 對照。能量儲存在磁場裡，磁能密度 $u_B=\dfrac{B^2}{2\mu_0}$。

## RL 電路

接上電池後，電流不會瞬間升到最大，而是指數趨近：

$$I(t)=\frac{\mathcal E}{R}\left(1-e^{-t/\tau}\right),\qquad\tau=\frac LR$$

斷開時電流以同樣的時間常數衰減。

## LC 振盪

電容器充滿電後接上電感，能量在電場與磁場之間來回，電荷與電流做簡諧振盪（對照彈簧振子，$L\leftrightarrow m$、$1/C\leftrightarrow k$）：

$$\omega=\frac1{\sqrt{LC}},\qquad f=\frac1{2\pi\sqrt{LC}}$$

收音機調台就是改變 $C$ 讓電路共振在電台頻率。真實電路有電阻，振盪會逐漸衰減。

## 互感

線圈 1 的電流變化在線圈 2 感應電動勢：$\mathcal E_2=-M\dfrac{dI_1}{dt}$。變壓器與無線充電都靠互感。
""",
    problems=[
        prob(r"電感 «L» H 的線圈，電流以 «r» A/s 的速率增加，自感電動勢大小是多少 V？", 0.5*4, "V", r"$|\mathcal E|=L\dfrac{dI}{dt}=«L»\times«r»=«ans»\ \mathrm V$。", L=0.5, r=4),
        prob(r"電感 «L» H 的線圈通過 «I» A，儲存的能量是多少 J？", 0.5*2*3**2, "J", r"$U=\tfrac12LI^2=\tfrac12\times«L»\times«I»^2=«ans»\ \mathrm J$。", L=2, I=3),
        prob(r"RL 電路 $L=«L»\ \mathrm H$、$R=«R»\ \Omega$，時間常數是多少 ms？", 0.2/100*1000, "ms", r"$\tau=\dfrac LR=\dfrac{«L»}{«R»}=0.002\ \mathrm s=«ans»\ \mathrm{ms}$。", L=0.2, R=100),
        prob(r"LC 電路 $L=«L»\ \mathrm{mH}$、$C=«C»\ \mathrm{nF}$，振盪頻率是多少 Hz？", 1/(2*pi*math.sqrt(10e-3*100e-9)), "Hz", r"$f=\dfrac{1}{2\pi\sqrt{LC}}=\dfrac{1}{2\pi\sqrt{«L»\times10^{-3}\times«C»\times10^{-9}}}=«ans»\ \mathrm{Hz}$。", L=10, C=100),
        prob(r"螺線管 «N» 匝、長 «l» m、截面積 «A» m²，電感是多少 mH？", mu0*500**2*1e-3/0.2*1000, "mH", r"$L=\dfrac{\mu_0N^2A}{l}=\dfrac{4\pi\times10^{-7}\times«N»^2\times«A»}{«l»}=«ans»\ \mathrm{mH}$。", N=500, l=0.2, A=1e-3),
    ],
))

add(Chapter(
    id="ac-circuits", unit="em", no=12, title="交流電路",
    lead="電阻、電感、電容在交流電下各有不同的行為；阻抗把三者合起來，共振是電路最重要的現象。",
    body=r"""
## 交流電與有效值

交流電壓 $v(t)=V_m\sin\omega t$，$\omega=2\pi f$（台灣市電 $f=60\ \mathrm{Hz}$）。交流電的有效值（rms）是產生相同熱功率的直流值：

$$V_{rms}=\frac{V_m}{\sqrt2}\approx0.707\,V_m$$

家用 110 V 是有效值，峰值約 156 V；220 V 的峰值約 311 V。電表與電器標示的都是有效值。

## 三種元件的反應

元件對交流電的阻礙叫電抗（單位 $\Omega$）：

- 電阻：$R$，電壓與電流**同相**，與頻率無關
- 電感：$X_L=\omega L$，電壓**領先**電流 $90^\circ$，頻率越高阻礙越大
- 電容：$X_C=\dfrac{1}{\omega C}$，電壓**落後**電流 $90^\circ$，頻率越高阻礙越小

直流（$\omega=0$）時，電感是導線、電容是斷路；高頻時剛好相反。濾波器就利用這個特性。

## RLC 串聯

總阻礙叫阻抗：

$$Z=\sqrt{R^2+(X_L-X_C)^2},\qquad I_{rms}=\frac{V_{rms}}{Z}$$

電流與電壓的相位差 $\phi$：$\tan\phi=\dfrac{X_L-X_C}{R}$。

## 共振

$X_L=X_C$ 時 $Z=R$ 最小，電流最大：

$$f_0=\frac{1}{2\pi\sqrt{LC}}$$

收音機、無線電的調諧電路就用共振挑出想要的頻率。

## 功率

只有電阻消耗功率：

$$P_{avg}=I_{rms}V_{rms}\cos\phi=I_{rms}^2R$$

$\cos\phi$ 叫功率因數。電感與電容只是把能量借出去再還回來，平均不耗能，但電流在線路上跑還是會有損耗，所以工廠要用電容補償來提高功率因數。

>! 交流電路的電壓不能直接代數相加：$V_R$、$V_L$、$V_C$ 的相位不同，要用向量（相量）加，所以 $V\ne V_R+V_L+V_C$。
""",
    problems=[
        prob(r"交流電壓峰值 «Vm» V，有效值是多少 V？", 311/math.sqrt(2), "V", r"$V_{rms}=\dfrac{V_m}{\sqrt2}=\dfrac{«Vm»}{\sqrt2}=«ans»\ \mathrm V$。", Vm=311),
        prob(r"電感 «L» H 在 «f» Hz 的交流電中，感抗是多少 Ω？", 2*pi*60*0.1, "Ω", r"$X_L=\omega L=2\pi fL=2\pi\times«f»\times«L»=«ans»\ \Omega$。", L=0.1, f=60),
        prob(r"電容 «C» μF 在 «f» Hz 的交流電中，容抗是多少 Ω？", 1/(2*pi*60*50e-6), "Ω", r"$X_C=\dfrac{1}{2\pi fC}=\dfrac{1}{2\pi\times«f»\times«C»\times10^{-6}}=«ans»\ \Omega$。", C=50, f=60),
        prob(r"RLC 串聯電路 $R=«R»\ \Omega$、$X_L=«XL»\ \Omega$、$X_C=«XC»\ \Omega$，阻抗是多少 Ω？", math.sqrt(30**2+(70-30)**2), "Ω", r"$Z=\sqrt{R^2+(X_L-X_C)^2}=\sqrt{«R»^2+(«XL»-«XC»)^2}=«ans»\ \Omega$。", R=30, XL=70, XC=30),
        prob(r"RLC 串聯 $L=«L»\ \mathrm H$、$C=«C»\ \mu\mathrm F$，共振頻率是多少 Hz？", 1/(2*pi*math.sqrt(0.05*20e-6)), "Hz", r"$f_0=\dfrac{1}{2\pi\sqrt{LC}}=\dfrac{1}{2\pi\sqrt{«L»\times«C»\times10^{-6}}}=«ans»\ \mathrm{Hz}$。", L=0.05, C=20),
    ],
))

add(Chapter(
    id="em-waves", unit="em", no=13, title="電磁波",
    lead="變化的電場產生磁場、變化的磁場產生電場：馬克士威方程式預言了電磁波，光就是它的一種。",
    body=r"""
## 馬克士威的結論

馬克士威方程式（高斯定律、磁的高斯定律、法拉第定律、安培與馬克士威定律）完整描述電磁現象。他補上「變化的電場也產生磁場」之後，推出電磁場可以像波一樣脫離電荷自行傳播，波速：

$$c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}=2.998\times10^8\ \mathrm{m/s}$$

這個數值與當時測得的光速吻合，確認光是電磁波。

## 電磁波的性質

- 橫波：$\vec E$、$\vec B$、傳播方向三者互相垂直
- $\vec E$ 與 $\vec B$ 同相，大小比 $E=cB$
- 不需介質，真空中速度都是 $c$
- 波速、頻率與波長：$c=f\lambda$

## 電磁波譜

按頻率由低到高：無線電波、微波、紅外線、可見光（約 400 到 700 nm）、紫外線、X 射線、γ 射線。它們本質相同，只是頻率不同，與物質的作用就大不相同：微波使水分子轉動，紅外線感覺到熱，X 射線穿透軟組織。

## 能量與強度

電磁波帶有能量，強度（單位面積的平均功率）：

$$I=\tfrac12c\varepsilon_0E_0^2$$

$E_0$ 是電場振幅。強度正比於電場振幅的平方。電磁波也帶動量，照在表面上產生輻射壓（彗星的尾巴被太陽光吹開、太陽帆就是這個）。

## 偏振

光是橫波，電場振動方向可以被篩選。理想偏振片只讓一個方向的電場通過。強度為 $I_0$ 的偏振光通過夾角 $\theta$ 的偏振片：

$$I=I_0\cos^2\theta\quad(\text{馬呂斯定律})$$

非偏振光通過第一片偏振片，強度剩一半。偏光太陽眼鏡用水平反射光是水平偏振的原理，擋掉眩光。

>! 兩片偏振片互相垂直（$90^\circ$）時完全不透光；但在它們中間再插入一片 $45^\circ$ 的偏振片，反而有光透出來（每一片重新設定偏振方向）。
""",
    problems=[
        prob(r"由 $\mu_0=4\pi\times10^{-7}$ 與 $\varepsilon_0=8.854\times10^{-12}$ 算出真空中的光速是多少 m/s？", 1/math.sqrt(mu0*eps0), "m/s", r"$c=\dfrac1{\sqrt{\mu_0\varepsilon_0}}=«ans»\ \mathrm{m/s}$。"),
        prob(r"FM 電台頻率 «f» MHz 的電磁波，波長是多少 m？（$c=2.998\times10^8$）", 2.998e8/100e6, "m", r"$\lambda=\dfrac cf=\dfrac{2.998\times10^8}{«f»\times10^6}=«ans»\ \mathrm m$。", f=100),
        prob(r"電磁波的電場振幅 $E_0=«E0»$ V/m，磁場振幅是多少 T？", 300/2.998e8, "T", r"$B_0=\dfrac{E_0}{c}=\dfrac{«E0»}{2.998\times10^8}=«ans»\ \mathrm T$。", E0=300),
        prob(r"電磁波電場振幅 $E_0=«E0»$ V/m，強度是多少 W/m²？", 0.5*2.998e8*eps0*100**2, "W/m²", r"$I=\tfrac12c\varepsilon_0E_0^2=\tfrac12\times2.998\times10^8\times8.854\times10^{-12}\times«E0»^2=«ans»\ \mathrm{W/m^2}$。", E0=100),
        prob(r"偏振光強度 «I0» W/m²，通過與偏振方向夾 «t»° 的偏振片後，強度是多少 W/m²？", 40*math.cos(math.radians(30))**2, "W/m²", r"$I=I_0\cos^2\theta=«I0»\times\cos^2«t»^\circ=«ans»\ \mathrm{W/m^2}$。", I0=40, t=30),
    ],
))
