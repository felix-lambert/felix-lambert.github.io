document.addEventListener("DOMContentLoaded", themeChange);

function themeChange() {
  // Select our toggle button
  let button = document.querySelector(".theme-toggle");

  // Add an event listener for a click
  button.addEventListener("click", function (e) {
    // Check the current data-theme value
    let currentTheme = document.documentElement.getAttribute("data-theme");

    if (currentTheme === "dark") {
      document.documentElement.setAttribute("data-theme", "light");
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  });
}
