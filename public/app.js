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
  }
});
