document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("formPerfil");
  const checkOtraCondicion = document.getElementById("otraCondicion");
  const contenedorOtraCondicion = document.getElementById(
    "contenedorOtraCondicion"
  );
  const detalleOtraCondicion = document.getElementById(
    "detalleOtraCondicion"
  );

  const token = localStorage.getItem("accessToken");
  const usuarioId = localStorage.getItem("usuarioId");

  if (!token || !usuarioId) {
    window.location.href = "login.html";
    return;
  }

  if (!formulario) {
    return;
  }

  async function cargarPerfil() {
    try {
      const usuario = await apiService.obtenerUsuario(usuarioId);

      document.getElementById("nombre").value = usuario.nombre ?? "";
      document.getElementById("edad").value =
        usuario.edad && usuario.edad !== 1 ? usuario.edad : "";
      document.getElementById("peso").value =
        usuario.peso && usuario.peso !== 3 ? usuario.peso : "";
      document.getElementById("estatura").value =
        usuario.estatura && usuario.estatura !== 0.5
          ? usuario.estatura
          : "";

      document.getElementById("actividad").value =
        usuario.actividad !== "Pendiente"
          ? usuario.actividad ?? ""
          : "";

      document.getElementById("objetivo").value =
        usuario.objetivo !== "Pendiente"
          ? usuario.objetivo ?? ""
          : "";

      document.getElementById("sueno").value =
        usuario.sueno && usuario.sueno !== 1 ? usuario.sueno : "";

      document.getElementById("habitoActividad").value =
        usuario.habito_actividad !== "Pendiente"
          ? usuario.habito_actividad ?? ""
          : "";

      document.getElementById("comentarios").value =
        usuario.comentarios ?? "";

      document
        .querySelectorAll(".condicion-salud")
        .forEach(function (checkbox) {
          checkbox.checked = false;
        });

      checkOtraCondicion.checked = false;
      detalleOtraCondicion.value = "";
      contenedorOtraCondicion.classList.add("d-none");

      const condiciones = usuario.condiciones || [];

      condiciones.forEach(function (condicion) {
        const nombreCondicion =
          typeof condicion === "string"
            ? condicion
            : condicion.nombre;

        const checkboxExistente = Array.from(
          document.querySelectorAll(".condicion-salud")
        ).find(function (checkbox) {
          return checkbox.value === nombreCondicion;
        });

        if (checkboxExistente) {
          checkboxExistente.checked = true;
        } else if (nombreCondicion) {
          checkOtraCondicion.checked = true;
          detalleOtraCondicion.value = nombreCondicion;
          contenedorOtraCondicion.classList.remove("d-none");
        }
      });
    } catch (error) {
      console.error("Error al cargar el perfil:", error);

      if (
        error.message === "Sesión no válida." ||
        error.message.includes("credenciales")
      ) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("usuarioId");
        localStorage.removeItem("nombreUsuario");

        window.location.href = "login.html";
        return;
      }

      alert("No fue posible cargar el perfil.");
    }
  }

  cargarPerfil();

  checkOtraCondicion.addEventListener("change", function () {
    if (this.checked) {
      contenedorOtraCondicion.classList.remove("d-none");
    } else {
      contenedorOtraCondicion.classList.add("d-none");
      detalleOtraCondicion.value = "";
      validators.mostrarError("errorOtraCondicion", "");
    }
  });

  formulario.addEventListener("submit", async function (event) {
    event.preventDefault();
    validators.limpiarErrores();

    const nombre = document.getElementById("nombre").value;
    const edad = document.getElementById("edad").value;
    const peso = document.getElementById("peso").value;
    const estatura = document.getElementById("estatura").value;
    const actividad = document.getElementById("actividad").value;
    const objetivo = document.getElementById("objetivo").value;
    const sueno = document.getElementById("sueno").value;
    const habitoActividad =
      document.getElementById("habitoActividad").value;
    const comentarios =
      document.getElementById("comentarios").value;

    let formularioValido = true;

    if (validators.esCampoVacio(nombre)) {
      validators.mostrarError(
        "errorNombre",
        "El campo Nombre completo es obligatorio."
      );
      formularioValido = false;
    } else if (!validators.esTextoValido(nombre, 3, 60)) {
      validators.mostrarError(
        "errorNombre",
        "Ingrese un nombre válido."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(edad)) {
      validators.mostrarError(
        "errorEdad",
        "El campo Edad es obligatorio."
      );
      formularioValido = false;
    } else if (!validators.esNumeroEnRango(edad, 1, 120)) {
      validators.mostrarError(
        "errorEdad",
        "El campo Edad debe estar entre 1 y 120."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(peso)) {
      validators.mostrarError(
        "errorPeso",
        "El campo Peso es obligatorio."
      );
      formularioValido = false;
    } else if (!validators.esNumeroEnRango(peso, 3, 300)) {
      validators.mostrarError(
        "errorPeso",
        "El campo Peso debe estar entre 3 y 300."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(estatura)) {
      validators.mostrarError(
        "errorEstatura",
        "El campo Estatura es obligatorio."
      );
      formularioValido = false;
    } else if (
      !validators.esNumeroEnRango(estatura, 0.5, 2.5)
    ) {
      validators.mostrarError(
        "errorEstatura",
        "La estatura debe estar entre 0.50 y 2.50 metros."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(actividad)) {
      validators.mostrarError(
        "errorActividad",
        "El campo Nivel de actividad es obligatorio."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(objetivo)) {
      validators.mostrarError(
        "errorObjetivo",
        "El campo Objetivo de bienestar es obligatorio."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(sueno)) {
      validators.mostrarError(
        "errorSueno",
        "El campo Horas de sueño es obligatorio."
      );
      formularioValido = false;
    } else if (!validators.esNumeroEnRango(sueno, 1, 24)) {
      validators.mostrarError(
        "errorSueno",
        "Las horas de sueño deben estar entre 1 y 24."
      );
      formularioValido = false;
    }

    if (validators.esCampoVacio(habitoActividad)) {
      validators.mostrarError(
        "errorHabitoActividad",
        "El campo Actividad física actual es obligatorio."
      );
      formularioValido = false;
    } else if (
      habitoActividad.trim().length < 3 ||
      habitoActividad.trim().length > 80
    ) {
      validators.mostrarError(
        "errorHabitoActividad",
        "Ingrese una actividad física válida."
      );
      formularioValido = false;
    }

    if (checkOtraCondicion.checked) {
      if (
        validators.esCampoVacio(detalleOtraCondicion.value)
      ) {
        validators.mostrarError(
          "errorOtraCondicion",
          "Debe especificar la otra condición."
        );
        formularioValido = false;
      } else if (
        !validators.esTextoValido(
          detalleOtraCondicion.value,
          3,
          60
        )
      ) {
        validators.mostrarError(
          "errorOtraCondicion",
          "Ingrese una condición válida."
        );
        formularioValido = false;
      }
    }

    if (!formularioValido) {
      return;
    }

    const condicionesSeleccionadas = [];

    document
      .querySelectorAll(".condicion-salud:checked")
      .forEach(function (checkbox) {
        condicionesSeleccionadas.push(checkbox.value);
      });

    if (checkOtraCondicion.checked) {
      condicionesSeleccionadas.push(
        detalleOtraCondicion.value.trim()
      );
    }

    const perfilUsuario = {
      nombre: nombre.trim(),
      edad: Number(edad),
      peso: Number(peso),
      estatura: Number(estatura),
      condiciones: condicionesSeleccionadas,
      actividad: actividad,
      objetivo: objetivo,
      sueno: Number(sueno),
      habitoActividad: habitoActividad.trim(),
      comentarios: comentarios.trim()
    };

    try {
      await apiService.actualizarUsuario(
        usuarioId,
        perfilUsuario
      );

      notificaciones.exito("Perfil guardado correctamente.");

      /*
       * No se reinicia el formulario porque esta pantalla también
       * se utiliza para consultar y editar el perfil existente.
       */
      await cargarPerfil();
    } catch (error) {
      notificaciones.error(
        error.message || "No fue posible guardar el perfil."
      );
    }
  });
});