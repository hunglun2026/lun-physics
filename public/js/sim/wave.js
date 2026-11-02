/* 振動與波模擬：彈簧振子、波的疊加與拍。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims;

  S["wave-shm"] = function (box) {
    var ui = U.make(box, 640, 300, "彈簧振子與位移對時間的圖"), c = ui.ctx;
    U.slider(ui, "m", "質量 m", 0.5, 5, 0.5, 1, "kg"); U.slider(ui, "k", "彈力常數 k", 10, 200, 5, 50, "N/m", 0); U.slider(ui, "A", "振幅 A", 0.2, 1, 0.05, 0.6, "m", 2);
    var t = 0, hist = [];
    ui.on.push(function () { hist = []; });
    var lp = U.loop(ui, function (dt) { t += dt; }, function () {
      U.clear(ui); var p = ui.p, w = Math.sqrt(p.k / p.m), T = 2 * Math.PI / w, x = p.A * Math.cos(w * t), v = -p.A * w * Math.sin(w * t);
      hist.push([t, x]); while (hist.length && hist[0][0] < t - 2.5 * T) hist.shift();
      // 左：彈簧與物塊
      var wall = 30, y = 70, cx = 150 + x * 110;
      U.line(c, wall, 30, wall, 110, U.GRAY, 4);
      c.beginPath(); c.moveTo(wall, y); for (var i = 0; i <= 24; i++) { var X = wall + (cx - 20 - wall) * i / 24; c.lineTo(X, y + (i % 2 ? -10 : 10) * (i > 0 && i < 24 ? 1 : 0)); }
      c.strokeStyle = U.GRAY; c.lineWidth = 2; c.stroke();
      c.fillStyle = U.BLUE; c.fillRect(cx - 20, y - 20, 40, 40); U.line(c, 150, 115, 150, 130, U.GRID, 1, [3, 3]);
      // 能量長條
      var E = 0.5 * p.k * p.A * p.A, K = 0.5 * p.m * v * v, Us = 0.5 * p.k * x * x, bx = 400, bw = 60;
      c.fillStyle = U.AMBER; c.fillRect(bx, 130 - 110 * K / E, bw, 110 * K / E); c.fillStyle = U.BLUE; c.fillRect(bx + 80, 130 - 110 * Us / E, bw, 110 * Us / E);
      U.line(c, bx - 10, 20, bx + 160, 20, U.GRAY, 1, [4, 4]); U.text(c, "總能量", bx + 100, 14, U.GRAY, 12, "left");
      U.text(c, "動能", bx + 30, 146, U.AMBER, 12, "center"); U.text(c, "彈性位能", bx + 110, 146, U.BLUE, 12, "center");
      // 下：x-t
      var A2 = U.axes(ui, 40, 165, 580, 120, t - 2.5 * T, t, -p.A * 1.1, p.A * 1.1, "t", "x");
      c.beginPath(); hist.forEach(function (q, i) { var X = A2.X(q[0]), Y = A2.Y(q[1]); i ? c.lineTo(X, Y) : c.moveTo(X, Y); }); c.strokeStyle = U.RED; c.lineWidth = 2.2; c.stroke();
      ui.read.textContent = "週期 T = 2π√(m/k) = " + T.toFixed(2) + " s　總能量 E = ½kA² = " + E.toFixed(2) + " J（改變振幅不會改變週期）";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };

  S["wave-superpos"] = function (box) {
    var ui = U.make(box, 640, 340, "兩個波疊加成合成波，滑桿調整第二個波的頻率與相位"), c = ui.ctx;
    U.slider(ui, "f2", "第二個波的頻率比", 0.5, 2.5, 0.05, 1.1, "×", 2); U.slider(ui, "ph", "相位差", 0, 360, 10, 0, "°", 0); U.slider(ui, "a2", "第二個波的振幅", 0, 1, 0.1, 1, "", 1);
    var t = 0;
    var lp = U.loop(ui, function (dt) { t += dt * 0.6; }, function () {
      U.clear(ui); var p = ui.p, ph = p.ph * Math.PI / 180, W = 580, f1 = 3;
      function wave(y0, h, fn, col, lab) {
        U.line(c, 40, y0, 620, y0, U.GRID, 1); c.beginPath();
        for (var i = 0; i <= 290; i++) { var x = i / 290, Y = y0 - h * fn(x); i ? c.lineTo(40 + x * W, Y) : c.moveTo(40 + x * W, Y); }
        c.strokeStyle = col; c.lineWidth = 2.4; c.stroke(); U.text(c, lab, 44, y0 - 38, col, 12);
      }
      var w1 = function (x) { return Math.sin(2 * Math.PI * (f1 * x - t)); };
      var w2 = function (x) { return p.a2 * Math.sin(2 * Math.PI * (f1 * p.f2 * x - t * p.f2) + ph); };
      wave(60, 36, w1, U.BLUE, "波 1"); wave(145, 36, w2, U.AMBER, "波 2"); wave(265, 70, function (x) { return (w1(x) + w2(x)) / 2; }, U.RED, "合成（疊加）");
      var df = Math.abs(f1 * p.f2 - f1);
      ui.read.textContent = df < 0.05 ? "頻率相同：相位差 0° 增強、180° 抵消" : "頻率差 " + df.toFixed(2) + "：合成波的包絡週期性變大變小，這就是「拍」（聲音忽大忽小）";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };
})();
