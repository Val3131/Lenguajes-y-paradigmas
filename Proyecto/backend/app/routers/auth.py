from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import (
    crear_access_token,
    generar_hash_contrasena,
    obtener_usuario_actual,
    verificar_contrasena
)
from app.database import obtener_db


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post(
    "/registro",
    response_model=schemas.TokenRespuesta,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(
    datos: schemas.RegistroUsuario,
    db: Session = Depends(obtener_db)
):
    correo_normalizado = datos.correo.lower().strip()

    usuario_existente = (
        db.query(models.Usuario)
        .filter(models.Usuario.correo == correo_normalizado)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario registrado con este correo"
        )

    usuario = models.Usuario(
        nombre=datos.nombre.strip(),
        correo=correo_normalizado,
        contrasena_hash=generar_hash_contrasena(datos.contrasena),

        # Valores temporales hasta completar el perfil
        edad=1,
        peso=3,
        estatura=0.50,
        actividad="Pendiente",
        objetivo="Pendiente",
        sueno=1,
        habito_actividad="Pendiente",
        comentarios=None
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = crear_access_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre
    }


@router.post(
    "/login",
    response_model=schemas.TokenRespuesta
)
def iniciar_sesion(
    datos: schemas.LoginUsuario,
    db: Session = Depends(obtener_db)
):
    correo_normalizado = datos.correo.lower().strip()

    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.correo == correo_normalizado)
        .first()
    )

    if usuario is None or not verificar_contrasena(
        datos.contrasena,
        usuario.contrasena_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = crear_access_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre
    }


@router.get(
    "/me",
    response_model=schemas.UsuarioAutenticado
)
def consultar_usuario_actual(
    usuario: models.Usuario = Depends(obtener_usuario_actual)
):
    return usuario