/**
 * Contact form endpoint.
 *
 * Sends through Mailjet's send API v3.1 with plain fetch — no dependencies, so
 * nothing to install and nothing to keep updated.
 *
 * Set these in Vercel → Project → Settings → Environment Variables:
 *   MJ_APIKEY_PUBLIC    Mailjet API key
 *   MJ_APIKEY_PRIVATE   Mailjet secret key
 *   MJ_FROM             verified sender address on Mailjet
 *   MJ_TO               where the enquiry should land (defaults to MJ_FROM)
 *
 * Never commit those values: this file only reads them at run time.
 */

const LIMITS = { name: 120, email: 160, organisation: 160, topic: 120, message: 6000 };

function clean(value, max) {
  return String(value ?? "").trim().slice(0, max);
}

function looksLikeEmail(value) {
  return /^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(value);
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : (req.body || {});

  // Honeypot: a real person never fills a field they cannot see.
  if (clean(body.website, 200)) return res.status(200).json({ ok: true });

  const name = clean(body.name, LIMITS.name);
  const email = clean(body.email, LIMITS.email);
  const organisation = clean(body.organisation, LIMITS.organisation);
  const topic = clean(body.topic, LIMITS.topic);
  const message = clean(body.message, LIMITS.message);

  if (!name || !email || !message || !looksLikeEmail(email)) {
    return res.status(400).json({ ok: false, error: "invalid_input" });
  }

  const key = process.env.MJ_APIKEY_PUBLIC;
  const secret = process.env.MJ_APIKEY_PRIVATE;
  const from = process.env.MJ_FROM;
  const to = process.env.MJ_TO || from;

  // Without credentials the form must not pretend it worked: the client falls
  // back to opening a mail client when it sees this.
  if (!key || !secret || !from) {
    return res.status(503).json({ ok: false, error: "not_configured" });
  }

  const lines = [
    message,
    "",
    "—",
    `Nome: ${name}`,
    organisation ? `Organizzazione: ${organisation}` : null,
    `Email: ${email}`,
    topic ? `Argomento: ${topic}` : null,
    `Pagina: ${clean(body.page, 300) || "—"}`,
  ].filter(Boolean);

  const payload = {
    Messages: [{
      From: { Email: from, Name: "isidesystems.com" },
      To: [{ Email: to }],
      ReplyTo: { Email: email, Name: name },
      Subject: `isidesystems.com — ${topic || "richiesta"} — ${name}`,
      TextPart: lines.join("\n"),
    }],
  };

  try {
    const auth = Buffer.from(`${key}:${secret}`).toString("base64");
    const r = await fetch("https://api.mailjet.com/v3.1/send", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Basic ${auth}` },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      const detail = await r.text();
      console.error("mailjet", r.status, detail.slice(0, 500));
      return res.status(502).json({ ok: false, error: "send_failed" });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error("mailjet", err);
    return res.status(502).json({ ok: false, error: "send_failed" });
  }
}
