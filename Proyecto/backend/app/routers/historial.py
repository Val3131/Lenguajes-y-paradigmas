import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, plan_service
from app.database import obtener_db


router = APIRouter(
    prefix="/usuarios/{usuario_id}/historial",
    tags=["Historial"]
)


def _snapshot_a_semana(progreso: models.Progreso) -> schemas.RecomendacionSemana | None:
    if not progreso.recomendacion_snapshot:
        return None

    plan = json.loads(progreso.recomendacion_snapshot)

    return schemas.RecomendacionSemana(
        fecha=progreso.fecha.strftime("%d/%m/%Y"),
        alimentacion=" ".join(plan["alimentacion"]),
        ejercicio=" ".join(plan["ejercicio"]),
        descanso=" ".join(plan["descanso"]),
        consejoIa=plan["consejo_ia"],
    )


@router.get(
    "",
    response_model=schemas.HistorialRespuesta
)
def obtener_historial(
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

    # Se toman los ultimos dos progresos registrados por el usuario.
    # Cada progreso guarda un snapshot de la recomendacion vigente en
    # el momento en que se registro, asi que comparar los dos ultimos
    # progresos equivale a comparar "semana anterior" vs "semana
    # actual" con datos reales (no textos fijos).
    ultimos_progresos = (
        db.query(models.Progreso)
        .filter(models.Progreso.usuario_id == usuario_id)
        .order_by(models.Progreso.fecha.desc())
        .limit(2)
        .all()
    )

    if len(ultimos_progresos) == 0:
        return schemas.HistorialRespuesta(
            mensaje=(
                "Todavía no hay progreso registrado. Registrá tu primer "
                "progreso semanal para empezar a construir tu historial."
            )
        )

    semana_actual = _snapshot_a_semana(ultimos_progresos[0])

    if len(ultimos_progresos) == 1:
        return schemas.HistorialRespuesta(
            semanaActual=semana_actual,
            mensaje=(
                "Solo hay un progreso registrado todavía; registrá otro "
                "progreso la próxima semana para ver la comparación."
            )
        )

    semana_anterior = _snapshot_a_semana(ultimos_progresos[1])

    return schemas.HistorialRespuesta(
        semanaAnterior=semana_anterior,
        semanaActual=semana_actual,
    )
