from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import obtener_db


router = APIRouter(
    prefix="/usuarios/{usuario_id}/historial",
    tags=["Historial"]
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

    return {
        "semanaAnterior": {
            "alimentacion": "Reducir azúcares y harinas refinadas.",
            "ejercicio": "Caminata de 20 minutos diarios.",
            "descanso": "Dormir 7 horas por noche."
        },
        "semanaActual": {
            "alimentacion": "Aumentar vegetales y proteínas magras.",
            "ejercicio": "Caminata de 30 minutos diarios.",
            "descanso": "Mejorar la higiene del sueño y evitar pantallas nocturnas."
        }
    }