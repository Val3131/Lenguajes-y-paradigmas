document.addEventListener("DOMContentLoaded", async function () {
  try {
    const datos = await apiService.obtenerHistorial();

    const historialAnterior = document.getElementById("historialAnterior");
    const historialActual = document.getElementById("historialActual");

    historialAnterior.innerHTML = `
      <h3 class="titulo-tarjeta">Semana anterior</h3>
      <p>Alimentación: ${datos.semanaAnterior.alimentacion}</p>
      <p>Ejercicio: ${datos.semanaAnterior.ejercicio}</p>
      <p>Descanso: ${datos.semanaAnterior.descanso}</p>
    `;

    historialActual.innerHTML = `
      <h3 class="titulo-tarjeta">Semana actual</h3>
      <p>Alimentación: ${datos.semanaActual.alimentacion}</p>
      <p>Ejercicio: ${datos.semanaActual.ejercicio}</p>
      <p>Descanso: ${datos.semanaActual.descanso}</p>
    `;
  } catch (error) {
    console.error("Error al cargar historial:", error);
  }
});