const validators = {
  esTextoValido: function (valor, minimo = 3, maximo = 60) {
    const texto = valor.trim();
    const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s-]+$/;
    return texto.length >= minimo && texto.length <= maximo && regex.test(texto);
  },

  esNumeroEnRango: function (valor, minimo, maximo) {
    const numero = Number(valor);
    return !isNaN(numero) && numero >= minimo && numero <= maximo;
  },

  esCampoVacio: function (valor) {
    return valor.trim() === "";
  },

  limpiarErrores: function () {
    const errores = document.querySelectorAll(".text-danger");
    errores.forEach(function (error) {
      error.textContent = "";
    });
  },

  mostrarError: function (idElemento, mensaje) {
    const elemento = document.getElementById(idElemento);
    if (elemento) {
      elemento.textContent = mensaje;
    }
  }
};