const notificaciones = {
  obtenerContenedor: function () {
    let contenedor = document.getElementById("contenedorNotificaciones");

    if (!contenedor) {
      contenedor = document.createElement("div");
      contenedor.id = "contenedorNotificaciones";
      contenedor.className = "contenedor-notificaciones";
      document.body.appendChild(contenedor);
    }

    return contenedor;
  },

  obtenerIcono: function (tipo) {
    const iconos = {
      success: "✓",
      danger: "✕",
      warning: "!",
      info: "i"
    };

    return iconos[tipo] || iconos.info;
  },

  mostrar: function (mensaje, tipo = "success", duracion = 4000) {
    const contenedor = this.obtenerContenedor();
    const alerta = document.createElement("div");

    alerta.className = `notificacion notificacion-${tipo}`;
    alerta.setAttribute("role", "alert");

    alerta.innerHTML = `
      <div class="notificacion-icono">
        ${this.obtenerIcono(tipo)}
      </div>

      <div class="notificacion-contenido">
        <p class="notificacion-mensaje">${mensaje}</p>
      </div>

      <button
        type="button"
        class="notificacion-cerrar"
        aria-label="Cerrar"
      >
        &times;
      </button>

      <div class="notificacion-progreso"></div>
    `;

    contenedor.appendChild(alerta);

    requestAnimationFrame(function () {
      alerta.classList.add("notificacion-visible");
    });

    const cerrar = function () {
      alerta.classList.remove("notificacion-visible");
      alerta.classList.add("notificacion-salida");

      setTimeout(function () {
        alerta.remove();
      }, 300);
    };

    alerta
      .querySelector(".notificacion-cerrar")
      .addEventListener("click", cerrar);

    const barraProgreso = alerta.querySelector(
      ".notificacion-progreso"
    );

    barraProgreso.style.animationDuration = `${duracion}ms`;

    setTimeout(cerrar, duracion);
  },

  exito: function (mensaje, duracion = 4000) {
    this.mostrar(mensaje, "success", duracion);
  },

  error: function (mensaje, duracion = 5000) {
    this.mostrar(mensaje, "danger", duracion);
  },

  advertencia: function (mensaje, duracion = 4500) {
    this.mostrar(mensaje, "warning", duracion);
  },

  informacion: function (mensaje, duracion = 4000) {
    this.mostrar(mensaje, "info", duracion);
  }
};