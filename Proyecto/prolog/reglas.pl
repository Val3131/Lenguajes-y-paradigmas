%% ============================================================
%% REGLAS.PL
%% Motor de inferencia: reglas de alimentacion, ejercicio y
%% descanso. Maneja multiples condiciones de salud simultaneas
%% (interseccion de restricciones) y combina alimentacion +
%% ejercicio + descanso en un plan integral por objetivo.
%% Requiere: hechos.pl cargado previamente (ver main.pl)
%% ============================================================

% ============================================================
% A. REGLAS DE ALIMENTACION
% ============================================================

% restringe(Condicion, PropiedadNutricional).
% Propiedades que una condicion de salud prohibe o desaconseja.
restringe(diabetes_tipo2,       azucar_alta).
restringe(diabetes_tipo2,       carbohidrato_refinado).
restringe(diabetes_tipo2,       indice_glucemico_alto).
restringe(hipertension,         sodio_alto).
restringe(obesidad,             grasa_alta).
restringe(obesidad,             azucar_alta).
restringe(obesidad,             carbohidrato_refinado).
restringe(intolerancia_lactosa, lactosa).
restringe(celiaquia,            gluten).
% hipotiroidismo y anemia no restringen alimentos directamente,
% mas bien exigen reforzar ciertos nutrientes (ver recomienda/2).

% recomienda(Condicion, PropiedadNutricional).
% Propiedades nutricionales deseables para cada condicion.
recomienda(diabetes_tipo2,       fibra_alta).
recomienda(diabetes_tipo2,       bajo_indice_glucemico).
recomienda(hipertension,         potasio_alto).
recomienda(hipertension,         sodio_bajo).
recomienda(hipotiroidismo,       yodo_alto).
recomienda(obesidad,             fibra_alta).
recomienda(obesidad,             proteina_alta).
recomienda(anemia,               hierro_alto).
recomienda(anemia,               hierro_medio).
recomienda(intolerancia_lactosa, sin_lactosa).
recomienda(celiaquia,            sin_gluten).

% Un alimento es apto para UNA condicion si ninguna de sus
% propiedades esta restringida por esa condicion.
alimento_apto_condicion(Alimento, Condicion) :-
    alimento(Alimento, _Grupo, Propiedades),
    \+ ( member(P, Propiedades), restringe(Condicion, P) ).

% Un alimento es apto para el usuario si lo es para TODAS sus
% condiciones a la vez (interseccion de restricciones = manejo
% de multiples condiciones simultaneas).
alimento_apto_usuario(Alimento, Condiciones) :-
    forall(member(C, Condiciones), alimento_apto_condicion(Alimento, C)).

% Alimento recomendado con condiciones: apto para todas y ademas
% cumple al menos una propiedad recomendada por alguna condicion.
%
% IMPORTANTE (orden de las metas): alimento/3 debe ir ANTES que
% alimento_apto_usuario/2. alimento_apto_usuario usa forall/2, que
% internamente usa negacion (\+) - si Alimento todavia es una
% variable libre en ese punto, la negacion "deshace" cualquier
% ligadura que intente probar y el chequeo de aptitud se vuelve
% vacuo (siempre verdadero). Ligando Alimento primero con alimento/3
% nos aseguramos de preguntar "¿ESTE alimento es apto?" en vez de
% "¿existe algun alimento apto?".
alimento_recomendado(Alimento, Condiciones) :-
    Condiciones \= [],
    alimento(Alimento, _Grupo, Propiedades),
    alimento_apto_usuario(Alimento, Condiciones),
    member(C, Condiciones),
    recomienda(C, P),
    member(P, Propiedades).

% Caso general (usuario sin condiciones registradas): se
% recomienda cualquier alimento con perfil saludable base.
alimento_recomendado(Alimento, []) :-
    alimento(Alimento, _Grupo, Propiedades),
    ( member(fibra_alta, Propiedades)
    ; member(proteina_alta, Propiedades)
    ; member(grasa_saludable, Propiedades)
    ).

