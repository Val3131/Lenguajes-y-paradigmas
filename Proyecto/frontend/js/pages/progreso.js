document.addEventListener("DOMContentLoaded", async function () {
  const formulario = document.getElementById("formProgreso");

  const token = localStorage.getItem("accessToken");
  const usuarioId = localStorage.getItem("usuarioId");

  if (!token || !usuarioId) {
    window.location.href = "login.html";
    return;
  }

  if (!formulario) {
    return;
  }

  const resumenPeso = document.getElementById("resumenPeso");
  const resumenSueno = document.getElementById("resumenSueno");
  const resumenActividad = document.getElementById(
    "resumenActividad"
  );

  const canvasPeso = document.getElementById("graficaPeso");
  const canvasSueno = document.getElementById("graficaSueno");

  let historialProgreso = [];
  let graficaPeso = null;
  let graficaSueno = null;

  function limpiarErroresProgreso() {
    validators.mostrarError("errorPesoActual", "");
    validators.mostrarError("errorSuenoActual", "");
    validators.mostrarError("errorActividadRealizada", "");
  }

  function actualizarResumen(progreso) {
    resumenPeso.textContent =
      `${progreso.peso_actual} kg`;

    resumenSueno.textContent =
      `${progreso.sueno_actual} horas`;

    resumenActividad.textContent =
      progreso.actividad_realizada;
  }

  function obtenerEtiquetas() {
    return historialProgreso.map(function (progreso, index) {
      if (progreso.fecha) {
        const fecha = new Date(progreso.fecha);

        return fecha.toLocaleDateString("es-CR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric"
        });
      }

      return `Registro ${index + 1}`;
    });
  }

  function renderizarGraficaPeso() {
    if (!canvasPeso) {
      return;
    }

    const etiquetas = obtenerEtiquetas();

    const pesos = historialProgreso.map(function (progreso) {
      return progreso.peso_actual;
    });

    if (graficaPeso) {
      graficaPeso.destroy();
    }

    graficaPeso = new Chart(canvasPeso, {
      type: "line",
      data: {
        labels: etiquetas,
        datasets: [
          {
            label: "Peso (kg)",
            data: pesos,
            borderColor: "#2c6170",
            backgroundColor: "rgba(44, 97, 112, 0.2)",
            borderWidth: 3,
            tension: 0.3,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true
          }
        },
        scales: {
          y: {
            beginAtZero: false
          }
        }
      }
    });
  }

  function renderizarGraficaSueno() {
    if (!canvasSueno) {
      return;
    }

    const etiquetas = obtenerEtiquetas();

    const horasSueno = historialProgreso.map(
      function (progreso) {
        return progreso.sueno_actual;
      }
    );

    if (graficaSueno) {
      graficaSueno.destroy();
    }

    graficaSueno = new Chart(canvasSueno, {
      type: "bar",
      data: {
        labels: etiquetas,
        datasets: [
          {
            label: "Horas de sueño",
            data: horasSueno,
            backgroundColor: "rgba(122, 166, 177, 0.7)",
            borderColor: "#7aa6b1",
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 24
          }
        }
      }
    });
  }

  function renderizarGraficas() {
    if (historialProgreso.length === 0) {
      return;
    }

    renderizarGraficaPeso();
    renderizarGraficaSueno();
  }

  async function cargarProgresos() {
    try {
      historialProgreso =
        await apiService.obtenerProgresos(usuarioId);

      if (historialProgreso.length === 0) {
        resumenPeso.textContent = "Sin registro";
        resumenSueno.textContent = "Sin registro";
        resumenActividad.textContent = "Sin registro";
        return;
      }

      const ultimoProgreso =
        historialProgreso[historialProgreso.length - 1];

      actualizarResumen(ultimoProgreso);
      renderizarGraficas();

    } catch (error) {
      console.error("Error al cargar progresos:", error);
      alert("No fue posible cargar los progresos.");
    }
  }

  await cargarProgresos();

  formulario.addEventListener(
    "submit",
    async function (event) {
      event.preventDefault();
      limpiarErroresProgreso();

      const pesoActual =
        document.getElementById("pesoActual").value;

      const suenoActual =
        document.getElementById("suenoActual").value;

      const actividadRealizada =
        document.getElementById(
          "actividadRealizada"
        ).value;

      let formularioValido = true;

      if (validators.esCampoVacio(pesoActual)) {
        validators.mostrarError(
          "errorPesoActual",
          "El campo Peso actual es obligatorio."
        );
        formularioValido = false;

      } else if (
        !validators.esNumeroEnRango(
          pesoActual,
          3,
          300
        )
      ) {
        validators.mostrarError(
          "errorPesoActual",
          "El peso debe estar entre 3 y 300."
        );
        formularioValido = false;
      }

      if (validators.esCampoVacio(suenoActual)) {
        validators.mostrarError(
          "errorSuenoActual",
          "El campo Horas de sueño es obligatorio."
        );
        formularioValido = false;

      } else if (
        !validators.esNumeroEnRango(
          suenoActual,
          1,
          24
        )
      ) {
        validators.mostrarError(
          "errorSuenoActual",
          "Las horas de sueño deben estar entre 1 y 24."
        );
        formularioValido = false;
      }

      if (
        validators.esCampoVacio(
          actividadRealizada
        )
      ) {
        validators.mostrarError(
          "errorActividadRealizada",
          "El campo Actividad realizada es obligatorio."
        );
        formularioValido = false;

      } else if (
        actividadRealizada.trim().length < 3 ||
        actividadRealizada.trim().length > 100
      ) {
        validators.mostrarError(
          "errorActividadRealizada",
          "Ingrese una actividad válida."
        );
        formularioValido = false;
      }

      if (!formularioValido) {
        return;
      }

      const progresoUsuario = {
        pesoActual: Number(pesoActual),
        suenoActual: Number(suenoActual),
        actividadRealizada:
          actividadRealizada.trim()
      };

      try {
        await apiService.crearProgreso(
          usuarioId,
          progresoUsuario
        );

        await cargarProgresos();

        notificaciones.exito("Progreso guardado correctamente.");
        formulario.reset();

      } catch (error) {
        console.error(
          "Error al guardar el progreso:",
          error
        );

        alert(
          error.message ||
          "No fue posible guardar el progreso."
        );
      }
    }
  );
});