document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");
  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });
  }

  document.querySelectorAll("[data-copy-text]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy-text");
      if (!text) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          var original = btn.textContent;
          btn.textContent = "متن پیام کپی شد!";
          setTimeout(function () {
            btn.textContent = original;
          }, 2000);
        });
      }
    });
  });
});
