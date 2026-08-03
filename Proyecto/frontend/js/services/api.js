const API_URL = "http://127.0.0.1:8000";

const apiService = {
  crearUsuario: async function (datos) {
    const respuesta = await fetch(`${API_URL}/usuarios`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    });

    if (!respuesta.ok) {
      throw new Error("No se pudo crear el usuario.");
    }

    return await respuesta.json();
  },

  actualizarUsuario: async function (usuarioId, datos) {
    const respuesta = await fetch(`${API_URL}/usuarios/${usuarioId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    });

    if (!respuesta.ok) {
      throw new Error("No se pudo actualizar el usuario.");
    }

    return await respuesta.json();
  },

  obtenerUsuario: async function (usuarioId) {
    const respuesta = await fetch(`${API_URL}/usuarios/${usuarioId}`);

    if (!respuesta.ok) {
      throw new Error("No se pudo obtener el usuario.");
    }

    return await respuesta.json();
  },

  crearProgreso: async function (usuarioId, datos) {
    const respuesta = await fetch(
      `${API_URL}/usuarios/${usuarioId}/progresos`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(datos)
      }
    );

    if (!respuesta.ok) {
      throw new Error("No se pudo guardar el progreso.");
    }

    return await respuesta.json();
  },

  obtenerProgresos: async function (usuarioId) {
    const respuesta = await fetch(
      `${API_URL}/usuarios/${usuarioId}/progresos`
    );

    if (!respuesta.ok) {
      throw new Error("No se pudieron obtener los progresos.");
    }

    return await respuesta.json();
  },

  obtenerRecomendaciones: async function (usuarioId) {
    const respuesta = await fetch(
      `${API_URL}/usuarios/${usuarioId}/recomendaciones`
    );

    if (!respuesta.ok) {
      throw new Error("No se pudieron obtener las recomendaciones.");
    }

    return await respuesta.json();
  },

  obtenerHistorial: async function (usuarioId) {
    const respuesta = await fetch(
      `${API_URL}/usuarios/${usuarioId}/historial`
    );

    if (!respuesta.ok) {
      throw new Error("No se pudo obtener el historial.");
    }

    return await respuesta.json();
  },
    registrarUsuario: async function (datos) {
    const respuesta = await fetch(`${API_URL}/auth/registro`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    });

    const contenido = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(contenido.detail || "No se pudo registrar el usuario.");
    }

    return contenido;
  },

  iniciarSesion: async function (datos) {
    const respuesta = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    });

    const contenido = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(contenido.detail || "No se pudo iniciar sesión.");
    }

    return contenido;
  },

  obtenerUsuarioActual: async function () {
    const token = localStorage.getItem("accessToken");

    const respuesta = await fetch(`${API_URL}/auth/me`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const contenido = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(contenido.detail || "Sesión no válida.");
    }

    return contenido;
  },
};