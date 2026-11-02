/* 互動模擬共用庫：畫布、滑桿、按鈕、動畫迴圈。每個模擬檔用 PHYS.sims["檔-名稱"] = function (box) {...} 註冊。 */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var INK = "#16202e", GRID = "#d7deea", BLUE = "#2a5db0", AMBER = "#c77d00", RED = "#b3261e", GREEN = "#17784a", GRAY = "#52607a";

  function make(box, w, h, desc) {
    box.textContent = "";
    var cv = document.createElement("canvas"), dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = w * dpr; cv.height = h * dpr; cv.setAttribute("role", "img"); cv.setAttribute("aria-label", desc || "互動模擬");
    var ctx = cv.getContext("2d"); ctx.scale(dpr, dpr);
    var ctl = document.createElement("div"); ctl.className = "simctl";
    var read = document.createElement("p"); read.className = "simread"; read.setAttribute("aria-live", "polite");
    var btns = document.createElement("div"); btns.className = "simbtn";
    box.appendChild(cv); box.appendChild(ctl); box.appendChild(btns); box.appendChild(read);
    return { cv: cv, ctx: ctx, ctl: ctl, read: read, btns: btns, W: w, H: h, p: {}, on: [] };
  }
  function slider(ui, k, label, min, max, step, val, unit, dec) {
    var l = document.createElement("label"), o = document.createElement("output"), r = document.createElement("input");
    r.type = "range"; r.min = min; r.max = max; r.step = step; r.value = val; ui.p[k] = +val;
    function show() { o.textContent = (+r.value).toFixed(dec == null ? 1 : dec) + (unit ? " " + unit : ""); }
    r.addEventListener("input", function () { ui.p[k] = +r.value; show(); ui.on.forEach(function (f) { f(k); }); });
    l.appendChild(document.createTextNode(label)); l.appendChild(o); l.appendChild(r); ui.ctl.appendChild(l); show();
    return r;
  }
  function button(ui, text, fn) {
    var b = document.createElement("button"); b.type = "button"; b.className = "btn ghost"; b.textContent = text;
    b.addEventListener("click", fn); ui.btns.appendChild(b); return b;
  }
  /* 動畫迴圈：畫面不在視窗內或分頁在背景時暫停；偏好減少動態時不自動播放（只靠滑桿重畫）。 */
  function loop(ui, step, draw) {
    var run = !reduce, last = null, vis = true;
    function frame(t) {
      if (run && vis && !document.hidden) { var dt = last == null ? 0 : Math.min((t - last) / 1000, 0.05); step(dt); draw(); }
      last = t; requestAnimationFrame(frame);
    }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(ui.cv);
    ui.on.push(function () { draw(); });
    draw(); requestAnimationFrame(frame);
    return { toggle: function () { run = !run; return run; }, running: function () { return run; } };
  }
  function clear(ui) { var c = ui.ctx; c.fillStyle = "#fff"; c.fillRect(0, 0, ui.W, ui.H); }
  function line(c, x1, y1, x2, y2, col, w, dash) {
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.strokeStyle = col || INK; c.lineWidth = w || 1.5;
    c.setLineDash(dash || []); c.stroke(); c.setLineDash([]);
  }
  function arrow(c, x1, y1, x2, y2, col, w) {
    var a = Math.atan2(y2 - y1, x2 - x1), s = 8;
    line(c, x1, y1, x2, y2, col, w || 2.5);
    c.beginPath(); c.moveTo(x2, y2); c.lineTo(x2 - s * Math.cos(a - 0.4), y2 - s * Math.sin(a - 0.4));
    c.lineTo(x2 - s * Math.cos(a + 0.4), y2 - s * Math.sin(a + 0.4)); c.closePath(); c.fillStyle = col || INK; c.fill();
  }
  function dot(c, x, y, r, col) { c.beginPath(); c.arc(x, y, r, 0, 6.2832); c.fillStyle = col || BLUE; c.fill(); }
  function text(c, s, x, y, col, size, align) {
    c.fillStyle = col || INK; c.font = (size || 13) + 'px "PhysSans","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif'; c.textAlign = align || "left"; c.fillText(s, x, y);
  }
  /* 座標軸：框出 (x0,y0,w,h)，資料範圍 [xmin,xmax]×[ymin,ymax]，回傳資料座標→畫面座標的函式 */
  function axes(ui, x0, y0, w, h, xmin, xmax, ymin, ymax, xl, yl) {
    var c = ui.ctx;
    function X(x) { return x0 + (x - xmin) / (xmax - xmin) * w; }
    function Y(y) { return y0 + h - (y - ymin) / (ymax - ymin) * h; }
    line(c, x0, y0 + h, x0 + w, y0 + h, GRAY, 1.5); line(c, x0, y0, x0, y0 + h, GRAY, 1.5);
    if (ymin < 0 && ymax > 0) line(c, x0, Y(0), x0 + w, Y(0), GRID, 1);
    text(c, xl || "", x0 + w, y0 + h + 16, GRAY, 12, "right"); text(c, yl || "", x0 + 4, y0 + 12, GRAY, 12);
    return { X: X, Y: Y };
  }
  window.PHYS.ui = { make: make, slider: slider, button: button, loop: loop, clear: clear, line: line, arrow: arrow, dot: dot, text: text, axes: axes,
    INK: INK, GRID: GRID, BLUE: BLUE, AMBER: AMBER, RED: RED, GREEN: GREEN, GRAY: GRAY, reduce: reduce };
})();
