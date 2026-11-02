// 建置時把公式排成 HTML：stdin 讀 JSON [{tex, display}]，stdout 輸出 HTML 字串陣列。
// 網站本身不載入 KaTeX 的腳本，只用它的 CSS 與字型（符合 script-src 'self'）。
import katex from "katex";

const chunks = [];
for await (const c of process.stdin) chunks.push(c);
const items = JSON.parse(Buffer.concat(chunks).toString("utf8"));
const out = items.map(({ tex, display }) =>
  katex.renderToString(tex, { displayMode: !!display, throwOnError: true, output: "htmlAndMathml", strict: "error" }),
);
process.stdout.write(JSON.stringify(out));
