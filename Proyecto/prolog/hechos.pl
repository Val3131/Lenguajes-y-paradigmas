%% ============================================================
%% HECHOS.PL
%% Sistema Inteligente de Gestion de Salud y Bienestar Personal
%% Base de conocimiento: condiciones de salud, alimentos y sus
%% propiedades nutricionales, actividades fisicas, niveles de
%% actividad, objetivos de bienestar y habitos de descanso.
%% ============================================================

% ---------------------------------------------------------
% 1. CONDICIONES DE SALUD
% ---------------------------------------------------------
% condicion(NombreCondicion).
condicion(diabetes_tipo2).
condicion(hipertension).
condicion(hipotiroidismo).
condicion(obesidad).
condicion(anemia).
condicion(intolerancia_lactosa).
condicion(celiaquia).
condicion(ninguna).            % usuario sin condiciones registradas

% ---------------------------------------------------------
% 2. GRUPOS DE ALIMENTOS
% ---------------------------------------------------------
grupo_alimento(proteina).
grupo_alimento(carbohidrato).
grupo_alimento(grasa).
grupo_alimento(vegetal).
grupo_alimento(fruta).
grupo_alimento(lacteo).
grupo_alimento(legumbre).
grupo_alimento(condimento).

% ---------------------------------------------------------
% 3. ALIMENTOS Y PROPIEDADES NUTRICIONALES
% ---------------------------------------------------------
% alimento(Nombre, Grupo, ListaDePropiedades).
alimento(pollo_pechuga,   proteina,     [proteina_alta, grasa_baja, sin_gluten, sin_lactosa]).
alimento(salmon,          proteina,     [proteina_alta, omega3, sin_gluten, sin_lactosa]).
alimento(mariscos,        proteina,     [proteina_alta, hierro_alto, sin_gluten, sin_lactosa]).
alimento(carnes_rojas,    proteina,     [proteina_alta, grasa_alta, hierro_alto, sin_gluten, sin_lactosa]).
alimento(embutidos,       proteina,     [grasa_alta, sodio_alto, sin_gluten, sin_lactosa]).

