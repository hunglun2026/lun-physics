/* 熱學模擬：氣體分子、PV 圖的過程比較、卡諾循環。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims, R = 8.314;

  S["thermo-gas"] = function (box) {
    var ui = U.make(box, 640, 300, "盒子裡的氣體分子，滑桿調整溫度與分子數"), c = ui.ctx;
    U.slider(ui, "T", "溫度 T", 100, 600, 10, 300, "K", 0); U.slider(ui, "N", "分子數 N", 10, 120, 5, 60, "", 0);
    var ps = [], hits = 0, tick = 0, rate = 0;
    function reset() {
      ps = []; for (var i = 0; i < ui.p.N; i++) { var a = Math.random() * 6.283, s = 1 + Math.random() * 0.6; ps.push({ x: 20 + Math.random() * 360, y: 20 + Math.random() * 260, dx: Math.cos(a), dy: Math.sin(a), k: 0.6 + Math.random() * 0.8 }); }
    }
    reset(); ui.on.push(function (k) { if (k === "N") reset(); });
    U.loop(ui, function (dt) {
      var sp = Math.sqrt(ui.p.T / 300) * 110; tick += dt;
      ps.forEach(function (q) {
        // 方向 (dx,dy) 單位向量、速率 = 溫度決定的基準速率 × 各分子自己的係數 k（分子速率有快有慢）
        q.vx = q.dx * sp * q.k; q.vy = q.dy * sp * q.k;
        q.x += q.vx * dt; q.y += q.vy * dt;
        if (q.x < 10) { q.x = 10; q.dx = Math.abs(q.dx); hits++; } if (q.x > 390) { q.x = 390; q.dx = -Math.abs(q.dx); hits++; }
        if (q.y < 10) { q.y = 10; q.dy = Math.abs(q.dy); } if (q.y > 290) { q.y = 290; q.dy = -Math.abs(q.dy); }
      });
      if (tick > 1) { rate = hits / tick; hits = 0; tick = 0; }
    }, function () {
      U.clear(ui); c.strokeStyle = U.GRAY; c.lineWidth = 3; c.strokeRect(10, 10, 380, 280);
      ps.forEach(function (q) { var f = Math.min(1, Math.hypot(q.vx, q.vy) / 260); U.dot(c, q.x, q.y, 4, "rgb(" + Math.round(40 + 190 * f) + "," + Math.round(93 - 40 * f) + "," + Math.round(176 - 140 * f) + ")"); });
      var K = 1.5 * 1.381e-23 * ui.p.T, vr = Math.sqrt(3 * R * ui.p.T / 0.028);
      U.text(c, "平均平移動能", 420, 50, U.GRAY, 13); U.text(c, (K * 1e21).toFixed(2) + " ×10^-21 J", 420, 78, U.INK, 20);
      U.text(c, "氮氣的 v_rms", 420, 130, U.GRAY, 13); U.text(c, vr.toFixed(0) + " m/s", 420, 158, U.INK, 20);
      U.text(c, "撞右牆次數／秒", 420, 210, U.GRAY, 13); U.text(c, rate.toFixed(0), 420, 238, U.INK, 20);
      ui.read.textContent = "溫度越高，分子越快（顏色越紅）；分子越多或越快，撞牆越頻繁，壓力越大。平均動能 = (3/2)kT。";
    });
  };

  S["thermo-pv"] = function (box) {
    var ui = U.make(box, 640, 320, "理想氣體從同一點出發的等溫、等壓、絕熱過程"), c = ui.ctx, mode = "iso", g = 5 / 3;
    U.slider(ui, "V2", "終點體積 V2（相對起點）", 0.5, 2.5, 0.05, 1.8, "×", 2);
    ["等溫", "等壓", "絕熱"].forEach(function (nm, i) { var k = ["iso", "bar", "adi"][i]; U.button(ui, nm, function () { mode = k; ui.on.forEach(function (f) { f(); }); }); });
    var n = 1, T1 = 300, V1 = 0.0249, P1 = n * R * T1 / V1;
    function P(m, V) { return m === "iso" ? P1 * V1 / V : m === "bar" ? P1 : P1 * Math.pow(V1 / V, g); }
    U.loop(ui, function () {}, function () {
      U.clear(ui); var r = ui.p.V2, V2 = V1 * r;
      var A = U.axes(ui, 60, 15, 540, 250, 0, V1 * 2.7 * 1000, 0, P1 * 2.2 / 1000, "V (L)", "P (kPa)");
      function curve(m, col, w, dash) {
        c.beginPath(); for (var i = 0; i <= 80; i++) { var V = V1 * (0.45 + 2.2 * i / 80); var X = A.X(V * 1000), Y = A.Y(P(m, V) / 1000); i ? c.lineTo(X, Y) : c.moveTo(X, Y); }
        c.strokeStyle = col; c.lineWidth = w; c.setLineDash(dash || []); c.stroke(); c.setLineDash([]);
      }
      ["iso", "bar", "adi"].forEach(function (m) { if (m !== mode) curve(m, U.GRID, 2, [5, 4]); });
      // 功的面積
      c.beginPath(); c.moveTo(A.X(V1 * 1000), A.Y(0)); for (var i = 0; i <= 60; i++) { var V = V1 + (V2 - V1) * i / 60; c.lineTo(A.X(V * 1000), A.Y(P(mode, V) / 1000)); } c.lineTo(A.X(V2 * 1000), A.Y(0)); c.closePath(); c.fillStyle = "rgba(42,93,176,.2)"; c.fill();
      curve(mode, U.BLUE, 3);
      U.dot(c, A.X(V1 * 1000), A.Y(P1 / 1000), 6, U.RED); U.dot(c, A.X(V2 * 1000), A.Y(P(mode, V2) / 1000), 6, U.AMBER);
      var W, dU, Q, T2 = P(mode, V2) * V2 / (n * R);
      if (mode === "iso") { W = n * R * T1 * Math.log(r); dU = 0; Q = W; } else if (mode === "bar") { W = P1 * (V2 - V1); dU = 1.5 * n * R * (T2 - T1); Q = dU + W; } else { W = (P1 * V1 - P(mode, V2) * V2) / (g - 1); dU = -W; Q = 0; }
      var nm = { iso: "等溫", bar: "等壓", adi: "絕熱" }[mode];
      ui.read.textContent = nm + "（1 mol 單原子氣體，起點 300 K）：對外作功 W = " + W.toFixed(0) + " J　內能變化 ΔU = " + dU.toFixed(0) + " J　吸熱 Q = " + Q.toFixed(0) + " J　終點溫度 " + T2.toFixed(0) + " K（藍色面積是功）";
    });
  };

  S["thermo-carnot"] = function (box) {
    var ui = U.make(box, 640, 320, "卡諾循環的 PV 圖，滑桿調整高溫與低溫熱源"), c = ui.ctx, g = 5 / 3;
    U.slider(ui, "TH", "高溫熱源 T_H", 400, 900, 10, 600, "K", 0); U.slider(ui, "TC", "低溫熱源 T_C", 200, 390, 10, 300, "K", 0);
    U.loop(ui, function () {}, function () {
      U.clear(ui); var p = ui.p, Va = 1, Vb = 2, k = Math.pow(p.TH / p.TC, 1 / (g - 1)), Vc = Vb * k, Vd = Va * k;
      var A = U.axes(ui, 60, 15, 540, 250, 0, Vc * 1.08, 0, p.TH / Va * 1.1, "V", "P");
      function seg(f, v1, v2, col) { c.beginPath(); for (var i = 0; i <= 60; i++) { var V = v1 + (v2 - v1) * i / 60; i ? c.lineTo(A.X(V), A.Y(f(V))) : c.moveTo(A.X(V), A.Y(f(V))); } c.strokeStyle = col; c.lineWidth = 3; c.stroke(); }
      var Pb = p.TH / Vb, Pc = p.TC / Vc, Pd = p.TC / Vd, Pa = p.TH / Va;
      c.beginPath(); c.moveTo(A.X(Va), A.Y(Pa));
      for (var i = 1; i <= 40; i++) { var V = Va + (Vb - Va) * i / 40; c.lineTo(A.X(V), A.Y(p.TH / V)); }
      for (i = 1; i <= 40; i++) { V = Vb + (Vc - Vb) * i / 40; c.lineTo(A.X(V), A.Y(Pb * Math.pow(Vb / V, g))); }
      for (i = 1; i <= 40; i++) { V = Vc + (Vd - Vc) * i / 40; c.lineTo(A.X(V), A.Y(p.TC / V)); }
      for (i = 1; i <= 40; i++) { V = Vd + (Va - Vd) * i / 40; c.lineTo(A.X(V), A.Y(Pd * Math.pow(Vd / V, g))); }
      c.closePath(); c.fillStyle = "rgba(199,125,0,.2)"; c.fill();
      seg(function (V) { return p.TH / V; }, Va, Vb, U.RED); seg(function (V) { return Pb * Math.pow(Vb / V, g); }, Vb, Vc, U.GRAY);
      seg(function (V) { return p.TC / V; }, Vc, Vd, U.BLUE); seg(function (V) { return Pd * Math.pow(Vd / V, g); }, Vd, Va, U.GRAY);
      ["a", "b", "c", "d"].forEach(function (l, j) { var pt = [[Va, Pa], [Vb, Pb], [Vc, Pc], [Vd, Pd]][j]; U.dot(c, A.X(pt[0]), A.Y(pt[1]), 5, U.INK); U.text(c, l, A.X(pt[0]) + 8, A.Y(pt[1]) - 6, U.INK, 14); });
      U.text(c, "等溫吸熱 T_H", A.X(1.25), A.Y(Pa) - 4, U.RED, 12); U.text(c, "等溫放熱 T_C", A.X(Vc * 0.78), A.Y(Pc) + 18, U.BLUE, 12);
      var e = 1 - p.TC / p.TH, QH = R * p.TH * Math.log(Vb / Va), W = e * QH;
      ui.read.textContent = "卡諾效率 e = 1 − T_C/T_H = " + (e * 100).toFixed(1) + "%　每莫耳吸熱 Q_H = " + QH.toFixed(0) + " J、作功 W = " + W.toFixed(0) + " J、排熱 " + (QH - W).toFixed(0) + " J（橘色面積是淨功）";
    });
  };
})();
