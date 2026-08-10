"""
Logica compartida para calcular el plan de recomendaciones de un
usuario (Prolog + IA generativa). La usan tanto el router de
recomendaciones (para mostrarlo en pantalla) como el router de
progresos (para guardar un snapshot en cada registro semanal y asi
poder armar el historial dinamico).
"""

from app import models, prolog_engine, ia_generativa
from app.prolog_mapeo import (
    mapear_condiciones,
    mapear_nivel_actividad,
    mapear_objetivo,
    formatear_alimento,
    formatear_actividad,
)


def calcular_plan(usuario: models.Usuario) -> dict:
    """Devuelve {alimentacion, ejercicio, descanso, consejo_ia} para
    el perfil actual del usuario. Lanza la excepcion original si
    Prolog falla; quien llama decide como convertirla en HTTPException."""

    condiciones_prolog = mapear_condiciones(
        [c.nombre for c in usuario.condiciones]
    )
    nivel_prolog = mapear_nivel_actividad(usuario.actividad)
    objetivo_prolog = mapear_objetivo(usuario.objetivo)

    plan = prolog_engine.obtener_plan(
        condiciones_prolog, nivel_prolog, objetivo_prolog
    )

    alimentacion = []
    if plan["alimentos_recomendados"]:
        nombres = [formatear_alimento(a) for a in plan["alimentos_recomendados"]]
        alimentacion.append("Alimentos recomendados: " + ", ".join(nombres) + ".")
    if plan["alimentos_restringidos"]:
        nombres = [formatear_alimento(a) for a in plan["alimentos_restringidos"]]
        alimentacion.append("Alimentos a evitar: " + ", ".join(nombres) + ".")
    if not alimentacion:
        alimentacion.append(
            "Aún no hay suficientes datos de tu perfil para generar "
            "recomendaciones de alimentación."
        )

    ejercicio = [
        f"Actividad recomendada: {formatear_actividad(a)}."
        for a in plan["rutina_ejercicio"]
    ]
    if not ejercicio:
        ejercicio.append(
            "Aún no hay una rutina segura disponible para tu perfil; "
            "consulta con un profesional antes de iniciar ejercicio."
        )

    descanso = [
        f"Dormir entre {plan['horas_sueno_min']} y {plan['horas_sueno_max']} "
        "horas por noche."
    ] + plan["habitos_descanso"]

    consejo_ia = ia_generativa.generar_consejo(alimentacion, ejercicio, descanso)

    return {
        "alimentacion": alimentacion,
        "ejercicio": ejercicio,
        "descanso": descanso,
        "consejo_ia": consejo_ia,
    }
