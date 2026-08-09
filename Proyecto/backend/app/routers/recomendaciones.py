from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, prolog_engine
from app.database import obtener_db
from app.prolog_mapeo import (
    mapear_condiciones,
    mapear_nivel_actividad,
    mapear_objetivo,
    formatear_alimento,
    formatear_actividad,
)


router = APIRouter(
    prefix="/usuarios/{usuario_id}/recomendaciones",
    tags=["Recomendaciones"]
)


@router.get(
    "",
    response_model=schemas.RecomendacionRespuesta
)
def obtener_recomendaciones(
    usuario_id: int,
    db: Session = Depends(obtener_db)
):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    condiciones_prolog = mapear_condiciones(
        [c.nombre for c in usuario.condiciones]
    )
    nivel_prolog = mapear_nivel_actividad(usuario.actividad)
    objetivo_prolog = mapear_objetivo(usuario.objetivo)

    try:
        plan = prolog_engine.obtener_plan(
            condiciones_prolog, nivel_prolog, objetivo_prolog
        )
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=500,
            detail=f"Error consultando el motor de recomendaciones: {exc}"
        ) from exc

    alimentacion = []
    if plan["alimentos_recomendados"]:
        nombres = [formatear_alimento(a) for a in plan["alimentos_recomendados"]]
        alimentacion.append("Alimentos recomendados: " + ", ".join(nombres) + ".")
    if plan["alimentos_restringidos"]:
        nombres = [formatear_alimento(a) for a in plan["alimentos_restringidos"]]
        alimentacion.append("Alimentos a evitar: " + ", ".join(nombres) + ".")
    if not alimentacion:
        # No deberia pasar en la practica (siempre hay alimentos base
        # recomendados), pero se evita devolver una lista vacia al frontend.
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

    return {
        "alimentacion": alimentacion,
        "ejercicio": ejercicio,
        "descanso": descanso,
    }
