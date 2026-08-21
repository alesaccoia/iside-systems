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

const SENDER = "Alessandro — Iside Systems";

const LIMITS = { name: 120, email: 160, organisation: 160, topic: 120, message: 6000 };

function clean(value, max) {
  return String(value ?? "").trim().slice(0, max);
}

function looksLikeEmail(value) {
  return /^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(value);
}


/* ------------------------------------------------------------------
   AI Maturity Check: the same report, as an HTML mail.

   The page sends structured fields, never markup: everything below is
   escaped and rendered here, so the endpoint cannot be used to post
   arbitrary HTML through Mailjet.
   ------------------------------------------------------------------ */
const BG = "#0e0e11", INK = "#eceae4", DIM = "#a6a3a9", ACC = "#ff4a2b",
      LINE = "#2a2a30";

function esc(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function items(list, max) {
  return (Array.isArray(list) ? list : []).slice(0, max).map((row, i) => `
      <tr><td style="padding:14px 0;border-bottom:1px solid ${LINE}">
        <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.14em;color:${ACC}">
          ${String(i + 1).padStart(2, "0")}</div>
        <div style="font:500 17px Helvetica,Arial,sans-serif;color:${INK};margin:6px 0 4px">
          ${esc(clean(row && row.title, 160))}</div>
        <div style="font:14px/1.6 Helvetica,Arial,sans-serif;color:${DIM}">
          ${esc(clean(row && row.body, 400))}</div>
      </td></tr>`).join("");
}

function axesRows(axes) {
  return (Array.isArray(axes) ? axes : []).slice(0, 8).map(a => {
    const value = Math.max(0, Math.min(100, Number(a && a.value) || 0));
    return `
      <tr>
        <td style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.12em;color:${DIM};
                   padding:7px 14px 7px 0;white-space:nowrap">${esc(clean(a && a.name, 40))}</td>
        <td style="width:100%;padding:7px 0">
          <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%">
            <tr><td style="background:#1c1c22;height:8px">
              <table role="presentation" cellpadding="0" cellspacing="0" style="width:${value}%">
                <tr><td style="background:${ACC};height:8px"></td></tr>
              </table>
            </td></tr>
          </table>
        </td>
        <td style="font:600 12px 'SFMono-Regular',Menlo,monospace;color:${INK};padding:7px 0 7px 14px">
          ${value}</td>
      </tr>`;
  }).join("");
}


function answerRows(answers) {
  return (Array.isArray(answers) ? answers : []).slice(0, 30).map(row => `
      <tr><td style="padding:11px 0;border-bottom:1px solid ${LINE}">
        <div style="font:13px/1.5 Helvetica,Arial,sans-serif;color:${DIM}">
          ${esc(clean(row && row.q, 200))}</div>
        <div style="font:500 15px/1.5 Helvetica,Arial,sans-serif;color:${INK};margin-top:3px">
          ${esc(clean(row && row.a, 400))}</div>
      </td></tr>`).join("");
}

function reportHtml(report, { name, forOwner, contact }) {
  const score = Math.max(0, Math.min(100, Number(report.score) || 0));
  const hello = forOwner
    ? `Nuova richiesta dall’AI Maturity Check.`
    : `Ciao ${esc(name.split(" ")[0] || name)}, ecco la tua mappa.`;
  const closing = forOwner
    ? `Rispondi a questa mail per scrivere direttamente a ${esc(name)}.`
    : `Ti scrivo io a breve, di persona, per dirti da dove partirei nel tuo caso.
       Se nel frattempo vuoi anticiparmi qualcosa, rispondi pure a questa mail.`;
  // without the charset an email client reads the accents as latin-1 mojibake
  return `<!doctype html><html lang="it"><head><meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>La tua mappa di maturità AI</title></head>
  <body style="margin:0;background:${BG}">
  <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;background:${BG}">
    <tr><td align="center" style="padding:32px 18px 56px">
      <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;max-width:640px">
        <tr><td style="padding-bottom:26px;border-bottom:1px solid ${LINE}">
          <span style="display:inline-block;width:22px;height:22px;border:2px solid ${INK};
                       vertical-align:middle"></span>
          <span style="font:700 12px 'SFMono-Regular',Menlo,monospace;letter-spacing:.14em;
                       color:${INK};padding-left:10px;vertical-align:middle">ISIDE SYSTEMS</span>
          <span style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.14em;
                       color:${DIM};float:right;padding-top:5px">AI MATURITY CHECK</span>
        </td></tr>

        <tr><td style="padding:34px 0 0">
          <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;color:${ACC}">
            ${esc(hello)}</div>
          <h1 style="font:600 30px/1.1 Helvetica,Arial,sans-serif;color:${INK};letter-spacing:-.02em;
                     margin:14px 0 0">${esc(clean(report.title, 200))}</h1>
          <p style="font:16px/1.65 Helvetica,Arial,sans-serif;color:${DIM};margin:16px 0 0">
            ${esc(clean(report.summary, 1200))}</p>
        </td></tr>

        <tr><td style="padding:30px 0 6px">
          <table role="presentation" cellpadding="0" cellspacing="0"
                 style="width:100%;border:1px solid ${LINE}">
            <tr><td style="padding:22px 22px 8px">
              <span style="font:600 44px Helvetica,Arial,sans-serif;color:${INK};
                           letter-spacing:-.04em">${score}</span>
              <span style="font:600 11px 'SFMono-Regular',Menlo,monospace;color:${DIM};
                           letter-spacing:.14em;padding-left:8px">/100 PRONTEZZA</span>
            </td></tr>
            <tr><td style="padding:6px 22px 22px">
              <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%">
                ${axesRows(report.axes)}
              </table>
            </td></tr>
          </table>
        </td></tr>

        <tr><td style="padding:34px 0 0">
          <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;color:${DIM};
                      padding-bottom:6px">QUICK WIN / PROSSIMI 90 GIORNI</div>
          <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%">
            ${items(report.wins, 8)}
          </table>
        </td></tr>

        <tr><td style="padding:30px 0 0">
          <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;color:${DIM};
                      padding-bottom:6px">FORMAZIONE</div>
          <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%">
            ${items(report.training, 4)}
          </table>
        </td></tr>

        <tr><td style="padding:30px 0 0">
          <div style="border-left:2px solid ${ACC};padding:4px 0 4px 16px">
            <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;
                        color:${DIM}">IL PRIMO PASSO</div>
            <p style="font:17px/1.6 Helvetica,Arial,sans-serif;color:${INK};margin:10px 0 0">
              ${esc(clean(report.advice, 600))}</p>
          </div>
        </td></tr>

        ${forOwner ? `
        <tr><td style="padding:34px 0 0">
          <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;color:${DIM};
                      padding-bottom:6px">TUTTE LE RISPOSTE</div>
          <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%">
            ${answerRows(report.answers)}
          </table>
        </td></tr>
        <tr><td style="padding:26px 0 0">
          <div style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.16em;color:${DIM};
                      padding-bottom:8px">CONTATTO</div>
          <div style="font:15px/1.7 Helvetica,Arial,sans-serif;color:${INK}">
            ${esc(name)}<br>
            <a href="mailto:${esc(contact && contact.email)}" style="color:${ACC};text-decoration:none">
              ${esc(contact && contact.email)}</a><br>
            <span style="color:${DIM}">${esc(clean(contact && contact.page, 200))}</span>
          </div>
        </td></tr>` : ""}

        <tr><td style="padding:34px 0 0;border-top:1px solid ${LINE}">
          <p style="font:15px/1.7 Helvetica,Arial,sans-serif;color:${DIM};margin:22px 0 0">
            ${closing}</p>
          <p style="font:600 11px 'SFMono-Regular',Menlo,monospace;letter-spacing:.14em;color:${DIM};
                    margin:26px 0 0">
            ALESSANDRO SACCOIA · ISIDE SYSTEMS SRLS · MILANO<br>
            <a href="https://www.isidesystems.com" style="color:${ACC};text-decoration:none">
              isidesystems.com</a>
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table></body></html>`;
}

function reportText(report, withAnswers) {
  const rows = [clean(report.title, 200), "", clean(report.summary, 1200), "",
    `Prontezza: ${Math.round(Number(report.score) || 0)}/100`];
  (report.axes || []).forEach(a => rows.push(`  ${clean(a.name, 40)}: ${Math.round(Number(a.value) || 0)}`));
  rows.push("", "QUICK WIN / PROSSIMI 90 GIORNI");
  (report.wins || []).forEach((w, i) => rows.push(`  ${i + 1}. ${clean(w.title, 160)} — ${clean(w.body, 400)}`));
  rows.push("", "FORMAZIONE");
  (report.training || []).forEach(w => rows.push(`  - ${clean(w.title, 160)} — ${clean(w.body, 400)}`));
  rows.push("", `IL PRIMO PASSO: ${clean(report.advice, 600)}`);
  if (withAnswers && Array.isArray(report.answers)) {
    rows.push("", "TUTTE LE RISPOSTE");
    report.answers.forEach(a => rows.push(`  ${clean(a.q, 200)} -> ${clean(a.a, 400)}`));
  }
  return rows.join("\n");
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

  // The maturity check sends its report as structured fields; everything else
  // is the plain enquiry form.
  const report = body.report && typeof body.report === "object" ? body.report : null;

  const messages = [{
    From: { Email: from, Name: SENDER },
    To: [{ Email: to }],
    ReplyTo: { Email: email, Name: name },
    Subject: report ? `AI Maturity Check — ${name}`
                    : `isidesystems.com — ${topic || "richiesta"} — ${name}`,
    TextPart: report ? `${lines.join("\n")}\n\n${reportText(report, true)}` : lines.join("\n"),
    ...(report ? { HTMLPart: reportHtml(report, { name, forOwner: true,
                                                  contact: { email, page: clean(body.page, 300) } }) } : {}),
  }];

  // and the person who filled it in gets their own copy
  if (report) {
    messages.push({
      From: { Email: from, Name: SENDER },
      To: [{ Email: email, Name: name }],
      ReplyTo: { Email: to },
      Subject: "AI Maturity Check — Iside Systems",
      TextPart: `${reportText(report)}\n\nTi scrivo io a breve, di persona.`,
      HTMLPart: reportHtml(report, { name, forOwner: false }),
    });
  }

  const payload = { Messages: messages };

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
