/* 首頁：標示已讀完的章節、統計、搜尋。 */
(function () {
  "use strict";
  var all = PHYS.all(), done = 0;
  document.querySelectorAll("a[data-ch]").forEach(function (a) {
    var p = all[a.dataset.ch];
    if (p && p.done) { a.classList.add("done"); done++; }
  });
  var dn = document.getElementById("doneN");
  if (dn) dn.textContent = done;

  var q = document.getElementById("q"), qn = document.getElementById("qn");
  if (!q) return;
  var meta = null;
  function filter() {
    var t = q.value.trim().toLowerCase(), shown = 0;
    document.querySelectorAll(".unit").forEach(function (u) {
      var any = false;
      u.querySelectorAll("li").forEach(function (li) {
        var a = li.querySelector("a"), m = meta && meta[a.dataset.ch];
        var hay = (a.textContent + " " + (m ? m.lead : "")).toLowerCase();
        var hit = !t || hay.indexOf(t) >= 0;
        li.hidden = !hit; if (hit) { any = true; shown++; }
      });
      u.hidden = !any;
    });
    qn.textContent = t ? (shown ? "找到 " + shown + " 章" : "沒有符合的章節") : "";
  }
  q.addEventListener("input", filter);
  fetch("/data/chapters.json").then(function (r) { return r.json(); }).then(function (a) {
    meta = {}; a.forEach(function (c) { meta[c.id] = c; }); filter();
  }).catch(function () { meta = {}; });
})();
