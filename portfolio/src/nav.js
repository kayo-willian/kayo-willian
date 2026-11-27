// Navigation stays visible and usable when JavaScript is disabled.
const header = document.querySelector(".header");
const menu = header.querySelector("button");
const nav = header.querySelector("nav");
function setOpen(open) {
  menu.setAttribute("aria-expanded", String(open));
  header.classList.toggle("open", open);
}
header.classList.add("enhanced");
menu.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  setOpen(open);
  if (open) nav.querySelector("a").focus();
});
nav.addEventListener("click", () => setOpen(false));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
    setOpen(false);
    menu.focus();
  }
});
// Bilingual home sections share anchors so the reader keeps their place.
const language = header.querySelector(".language");
const languagePath = language.getAttribute("href");
function syncLanguage() {
  const fragment = window.location.hash;
  const target = document.getElementById(fragment.slice(1));
  if (target instanceof HTMLDetailsElement) target.open = true;
  language.href = languagePath + (target ? fragment : "");
}
window.addEventListener("hashchange", syncLanguage);
syncLanguage();
