/* 力學模擬：直線運動、拋體、斜面、碰撞、軌道。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims;

  S["mech-motion1d"] = function (box) {
    var ui = U.make(box, 640, 320, "位置與速度對時間的圖，滑桿調整初速與加速度"), c = ui.ctx;
    U.slider(ui, "v0", "初速 v0", -10, 10, 0.5, 2, "m/s"); U.slider(ui, "a", "加速度 a", -5, 5, 0.5, 1, "m/s²");
    var t = 0, T = 6;
    var lp = U.loop(ui, function (dt) { t += dt; if (t > T) t = 0; }, function () {
      U.clear(ui); var p = ui.p, xs = [], vmax = Math.abs(p.v0) + Math.abs(p.a) * T + 1, xr = 0;
      for (var s = 0; s <= T; s += 0.1) xr = Math.max(xr, Math.abs(p.v0 * s + 0.5 * p.a * s * s));
      xr = Math.max(xr, 1);
      var A = U.axes(ui, 40, 20, 270, 250, 0, T, -xr, xr, "t (s)", "x (m)"), B = U.axes(ui, 350, 20, 270, 250, 0, T, -vmax, vmax, "t (s)", "v (m/s)");
      c.beginPath(); for (var s2 = 0; s2 <= T + 1e-9; s2 += 0.05) { var X = A.X(s2), Y = A.Y(p.v0 * s2 + 0.5 * p.a * s2 * s2); s2 ? c.lineTo(X, Y) : c.moveTo(X, Y); }
      c.strokeStyle = U.BLUE; c.lineWidth = 2.5; c.stroke();
      U.line(c, B.X(0), B.Y(p.v0), B.X(T), B.Y(p.v0 + p.a * T), U.AMBER, 2.5);
      var x = p.v0 * t + 0.5 * p.a * t * t, v = p.v0 + p.a * t;
      U.dot(c, A.X(t), A.Y(x), 5, U.RED); U.dot(c, B.X(t), B.Y(v), 5, U.RED);
      U.text(c, "x-t 圖的斜率是速度", 50, 300, U.GRAY); U.text(c, "v-t 圖的斜率是加速度", 360, 300, U.GRAY);
      ui.read.textContent = "t = " + t.toFixed(1) + " s　x = " + x.toFixed(2) + " m　v = " + v.toFixed(2) + " m/s";
    });
    U.button(ui, "暫停／繼續", function () { lp.toggle(); });
  };

  S["mech-projectile"] = function (box) {
    var ui = U.make(box, 640, 300, "拋體軌跡，滑桿調整初速與仰角"), c = ui.ctx, g = 9.8;
    U.slider(ui, "v0", "初速 v0", 5, 40, 1, 20, "m/s", 0); U.slider(ui, "th", "仰角 θ", 5, 85, 1, 45, "°", 0);
    var t = 0, flying = true;
    function tf() { return 2 * ui.p.v0 * Math.sin(ui.p.th * Math.PI / 180) / g; }
    var lp = U.loop(ui, function (dt) { if (flying) { t += dt; if (t > tf() + 0.8) t = 0; } }, function () {
      U.clear(ui); var p = ui.p, a = p.th * Math.PI / 180, vx = p.v0 * Math.cos(a), vy = p.v0 * Math.sin(a);
      var R = vx * tf(), H = vy * vy / (2 * g), xm = Math.max(R, 20) * 1.1, ym = Math.max(H, 8) * 1.3;
      var A = U.axes(ui, 40, 15, 580, 250, 0, xm, 0, ym, "x (m)", "y (m)");
      c.beginPath(); for (var s = 0; s <= tf() + 1e-9; s += tf() / 60) { var X = A.X(vx * s), Y = A.Y(vy * s - 0.5 * g * s * s); s ? c.lineTo(X, Y) : c.moveTo(X, Y); }
      c.strokeStyle = U.GRID; c.lineWidth = 3; c.stroke();
      var tt = Math.min(t, tf()), x = vx * tt, y = vy * tt - 0.5 * g * tt * tt;
      U.dot(c, A.X(x), A.Y(y), 6, U.RED);
      U.arrow(c, A.X(x), A.Y(y), A.X(x) + vx * 2.2, A.Y(y), U.BLUE, 2); U.arrow(c, A.X(x), A.Y(y), A.X(x), A.Y(y) - (vy - g * tt) * 2.2, U.GREEN, 2);
      ui.read.textContent = "射程 R = " + R.toFixed(1) + " m　最大高度 H = " + H.toFixed(1) + " m　滯空 " + tf().toFixed(2) + " s　（藍：水平速度，綠：鉛直速度）";
    });
    U.button(ui, "重新發射", function () { t = 0; });
  };

  S["mech-incline"] = function (box) {
    var ui = U.make(box, 640, 300, "斜面上的物體受力，滑桿調整角度與摩擦係數"), c = ui.ctx, g = 9.8;
    U.slider(ui, "th", "斜面角度 θ", 0, 60, 1, 30, "°", 0); U.slider(ui, "mu", "動摩擦係數 μ", 0, 1, 0.05, 0.2, "", 2);
    var s = 0, v = 0;
    function acc() { var p = ui.p, a = p.th * Math.PI / 180; var net = g * Math.sin(a) - p.mu * g * Math.cos(a); return net > 0 ? net : 0; }
    ui.on.push(function () { s = 0; v = 0; });
    U.loop(ui, function (dt) { v += acc() * dt; s += v * dt; if (s > 5) { s = 0; v = 0; } }, function () {
      U.clear(ui); var p = ui.p, a = p.th * Math.PI / 180, L = 460, x0 = 70, y0 = 270;
      var x1 = x0 + L * Math.cos(a), y1 = y0 - L * Math.sin(a);
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y0); c.lineTo(x1, y1); c.closePath(); c.fillStyle = "#eef2f9"; c.fill(); c.strokeStyle = U.GRAY; c.lineWidth = 2; c.stroke();
      var d = 40 + s * 60, cx = x1 - d * Math.cos(a) - 18 * Math.sin(a), cy = y1 + d * Math.sin(a) - 18 * Math.cos(a);
      c.save(); c.translate(cx, cy); c.rotate(-a); c.fillStyle = U.AMBER; c.fillRect(-18, -14, 36, 28); c.restore();
      var m = 3; // 畫箭頭長度的比例
      U.arrow(c, cx, cy, cx, cy + 9.8 * m * 3, U.RED, 2.5); U.text(c, "mg", cx + 6, cy + 9.8 * m * 3, U.RED);
      var N = 9.8 * Math.cos(a) * m * 3, nx = cx - N * Math.sin(a) * -1, ny = cy - N * Math.cos(a);
      U.arrow(c, cx, cy, cx + N * Math.sin(a), cy - N * Math.cos(a), U.BLUE, 2.5); U.text(c, "N", cx + N * Math.sin(a) + 6, cy - N * Math.cos(a), U.BLUE);
      var f = Math.min(p.mu * 9.8 * Math.cos(a), 9.8 * Math.sin(a)) * m * 3;
      if (f > 0.5) { U.arrow(c, cx, cy, cx + f * Math.cos(a), cy - f * Math.sin(a), U.GREEN, 2.5); U.text(c, "f", cx + f * Math.cos(a) + 4, cy - f * Math.sin(a) - 4, U.GREEN); }
      ui.read.textContent = acc() > 0 ? "沿斜面加速度 a = g(sinθ − μcosθ) = " + acc().toFixed(2) + " m/s²" : "μ ≥ tanθ（= " + Math.tan(a).toFixed(2) + "），物體不會下滑";
    });
  };

  S["mech-collide"] = function (box) {
    var ui = U.make(box, 640, 220, "一維碰撞，滑桿調整質量、初速與恢復係數"), c = ui.ctx;
    U.slider(ui, "m1", "質量 m1", 1, 5, 0.5, 2, "kg"); U.slider(ui, "m2", "質量 m2", 1, 5, 0.5, 1, "kg");
    U.slider(ui, "v1", "m1 初速", 0, 6, 0.5, 4, "m/s"); U.slider(ui, "e", "恢復係數 e（1＝彈性，0＝完全非彈性）", 0, 1, 0.05, 1, "", 2);
    var x1, x2, w1, w2, hit;
    function reset() { x1 = 60; x2 = 380; w1 = ui.p.v1 * 20; w2 = 0; hit = false; }
    reset(); ui.on.push(reset);
    U.loop(ui, function (dt) {
      x1 += w1 * dt; x2 += w2 * dt;
      if (!hit && x1 + 24 >= x2 - 24) {
        var p = ui.p, v1 = w1 / 20, u1 = ((p.m1 - p.e * p.m2) * v1) / (p.m1 + p.m2), u2 = ((1 + p.e) * p.m1 * v1) / (p.m1 + p.m2);
        w1 = u1 * 20; w2 = u2 * 20; hit = true;
      }
      if (x1 > 700 || x2 > 700 || x1 < -60) reset();
    }, function () {
      U.clear(ui); var p = ui.p; U.line(c, 0, 150, 640, 150, U.GRAY, 2);
      var r1 = 18 + p.m1 * 3, r2 = 18 + p.m2 * 3;
      c.fillStyle = U.BLUE; c.fillRect(x1 - r1, 150 - 2 * r1, 2 * r1, 2 * r1); c.fillStyle = U.AMBER; c.fillRect(x2 - r2, 150 - 2 * r2, 2 * r2, 2 * r2);
      U.text(c, "m1", x1, 150 - r1 + 4, "#fff", 13, "center"); U.text(c, "m2", x2, 150 - r2 + 4, "#fff", 13, "center");
      var v1 = p.v1, K0 = 0.5 * p.m1 * v1 * v1, K = 0.5 * p.m1 * Math.pow(w1 / 20, 2) + 0.5 * p.m2 * Math.pow(w2 / 20, 2), P0 = p.m1 * v1, P = p.m1 * w1 / 20 + p.m2 * w2 / 20;
      ui.read.textContent = "動量：碰前 " + P0.toFixed(2) + "，現在 " + P.toFixed(2) + " kg·m/s　動能：碰前 " + K0.toFixed(2) + "，現在 " + K.toFixed(2) + " J";
    });
    U.button(ui, "重來", reset);
  };

  S["mech-orbit"] = function (box) {
    var ui = U.make(box, 640, 340, "行星繞太陽的軌道，滑桿調整初速"), c = ui.ctx;
    U.slider(ui, "v", "近日點速度（1＝圓軌道）", 0.6, 1.35, 0.01, 1.1, "", 2);
    var x, y, vx, vy, trail;
    function reset() { x = 1; y = 0; vx = 0; vy = ui.p.v; trail = []; }
    reset(); ui.on.push(reset);
    U.loop(ui, function (dt) {
      for (var i = 0; i < 20; i++) {
        var h = dt * 1.2 / 20, r = Math.hypot(x, y); if (r < 0.12) { reset(); return; }
        var ax = -x / (r * r * r), ay = -y / (r * r * r);
        vx += ax * h / 2; vy += ay * h / 2; x += vx * h; y += vy * h;
        r = Math.hypot(x, y); ax = -x / (r * r * r); ay = -y / (r * r * r); vx += ax * h / 2; vy += ay * h / 2;
      }
      trail.push([x, y]); if (trail.length > 900) trail.shift();
    }, function () {
      U.clear(ui); var sc = 105, ox = 320, oy = 170;
      U.dot(c, ox, oy, 9, U.AMBER);
      c.beginPath(); trail.forEach(function (q, i) { var X = ox + q[0] * sc, Y = oy - q[1] * sc; i ? c.lineTo(X, Y) : c.moveTo(X, Y); }); c.strokeStyle = U.GRID; c.lineWidth = 2; c.stroke();
      U.dot(c, ox + x * sc, oy - y * sc, 6, U.BLUE);
      var r = Math.hypot(x, y), v2 = vx * vx + vy * vy, E = 0.5 * v2 - 1 / r, L = x * vy - y * vx;
      ui.read.textContent = "角動量 L = " + L.toFixed(3) + "（全程不變）　總能量 E = " + E.toFixed(3) + (E >= 0 ? "（E ≥ 0，不是封閉軌道，會飛走）" : "（E < 0，封閉橢圓軌道）");
    });
    U.button(ui, "重來", reset);
  };
})();
