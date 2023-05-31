const logoutModal = document.getElementById("popup-modal");

if (window.getComputedStyle(logoutModal).display !== "none") {
  console.log("Logout modal is visible");
} else {
  console.log("Logout modal is not visible");
}

setTimeout(function () {
  hideModal();
}, 7000);
