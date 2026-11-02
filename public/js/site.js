/* 全站共用：本機進度、回報錯誤對話框。進度只存在這台裝置的 localStorage，不上傳。 */
(function () {
  "use strict";
  var KEY = "phys.progress.v1";
  var mem = {};
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return mem; }
  }
  function save(o) {
    mem = o;
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* 無痕或被擋：本次分頁內有效即可 */ }
  }
  window.PHYS = {
    sims: {},
    get: function (id) { var o = load(); return o[id] || { done: false, solved: [] }; },
    set: function (id, v) { var o = load(); o[id] = v; save(o); },
    all: load
  };

  // 回報錯誤
  var dlg = document.getElementById("reportDlg");
  if (!dlg || typeof dlg.showModal !== "function") return;
  var txt = document.getElementById("reportText"), msg = document.getElementById("reportMsg"), send = document.getElementById("reportSend");
  document.querySelectorAll("[data-report]").forEach(function (b) {
    b.addEventListener("click", function () { msg.textContent = ""; send.disabled = false; dlg.showModal(); txt.focus(); });
  });
  document.getElementById("reportCancel").addEventListener("click", function () { dlg.close(); });
  document.getElementById("reportForm").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var text = txt.value.trim();
    if (text.length < 4) { msg.textContent = "請多寫幾個字，讓我們知道哪裡有問題。"; return; }
    send.disabled = true; msg.textContent = "送出中…";
    fetch("/report", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text: text, page: location.pathname }) })
      .then(function (r) {
        if (r.status === 429) throw new Error("送太多次了，請十分鐘後再試。");
        if (!r.ok) throw new Error("送出失敗，請稍後再試。");
        msg.textContent = "已收到，謝謝你。"; txt.value = "";
        setTimeout(function () { dlg.close(); }, 1200);
      })
      .catch(function (e) { msg.textContent = e.message; send.disabled = false; });
  });
})();
