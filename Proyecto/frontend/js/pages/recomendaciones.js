document.addEventListener("DOMContentLoaded", async function () {
  try {
    const usuarioId = localStorage.getItem("usuarioId");

    if (!usuarioId) {
      alert("Primero debe registrar su perfil.");
      return;
    }

    const datos = await apiService.obtenerRecomendaciones(usuarioId);

    const listaAlimentacion = document.getElementById("listaAlimentacion");
    const listaEjercicio = document.getElementById("listaEjercicio");
    const listaDescanso = document.getElementById("listaDescanso");

    listaAlimentacion.innerHTML = "";
    listaEjercicio.innerHTML = "";
    listaDescanso.innerHTML = "";

    datos.alimentacion.forEach(function(item) {
      listaAlimentacion.innerHTML += `<li>${item}</li>`;
    });

    datos.ejercicio.forEach(function(item) {
      listaEjercicio.innerHTML += `<li>${item}</li>`;
    });

    datos.descanso.forEach(function(item) {
      listaDescanso.innerHTML += `<li>${item}</li>`;
    });
  } catch (error) {
    console.error("Error al cargar recomendaciones:", error);
  }
});