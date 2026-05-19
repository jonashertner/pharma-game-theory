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
      "background:#0b0d10", "color:#e6e8eb",
      "display:flex", "align-items:center", "justify-content:center",
      "z-index:99999",
      "font-family:-apple-system,BlinkMacSystemFont,'Inter','Segoe UI',Roboto,sans-serif",
    ].join(";");

    const card = document.createElement("div");
    card.style.cssText = [
      "background:#14171c", "border:1px solid #2a2f37", "border-radius:12px",
      "padding:42px 44px", "max-width:420px", "width:90%",
      "box-shadow:0 20px 60px rgba(0,0,0,0.5)",
    ].join(";");

    const brand = document.createElement("div");
    brand.style.cssText = "font-size:11px;color:#8b94a3;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;";
    brand.textContent = "Roche pharma-pricing simulation";

    const title = document.createElement("h2");
    title.style.cssText = "margin:0 0 8px 0;font-size:22px;font-weight:600;letter-spacing:-0.01em;color:#e6e8eb;";
    title.textContent = "Restricted access";

    const sub = document.createElement("p");
    sub.style.cssText = "margin:0 0 24px 0;color:#8b94a3;font-size:14px;line-height:1.5;";
    sub.textContent = "This site contains pre-board strategic analysis. Enter the access passcode to continue.";

    const input = document.createElement("input");
    input.type = "password";
    input.id = "passcode-input";
    input.autocomplete = "current-password";
    input.placeholder = "Passcode";
    input.style.cssText = [
      "width:100%", "background:#0b0d10", "color:#e6e8eb",
      "border:1px solid #2a2f37", "border-radius:6px",
      "padding:11px 13px", "font-size:15px", "font-family:inherit",
      "outline:none", "transition:border-color 0.15s ease",
    ].join(";");

    const btn = document.createElement("button");
    btn.id = "passcode-submit";
    btn.textContent = "Enter";
    btn.style.cssText = [
      "margin-top:14px", "width:100%",
      "background:#7aa2f7", "color:#001a33",
      "border:none", "border-radius:6px",
      "padding:11px 14px", "font-size:14px", "font-weight:600",
      "cursor:pointer", "font-family:inherit",
      "transition:background 0.15s ease",
    ].join(";");

    const msg = document.createElement("div");
    msg.id = "passcode-msg";
    msg.style.cssText = "margin-top:14px;font-size:12.5px;color:#f7768e;min-height:18px;text-align:center;";

    const foot = document.createElement("div");
    foot.style.cssText = "margin-top:22px;color:#8b94a3;font-size:11px;line-height:1.5;border-top:1px solid #2a2f37;padding-top:14px;";
    foot.textContent = "Independent public-source analysis, not an official Roche document. No NDA-protected information.";

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
        // brief shake
        input.style.borderColor = "#f7768e";
        setTimeout(() => { input.style.borderColor = "#2a2f37"; }, 800);
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
