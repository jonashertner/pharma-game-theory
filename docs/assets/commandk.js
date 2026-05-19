// Cmd+K command palette
// Loads search-index.json (auto-built) and lets the user fuzzy-match across
// every page and every H2/H3 section.

(function() {
  "use strict";
  let INDEX = null;
  let activeIdx = 0;
  let filtered = [];

  async function loadIndex() {
    if (INDEX) return INDEX;
    try {
      const resp = await fetch("search-index.json");
      INDEX = await resp.json();
    } catch (e) {
      INDEX = [];
    }
    return INDEX;
  }

  function el(tag, opts, children) {
    const node = document.createElement(tag);
    if (opts) {
      if (opts.className) node.className = opts.className;
      if (opts.text !== undefined) node.textContent = opts.text;
      if (opts.attrs) for (const [k,v] of Object.entries(opts.attrs)) node.setAttribute(k, v);
    }
    if (children) for (const c of children) if (c) node.appendChild(c);
    return node;
  }
  function clear(p) { while (p.firstChild) p.removeChild(p.firstChild); }

  function flatten(index) {
    const out = [];
    for (const p of index) {
      out.push({
        type: "page",
        page: p.page,
        title: p.title,
        url: p.page,
        haystack: p.title.toLowerCase(),
      });
      for (const s of (p.sections || [])) {
        out.push({
          type: "section",
          page: p.page,
          title: s.label,
          pageTitle: p.title,
          level: s.level,
          url: p.page + "#" + s.id,
          haystack: (s.label + " " + p.title).toLowerCase(),
        });
      }
    }
    return out;
  }

  function score(item, terms) {
    let total = 0;
    for (const t of terms) {
      const h = item.haystack;
      const i = h.indexOf(t);
      if (i < 0) {
        let j = 0;
        for (let k = 0; k < t.length; k++) {
          const idx = h.indexOf(t[k], j);
          if (idx < 0) return null;
          j = idx + 1;
        }
        total += 5 + (j - t.length) * 0.1;
      } else {
        total += i === 0 ? 0 : (i * 0.2);
      }
    }
    return total;
  }

  function filter(query, items) {
    const q = query.trim().toLowerCase();
    if (!q) return items.slice(0, 60);
    const terms = q.split(/\s+/);
    const scored = [];
    for (const it of items) {
      const s = score(it, terms);
      if (s !== null) scored.push({ it, s });
    }
    scored.sort((a, b) => a.s - b.s);
    return scored.slice(0, 40).map(x => x.it);
  }

  function renderItems(listEl, items) {
    clear(listEl);
    if (!items.length) {
      listEl.appendChild(el("div", {
        className: "palette-empty",
        text: "No matches. Try \"firewall\", \"Roche\", \"Section 232\", \"dynamics\"…",
      }));
      return;
    }
    items.forEach((it, idx) => {
      const item = el("a", {
        className: "palette-item" + (idx === activeIdx ? " active" : ""),
        attrs: { href: it.url, "data-idx": idx, role: "option" },
      });
      const iconText = it.type === "section" ? "§" : "↗";
      item.appendChild(el("span", { className: "icon", text: iconText }));
      item.appendChild(el("span", { className: "title", text: it.title }));
      if (it.type === "section" && it.pageTitle) {
        item.appendChild(el("span", { className: "crumb", text: it.pageTitle }));
      }
      item.appendChild(el("span", { className: "arrow", text: "↩" }));
      listEl.appendChild(item);
    });
  }

  async function openPalette() {
    await loadIndex();
    const items = flatten(INDEX);
    activeIdx = 0;
    filtered = filter("", items);
    const overlay = document.getElementById("palette-overlay");
    const input = document.getElementById("palette-input");
    const listEl = document.getElementById("palette-list");
    if (!overlay) return;
    renderItems(listEl, filtered);
    overlay.classList.add("open");
    setTimeout(() => input.focus(), 30);

    input.value = "";
    function onInput() {
      activeIdx = 0;
      filtered = filter(input.value, items);
      renderItems(listEl, filtered);
    }
    function onKey(e) {
      if (e.key === "Escape") { closePalette(); return; }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIdx = Math.min(filtered.length - 1, activeIdx + 1);
        renderItems(listEl, filtered);
        scrollActiveIntoView(listEl);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIdx = Math.max(0, activeIdx - 1);
        renderItems(listEl, filtered);
        scrollActiveIntoView(listEl);
      } else if (e.key === "Enter") {
        e.preventDefault();
        const it = filtered[activeIdx];
        if (it) window.location.href = it.url;
      }
    }
    input.addEventListener("input", onInput);
    input.addEventListener("keydown", onKey);
    overlay.addEventListener("click", e => {
      if (e.target === overlay) closePalette();
    });
    overlay._cleanup = () => {
      input.removeEventListener("input", onInput);
      input.removeEventListener("keydown", onKey);
    };
  }
  function scrollActiveIntoView(listEl) {
    const active = listEl.querySelector(".palette-item.active");
    if (active) active.scrollIntoView({ block: "nearest" });
  }
  function closePalette() {
    const overlay = document.getElementById("palette-overlay");
    if (!overlay) return;
    overlay.classList.remove("open");
    if (overlay._cleanup) overlay._cleanup();
  }

  function buildHint(keyTexts, label) {
    const span = el("span", { className: "hint" });
    for (const k of keyTexts) {
      span.appendChild(el("kbd", { text: k }));
    }
    span.appendChild(document.createTextNode(" " + label));
    return span;
  }

  function buildOverlay() {
    if (document.getElementById("palette-overlay")) return;
    const overlay = el("div", {
      attrs: { id: "palette-overlay", role: "dialog", "aria-modal": "true", "aria-label": "Search palette" },
      className: "palette-overlay",
    });
    const palette = el("div", { className: "palette" });
    const input = el("input", {
      attrs: {
        id: "palette-input", type: "search",
        placeholder: "Jump to anything — pages, sections, actors…",
        autocomplete: "off", "aria-autocomplete": "list",
      },
      className: "palette-input",
    });
    const list = el("div", { className: "palette-list", attrs: { id: "palette-list", role: "listbox" } });
    const footer = el("div", { className: "palette-footer" });
    footer.appendChild(buildHint(["↩"], "go"));
    footer.appendChild(buildHint(["↑", "↓"], "move"));
    footer.appendChild(buildHint(["esc"], "close"));
    palette.appendChild(input);
    palette.appendChild(list);
    palette.appendChild(footer);
    overlay.appendChild(palette);
    document.body.appendChild(overlay);
  }

  document.addEventListener("DOMContentLoaded", () => {
    buildOverlay();
    const trigger = document.getElementById("palette-trigger");
    if (trigger) trigger.addEventListener("click", openPalette);
    document.addEventListener("keydown", e => {
      const target = e.target;
      const isInput = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA");
      const isMod = (e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K");
      if (isMod) { e.preventDefault(); openPalette(); }
      else if (!isInput && e.key === "/" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        openPalette();
      }
    });
  });
})();
