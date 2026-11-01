// elpasotrafficticketfirm.com — Cloudflare Worker
// Serves the static site from ./public (assets binding), handles legacy WordPress URLs,
// and receives lead-form posts at /api/contact (sent by email through Resend).

const CANONICAL_HOST = "elpasotrafficticketfirm.com";

// Old WordPress URLs that no longer exist → where they should go (301).
const REDIRECTS = {
  "/test": "/hire-me/",
  "/submission-confirmed": "/hire-me/",
  "/browse-submissions": "/hire-me/",
  "/hire-us": "/hire-me/",
  "/blog": "/category/blog/",
  "/category/uncategorized": "/category/blog/",
  "/feed": "/category/blog/",
  "/comments/feed": "/category/blog/",
  "/author/admin": "/contact/",
  "/sitemap_index.xml": "/sitemap.xml",
  "/wp-sitemap.xml": "/sitemap.xml",
  "/page-sitemap.xml": "/sitemap.xml",
  "/post-sitemap.xml": "/sitemap.xml",
  "/category-sitemap.xml": "/sitemap.xml",
  "/author-sitemap.xml": "/sitemap.xml",
};

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "SAMEORIGIN",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
};

function withHeaders(res, extra = {}) {
  const r = new Response(res.body, res);
  for (const [k, v] of Object.entries({ ...SECURITY_HEADERS, ...extra })) r.headers.set(k, v);
  return r;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...SECURITY_HEADERS } });
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function handleContact(request, env) {
  if (request.method !== "POST") return json({ ok: false, error: "method_not_allowed" }, 405);
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }
  if (data.website) return json({ ok: true }); // honeypot — pretend success
  const name = String(data.name || "").trim().slice(0, 120);
  const phone = String(data.phone || "").trim().slice(0, 40);
  const email = String(data.email || "").trim().slice(0, 160);
  if (!name || !phone) return json({ ok: false, error: "missing_fields" }, 400);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: "bad_email" }, 400);

  const kind = data.form === "lookup" ? "Ticket / Warrant Lookup" : "Hire Me";
  const fields = ["ticket_type", "count", "warrants", "citation", "dob", "dl", "court", "message", "page"];
  const rows = [["Name", name], ["Phone", phone], ["Email", email]]
    .concat(fields.filter((f) => data[f]).map((f) => [f.replace(/_/g, " "), String(data[f]).slice(0, 2000)]))
    .map(([k, v]) => `<tr><td style="padding:6px 10px;border:1px solid #ddd;font-weight:bold;text-transform:capitalize">${esc(k)}</td><td style="padding:6px 10px;border:1px solid #ddd;white-space:pre-wrap">${esc(v)}</td></tr>`)
    .join("");
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const html = `<h2 style="font-family:Arial">New website lead — ${esc(kind)}</h2><table style="font-family:Arial;border-collapse:collapse">${rows}</table><p style="font-family:Arial;color:#777;font-size:12px">Sent from elpasotrafficticketfirm.com · IP ${esc(ip)} · ${new Date().toISOString()}</p>`;
  const text = [["Name", name], ["Phone", phone], ["Email", email]].concat(fields.filter((f) => data[f]).map((f) => [f, data[f]])).map(([k, v]) => `${k}: ${v}`).join("\n");

  if (!env.RESEND_API_KEY) {
    console.log("Lead received but RESEND_API_KEY is not set:\n" + text);
    return json({ ok: false, error: "not_configured" }, 503);
  }
  const to = (env.LEAD_TO_EMAIL || "help@elpasotrafficticket.com").split(",").map((s) => s.trim());
  const from = env.LEAD_FROM_EMAIL || "El Paso Traffic Ticket Firm <leads@elpasotrafficticketfirm.com>";
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from, to, reply_to: email || undefined, subject: `New lead (${kind}): ${name} — ${data.ticket_type || data.court || "traffic ticket"}`, html, text }),
  });
  if (!res.ok) {
    console.log("Resend error", res.status, await res.text());
    return json({ ok: false, error: "send_failed" }, 502);
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Canonical host: www → apex (only on the production domain)
    if (url.hostname === "www." + CANONICAL_HOST) {
      url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === "/api/contact") return handleContact(request, env);
    if (url.pathname.startsWith("/api/")) return json({ ok: false, error: "not_found" }, 404);

    // Legacy WordPress noise → 410 so crawlers drop it quickly
    const p = url.pathname;
    if (/^\/(wp-admin|wp-login\.php|wp-json|wp-content|wp-includes|xmlrpc\.php|cdn-cgi\/l\/email-protection)/.test(p) || /\?replytocom=/.test(url.search)) {
      return new Response(null, { status: 410, headers: { "Cache-Control": "public, max-age=86400", ...SECURITY_HEADERS } });
    }

    // Explicit redirects (with or without trailing slash)
    const key = p.length > 1 && p.endsWith("/") ? p.slice(0, -1) : p;
    if (REDIRECTS[key]) return Response.redirect(url.origin + REDIRECTS[key], 301);

    // Static assets (html_handling adds the trailing slash for directory pages)
    const res = await env.ASSETS.fetch(request);
    const ct = res.headers.get("Content-Type") || "";
    const extra = {};
    if (ct.includes("text/html")) {
      extra["Cache-Control"] = "public, max-age=0, must-revalidate";
      // Dev preview on *.workers.dev must not be indexed
      if (url.hostname.endsWith(".workers.dev")) extra["X-Robots-Tag"] = "noindex, nofollow";
    } else if (/\.(webp|png|jpg|svg|ico|woff2?)$/.test(p) || /\?v=/.test(url.search)) {
      extra["Cache-Control"] = "public, max-age=31536000, immutable";
    }
    return withHeaders(res, extra);
  },
};
