% Lista inicial de estudiantes
estudiantes([
    estudiante("Valeria", 90, "Ingenieria en Sistemas"),
    estudiante("Carlos", 85, "Administracion"),
    estudiante("Maria", 95, "Ingenieria en Sistemas")
]).

% Agregar estudiante a una lista
agregar_estudiante(Nombre, Nota, Carrera, Lista, [estudiante(Nombre, Nota, Carrera) | Lista]).

% Buscar estudiante por nombre
buscar_estudiante(Nombre, [estudiante(Nombre, Nota, Carrera) | _], estudiante(Nombre, Nota, Carrera)).

buscar_estudiante(Nombre, [_ | Resto], Resultado) :-
    buscar_estudiante(Nombre, Resto, Resultado).

% Calcular promedio
sumar_notas([], 0).

sumar_notas([estudiante(_, Nota, _) | Resto], Suma) :-
    sumar_notas(Resto, SumaResto),
    Suma is Nota + SumaResto.

contar_estudiantes([], 0).

contar_estudiantes([_ | Resto], Total) :-
    contar_estudiantes(Resto, TotalResto),
    Total is TotalResto + 1.

calcular_promedio(Lista, Promedio) :-
    sumar_notas(Lista, Suma),
    contar_estudiantes(Lista, Total),
    Promedio is Suma / Total.

% Recorrer lista de estudiantes
mostrar_estudiantes([]).

mostrar_estudiantes([estudiante(Nombre, Nota, Carrera) | Resto]) :-
    write("Nombre: "), write(Nombre), nl,
    write("Nota: "), write(Nota), nl,
    write("Carrera: "), write(Carrera), nl,
    write("-------------------"), nl,
    mostrar_estudiantes(Resto).

% Ejemplo de uso
ejecutar :-
    estudiantes(Lista),
    agregar_estudiante("Ana", 88, "Contabilidad", Lista, NuevaLista),
    mostrar_estudiantes(NuevaLista),
    buscar_estudiante("Carlos", NuevaLista, Resultado),
    write("Estudiante encontrado: "), write(Resultado), nl,
    calcular_promedio(NuevaLista, Promedio),
    write("Promedio general: "), write(Promedio).