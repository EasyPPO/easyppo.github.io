"use strict";

const dialog = document.querySelector(".figure-dialog");
const dialogImage = dialog.querySelector(".dialog-image");
const dialogCaption = dialog.querySelector(".dialog-caption");
const closeButton = dialog.querySelector(".close-dialog");
let lastFigure;

document.querySelectorAll("[data-lightbox]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (typeof dialog.showModal !== "function") return;
    event.preventDefault();
    lastFigure = link;
    const image = link.querySelector("img");
    dialogImage.src = link.href;
    dialogImage.alt = image.alt;
    dialog.querySelector(".original-link").href = link.href;
    dialogCaption.textContent = link.closest("figure").querySelector("figcaption").textContent.replace("Click any figure to enlarge.", "").trim();
    dialog.showModal();
    document.body.classList.add("dialog-open");
    closeButton.focus();
  });
});
closeButton.addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  const rect = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
});
dialog.addEventListener("close", () => {
  document.body.classList.remove("dialog-open");
  if (lastFigure) lastFigure.focus({ preventScroll: true });
});

const copyButton = document.querySelector("[data-copy]");
const copyStatus = document.querySelector("#copy-status");
copyButton.hidden = false;
let copyReset;
copyButton.addEventListener("click", async () => {
  const citation = document.querySelector("#bibtex");
  try {
    await navigator.clipboard.writeText(citation.textContent);
    copyStatus.textContent = "Citation copied.";
    copyButton.dataset.copied = "true";
    copyButton.setAttribute("aria-label", "BibTeX copied");
    copyButton.title = "Copied";
    clearTimeout(copyReset);
    copyReset = setTimeout(() => {
      delete copyButton.dataset.copied;
      copyButton.setAttribute("aria-label", "Copy BibTeX");
      copyButton.title = "Copy BibTeX";
    }, 2000);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(citation);
    selection.removeAllRanges();
    selection.addRange(range);
    copyStatus.textContent = "Citation selected. Use your browser’s Copy command.";
  }
});

const navigation = [...document.querySelectorAll(".nav-links a")];
const sections = navigation.map((link) => document.querySelector(link.hash));
let updateQueued = false;
function updateNavigation() {
  updateQueued = false;
  let current;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 150) current = section.id;
  }
  navigation.forEach((link) => {
    if (link.hash === `#${current}`) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
}
window.addEventListener("scroll", () => {
  if (!updateQueued) {
    updateQueued = true;
    window.requestAnimationFrame(updateNavigation);
  }
}, { passive: true });
updateNavigation();
