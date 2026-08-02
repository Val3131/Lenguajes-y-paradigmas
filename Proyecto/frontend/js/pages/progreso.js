document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("formProgreso");

  if (!formulario) {
    return;
  }

  const resumenPeso = document.getElementById("resumenPeso");
  const resumenSueno = document.getElementById("resumenSueno");
  const resumenActividad = document.getElementById("resumenActividad");

  const canvasPeso = document.getElementById("graficaPeso");
  const canvasSueno = document.getElementById("graficaSueno");

  let historialProgreso = JSON.parse(localStorage.getItem("historialProgreso")) || [];
  let graficaPeso = null;
  let graficaSueno = null;

  function limpiarErroresProgreso() {
    validators.mostrarError("errorPesoActual", "");
    validators.mostrarError("errorSuenoActual", "");
    validators.mostrarError("errorActividadRealizada", "");
  }

  function actualizarResumen(datos) {
    resumenPeso.textContent = datos.pesoActual + " kg";
    resumenSueno.textContent = datos.suenoActual + " horas";
    resumenActividad.textContent = datos.actividadRealizada;
  }

  function obtenerEtiquetas() {
    return historialProgreso.map(function (_, index) {
      return "Registro " + (index + 1);
    });
  }

  function renderizarGraficaPeso() {
    const etiquetas = obtenerEtiquetas();
    const pesos = historialProgreso.map(function (item) {
      return item.pesoActual;
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
    const etiquetas = obtenerEtiquetas();
    const suenos = historialProgreso.map(function (item) {
      return item.suenoActual;
    });

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
            data: suenos,
            backgroundColor: "rgba(122, 166, 177, 0.7)",
            borderColor: "#7aa6b1",
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
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

  const progresoGuardado = localStorage.getItem("progresoActual");
  if (progresoGuardado) {
    const datosGuardados = JSON.parse(progresoGuardado);
    actualizarResumen(datosGuardados);
  }

  renderizarGraficas();

  formulario.addEventListener("submit", function (event) {
    event.preventDefault();
    limpiarErroresProgreso();

    const pesoActual = document.getElementById("pesoActual").value;
    const suenoActual = document.getElementById("suenoActual").value;
    const actividadRealizada = document.getElementById("actividadRealizada").value;

    let formularioValido = true;

    if (validators.esCampoVacio(pesoActual)) {
      validators.mostrarError("errorPesoActual", "El campo Peso actual es obligatorio.");
      formularioValido = false;
    } else if (!validators.esNumeroEnRango(pesoActual, 3, 300)) {
      validators.mostrarError("errorPesoActual", "El peso debe estar entre 3 y 300.");
      formularioValido = false;
    }

    if (validators.esCampoVacio(suenoActual)) {
      validators.mostrarError("errorSuenoActual", "El campo Horas de sueño es obligatorio.");
      formularioValido = false;
    } else if (!validators.esNumeroEnRango(suenoActual, 1, 24)) {
      validators.mostrarError("errorSuenoActual", "Las horas de sueño deben estar entre 1 y 24.");
      formularioValido = false;
    }

    if (validators.esCampoVacio(actividadRealizada)) {
      validators.mostrarError("errorActividadRealizada", "El campo Actividad realizada es obligatorio.");
      formularioValido = false;
    } else if (actividadRealizada.trim().length < 3 || actividadRealizada.trim().length > 80) {
      validators.mostrarError("errorActividadRealizada", "Ingrese una actividad válida.");
      formularioValido = false;
    }

    if (!formularioValido) {
      return;
    }

    const progresoUsuario = {
      pesoActual: Number(pesoActual),
      suenoActual: Number(suenoActual),
      actividadRealizada: actividadRealizada.trim()
    };

    localStorage.setItem("progresoActual", JSON.stringify(progresoUsuario));

    historialProgreso.push(progresoUsuario);
    localStorage.setItem("historialProgreso", JSON.stringify(historialProgreso));

    actualizarResumen(progresoUsuario);
    renderizarGraficas();

    alert("Progreso guardado correctamente.");
    formulario.reset();
  });
});