"use strict";
// Clase principal Estudiante
class Estudiante {
    nombre;
    nota;
    carrera;
    constructor(nombre, nota, carrera) {
        this.nombre = nombre;
        this.nota = nota;
        this.carrera = carrera;
    }
}
// Clase hija que hereda de Estudiante
class EstudianteBeca extends Estudiante {
    tipoBeca;
    constructor(nombre, nota, carrera, tipoBeca) {
        // Llama al constructor de Estudiante
        super(nombre, nota, carrera);
        this.tipoBeca = tipoBeca;
    }
}
// Lista inicial de estudiantes
let estudiantes = [
    new Estudiante("Valeria", 90, "Ingenieria en Sistemas"),
    new Estudiante("Carlos", 85, "Administracion"),
    new EstudianteBeca("Maria", 95, "Ingenieria en Sistemas", "Beca Academica")
];
// Agregar estudiante a la lista
function agregarEstudiante(nombre, nota, carrera, lista) {
    let nuevoEstudiante = new Estudiante(nombre, nota, carrera);
    lista.push(nuevoEstudiante);
    return lista;
}
// Buscar estudiante por nombre
function buscarEstudiante(nombre, lista) {
    for (let estudiante of lista) {
        if (estudiante.nombre === nombre) {
            return estudiante;
        }
    }
    return undefined;
}
// Calcular promedio de notas
function calcularPromedio(lista) {
    let suma = 0;
    for (let estudiante of lista) {
        suma = suma + estudiante.nota;
    }
    return suma / lista.length;
}
// Recorrer lista de estudiantes
function mostrarEstudiantes(lista) {
    for (let estudiante of lista) {
        console.log("Nombre:", estudiante.nombre);
        console.log("Nota:", estudiante.nota);
        console.log("Carrera:", estudiante.carrera);
        console.log("-------------------");
    }
}
// Ejemplo de uso
// Agregar estudiante nuevo
agregarEstudiante("Ana", 88, "Contabilidad", estudiantes);
// Mostrar todos los estudiantes
mostrarEstudiantes(estudiantes);
// Buscar estudiante
let resultado = buscarEstudiante("Carlos", estudiantes);
console.log("Estudiante encontrado:", resultado);
// Calcular promedio
let promedio = calcularPromedio(estudiantes);
console.log("Promedio general:", promedio);
