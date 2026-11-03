"""說明頁「怎麼用」：結構化的新手指南（步驟卡、範例框、學習順序、常見問題）。

文字塊交給 render.body_to_html（含 $公式$ 佔位符），外層卡片用手寫 HTML；build.py 之後統一 finish()。
"""
from __future__ import annotations

import render as R


def P_help(rng: dict[str, tuple[int, int]]):
    def r(u: str) -> str:
        a, b = rng[u]
        return f'<a href="/home#u-{u}">第 {a}～{b} 章</a>'

    md = R.body_to_html
    inline = R.inline
    demo = md("""> 這是「重點」框：公式、定義、一定要記住的結論。

>! 這是「常見錯誤」框：大多數人會踩的坑，先看過就能少錯一次。""")
    sci = inline(r"`3.2e5` 代表 $3.2\times10^5$，`4e-3` 代表 $4\times10^{-3}$")
    g = inline(r"全站重力加速度取 $g = 9.8\ \mathrm{m/s^2}$")
    body = f"""<p class="lead">三分鐘看完，之後就能自己走。</p>
<ul class="toc" aria-label="本頁目錄"><li><a href="#start">快速上手</a></li><li><a href="#chapter">一章的樣子</a></li><li><a href="#sim">玩模擬</a></li><li><a href="#answer">輸入答案</a></li><li><a href="#order">教學順序</a></li><li><a href="#progress">進度</a></li><li><a href="#faq">常見問題</a></li></ul>

<h2 id="start">快速上手</h2>
<ol class="cards">
<li class="card"><span class="n">1</span><h3>選一章</h3><p>首頁按單元排好。完全沒基礎就從力學第一章開始；想找特定主題，用首頁的搜尋框打關鍵字。</p></li>
<li class="card"><span class="n">2</span><h3>讀講解、玩模擬</h3><p>先看講解，遇到模擬就拖滑桿試試看。不懂的地方先跳過，做題時會再回頭用到。</p></li>
<li class="card"><span class="n">3</span><h3>做題、標記讀完</h3><p>整章題目都答對，或按「標記這章讀完」，首頁的章節就會變成綠色打勾。</p></li>
</ol>

<h2 id="chapter">一章的樣子</h2>
<p>每一章由上到下是：開頭一句話說明這章在解決什麼，接著是講解與公式（互動模擬穿插在講解裡）、練習題，最後是延伸閱讀與上一章、下一章的按鈕。講解裡有兩種色塊：</p>
<div class="demo">{demo}</div>
<p>公式用數學排版，手機上太長的公式可以左右滑動看完整。</p>

<h2 id="sim">怎麼玩互動模擬</h2>
<ul>
<li>拖動滑桿，畫面和下方的數字會即時改變；有些模擬還有按鈕，可以開始、暫停或重來</li>
<li>手機和平板用手指拖動就好</li>
<li>模擬是簡化版，目的是建立直覺，看趨勢與比例，不拿來取代題目的精確計算</li>
<li>如果顯示「模擬載入失敗」，重新整理一次；還是不行請按頁面下方的「回報錯誤」</li>
</ul>

<h2 id="answer">輸入答案</h2>
<div class="cards">
<div class="card"><h3>只輸入數字</h3><p>不用寫單位，單位已經顯示在輸入框旁邊。</p></div>
<div class="card"><h3>很大或很小的數</h3><p>用科學記號：{sci}。</p></div>
<div class="card"><h3>容許約 2% 誤差</h3><p>四捨五入的差別不會被判錯。但中途就先四捨五入，誤差可能累積超過 2%。</p></div>
</div>
<p>答錯時會有兩種訊息：「很接近了」代表你的數字在 15% 以內，多半是計算小失誤或有效位數；「再算算看」代表方向可能不對，可以先看提示。{g}，其他常數都會在題目裡寫明。</p>

<h2 id="order">教學順序與先修</h2>
<p>章節順序已對照 Halliday、Resnick、Walker 的《Fundamentals of Physics》與 Young、Freedman 的《University Physics》兩本標準教科書的目錄：力學、振動與波、熱學、電磁學、光學、近代物理，主線章序相同，所以由第 1 章一路讀下去就是最穩的走法。想跳著讀，可以照下表確認需要先會什麼。</p>
<div class="tbl"><table>
<thead><tr><th>單元</th><th>章節</th><th>建議先會</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>力學</td><td>{r("mechanics")}</td><td>高中代數、三角函數</td><td>整套課的基礎。向量與牛頓定律先紮實，後面都會用到</td></tr>
<tr><td>振動與波</td><td>{r("waves")}</td><td>力學的力與能量</td><td>簡諧運動就是彈簧與能量守恆的應用</td></tr>
<tr><td>熱學</td><td>{r("thermo")}</td><td>力學的能量</td><td>熱力學第一定律是能量守恆的延伸</td></tr>
<tr><td>電磁學</td><td>{r("em")}</td><td>力學的向量、功與能量</td><td>電場與電位的算法跟重力場很像；少數章節會用到積分的概念</td></tr>
<tr><td>光學</td><td>{r("optics")}</td><td>振動與波</td><td>干涉與繞射就是波的疊加；最後一章電磁波也是光學的基礎</td></tr>
<tr><td>近代物理</td><td>{r("modern")}</td><td>力學、電磁學</td><td>相對論與量子都在修正前面的古典想法</td></tr>
</tbody></table></div>

<h2 id="progress">進度與隱私</h2>
<p>「標記這章讀完」和答對的題目，只存在你這台裝置的瀏覽器裡，不會上傳，也不用登入。換裝置、換瀏覽器，或清除瀏覽器資料之後，進度就會歸零。</p>

<h2 id="faq">常見問題</h2>
<div class="faq">
<details><summary>要註冊或付費嗎？</summary><p>不用。沒有帳號、沒有廣告，全部免費。</p></details>
<details><summary>一定要會微積分嗎？</summary><p>大部分章節只用到代數與三角函數。電磁學有少數地方會提到「把很多小塊加起來」的積分概念，文字會說明做法，不會要求你自己積分。</p></details>
<details><summary>我的答案明明對，卻被判錯？</summary><p>先檢查三件事：單位有沒有換算（例如公分要換成公尺）、中途有沒有太早四捨五入、題目指定的 g 值或常數有沒有照用。都對的話，請按「回報錯誤」告訴我們題號。</p></details>
<details><summary>為什麼進度不見了？</summary><p>進度存在瀏覽器裡。使用無痕視窗、換手機或電腦、清除網站資料，都會讓它消失。</p></details>
<details><summary>發現講解有錯怎麼辦？</summary><p>每一頁最下方都有「回報錯誤」，不用留姓名或聯絡方式，寫清楚哪一題或哪一句就好。程式能驗算題目與答案，但觀念有沒有講對還是要靠大家回報。</p></details>
<details><summary>可以用手機讀嗎？</summary><p>可以。版面和模擬都有照手機調整；長公式左右滑動即可。</p></details>
</div>"""
    return ("怎麼用", "三分鐘學會用這個網站：怎麼讀章節、玩模擬、輸入答案、建議學習順序與常見問題。", body)
