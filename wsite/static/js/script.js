// Lấy thẻ nút "Đặt câu hỏi ngay"
var openPopupBtn = document.getElementById("openPopupBtn");

// Lấy thẻ cửa sổ nổi
var popup = document.getElementById("popup");

// Gán sự kiện click cho nút "Đặt câu hỏi ngay"
openPopupBtn.addEventListener("click", function (event) {
  event.preventDefault(); // Ngăn chặn hành vi mặc định của thẻ a

  // Hiển thị cửa sổ nổi
  popup.style.display = "block";
});

// Đóng cửa sổ nổi khi nhấp vào nút đóng
document
  .getElementsByClassName("close")[0]
  .addEventListener("click", function () {
    popup.style.display = "none";
  });
