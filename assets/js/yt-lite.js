// Façade YouTube : remplace la vignette par l'iframe réelle au premier clic.
// Sans JS, le lien renvoie simplement vers youtube.com (dégradation propre).
(function () {
  document.addEventListener("click", function (e) {
    var facade = e.target.closest ? e.target.closest(".yt-lite") : null;
    if (!facade || facade.dataset.loaded) return;
    e.preventDefault();
    facade.dataset.loaded = "1";
    var iframe = document.createElement("iframe");
    iframe.src =
      "https://www.youtube-nocookie.com/embed/" +
      facade.dataset.id +
      "?autoplay=1&rel=0";
    iframe.title = "Vidéo YouTube";
    iframe.allow =
      "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    facade.textContent = "";
    facade.appendChild(iframe);
  });
})();
