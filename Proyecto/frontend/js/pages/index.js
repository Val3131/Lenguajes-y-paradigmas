document.addEventListener("DOMContentLoaded", function () {

  const token = localStorage.getItem("accessToken");

  if (token) {
    window.location.replace("./pages/perfil.html");
  }

});