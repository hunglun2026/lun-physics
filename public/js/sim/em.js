/* 電磁學模擬：電場、RC 電路、磁場中的帶電粒子、發電機。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims;

  S["em-efield"] = function (box) {
    var ui = U.make(box, 640, 340, "兩個點電荷的電場箭頭圖，滑桿調整電荷與距離"), c = ui.ctx;
    U.slider(ui, "q1", "左邊電荷 q1", -3, 3, 1, 2, "", 0); U.slider(ui, "q2", "右邊電荷 q2", -3, 3, 1, -2, "", 0); U.slider(ui, "d", "距離", 100, 400, 10, 240, "", 0);
    U.loop(ui, function () {}, function () {
      U.clear(ui); var p = ui.p, cx = 320, cy = 170, x1 = cx - p.d / 2, x2 = cx + p.d / 2;
      function E(x, y) {
        var ex = 0, ey = 0;
        [[x1, p.q1], [x2, p.q2]].forEach(function (q) { var dx = x - q[0], dy = y - cy, r2 = dx * dx + dy * dy + 100, r = Math.sqrt(r2); ex += q[1] * dx / (r2 * r) * 2e4; ey += q[1] * dy / (r2 * r) * 2e4; });
        return [ex, ey];
      }
      for (var x = 30; x < 620; x += 30) for (var y = 25; y < 330; y += 30) {
        if (Math.hypot(x - x1, y - cy) < 16 || Math.hypot(x - x2, y - cy) < 16) continue;
        var f = E(x, y), m = Math.hypot(f[0], f[1]); if (m < 1e-6) continue;
        var len = Math.min(24, 6 + Math.log(1 + m * 40) * 5), ux = f[0] / m * len, uy = f[1] / m * len;
        var al = Math.min(1, 0.25 + Math.log(1 + m * 40) / 4);
        c.globalAlpha = al; U.arrow(c, x - ux / 2, y - uy / 2, x + ux / 2, y + uy / 2, U.GRAY, 1.6); c.globalAlpha = 1;
      }
      [[x1, p.q1], [x2, p.q2]].forEach(function (q) {
        U.dot(c, q[0], cy, 13, q[1] > 0 ? U.RED : q[1] < 0 ? U.BLUE : U.GRID); U.text(c, q[1] > 0 ? "+" : q[1] < 0 ? "−" : "0", q[0], cy + 5, "#fff", 16, "center");
      });
      ui.read.textContent = "箭頭方向是正試探電荷受力的方向，越亮越強。試試 q1 與 q2 同號（中點電場互相抵消）與異號（中點電場相加）。";
    });
  };

  S["em-rc"] = function (box) {
    var ui = U.make(box, 640, 300, "RC 電路的充電與放電曲線，滑桿調整電阻與電容"), c = ui.ctx;
    U.slider(ui, "R", "電阻 R", 1, 10, 1, 4, "kΩ", 0); U.slider(ui, "C", "電容 C", 1, 10, 1, 5, "μF", 0);
    var t = 0, charge = true;
    var lp = U.loop(ui, function (dt) { t += dt; var tau = ui.p.R * ui.p.C * 1e-3; if (t > 5 * tau) { t = 0; charge = !charge; } }, function () {
      U.clear(ui); var p = ui.p, tau = p.R * p.C * 1e-3, T = 5 * tau, A = U.axes(ui, 50, 20, 560, 220, 0, 5, 0, 1.05, "t / τ", "V / ε");
      U.line(c, A.X(0), A.Y(1), A.X(5), A.Y(1), U.GRID, 1, [4, 4]); U.line(c, A.X(1), A.Y(0), A.X(1), A.Y(1.05), U.GRID, 1, [4, 4]);
      c.beginPath(); for (var i = 0; i <= 100; i++) { var x = i / 20, v = charge ? 1 - Math.exp(-x) : Math.exp(-x); i ? c.lineTo(A.X(x), A.Y(v)) : c.moveTo(A.X(x), A.Y(v)); }
      c.strokeStyle = U.GRID; c.lineWidth = 3; c.stroke();
      var x2 = Math.min(t / tau, 5), v2 = charge ? 1 - Math.exp(-x2) : Math.exp(-x2);
      c.beginPath(); for (i = 0; i <= 100; i++) { var xx = x2 * i / 100, vv = charge ? 1 - Math.exp(-xx) : Math.exp(-xx); i ? c.lineTo(A.X(xx), A.Y(vv)) : c.moveTo(A.X(xx), A.Y(vv)); }
      c.strokeStyle = U.BLUE; c.lineWidth = 3; c.stroke(); U.dot(c, A.X(x2), A.Y(v2), 6, U.RED);
      U.text(c, "τ", A.X(1), A.Y(0) + 32, U.GRAY, 13, "center");
      ui.read.textContent = (charge ? "充電" : "放電") + "中　τ = RC = " + (tau * 1000).toFixed(1) + " ms　目前 V = " + (v2 * 100).toFixed(0) + "% ε（一個 τ 後：" + (charge ? "63%" : "37%") + "）";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };

  S["em-bfield"] = function (box) {
    var ui = U.make(box, 640, 320, "帶電粒子在垂直紙面向內的磁場中做圓周運動"), c = ui.ctx;
    U.slider(ui, "v", "速率 v", 1, 5, 0.5, 3, "", 1); U.slider(ui, "B", "磁場 B", 0.5, 3, 0.25, 1, "T", 2); U.slider(ui, "q", "電荷正負（+1 或 −1）", -1, 1, 2, 1, "", 0);
    var a = 0, trail = [];
    ui.on.push(function () { trail = []; });
    U.loop(ui, function (dt) { a += dt * ui.p.B * ui.p.v / ui.p.v * 1.2 * Math.sign(-ui.p.q || 1); }, function () {
      U.clear(ui); var p = ui.p, r = 40 * p.v / p.B, cx = 320, cy = 170;
      for (var x = 40; x < 620; x += 40) for (var y = 30; y < 320; y += 40) { U.text(c, "×", x, y + 4, "#c9d3e6", 14, "center"); }
      if (r < 150) {
        c.beginPath(); c.arc(cx, cy, r, 0, 6.2832); c.strokeStyle = U.GRID; c.lineWidth = 2; c.setLineDash([5, 4]); c.stroke(); c.setLineDash([]);
        var px = cx + r * Math.cos(a), py = cy + r * Math.sin(a); U.dot(c, px, py, 8, p.q > 0 ? U.RED : U.BLUE);
        var dir = Math.sign(-p.q || 1); U.arrow(c, px, py, px - dir * Math.sin(a) * 38, py + dir * Math.cos(a) * 38, U.GREEN, 2.5);
        U.arrow(c, px, py, px + (cx - px) * 0.35, py + (cy - py) * 0.35, U.AMBER, 2.5);
      } else U.text(c, "半徑太大，超出畫面（試試降低速率或加大磁場）", cx, cy, U.GRAY, 14, "center");
      ui.read.textContent = "半徑 r = mv/(qB) 正比於 v/B：這裡 r ∝ " + (p.v / p.B).toFixed(2) + "。綠：速度，橘：磁力（永遠指向圓心，不作功）。" + (p.q > 0 ? "正電荷" : "負電荷") + "在磁場指入紙面時沿" + (p.q > 0 ? "逆" : "順") + "時針轉。";
    });
  };

  S["em-gen"] = function (box) {
    var ui = U.make(box, 640, 320, "旋轉線圈發電機與輸出的弦波電動勢"), c = ui.ctx;
    U.slider(ui, "w", "轉速 ω", 1, 6, 0.5, 2.5, "rad/s"); U.slider(ui, "B", "磁場 B（相對）", 0.5, 2, 0.1, 1, "", 1);
    var th = 0, hist = [];
    var lp = U.loop(ui, function (dt) { th += ui.p.w * dt; hist.push(Math.sin(th) * ui.p.w * ui.p.B); if (hist.length > 240) hist.shift(); }, function () {
      U.clear(ui); var p = ui.p, cx = 130, cy = 150;
      c.fillStyle = "#ffe6e3"; c.fillRect(30, 50, 40, 200); c.fillStyle = "#e3ecff"; c.fillRect(190, 50, 40, 200); U.text(c, "N", 50, 155, U.RED, 18, "center"); U.text(c, "S", 210, 155, U.BLUE, 18, "center");
      var h = 60, w = 60 * Math.abs(Math.cos(th)) + 4;
      c.strokeStyle = U.AMBER; c.lineWidth = 5; c.strokeRect(cx - w / 2, cy - h, w, 2 * h);
      U.text(c, "磁通量 Φ = BA cosθ，電動勢 ε = −dΦ/dt", 30, 290, U.GRAY, 12);
      var A = U.axes(ui, 300, 30, 320, 250, 0, 240, -6.5, 6.5, "t", "ε");
      c.beginPath(); hist.forEach(function (v, i) { var X = A.X(i), Y = A.Y(v); i ? c.lineTo(X, Y) : c.moveTo(X, Y); }); c.strokeStyle = U.RED; c.lineWidth = 2.2; c.stroke();
      ui.read.textContent = "峰值電動勢 ε_max = NBAω（正比於 B 與 ω）= " + (p.w * p.B).toFixed(2) + "（相對值）。線圈與磁場垂直（Φ 最大）時 ε = 0；平行時 ε 最大。";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };
})();
