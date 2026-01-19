function getScrollPosition() {
  return typeof window === "undefined"
    ? { x: 0, y: 0 }
    : { x: window.scrollX, y: window.scrollY };
}

let hasScrolled = false;
function checkScrollPosition() {
  const document = window.document.documentElement;
  const position = getScrollPosition();
  const scrolled = position.y > 0;

  if (scrolled != hasScrolled) {
    hasScrolled = scrolled;
    if (scrolled) {
      document.dataset.scrolled = "";
    } else if (document.dataset.scrolled !== undefined) {
      delete document.dataset.scrolled;
    }
  }
}

function initDropdownToggle() {
  document.querySelectorAll(".esi-nav-header-item-dropdown").forEach((item) => {
    item.addEventListener("click", (event) => {
      if (item.dataset.open) {
        delete item.dataset.open;
      } else {
        item.dataset.open = "true";
      }
    });
  });
}

window.addEventListener("scroll", checkScrollPosition);
window.addEventListener("load", checkScrollPosition);
window.addEventListener("load", initDropdownToggle);
