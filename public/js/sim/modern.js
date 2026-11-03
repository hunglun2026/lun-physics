/* 近代物理模擬：時間膨脹與長度收縮、光電效應、放射性衰變。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims;

  S["modern-dilation"] = function (box) {
    var ui = U.make(box, 640, 320, "勞侖茲因子、時間膨脹與長度收縮"), c = ui.ctx;
    U.slider(ui, "b", "速率 v / c", 0, 0.99, 0.01, 0.8, "", 2);
    var t = 0;
    var lp = U.loop(ui, function (dt) { t += dt; }, function () {
      U.clear(ui); var b = ui.p.b, g = 1 / Math.sqrt(1 - b * b);
      // 左：γ–β 曲線
      var A = U.axes(ui, 40, 20, 270, 190, 0, 1, 1, 8, "v / c", "γ");
      c.beginPath(); for (var i = 0; i <= 200; i++) { var x = i / 200 * 0.995, y = Math.min(8, 1 / Math.sqrt(1 - x * x)); i ? c.lineTo(A.X(x), A.Y(y)) : c.moveTo(A.X(x), A.Y(y)); } c.strokeStyle = U.BLUE; c.lineWidth = 2.5; c.stroke();
      U.dot(c, A.X(b), A.Y(Math.min(8, g)), 6, U.RED);
      // 右：兩個鐘（地面的與運動的）
      function clock(cx, cy, ang, col, lab) {
        c.beginPath(); c.arc(cx, cy, 38, 0, 6.2832); c.strokeStyle = col; c.lineWidth = 3; c.stroke();
        U.line(c, cx, cy, cx + 30 * Math.sin(ang), cy - 30 * Math.cos(ang), col, 3); U.text(c, lab, cx, cy + 58, col, 12, "center");
      }
      clock(420, 70, t * 2 * Math.PI / 4, U.GRAY, "地面的鐘"); clock(550, 70, t * 2 * Math.PI / 4 / g, U.RED, "運動中的鐘");
      // 長度收縮
      var L0 = 260; c.strokeStyle = U.GRAY; c.lineWidth = 2; c.setLineDash([5, 4]); c.strokeRect(360, 250, L0, 30); c.setLineDash([]);
      c.fillStyle = U.AMBER; c.fillRect(360, 250, L0 / g, 30); U.text(c, "太空船在地面量到的長度（虛線是原長）", 360, 243, U.GRAY, 12);
      ui.read.textContent = "γ = " + g.toFixed(3) + "　運動的鐘走得慢：地面上過 1 s，船上只過 " + (1 / g).toFixed(3) + " s　長度縮成原長的 " + (100 / g).toFixed(1) + "%";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };

  S["modern-photo"] = function (box) {
    var ui = U.make(box, 640, 320, "光電效應：光子能量與金屬功函數，滑桿調整"), c = ui.ctx;
    U.slider(ui, "E", "光子能量 hf", 1, 5, 0.1, 3, "eV", 1); U.slider(ui, "phi", "功函數 φ", 1.5, 4.5, 0.1, 2.3, "eV", 1); U.slider(ui, "I", "光強度", 1, 10, 1, 4, "", 0);
    var ph = [], el = [], acc = 0;
    var lam = function () { return 1239.84 / ui.p.E; };
    U.loop(ui, function (dt) {
      acc += dt * ui.p.I * 2.2;
      while (acc > 1) { acc -= 1; ph.push({ x: 20, y: 60 + Math.random() * 200 }); }
      var K = ui.p.E - ui.p.phi;
      ph.forEach(function (q) { q.x += 260 * dt; if (q.x >= 380 && !q.hit) { q.hit = true; if (K > 0) el.push({ x: 380, y: q.y, vx: -(60 + 90 * Math.sqrt(K)), vy: (Math.random() - 0.5) * 30 }); } });
      ph = ph.filter(function (q) { return q.x < 385; });
      el.forEach(function (q) { q.x += q.vx * dt; q.y += q.vy * dt; }); el = el.filter(function (q) { return q.x > 140; });
    }, function () {
      U.clear(ui); var p = ui.p, K = p.E - p.phi, l = lam();
      c.fillStyle = "#b9c4d8"; c.fillRect(380, 40, 40, 240); U.text(c, "金屬", 400, 300, U.GRAY, 12, "center");
      c.fillStyle = "#eef2f9"; c.fillRect(150, 40, 8, 240); U.text(c, "集電板", 154, 300, U.GRAY, 12, "center");
      var colr = l >= 380 && l <= 780 ? "hsl(" + Math.round(Math.max(0, Math.min(270, (l - 380) / (700 - 380) * 270))) + ",90%,50%)" : "#7c3aed";
      if (l >= 380 && l <= 700) { var h = 270 - (l - 380) / 320 * 270; colr = "hsl(" + Math.round(h) + ",90%,48%)"; }
      ph.forEach(function (q) { U.dot(c, q.x, q.y, 5, colr); });
      el.forEach(function (q) { U.dot(c, q.x, q.y, 4, U.INK); });
      ui.read.textContent = "光子波長 " + l.toFixed(0) + " nm" + (l < 380 ? "（紫外線）" : l > 700 ? "（紅外線）" : "") + "。" + (K > 0 ? "電子最大動能 K = hf − φ = " + K.toFixed(2) + " eV。把光強度調大只會讓電子變多，不會變快。" : "hf < φ：不論多亮都打不出電子（要提高光子能量，不是增加亮度）。");
    });
  };

  S["modern-decay"] = function (box) {
    var ui = U.make(box, 640, 320, "100 個放射性原子核的隨機衰變與衰變曲線"), c = ui.ctx;
    U.slider(ui, "T", "半衰期 T½", 1, 5, 0.5, 2, "s");
    var N0 = 100, alive, t, hist;
    function reset() { alive = []; for (var i = 0; i < N0; i++) alive.push(true); t = 0; hist = [[0, N0]]; }
    reset(); ui.on.push(function () { reset(); });
    var lp = U.loop(ui, function (dt) {
      t += dt; var lam = Math.LN2 / ui.p.T, p = 1 - Math.exp(-lam * dt), n = 0;
      for (var i = 0; i < N0; i++) { if (alive[i] && Math.random() < p) alive[i] = false; if (alive[i]) n++; }
      hist.push([t, n]); if (t > 10 * ui.p.T || n === 0) reset();
    }, function () {
      U.clear(ui); var p = ui.p, n = hist[hist.length - 1][1];
      for (var i = 0; i < N0; i++) U.dot(c, 36 + (i % 10) * 24, 36 + Math.floor(i / 10) * 24, 8, alive[i] ? U.BLUE : "#e6ebf5");
      var A = U.axes(ui, 330, 20, 290, 250, 0, 6 * p.T, 0, N0 * 1.05, "t (s)", "剩餘核數 N");
      c.beginPath(); for (var j = 0; j <= 100; j++) { var x = 6 * p.T * j / 100, y = N0 * Math.pow(0.5, x / p.T); j ? c.lineTo(A.X(x), A.Y(y)) : c.moveTo(A.X(x), A.Y(y)); } c.strokeStyle = U.AMBER; c.lineWidth = 2.5; c.stroke();
      c.beginPath(); hist.forEach(function (q, k) { var X = A.X(Math.min(q[0], 6 * p.T)), Y = A.Y(q[1]); k ? c.lineTo(X, Y) : c.moveTo(X, Y); }); c.strokeStyle = U.RED; c.lineWidth = 2; c.stroke();
      [1, 2, 3].forEach(function (k) { U.line(c, A.X(k * p.T), A.Y(0), A.X(k * p.T), A.Y(N0 * Math.pow(0.5, k)), U.GRID, 1, [3, 3]); U.text(c, N0 * Math.pow(0.5, k) + "", A.X(k * p.T) + 4, A.Y(N0 * Math.pow(0.5, k)) - 4, U.GRAY, 11); });
      ui.read.textContent = "t = " + t.toFixed(1) + " s　剩下 " + n + " 個（橘線是理論值 N0(½)^(t/T½)；紅線是這次隨機結果，會上下抖動）。每過一個半衰期剩下一半。";
    });
    U.button(ui, "重新開始", reset); U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };
  S["modern-box"] = function (box) {
    var ui = U.make(box, 640, 320, "無限深井中電子的波函數、機率密度與能階"), c = ui.ctx;
    U.slider(ui, "n", "量子數 n", 1, 5, 1, 1, "", 0);
    U.slider(ui, "L", "井寬 L", 0.3, 1.5, 0.05, 0.5, "nm", 2);
    var E1c = 0.376; // eV·nm²，電子的 h²/(8m)
    function draw() {
      U.clear(ui); var p = ui.p, n = Math.round(p.n), L = p.L, i, E = E1c * n * n / (L * L);
      var A = U.axes(ui, 50, 20, 340, 250, 0, L, -1.6, 1.6, "x (nm)", "");
      c.fillStyle = "#e9f0fd"; c.beginPath(); c.moveTo(A.X(0), A.Y(0)); // |ψ|² 填色（相對尺度）
      for (i = 0; i <= 200; i++) { var x = L * i / 200, y = (2 / L) * Math.pow(Math.sin(n * Math.PI * x / L), 2) * L / 2; c.lineTo(A.X(x), A.Y(y)); }
      c.lineTo(A.X(L), A.Y(0)); c.closePath(); c.fill();
      c.beginPath(); for (i = 0; i <= 200; i++) { var x2 = L * i / 200, y2 = Math.sqrt(2 / L) * Math.sin(n * Math.PI * x2 / L) * Math.sqrt(L / 2); i ? c.lineTo(A.X(x2), A.Y(y2)) : c.moveTo(A.X(x2), A.Y(y2)); }
      c.strokeStyle = U.BLUE; c.lineWidth = 2.5; c.stroke();
      U.line(c, A.X(0), A.Y(0), A.X(L), A.Y(0), U.GRID, 1, [4, 4]);
      U.line(c, A.X(0), 20, A.X(0), 270, U.INK, 3); U.line(c, A.X(L), 20, A.X(L), 270, U.INK, 3);
      U.text(c, "藍線：波函數 ψ　淺藍色塊：機率密度 |ψ|²", 52, 14, U.GRAY, 11);
      // 右側能階圖
      var top = 30, bot = 270;
      U.text(c, "能階 (eV)", 500, 22, U.GRAY, 12, "center");
      for (var k = 1; k <= 5; k++) {
        var Ek = E1c * k * k / (L * L), yy = bot - (bot - top) * Math.min(Ek / (E1c * 25 / (L * L)), 1);
        U.line(c, 450, yy, 550, yy, k === n ? U.RED : U.GRID, k === n ? 3 : 1.5);
        U.text(c, "n=" + k + "　" + Ek.toFixed(2), 556, yy + 4, k === n ? U.RED : U.GRAY, 11);
      }
      ui.read.textContent = "n = " + n + "，E = n²E1 = " + E.toFixed(2) + " eV（E1 = 0.376/L² = " + (E1c / (L * L)).toFixed(2) + " eV）。" +
        (n > 1 ? "有 " + (n - 1) + " 個節點（機率為 0 的位置）。" : "基態沒有節點，機率集中在中央。") + "把井變窄，能階全部往上推開。";
    }
    ui.on.push(draw); draw();
  };
})();
