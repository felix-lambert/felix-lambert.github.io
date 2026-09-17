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

  // --- Header shadow once the page is scrolled. ---
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

  // --- Reveal sections as they enter the viewport (respects reduced motion). ---
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var targets = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    targets.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    targets.forEach(function (el) {
      io.observe(el);
    });
    // Safety net: never leave content hidden if the observer does not fire
    // (print, odd embeds, very old engines).
    setTimeout(function () {
      targets.forEach(function (el) {
        el.classList.add("is-visible");
      });
    }, 2500);
  }
})();
