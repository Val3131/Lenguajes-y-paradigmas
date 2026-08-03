document.addEventListener("DOMContentLoaded", function () {
  const botonCerrarSesion = document.getElementById("btnCerrarSesion");

  if (!botonCerrarSesion) {
    return;
  }

  botonCerrarSesion.addEventListener("click", function () {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("usuarioId");
    localStorage.removeItem("nombreUsuario");

    window.location.href = "login.html";
  });
});