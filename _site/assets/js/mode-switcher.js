document.addEventListener("DOMContentLoaded", themeChange);

const theme = localStorage.getItem("theme");

console.log("theme");
console.log(theme);

if (theme === "dark") {
  document.documentElement.setAttribute("data-theme", "dark");
}
if (theme === "light") {
  document.documentElement.setAttribute("data-theme", "light");
}

function themeChange() {
  // Select our toggle button
  let button = document.querySelector(".theme-toggle");

  // Add an event listener for a click
  button.addEventListener("click", function (e) {
    // Check the current data-theme value
    let currentTheme = document.documentElement.getAttribute("data-theme");

    console.log(theme);

    if (currentTheme === "dark") {
      document.documentElement.setAttribute("data-theme", "light");
      window.localStorage.setItem("theme", "light");
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      window.localStorage.setItem("theme", "dark");
    }
  });
}
