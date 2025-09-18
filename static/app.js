document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const btn = document.getElementById("toggle-theme");
  if (!btn) return;

  btn.addEventListener("click", () => {
    root.classList.toggle("theme-dark");
  });
});