% Alimento restringido para el usuario: viola al menos una
% condicion de la lista.
alimento_restringido(Alimento, Condiciones) :-
    alimento(Alimento, _Grupo, Propiedades),
    member(C, Condiciones),
    member(P, Propiedades),
    restringe(C, P).

% Listas ordenadas y sin duplicados (interfaz de consulta).
alimentos_recomendados_usuario(Condiciones, ListaOrdenada) :-
    findall(A, alimento_recomendado(A, Condiciones), Lista),
    sort(Lista, ListaOrdenada).

alimentos_restringidos_usuario(Condiciones, ListaOrdenada) :-
    findall(A, alimento_restringido(A, Condiciones), Lista),
    sort(Lista, ListaOrdenada).


% ============================================================
% B. REGLAS DE ACTIVIDAD FISICA / EJERCICIO
% ============================================================

% contraindica(Condicion, TipoOEsfuerzo).
% Una condicion puede contraindicar un TIPO de actividad o un
% NIVEL DE ESFUERZO especifico.
contraindica(hipertension, alta_intensidad).
contraindica(hipertension, alto).
contraindica(obesidad,     alta_intensidad).   % debe iniciar con bajo impacto
contraindica(anemia,       alto).              % evitar esfuerzo maximo si hay anemia

% Actividad segura para UNA condicion: ni su tipo ni su esfuerzo
% estan contraindicados por esa condicion.
actividad_segura_condicion(Actividad, Condicion) :-
    actividad(Actividad, Tipo, Esfuerzo, _Beneficios),
    \+ contraindica(Condicion, Tipo),
    \+ contraindica(Condicion, Esfuerzo).

% Actividad segura para TODAS las condiciones del usuario
% (manejo de multiples condiciones simultaneas).
actividad_segura_usuario(Actividad, Condiciones) :-
    Condiciones \= [],
    forall(member(C, Condiciones), actividad_segura_condicion(Actividad, C)).
actividad_segura_usuario(Actividad, []) :-
    actividad(Actividad, _, _, _).

% esfuerzo_maximo(NivelActividadUsuario, EsfuerzoMaximoPermitido)
% Un usuario sedentario debe iniciar con esfuerzo bajo, etc.
esfuerzo_maximo(sedentario,           bajo).
esfuerzo_maximo(levemente_activo,     moderado).
esfuerzo_maximo(moderadamente_activo, alto).
esfuerzo_maximo(muy_activo,           alto).

nivel_esfuerzo_orden(bajo,     1).
nivel_esfuerzo_orden(moderado, 2).
nivel_esfuerzo_orden(alto,     3).

actividad_apta_nivel(Actividad, NivelUsuario) :-
    actividad(Actividad, _Tipo, Esfuerzo, _Beneficios),
    esfuerzo_maximo(NivelUsuario, Max),
    nivel_esfuerzo_orden(Esfuerzo, OrdenEsfuerzo),
    nivel_esfuerzo_orden(Max, OrdenMax),
    OrdenEsfuerzo =< OrdenMax.

% Actividad recomendada final: segura para todas las condiciones
% y adecuada al nivel de actividad actual del usuario.
%
% Mismo motivo que en alimento_recomendado/2: actividad_apta_nivel/2
% va primero porque liga Actividad (via actividad/4); recien con
% Actividad ya concreta tiene sentido preguntar si ES segura con
% actividad_segura_usuario/2 (que usa forall/negacion por dentro).
actividad_recomendada(Actividad, Condiciones, NivelUsuario) :-
    actividad_apta_nivel(Actividad, NivelUsuario),
    actividad_segura_usuario(Actividad, Condiciones).

rutina_recomendada_usuario(Condiciones, NivelUsuario, ListaOrdenada) :-
    findall(A, actividad_recomendada(A, Condiciones, NivelUsuario), Lista),
    sort(Lista, ListaOrdenada).

% objetivo_beneficio(Objetivo, Beneficio) empareja objetivos de
% bienestar con los beneficios que ofrecen las actividades.
objetivo_beneficio(perdida_peso,         control_peso).
objetivo_beneficio(perdida_peso,         quema_calorica).
objetivo_beneficio(ganancia_muscular,    ganancia_muscular).
objetivo_beneficio(ganancia_muscular,    fuerza).
objetivo_beneficio(mantenimiento,        cardiovascular).
objetivo_beneficio(mejora_cardiovascular,cardiovascular).
objetivo_beneficio(mejora_cardiovascular,resistencia).
objetivo_beneficio(reduccion_estres,     reduccion_estres).
objetivo_beneficio(reduccion_estres,     flexibilidad).

