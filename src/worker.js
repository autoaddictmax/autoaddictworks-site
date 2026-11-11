// Auto Addict Works site worker: serves the static site and relays form leads to GHL.
// The GHL inbound-webhook URL lives in the Cloudflare secret GHL_WEBHOOK_URL (never in this public repo).
const FIELDS = ["name", "phone", "email", "vehicle", "vin", "reason", "message", "build", "type", "source", "page", "submittedAt"];

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
}

async function handleLead(request, env) {
  // GET = health check: shows whether the secrets are set, never their values.
  if (request.method === "GET") return json({ ok: true, ghl: !!env.GHL_WEBHOOK_URL, captcha: !!env.TURNSTILE_SECRET });
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  let d;
  try { d = await request.json(); } catch { return json({ ok: false, error: "bad json" }, 400); }
  // Honeypot: real visitors never fill the hidden "company" field. Pretend success for bots.
  if (d.company) return json({ ok: true });
  // Cloudflare Turnstile check (enforced once the TURNSTILE_SECRET secret is set).
  if (env.TURNSTILE_SECRET) {
    const token = d["cf-turnstile-response"];
    if (!token) return json({ ok: false, error: "captcha" }, 403);
    const form = new FormData();
    form.append("secret", env.TURNSTILE_SECRET);
    form.append("response", token);
    const ip = request.headers.get("CF-Connecting-IP");
    if (ip) form.append("remoteip", ip);
    const v = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
    const vr = await v.json().catch(() => ({}));
    if (!vr.success) return json({ ok: false, error: "captcha" }, 403);
  }
  const lead = {};
  // Always send every field (blank when empty) so GHL's field mapping sees the full set.
  for (const k of FIELDS) lead[k] = d[k] != null ? String(d[k]).trim().slice(0, 4000) : "";
  if (!lead.name || !lead.phone) return json({ ok: false, error: "name and phone required" }, 400);
  if (!lead.message && !lead.build) return json({ ok: false, error: "message required" }, 400);
  if (!lead.vehicle) return json({ ok: false, error: "vehicle required" }, 400);
  if (lead.type === "Service request" && !lead.email) return json({ ok: false, error: "email required" }, 400);
  // Fill "Service" so the notification never shows a blank line.
  if (!lead.reason) lead.reason = lead.build ? "Performance build" : lead.type === "Call back request" ? "Call back" : "General question";
  const digits = lead.phone.replace(/\D/g, "");
  if (digits.length < 10 || digits.length > 11) return json({ ok: false, error: "phone" }, 400);
  const parts = lead.name.split(/\s+/);
  lead.first_name = parts[0];
  lead.last_name = parts.slice(1).join(" ");
  lead.phone = "+" + (digits.length === 10 ? "1" + digits : digits);
  lead.source = "Auto Addict Works Website";
  if (!env.GHL_WEBHOOK_URL) return json({ ok: false, error: "not configured" }, 503);
  const r = await fetch(env.GHL_WEBHOOK_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(lead) });
  return r.ok ? json({ ok: true }) : json({ ok: false, error: "upstream " + r.status }, 502);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/lead") return handleLead(request, env);
    return env.ASSETS.fetch(request);
  },
};
