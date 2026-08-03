document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("formRegistro");

  if (!formulario) {
    return;
  }

  formulario.addEventListener("submit", async function (event) {
    event.preventDefault();

    const datos = {
      nombre: document.getElementById("nombre").value.trim(),
      correo: document.getElementById("correo").value.trim(),
      contrasena: document.getElementById("contrasena").value
    };

    try {
      const respuesta = await apiService.registrarUsuario(datos);

      localStorage.setItem("accessToken", respuesta.access_token);
      localStorage.setItem("usuarioId", respuesta.usuario_id);
      localStorage.setItem("nombreUsuario", respuesta.nombre);

      window.location.replace("./perfil.html");

    } catch (error) {
      console.error("Error al registrar usuario:", error);

      notificaciones.error(
        error.message || "No fue posible registrar el usuario."
      );
    }
  });
});