from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import obtener_db


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post(
    "",
    response_model=schemas.UsuarioRespuesta,
    status_code=201
)
def crear_usuario(
    datos: schemas.UsuarioCrear,
    db: Session = Depends(obtener_db)
):
    usuario = models.Usuario(
        nombre=datos.nombre,
        edad=datos.edad,
        peso=datos.peso,
        estatura=datos.estatura,
        actividad=datos.actividad,
        objetivo=datos.objetivo,
        sueno=datos.sueno,
        habito_actividad=datos.habitoActividad,
        comentarios=datos.comentarios
    )

    db.add(usuario)

    for nombre_condicion in datos.condiciones:
        condicion = models.CondicionSalud(
            nombre=nombre_condicion,
            usuario=usuario
        )
        db.add(condicion)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.get(
    "",
    response_model=list[schemas.UsuarioRespuesta]
)
def consultar_usuarios(
    db: Session = Depends(obtener_db)
):
    return db.query(models.Usuario).all()


@router.get(
    "/{usuario_id}",
    response_model=schemas.UsuarioRespuesta
)
def consultar_usuario(
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

    return usuario