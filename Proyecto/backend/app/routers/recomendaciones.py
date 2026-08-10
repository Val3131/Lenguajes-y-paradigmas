from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, plan_service
from app.database import obtener_db


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

    try:
        return plan_service.calcular_plan(usuario)
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=500,
            detail=f"Error consultando el motor de recomendaciones: {exc}"
        ) from exc
