/* 章節頁：練習題檢查、讀完標記、載入互動模擬。 */
(function () {
  "use strict";
  var art = document.querySelector("article.chapter");
  if (!art) return;
  var id = art.dataset.ch, n = +art.dataset.nprob;
  var st = PHYS.get(id);

  var doneBtn = document.getElementById("doneBtn");
  function paintDone() {
    doneBtn.setAttribute("aria-pressed", st.done ? "true" : "false");
    doneBtn.textContent = st.done ? "已讀完（再按取消）" : "標記這章讀完";
  }
  doneBtn.addEventListener("click", function () { st.done = !st.done; PHYS.set(id, st); paintDone(); });
  paintDone();

  // 輸入容錯：全形數字與負號、逗號、× 10^ 寫法
  function parse(s) {
    s = s.trim().replace(/[０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); })
      .replace(/[−–－]/g, "-").replace(/,/g, "").replace(/\s+/g, "")
      .replace(/[×x*]10\^?\{?(-?\d+)\}?/i, "e$1");
    if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(s)) return NaN;
    return parseFloat(s);
  }
  function close(a, b, tol) {
    if (b === 0) return Math.abs(a) <= 0.02;
    return Math.abs(a - b) / Math.abs(b) <= tol;
  }

  document.querySelectorAll(".prob").forEach(function (box) {
    var i = +box.dataset.i, ans = parseFloat(box.dataset.ans), tol = parseFloat(box.dataset.tol);
    var inp = box.querySelector(".ans"), res = box.querySelector(".res");
    function mark() { box.classList.add("ok"); }
    if (st.solved.indexOf(i) >= 0) { mark(); res.textContent = "你之前答對了"; res.className = "res ok"; }
    function check() {
      var v = parse(inp.value);
      if (isNaN(v)) { res.textContent = "請輸入數字，例如 12.5 或 3.2e5"; res.className = "res bad"; return; }
      if (close(v, ans, tol)) {
        res.textContent = "答對了"; res.className = "res ok"; mark();
        if (st.solved.indexOf(i) < 0) st.solved.push(i);
        if (st.solved.length >= n) st.done = true;
        PHYS.set(id, st); paintDone();
      } else {
        res.textContent = close(v, ans, 0.15) ? "很接近了，檢查一下計算或有效位數" : "再算算看，卡住可以先看提示";
        res.className = "res bad";
      }
    }
    box.querySelector("[data-act=check]").addEventListener("click", check);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") check(); });
  });

  // 互動模擬：名稱格式「檔案-名稱」，載入 /js/sim/<檔案>.js（先載 simlib.js），該檔註冊 PHYS.sims[完整名稱](容器)
  var me = document.querySelector('script[src*="/js/chapter.js"]');
  var v = me ? (me.src.split("?v=")[1] || "") : "";
  function load(src, cb, fail) {
    var s = document.createElement("script");
    s.src = src + "?v=" + v; s.onload = cb; s.onerror = fail; document.head.appendChild(s);
  }
  var figs = document.querySelectorAll("figure.sim");
  if (!figs.length) return;
  load("/js/simlib.js", function () {
    figs.forEach(function (fig) {
      var name = fig.dataset.sim, box = fig.querySelector(".simbox"), file = name.split("-")[0];
      function run() {
        if (PHYS.sims[name]) PHYS.sims[name](box); else box.textContent = "模擬載入失敗";
      }
      if (PHYS.sims[name]) return run();
      load("/js/sim/" + file + ".js", run, function () { box.textContent = "模擬載入失敗"; });
    });
  }, function () { figs.forEach(function (f) { f.querySelector(".simbox").textContent = "模擬載入失敗"; }); });
})();
