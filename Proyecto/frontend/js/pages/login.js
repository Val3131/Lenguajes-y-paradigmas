document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("formLogin");

  formulario.addEventListener("submit", async function (event) {
    event.preventDefault();

    const datos = {
      correo: document.getElementById("correo").value.trim(),
      contrasena: document.getElementById("contrasena").value
    };

    try {
      const respuesta = await apiService.iniciarSesion(datos);

      localStorage.setItem("accessToken", respuesta.access_token);
      localStorage.setItem("usuarioId", respuesta.usuario_id);
      localStorage.setItem("nombreUsuario", respuesta.nombre);

      window.location.href = "perfil.html";

    } catch (error) {
      notificaciones.error(
        error.message || "No fue posible iniciar sesión."
      );
    }
  });
});