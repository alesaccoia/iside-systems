/* Whitepaper gate: the PDF arrives by mail, so the form has to succeed before
   anything is downloaded. Same endpoint as the maturity check. */
(function () {
  var cfg = window.WPAPER || {};
  var form = document.getElementById("wform");
  if (!form) return;
  var note = document.getElementById("wnote");
  var button = form.querySelector("button[type=submit]");

  function push(event, extra) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: event }, extra || {}));
  }

  var started = false;
  form.addEventListener("focusin", function () {
    if (started) return;
    started = true;
    push("whitepaper_start", { lang: cfg.lang });
  });

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var data = new FormData(form);
    var first = (data.get("name") || "").toString().trim();
    var last = (data.get("surname") || "").toString().trim();
    var email = (data.get("email") || "").toString().trim();
    if (!first || !last || !/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email)) {
      note.className = "wnote bad";
      note.textContent = cfg.fail;
      return;
    }

    button.disabled = true;
    note.className = "wnote";
    note.textContent = cfg.sending;

    fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        whitepaper: true,
        name: first + " " + last,
        email: email,
        message: (data.get("message") || "").toString(),
        optin: data.get("optin") === "1",
        website: (data.get("website") || "").toString(),
        lang: cfg.lang,
        page: location.href
      })
    })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (out) {
        if (!out || !out.ok) throw new Error("send_failed");
        form.classList.add("sent");
        note.className = "wnote good";
        note.textContent = cfg.done;
        button.disabled = false;
        button.textContent = cfg.cta;
        push("whitepaper_lead", { lang: cfg.lang, optin: data.get("optin") === "1" });
        // the mail carries the file; the browser gets it straight away too
        var a = document.createElement("a");
        a.href = cfg.pdf;
        a.setAttribute("download", "");
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch(function () {
        note.className = "wnote bad";
        note.textContent = cfg.fail;
        button.disabled = false;
      });
  });
})();
