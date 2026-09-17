// Theme toggle: respects the OS preference until the visitor picks one.
(function () {
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");
  if (!button) return;

  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }
  function apply(theme) {
    root.setAttribute("data-theme", theme);
    button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }
  apply(current());

  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    apply(next);
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
  });

  // Follow OS changes only while the visitor has not chosen explicitly.
  try {
    if (!localStorage.getItem("theme") && window.matchMedia) {
      window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", function (e) {
          apply(e.matches ? "dark" : "light");
        });
    }
  } catch (e) {}
})();