alimento(lentejas,        legumbre,     [proteina_media, fibra_alta, hierro_alto, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(garbanzos,       legumbre,     [proteina_media, fibra_alta, hierro_medio, bajo_indice_glucemico, sin_gluten, sin_lactosa]).

alimento(espinaca,        vegetal,      [hierro_alto, fibra_alta, vitamina_a, sin_gluten, sin_lactosa]).
alimento(brocoli,         vegetal,      [fibra_alta, vitamina_c, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(algas_yodadas,   vegetal,      [yodo_alto, fibra_alta, sin_gluten, sin_lactosa]).

alimento(arroz_integral,  carbohidrato, [fibra_alta, carbohidrato_complejo, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(arroz_blanco,    carbohidrato, [carbohidrato_refinado, indice_glucemico_alto, sin_gluten, sin_lactosa]).
alimento(pan_blanco,      carbohidrato, [carbohidrato_refinado, indice_glucemico_alto, gluten, sin_lactosa]).
alimento(pan_integral,    carbohidrato, [fibra_alta, carbohidrato_complejo, gluten, sin_lactosa]).
alimento(avena,           carbohidrato, [fibra_alta, carbohidrato_complejo, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(quinoa,          carbohidrato, [proteina_media, fibra_alta, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(azucar_refinada, carbohidrato, [azucar_alta, indice_glucemico_alto, sin_gluten, sin_lactosa]).

alimento(leche_entera,        lacteo, [proteina_media, calcio_alto, lactosa, sin_gluten]).
alimento(yogur_natural,       lacteo, [proteina_media, calcio_alto, lactosa, probioticos, sin_gluten]).
alimento(queso_bajo_sodio,    lacteo, [proteina_media, calcio_alto, lactosa, sodio_bajo, sin_gluten]).
alimento(leche_deslactosada,  lacteo, [proteina_media, calcio_alto, sin_lactosa, sin_gluten]).

alimento(aguacate,        grasa, [grasa_saludable, fibra_alta, potasio_alto, sin_gluten, sin_lactosa]).
alimento(aceite_oliva,    grasa, [grasa_saludable, sin_gluten, sin_lactosa]).
alimento(nueces,          grasa, [grasa_saludable, proteina_media, hierro_medio, sin_gluten, sin_lactosa]).
alimento(fritos,          grasa, [grasa_alta, sodio_alto, sin_gluten, sin_lactosa]).

alimento(platano,         fruta, [potasio_alto, azucar_natural, fibra_media, sin_gluten, sin_lactosa]).
alimento(manzana,         fruta, [fibra_alta, azucar_natural, bajo_indice_glucemico, sin_gluten, sin_lactosa]).
alimento(naranja,         fruta, [vitamina_c, azucar_natural, fibra_media, sin_gluten, sin_lactosa]).

alimento(sal_de_mesa,     condimento, [sodio_alto, sin_gluten, sin_lactosa]).
alimento(sal_yodada,      condimento, [sodio_alto, yodo_alto, sin_gluten, sin_lactosa]).

% ---------------------------------------------------------
% 4. ACTIVIDADES FISICAS
% ---------------------------------------------------------
% actividad(Nombre, Tipo, NivelEsfuerzo, ListaDeBeneficios).
% Tipo         in {aerobica, anaerobica, bajo_impacto, alta_intensidad}
% NivelEsfuerzo in {bajo, moderado, alto}
actividad(caminata,        aerobica,        bajo,     [cardiovascular, bajo_impacto, control_peso]).
actividad(trote_suave,     aerobica,        moderado, [cardiovascular, control_peso, quema_calorica]).
actividad(ciclismo,        aerobica,        moderado, [cardiovascular, resistencia, quema_calorica]).
actividad(natacion,        aerobica,        moderado, [cardiovascular, bajo_impacto, articulaciones]).
actividad(hiit,            alta_intensidad, alto,     [quema_calorica, resistencia, cardiovascular]).
actividad(spinning,        alta_intensidad, alto,     [cardiovascular, quema_calorica]).
actividad(pesas_ligeras,   anaerobica,      moderado, [ganancia_muscular, tonificacion]).
actividad(pesas_pesadas,   anaerobica,      alto,     [ganancia_muscular, fuerza]).
actividad(yoga,            bajo_impacto,    bajo,     [flexibilidad, reduccion_estres, equilibrio]).
actividad(pilates,         bajo_impacto,    bajo,     [fortalecimiento_core, flexibilidad]).
actividad(estiramientos,   bajo_impacto,    bajo,     [flexibilidad, recuperacion]).

% ---------------------------------------------------------
% 5. NIVELES DE ACTIVIDAD DEL USUARIO
% ---------------------------------------------------------
nivel_actividad(sedentario).
nivel_actividad(levemente_activo).
nivel_actividad(moderadamente_activo).
nivel_actividad(muy_activo).

% ---------------------------------------------------------
% 6. OBJETIVOS DE BIENESTAR
% ---------------------------------------------------------
objetivo(perdida_peso).
objetivo(ganancia_muscular).
objetivo(mantenimiento).
objetivo(mejora_cardiovascular).
objetivo(reduccion_estres).

% ---------------------------------------------------------
% 7. HABITOS DE DESCANSO
% ---------------------------------------------------------
% horas_sueno_base(NivelActividad, HorasMinimas, HorasMaximas).
horas_sueno_base(sedentario,            7, 9).
horas_sueno_base(levemente_activo,      7, 9).
horas_sueno_base(moderadamente_activo,  7, 9).
horas_sueno_base(muy_activo,            8, 10).

% habito_sueno(Identificador, Descripcion).
habito_sueno(horario_regular,               'Acostarse y levantarse a la misma hora todos los dias, incluidos fines de semana').
habito_sueno(evitar_pantallas,              'Evitar pantallas (celular, TV, computadora) al menos 30 minutos antes de dormir').
habito_sueno(ambiente_oscuro,               'Mantener la habitacion oscura, fresca y silenciosa').
habito_sueno(evitar_cafeina,                'Evitar cafeina y estimulantes despues de las 4:00 pm').
habito_sueno(evitar_ejercicio_intenso_noche,'Evitar ejercicio de alta intensidad en las 2 horas previas a dormir').
habito_sueno(tecnica_relajacion,            'Practicar respiracion profunda, meditacion o relajacion muscular antes de dormir').
