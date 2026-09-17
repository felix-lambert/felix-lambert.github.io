// Progressive enhancements only: the site works fully without this file.
(function () {
  var root = document.documentElement;
  root.classList.add("js");

  // --- Theme toggle: follows the OS until the visitor picks explicitly. ---
  var button = document.querySelector(".theme-toggle");
  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }
  function apply(theme) {
    root.setAttribute("data-theme", theme);
    if (button) button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }
  apply(current());
  if (button) {
    button.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      apply(next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {}
    });
  }
  try {
    if (!localStorage.getItem("theme") && window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
        apply(e.matches ? "dark" : "light");
      });
    }
  } catch (e) {}

  // --- Header border once the page is scrolled. ---
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // --- Copy email button. ---
  var copy = document.querySelector(".copy-email");
  if (copy && navigator.clipboard) {
    var label = copy.textContent;
    copy.addEventListener("click", function () {
      navigator.clipboard.writeText(copy.getAttribute("data-email")).then(function () {
        copy.textContent = copy.getAttribute("data-copied");
        copy.classList.add("is-done");
        setTimeout(function () {
          copy.textContent = label;
          copy.classList.remove("is-done");
        }, 1800);
      });
    });
  } else if (copy) {
    copy.hidden = true;
  }
})();
