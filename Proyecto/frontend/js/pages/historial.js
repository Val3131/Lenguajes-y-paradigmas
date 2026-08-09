document.addEventListener("DOMContentLoaded", async function () {
  try {
    const usuarioId = localStorage.getItem("usuarioId");

    if (!usuarioId) {
      alert("Primero debe registrar su perfil.");
      return;
    }

    const datos = await apiService.obtenerHistorial(usuarioId);

    const historialAnterior = document.getElementById("historialAnterior");
    const historialActual = document.getElementById("historialActual");

    if (datos.mensaje) {
      const mensajeHtml = `<p class="mb-0">${datos.mensaje}</p>`;
      if (!datos.semanaActual) {
        historialAnterior.innerHTML = `<h3 class="titulo-tarjeta">Semana anterior</h3>${mensajeHtml}`;
        historialActual.innerHTML = `<h3 class="titulo-tarjeta">Semana actual</h3>`;
        return;
      }
      historialAnterior.innerHTML = `<h3 class="titulo-tarjeta">Semana anterior</h3>${mensajeHtml}`;
    } else if (datos.semanaAnterior) {
      historialAnterior.innerHTML = `
        <h3 class="titulo-tarjeta">Semana anterior (${datos.semanaAnterior.fecha})</h3>
        <p>Alimentación: ${datos.semanaAnterior.alimentacion}</p>
        <p>Ejercicio: ${datos.semanaAnterior.ejercicio}</p>
        <p>Descanso: ${datos.semanaAnterior.descanso}</p>
        <p><em>${datos.semanaAnterior.consejoIa}</em></p>
      `;
    }

    if (datos.semanaActual) {
      historialActual.innerHTML = `
        <h3 class="titulo-tarjeta">Semana actual (${datos.semanaActual.fecha})</h3>
        <p>Alimentación: ${datos.semanaActual.alimentacion}</p>
        <p>Ejercicio: ${datos.semanaActual.ejercicio}</p>
        <p>Descanso: ${datos.semanaActual.descanso}</p>
        <p><em>${datos.semanaActual.consejoIa}</em></p>
      `;
    }
  } catch (error) {
    console.error("Error al cargar historial:", error);
  }
});
