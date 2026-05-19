// In-page table of contents
// For pages with a <article class="prose-article">, scans h2 + h3 elements and
// renders a sticky sidebar (desktop) plus a collapsible inline TOC (mobile).
// Highlights the current section via IntersectionObserver.

(function() {
  "use strict";

  function slugify(s) {
    return s.toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-")
      .slice(0, 80);
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

  function buildToc() {
    const article = document.querySelector(".prose-article");
    if (!article) return;
    const headings = article.querySelectorAll("h2, h3");
    if (headings.length < 3) return;   // not worth a TOC on short pages

    // Ensure IDs
    const items = [];
    headings.forEach(h => {
      if (!h.id) {
        h.id = slugify(h.textContent || "");
      }
      items.push({
        id: h.id,
        text: h.textContent.trim(),
        level: parseInt(h.tagName[1], 10),
        el: h,
      });
    });

    // Desktop sticky TOC
    const toc = el("aside", { className: "page-toc", attrs: { "aria-label": "On this page" } });
    toc.appendChild(el("div", { className: "toc-head", text: "On this page" }));
    items.forEach(it => {
      const a = el("a", {
        attrs: { href: "#" + it.id, "data-id": it.id },
        className: "level-" + it.level,
        text: it.text,
      });
      toc.appendChild(a);
    });
    document.body.appendChild(toc);

    // Mobile inline TOC (collapsible <details>)
    const inline = el("details", { className: "page-toc-inline" });
    inline.appendChild(el("summary", { text: "On this page" }));
    // Build hierarchical list
    const ul = el("ul");
    items.forEach(it => {
      if (it.level === 2) {
        const li = el("li");
        li.appendChild(el("a", { attrs: { href: "#" + it.id }, text: it.text }));
        ul.appendChild(li);
      } else if (it.level === 3) {
        // Nest under last h2 li
        const last = ul.lastChild;
        if (last) {
          let sub = last.querySelector("ul");
          if (!sub) {
            sub = el("ul", { className: "level-3" });
            last.appendChild(sub);
          }
          const subli = el("li");
          subli.appendChild(el("a", { attrs: { href: "#" + it.id }, text: it.text }));
          sub.appendChild(subli);
        }
      }
    });
    inline.appendChild(ul);
    article.insertBefore(inline, article.firstChild);

    // IntersectionObserver to highlight active section
    if (!("IntersectionObserver" in window)) return;
    const links = toc.querySelectorAll("a");
    const byId = new Map();
    links.forEach(a => byId.set(a.getAttribute("data-id"), a));

    let activeId = null;
    function setActive(id) {
      if (id === activeId) return;
      activeId = id;
      links.forEach(a => a.classList.toggle("active", a.dataset.id === id));
    }

    const observer = new IntersectionObserver(entries => {
      // Pick the topmost intersecting heading
      const intersecting = entries.filter(e => e.isIntersecting);
      if (intersecting.length) {
        // Use the one closest to the top
        intersecting.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        setActive(intersecting[0].target.id);
      }
    }, {
      rootMargin: "-80px 0px -70% 0px",
      threshold: 0,
    });
    items.forEach(it => observer.observe(it.el));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildToc);
  } else {
    buildToc();
  }
})();
