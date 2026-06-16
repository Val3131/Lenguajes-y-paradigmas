// Clase principal Estudiante
class Estudiante {

    nombre: string;
    nota: number;
    carrera: string;


    constructor(nombre: string, nota: number, carrera: string) {
        this.nombre = nombre;
        this.nota = nota;
        this.carrera = carrera;
    }
}


// Clase hija que hereda de Estudiante
class EstudianteBeca extends Estudiante {

    tipoBeca: string;


    constructor(
        nombre: string,
        nota: number,
        carrera: string,
        tipoBeca: string
    ) {

        // Llama al constructor de Estudiante
        super(nombre, nota, carrera);

        this.tipoBeca = tipoBeca;
    }
}


// Lista inicial de estudiantes
let estudiantes: Estudiante[] = [

    new Estudiante(
        "Valeria",
        90,
        "Ingenieria en Sistemas"
    ),

    new Estudiante(
        "Carlos",
        85,
        "Administracion"
    ),

    new EstudianteBeca(
        "Maria",
        95,
        "Ingenieria en Sistemas",
        "Beca Academica"
    )

];


// Agregar estudiante a la lista
function agregarEstudiante(
    nombre: string,
    nota: number,
    carrera: string,
    lista: Estudiante[]
): Estudiante[] {

    let nuevoEstudiante =
        new Estudiante(
            nombre,
            nota,
            carrera
        );


    lista.push(nuevoEstudiante);

    return lista;
}


// Buscar estudiante por nombre
function buscarEstudiante(
    nombre: string,
    lista: Estudiante[]
): Estudiante | undefined {


    for (let estudiante of lista) {


        if (estudiante.nombre === nombre) {

            return estudiante;

        }
    }


    return undefined;
}


// Calcular promedio de notas
function calcularPromedio(
    lista: Estudiante[]
): number {


    let suma = 0;


    for (let estudiante of lista) {

        suma = suma + estudiante.nota;

    }


    return suma / lista.length;
}


// Recorrer lista de estudiantes
function mostrarEstudiantes(
    lista: Estudiante[]
): void {


    for (let estudiante of lista) {

        console.log(
            "Nombre:",
            estudiante.nombre
        );

        console.log(
            "Nota:",
            estudiante.nota
        );

        console.log(
            "Carrera:",
            estudiante.carrera
        );

        console.log("-------------------");

    }

}


// Ejemplo de uso

// Agregar estudiante nuevo
agregarEstudiante(
    "Ana",
    88,
    "Contabilidad",
    estudiantes
);


// Mostrar todos los estudiantes
mostrarEstudiantes(estudiantes);


// Buscar estudiante
let resultado =
    buscarEstudiante(
        "Carlos",
        estudiantes
    );


console.log(
    "Estudiante encontrado:",
    resultado
);


// Calcular promedio
let promedio =
    calcularPromedio(estudiantes);


console.log(
    "Promedio general:",
    promedio
);