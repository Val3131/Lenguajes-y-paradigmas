const apiService = {
  obtenerRecomendaciones: async function () {
    const respuesta = await fetch("../data/siRecomendaciones.json");
    return await respuesta.json();
  },

  obtenerProgreso: async function () {
    const respuesta = await fetch("../data/siProgreso.json");
    return await respuesta.json();
  },

  obtenerHistorial: async function () {
    const respuesta = await fetch("../data/siHistorial.json");
    return await respuesta.json();
  },

  obtenerPerfil: async function () {
    const respuesta = await fetch("../data/siPerfil.json");
    return await respuesta.json();
  }
};