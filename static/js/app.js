document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const btn = document.getElementById("toggle-theme");
  if (!btn) return;

  btn.addEventListener("click", () => {
    root.classList.toggle("theme-dark");
  });
});
(function () {
  try {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.dataset.color = prefersDark ? 'dark' : 'light';
  } catch (e) {
    // no-op
  }
})();