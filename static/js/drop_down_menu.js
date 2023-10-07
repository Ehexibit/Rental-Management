// JavaScript for handling dropdown functionality
document.addEventListener("DOMContentLoaded", function () {
  const dropdownButton = document.getElementById("dropdown-btn");
  const dropdownMenu = document.getElementById("dropdown-menu");

  // Toggle the dropdown menu on button click
  dropdownButton.addEventListener("click", function () {
    if (dropdownMenu.style.display === "block") {
      dropdownMenu.style.display = "none";
    } else {
      dropdownMenu.style.display = "block";
    }
  });

  // Close the dropdown when clicking outside of it
  document.addEventListener("click", function (event) {
    if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
      dropdownMenu.style.display = "none";
    }
  });
});