actividad_para_objetivo(Actividad, Objetivo) :-
    actividad(Actividad, _Tipo, _Esfuerzo, Beneficios),
    objetivo_beneficio(Objetivo, B),
    member(B, Beneficios).

% Rutina ajustada a condiciones + nivel + objetivo. Si no hay
% actividades que casen exactamente con el objetivo, se recurre
% a la rutina general segura como respaldo (nunca deja al
% usuario sin recomendacion).
rutina_para_objetivo_usuario(Condiciones, NivelUsuario, Objetivo, ListaFinal) :-
    findall(A,
            ( actividad_recomendada(A, Condiciones, NivelUsuario),
              actividad_para_objetivo(A, Objetivo) ),
            Lista),
    ( Lista == []
    -> rutina_recomendada_usuario(Condiciones, NivelUsuario, ListaFinal)
    ;  sort(Lista, ListaFinal)
    ).


% ============================================================
% C. REGLAS DE DESCANSO
% ============================================================

horas_sueno_recomendadas(NivelUsuario, MinHoras, MaxHoras) :-
    horas_sueno_base(NivelUsuario, MinHoras, MaxHoras).

% incluir_habito/2: la tecnica de relajacion solo se agrega de
% forma explicita cuando el objetivo es reduccion de estres;
% el resto de habitos de higiene del sueno aplica siempre.
incluir_habito(tecnica_relajacion, Objetivo) :- !, Objetivo == reduccion_estres.
incluir_habito(_Habito, _Objetivo).

habitos_descanso_recomendados(Objetivo, ListaIds) :-
    findall(H, ( habito_sueno(H, _Desc), incluir_habito(H, Objetivo) ), ListaIds).

habitos_descanso_texto(Objetivo, ListaTextos) :-
    findall(D, ( habito_sueno(H, D), incluir_habito(H, Objetivo) ), ListaTextos).


% ============================================================
% D. PLAN INTEGRAL (ALIMENTACION + EJERCICIO + DESCANSO)
% ============================================================

% plan_bienestar(+Condiciones, +NivelUsuario, +Objetivo, -Plan)
% Plan = plan(Alimentos, AlimentosRestringidos, Rutina,
%             HorasSuenoMin-HorasSuenoMax, HabitosDescanso)
plan_bienestar(Condiciones, NivelUsuario, Objetivo,
               plan(Alimentos, Restringidos, Rutina, MinH-MaxH, Habitos)) :-
    condicion_valida_lista(Condiciones),
    nivel_actividad(NivelUsuario),
    objetivo(Objetivo),
    alimentos_recomendados_usuario(Condiciones, Alimentos),
    alimentos_restringidos_usuario(Condiciones, Restringidos),
    rutina_para_objetivo_usuario(Condiciones, NivelUsuario, Objetivo, Rutina),
    horas_sueno_recomendadas(NivelUsuario, MinH, MaxH),
    habitos_descanso_texto(Objetivo, Habitos).

% Valida que cada elemento de la lista de condiciones sea una
% condicion conocida en la base de hechos.
condicion_valida_lista([]).
condicion_valida_lista([C|Resto]) :-
    condicion(C),
    condicion_valida_lista(Resto).

% Utilidad para imprimir un plan de forma legible en consola.
imprimir_plan(plan(Alimentos, Restringidos, Rutina, MinH-MaxH, Habitos)) :-
    format("  Alimentos recomendados: ~w~n", [Alimentos]),
    format("  Alimentos a evitar:     ~w~n", [Restringidos]),
    format("  Rutina de ejercicio:    ~w~n", [Rutina]),
    format("  Horas de sueno:         ~w a ~w horas~n", [MinH, MaxH]),
    format("  Habitos de descanso:~n", []),
    forall(member(H, Habitos), format("    - ~w~n", [H])).
