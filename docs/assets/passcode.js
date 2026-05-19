// Passcode gate — runs before page render.
//
// SECURITY NOTE: this is a JavaScript-only client-side gate. Anyone who reads
// the page source can see the SHA-256 hash and brute-force a weak passcode
// offline. It blocks search engines (combined with the noindex meta tag) and
// casual visitors, but is NOT a substitute for server-side auth. For real
// access control, deploy via Cloudflare Pages + Cloudflare Access, or a
// password-protected Vercel/Netlify deployment.
//
// Update the passcode hash with:  python tools/set_passcode.py <new_passcode>
//
// Default passcode: roche-board-2026  (CHANGE BEFORE DEPLOYING)

(function() {
  "use strict";

  // SHA-256 hex of the passcode. Replace with `tools/set_passcode.py`.
  const EXPECTED_HASH = "daeebab6390ec9085bd7511380d108bf810bdcf62836ed20c5dea5efcf015409";
  const STORAGE_KEY = "rgt-pass-v1";

  // If already authorised in localStorage, skip the gate entirely.
  try {
    if (localStorage.getItem(STORAGE_KEY) === EXPECTED_HASH) return;
  } catch (e) { /* localStorage unavailable */ }

  // Hide page content until gate passes.
  const styleEl = document.createElement("style");
  styleEl.textContent = "body > *:not(#passcode-overlay) { visibility: hidden !important; } #passcode-overlay { visibility: visible !important; }";
  document.documentElement.appendChild(styleEl);

  async function sha256Hex(text) {
    const buf = new TextEncoder().encode(text);
    const hashBuf = await crypto.subtle.digest("SHA-256", buf);
    return Array.from(new Uint8Array(hashBuf))
      .map(b => b.toString(16).padStart(2, "0"))
      .join("");
  }

  function buildOverlay() {
    const overlay = document.createElement("div");
    overlay.id = "passcode-overlay";
    overlay.style.cssText = [
      "position:fixed", "top:0", "left:0", "right:0", "bottom:0",
      "background:#fafaf9", "color:#18181b",
      "display:flex", "align-items:center", "justify-content:center",
      "z-index:99999", "padding:16px",
      "font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif",
    ].join(";");

    const card = document.createElement("div");
    card.style.cssText = [
      "background:#ffffff", "border:1px solid #e7e5e0", "border-radius:12px",
      "padding:44px 46px", "max-width:440px", "width:100%",
      "box-shadow:0 1px 3px rgba(0,0,0,0.04),0 12px 36px rgba(0,0,0,0.06)",
    ].join(";");

    const brand = document.createElement("div");
    brand.style.cssText = "font-size:10.5px;color:#737373;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:18px;font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:500;";
    brand.textContent = "Pharma negotiation simulation";

    const title = document.createElement("h2");
    title.style.cssText = "margin:0 0 10px 0;font-size:26px;font-weight:500;letter-spacing:-0.022em;color:#18181b;font-family:'Source Serif 4',Charter,Cambria,Georgia,serif;line-height:1.15;";
    title.textContent = "Restricted access";

    const sub = document.createElement("p");
    sub.style.cssText = "margin:0 0 28px 0;color:#404044;font-size:15px;line-height:1.55;font-family:'Source Serif 4',Charter,Cambria,Georgia,serif;";
    sub.textContent = "This site contains pre-board strategic analysis. Enter the access passcode to continue.";

    const input = document.createElement("input");
    input.type = "password";
    input.id = "passcode-input";
    input.autocomplete = "current-password";
    input.placeholder = "Passcode";
    input.style.cssText = [
      "width:100%", "background:#fafaf9", "color:#18181b",
      "border:1px solid #d4d2cc", "border-radius:6px",
      "padding:12px 14px", "font-size:15px", "font-family:inherit",
      "outline:none", "transition:border-color 150ms ease,box-shadow 150ms ease",
      "letter-spacing:-0.005em",
    ].join(";");

    const btn = document.createElement("button");
    btn.id = "passcode-submit";
    btn.textContent = "Enter";
    btn.style.cssText = [
      "margin-top:14px", "width:100%",
      "background:#1e3a5f", "color:#ffffff",
      "border:1px solid #1e3a5f", "border-radius:6px",
      "padding:12px 16px", "font-size:14px", "font-weight:500",
      "cursor:pointer", "font-family:inherit",
      "transition:background 150ms ease", "letter-spacing:-0.005em",
    ].join(";");

    const msg = document.createElement("div");
    msg.id = "passcode-msg";
    msg.style.cssText = "margin-top:14px;font-size:13px;color:#b91c1c;min-height:18px;text-align:center;font-family:inherit;";

    const foot = document.createElement("div");
    foot.style.cssText = "margin-top:26px;color:#737373;font-size:11.5px;line-height:1.55;border-top:1px solid #e7e5e0;padding-top:16px;font-family:inherit;letter-spacing:-0.003em;";
    foot.textContent = "Independent public-source analysis. Not an official Roche document. No NDA-protected information.";

    card.appendChild(brand);
    card.appendChild(title);
    card.appendChild(sub);
    card.appendChild(input);
    card.appendChild(btn);
    card.appendChild(msg);
    card.appendChild(foot);
    overlay.appendChild(card);
    return { overlay, input, btn, msg };
  }

  function mountGate() {
    const { overlay, input, btn, msg } = buildOverlay();
    document.body.appendChild(overlay);
    setTimeout(() => input.focus(), 50);

    async function tryUnlock() {
      const code = input.value.trim();
      if (!code) return;
      const hashed = await sha256Hex(code);
      if (hashed === EXPECTED_HASH) {
        try { localStorage.setItem(STORAGE_KEY, hashed); } catch (e) {}
        styleEl.remove();
        overlay.remove();
      } else {
        msg.textContent = "Passcode not recognised. Try again.";
        input.value = "";
        input.focus();
        input.style.borderColor = "#b91c1c";
        input.style.boxShadow = "0 0 0 3px rgba(185,28,28,0.08)";
        setTimeout(() => {
          input.style.borderColor = "#d4d2cc";
          input.style.boxShadow = "none";
        }, 900);
      }
    }
    btn.addEventListener("click", tryUnlock);
    input.addEventListener("keydown", e => {
      if (e.key === "Enter") tryUnlock();
    });
  }

  if (document.body) {
    mountGate();
  } else {
    document.addEventListener("DOMContentLoaded", mountGate);
  }
})();
