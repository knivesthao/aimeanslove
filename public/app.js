// Copy buttons only. Board cards are server-rendered; no fetching, no filters.
// Mobile menu toggle.
document.addEventListener("click", (e) => {
  const m = e.target.closest("#menubtn");
  if (m) {
    const links = document.querySelector(".topnav .links");
    links.classList.toggle("hidden");
    links.classList.toggle("flex");
    m.setAttribute("aria-expanded", links.classList.contains("flex") ? "true" : "false");
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
    s.textContent = "copied";
    setTimeout(() => (s.textContent = "copy prompt"), 1200);
  }
});
