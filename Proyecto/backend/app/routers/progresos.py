from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import obtener_db


router = APIRouter(
    prefix="/usuarios/{usuario_id}/progresos",
    tags=["Progresos"]
)


@router.post(
    "",
    response_model=schemas.ProgresoRespuesta,
    status_code=201
)
def crear_progreso(
    usuario_id: int,
    datos: schemas.ProgresoCrear,
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

    progreso = models.Progreso(
        usuario_id=usuario_id,
        peso_actual=datos.pesoActual,
        sueno_actual=datos.suenoActual,
        actividad_realizada=datos.actividadRealizada
    )

    db.add(progreso)
    db.commit()
    db.refresh(progreso)

    return progreso


@router.get(
    "",
    response_model=list[schemas.ProgresoRespuesta]
)
def consultar_progresos(
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

    progresos = (
        db.query(models.Progreso)
        .filter(models.Progreso.usuario_id == usuario_id)
        .order_by(models.Progreso.fecha.asc())
        .all()
    )

    return progresos


@router.get(
    "/{progreso_id}",
    response_model=schemas.ProgresoRespuesta
)
def consultar_progreso(
    usuario_id: int,
    progreso_id: int,
    db: Session = Depends(obtener_db)
):
    progreso = (
        db.query(models.Progreso)
        .filter(
            models.Progreso.id == progreso_id,
            models.Progreso.usuario_id == usuario_id
        )
        .first()
    )

    if progreso is None:
        raise HTTPException(
            status_code=404,
            detail="Progreso no encontrado"
        )

    return progreso