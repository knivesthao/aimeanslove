// Copy buttons only. Board cards are server-rendered; no fetching, no filters.
// Icons: Lucide replaces <i data-lucide> with inline SVG.
window.lucide?.createIcons();
// Mobile menu toggle.
document.addEventListener("click", (e) => {
  const o = e.target.closest("[data-open-support]");
  if (o) {
    e.preventDefault();
    document.getElementById("support-dialog")?.showModal();
    return;
  }
  const dlg = document.getElementById("support-dialog");
  if (dlg && (e.target === dlg || e.target.closest("[data-close-support]"))) {
    dlg.close();
    return;
  }
  const co = e.target.closest("[data-open-contact]");
  if (co) {
    e.preventDefault();
    document.getElementById("contact-dialog")?.showModal();
    return;
  }
  const cdlg = document.getElementById("contact-dialog");
  if (cdlg && (e.target === cdlg || e.target.closest("[data-close-contact]"))) {
    cdlg.close();
    return;
  }
  const c = e.target.closest("[data-copy]");
  if (c) {
    navigator.clipboard?.writeText(c.dataset.copy);
    c.textContent = "copied";
    setTimeout(() => (c.textContent = "copy"), 1200);
    return;
  }
  const s = e.target.closest("[data-copy-skill]");
  if (s) {
    const p = s.closest(".skill")?.querySelector(".prompt")?.textContent ?? "";
    navigator.clipboard?.writeText(p);
    navigator.sendBeacon?.("/api/copy?skill=" + encodeURIComponent(s.dataset.copySkill ?? ""));
    s.textContent = "copied";
    setTimeout(() => (s.textContent = "copy prompt"), 1200);
    return;
  }
  const t = e.target.closest("[data-trim]");
  if (t && e.target === t) {
    updatePackCount();
    return;
  }
  const pa = e.target.closest("[data-pack-all]");
  if (pa) {
    document.querySelectorAll("[data-trim]").forEach((c) => (c.checked = true));
    updatePackCount();
    return;
  }
  const pn = e.target.closest("[data-pack-none]");
  if (pn) {
    document.querySelectorAll("[data-trim]").forEach((c) => (c.checked = false));
    updatePackCount();
    return;
  }
  const pk = e.target.closest("[data-pack]");
  if (pk) {
    const cards = [...document.querySelectorAll(".skill")].filter((card) =>
      card.querySelector("[data-trim]")?.checked
    );
    const pack = cards
      .map((card) => card.querySelector(".prompt")?.textContent ?? "")
      .filter(Boolean)
      .join("\n\n---\n\n");
    if (!pack) return;
    navigator.clipboard?.writeText(pack);
    cards.forEach((card) => {
      const id = card.querySelector("[data-trim]")?.dataset.trim ?? "";
      if (id) navigator.sendBeacon?.("/api/copy?skill=" + encodeURIComponent(id));
    });
    const label = pk.querySelector("[data-pack-count]");
    pk.dataset.done = "1";
    if (label) label.textContent = "copied " + cards.length;
    setTimeout(() => {
      delete pk.dataset.done;
      updatePackCount();
    }, 1500);
  }
});

function updatePackCount() {
  const n = document.querySelectorAll("[data-trim]:checked").length;
  document.querySelectorAll("[data-pack-count]").forEach((el) => {
    if (!el.closest("[data-pack]")?.dataset.done) el.textContent = String(n);
  });
}
