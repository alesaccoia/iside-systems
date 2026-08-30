/* Whitepaper gate: the PDF arrives by mail, so the form has to succeed first.
   The form lives in a modal, and every step is pushed to the data layer:
   whitepaper_open, whitepaper_lead, file_download (GA4 recommended event). */
(function () {
  var cfg = window.WPAPER || {};
  var modal = document.getElementById("wmodal");
  var form = document.getElementById("wform");
  var open = document.getElementById("wopen");
  if (!modal || !form || !open) return;
  var note = document.getElementById("wnote");
  var button = form.querySelector("button[type=submit]");
  var lastFocus = null;

  function push(event, extra) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: event, lang: cfg.lang };
    if (extra) Object.keys(extra).forEach(function (k) { payload[k] = extra[k]; });
    window.dataLayer.push(payload);
  }

  function show() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.documentElement.style.overflow = "hidden";
    var first = form.querySelector("input[name=name]");
    if (first) first.focus();
    push("whitepaper_open", { link_url: location.href });
  }

  function hide() {
    modal.hidden = true;
    document.documentElement.style.overflow = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  open.addEventListener("click", show);
  modal.addEventListener("click", function (ev) {
    if (ev.target.closest("[data-wclose]")) hide();
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && !modal.hidden) hide();
  });

  // the tab order must not walk out of an open dialog
  modal.addEventListener("keydown", function (ev) {
    if (ev.key !== "Tab") return;
    var f = modal.querySelectorAll("button,input,textarea,a[href]");
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (ev.shiftKey && document.activeElement === first) { last.focus(); ev.preventDefault(); }
    else if (!ev.shiftKey && document.activeElement === last) { first.focus(); ev.preventDefault(); }
  });

  function download() {
    var a = document.createElement("a");
    a.href = cfg.pdf;
    a.setAttribute("download", "");
    document.body.appendChild(a);
    a.click();
    a.remove();
    // GA4 only fires file_download by itself on plain links: this one is scripted
    push("file_download", {
      file_name: cfg.file,
      file_extension: "pdf",
      link_url: location.origin + cfg.pdf,
      link_text: cfg.cta
    });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var data = new FormData(form);
    var first = (data.get("name") || "").toString().trim();
    var last = (data.get("surname") || "").toString().trim();
    var email = (data.get("email") || "").toString().trim();
    var optin = data.get("optin") === "1";
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
        optin: optin,
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
        push("whitepaper_lead", { optin: optin });
        download();
      })
      .catch(function () {
        note.className = "wnote bad";
        note.textContent = cfg.fail;
        button.disabled = false;
      });
  });
})();
