var openPopupBtn = document.getElementById("openPopupBtn");
var popup = document.getElementById("popup");
openPopupBtn.addEventListener("click", function (event) {
  event.preventDefault();
  popup.style.display = "block";
});

document
  .getElementsByClassName("close")[0]
  .addEventListener("click", function () {
    popup.style.display = "none";
  });
