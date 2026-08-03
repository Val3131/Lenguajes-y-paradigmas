document.addEventListener("DOMContentLoaded", function () {

    const nombre =
        localStorage.getItem("nombreUsuario");

    const span =
        document.getElementById("nombreUsuarioNavbar");

    if (span && nombre) {
        span.textContent = `Hola, ${nombre}`;
    }

});