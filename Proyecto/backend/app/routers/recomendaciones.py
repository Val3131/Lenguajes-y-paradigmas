from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
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

    recomendaciones = {
        "alimentacion": [
            "Reducir azúcares refinados.",
            "Consumir vegetales frescos diariamente.",
            "Priorizar proteínas magras y alimentos ricos en fibra."
        ],
        "ejercicio": [
            "Realizar caminatas de 20 minutos al día.",
            "Practicar ejercicio de bajo impacto tres veces por semana.",
            "Realizar estiramientos diariamente."
        ],
        "descanso": [
            "Dormir entre 7 y 8 horas por noche.",
            "Evitar pantallas antes de dormir.",
            "Mantener una rutina constante de sueño."
        ]
    }

    return recomendaciones