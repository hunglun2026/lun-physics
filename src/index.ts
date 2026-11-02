import type { Env } from "./env";
import { handleReport } from "./report";

// 全站都是 public/ 的靜態檔；只有 POST /report（頁底「回報錯誤」）先進程式，其餘交給 ASSETS。
export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname === "/report") return handleReport(req, env);
    return env.ASSETS.fetch(req);
  },
};
