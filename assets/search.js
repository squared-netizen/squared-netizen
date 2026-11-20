// The docs' search (docs/search.html?q=...): every gathered document, from
// docs/search-index.json (tools/docs.py writes it). A page scores by each word
// of the query in its title, its headings and its text; every word must be
// somewhere in the page. Results show a snippet around the first match.
(function () {
  "use strict";
  const params = new URLSearchParams(location.search);
  const query = (params.get("q") || "").trim();
  const out = document.getElementById("results");
  const box = document.querySelector('form.search input[name="q"]');
  if (box) box.value = query;
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  if (!query) {
    out.innerHTML = "<p>Type a word or two in the search box.</p>";
    return;
  }
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  const count = (hay, w) => {
    let n = 0, at = hay.indexOf(w);
    while (at >= 0 && n < 50) { n++; at = hay.indexOf(w, at + w.length); }
    return n;
  };
  fetch("search-index.json")
    .then((r) => r.json())
    .then((pages) => {
      const hits = [];
      for (const p of pages) {
        const title = p.t.toLowerCase(), heads = p.h.join(" ").toLowerCase(), text = p.x.toLowerCase();
        const path = p.p.toLowerCase() + " " + p.r.toLowerCase();
        let score = 0, all = true;
        for (const w of words) {
          const s = count(title, w) * 20 + count(heads, w) * 6 + count(path, w) * 4 + count(text, w);
          if (s === 0) { all = false; break; }
          score += s;
        }
        if (all) hits.push([score, p]);
      }
      hits.sort((a, b) => b[0] - a[0]);
      if (!hits.length) {
        out.innerHTML = `<p>Nothing found for <b>${esc(query)}</b>.</p>`;
        return;
      }
      const html = [`<p>${hits.length} document${hits.length > 1 ? "s" : ""} for <b>${esc(query)}</b>.</p><ol class="hits">`];
      for (const [, p] of hits.slice(0, 100)) {
        const lower = p.x.toLowerCase();
        let at = lower.indexOf(words[0]);
        let snippet = "";
        if (at >= 0) {
          const from = Math.max(0, at - 80);
          snippet = (from > 0 ? "… " : "") + p.x.slice(from, at + 160) + " …";
        }
        let s = esc(snippet);
        for (const w of words) s = s.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi"), "<mark>$1</mark>");
        html.push(`<li><a href="../${esc(encodeURI(p.u))}">${esc(p.t)}</a> <span class="path">${esc(p.r)} · ${esc(p.p)}</span><div class="snip">${s}</div></li>`);
      }
      html.push("</ol>");
      out.innerHTML = html.join("");
    })
    .catch(() => { out.innerHTML = "<p>The search index could not be read.</p>"; });
})();
