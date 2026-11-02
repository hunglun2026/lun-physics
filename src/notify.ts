import type { Env } from "./env";

// ntfy：對 https://ntfy.sh/<主題> 送一則訊息，手機 App 訂閱同主題就會跳通知。
// 主題名當密碼用（公開主題，知道名稱的人都收得到），所以放 secret，不進程式碼。
// 回傳是否真的送達（ntfy 回 2xx）；失敗原因寫進 console.log（wrangler tail 看得到），不含主題名。
export async function notifyError(env: Env, title: string, body: string): Promise<boolean> {
  if (!env.NTFY_TOPIC) {
    console.log("ntfy: NTFY_TOPIC 沒設定");
    return false;
  }
  try {
    const r = await fetch(`https://ntfy.sh/${env.NTFY_TOPIC}`, {
      method: "POST",
      // header 只能放 ASCII，中文標題用 RFC 2047 編碼
      headers: { Title: `=?UTF-8?B?${btoa(String.fromCharCode(...new TextEncoder().encode(title)))}?=`, Priority: "high", Tags: "warning" },
      body: body.slice(0, 1000),
    });
    if (!r.ok) console.log("ntfy: HTTP", r.status, (await r.text()).slice(0, 200));
    return r.ok;
  } catch (e) {
    console.log("ntfy: 例外", String(e));
    return false;
  }
}
