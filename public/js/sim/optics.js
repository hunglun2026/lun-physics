/* 光學模擬：薄透鏡成像、雙狹縫干涉與單縫繞射。 */
(function () {
  "use strict";
  var U = PHYS.ui, S = PHYS.sims;

  S["optics-lens"] = function (box) {
    var ui = U.make(box, 640, 300, "凸透鏡成像光線圖，滑桿調整焦距與物距"), c = ui.ctx;
    U.slider(ui, "f", "焦距 f", 5, 20, 1, 10, "cm", 0); U.slider(ui, "do", "物距 do", 4, 45, 1, 30, "cm", 0);
    U.loop(ui, function () {}, function () {
      U.clear(ui); var p = ui.p, k = 6.4, cx = 320, cy = 160, ho = 45, f = p.f, d = p.do;
      U.line(c, 10, cy, 630, cy, U.GRAY, 1.5); U.line(c, cx, 30, cx, 290, U.BLUE, 3); U.text(c, "透鏡", cx + 6, 38, U.BLUE, 12);
      [-f, f].forEach(function (ff) { U.dot(c, cx + ff * k, cy, 3.5, U.GRAY); U.text(c, "F", cx + ff * k, cy + 18, U.GRAY, 12, "center"); });
      var xo = cx - d * k, yo = cy - ho; U.arrow(c, xo, cy, xo, yo, U.AMBER, 3);
      var near = Math.abs(d - f) < 0.3; // 物在焦點上：成像於無窮遠
      if (near) { ui.read.textContent = "物體正好在焦點上：折射後是平行光，像在無窮遠處（f = do）。"; U.line(c, xo, yo, cx, yo, U.RED, 1.5); U.line(c, cx, yo, 630, yo + (cy - yo) * 0, U.RED, 1.5); return; }
      var di = f * d / (d - f), m = -di / d, xi = cx + di * k, yi = cy - m * ho; // 像尖端：倒立時 m<0，尖端在軸線下方
      var inRange = Math.abs(xi - cx) < 400;
      // 光線 1：平行光軸入射，通過透鏡後經過（或反向延長經過）像尖端
      U.line(c, xo, yo, cx, yo, U.RED, 1.6);
      // 光線 2：通過透鏡中心不偏折
      U.line(c, xo, yo, cx, cy, U.GREEN, 1.6);
      if (inRange) {
        // 兩條光線過透鏡後都在「透鏡上的點 → 像尖端」那條直線上：實像時匯聚到像尖端，虛像時往外發散、反向延長才交會
        [[yo, U.RED], [cy, U.GREEN]].forEach(function (r) {
          var slope = (yi - r[0]) / (xi - cx);
          U.line(c, cx, r[0], 630, r[0] + slope * (630 - cx), r[1], 1.6);
          if (di < 0) U.line(c, cx, r[0], xi, yi, r[1], 1.4, [5, 4]);
        });
        U.arrow(c, xi, cy, xi, yi, U.BLUE, 3);
      }
      var kind = di > 0 ? "實像" : "虛像", ori = m < 0 ? "倒立" : "正立", size = Math.abs(m) > 1.01 ? "放大" : Math.abs(m) < 0.99 ? "縮小" : "等大";
      ui.read.textContent = "像距 di = " + di.toFixed(1) + " cm　放大率 m = " + m.toFixed(2) + "　→ " + ori + size + "的" + kind + (di < 0 ? "（物距小於焦距：放大鏡）" : "") + (inRange ? "" : "（像在畫面外）");
    });
  };

  function rgb(l) { // 波長 nm → 近似顏色
    var r = 0, g = 0, b = 0;
    if (l < 440) { r = -(l - 440) / 60; b = 1; } else if (l < 490) { g = (l - 440) / 50; b = 1; } else if (l < 510) { g = 1; b = -(l - 510) / 20; }
    else if (l < 580) { r = (l - 510) / 70; g = 1; } else if (l < 645) { r = 1; g = -(l - 645) / 65; } else { r = 1; }
    return [Math.round(255 * r), Math.round(255 * g), Math.round(255 * b)];
  }

  S["optics-slit"] = function (box) {
    var ui = U.make(box, 640, 300, "雙狹縫干涉條紋的強度分布，滑桿調整波長、縫距與縫寬"), c = ui.ctx;
    U.slider(ui, "lam", "波長 λ", 400, 700, 10, 550, "nm", 0); U.slider(ui, "d", "縫距 d", 0.1, 0.6, 0.05, 0.3, "mm", 2); U.slider(ui, "a", "縫寬 a", 0.02, 0.12, 0.01, 0.04, "mm", 2);
    U.loop(ui, function () {}, function () {
      U.clear(ui); var p = ui.p, L = 1.5, Y = 12e-3, lam = p.lam * 1e-9, d = p.d * 1e-3, a = p.a * 1e-3, col = rgb(p.lam);
      function I(y) { var b = Math.PI * d * y / (lam * L), s = Math.PI * a * y / (lam * L), sinc = Math.abs(s) < 1e-9 ? 1 : Math.sin(s) / s; return Math.pow(Math.cos(b), 2) * sinc * sinc; }
      // 條紋影像（上）
      for (var x = 0; x < 600; x++) { var y = (x / 600 - 0.5) * 2 * Y, v = I(y); c.fillStyle = "rgb(" + Math.round(col[0] * v) + "," + Math.round(col[1] * v) + "," + Math.round(col[2] * v) + ")"; c.fillRect(20 + x, 20, 1, 70); }
      c.strokeStyle = U.GRAY; c.lineWidth = 1; c.strokeRect(20, 20, 600, 70);
      // 強度曲線（下）
      var A = U.axes(ui, 20, 120, 600, 150, -Y * 1000, Y * 1000, 0, 1.05, "屏上位置 y (mm)", "強度");
      c.beginPath(); for (var i = 0; i <= 600; i++) { var yy = (i / 600 - 0.5) * 2 * Y; i ? c.lineTo(A.X(yy * 1000), A.Y(I(yy))) : c.moveTo(A.X(yy * 1000), A.Y(I(yy))); } c.strokeStyle = U.BLUE; c.lineWidth = 2; c.stroke();
      c.beginPath(); for (i = 0; i <= 600; i++) { yy = (i / 600 - 0.5) * 2 * Y; var s = Math.PI * a * yy / (lam * L), e = Math.abs(s) < 1e-9 ? 1 : Math.pow(Math.sin(s) / s, 2); i ? c.lineTo(A.X(yy * 1000), A.Y(e)) : c.moveTo(A.X(yy * 1000), A.Y(e)); } c.strokeStyle = U.AMBER; c.lineWidth = 1.6; c.setLineDash([5, 4]); c.stroke(); c.setLineDash([]);
      ui.read.textContent = "條紋間距 Δy = λL/d = " + (lam * L / d * 1000).toFixed(2) + " mm（屏距 L = 1.5 m）。橘色虛線是單縫繞射的包絡：縫越窄，包絡越寬。";
    });
  };
})();
