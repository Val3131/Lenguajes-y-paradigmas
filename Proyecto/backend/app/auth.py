from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app import models
from app.database import obtener_db


SECRET_KEY = "CAMBIA_ESTA_CLAVE_POR_UNA_MUY_LARGA_Y_ALEATORIA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def generar_hash_contrasena(contrasena: str) -> str:
    return password_hash.hash(contrasena)


def verificar_contrasena(
    contrasena: str,
    contrasena_hash: str
) -> bool:
    return password_hash.verify(
        contrasena,
        contrasena_hash
    )


def crear_access_token(
    usuario_id: int,
    minutos_expiracion: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=minutos_expiracion
    )

    contenido = {
        "sub": str(usuario_id),
        "exp": expiracion
    }

    return jwt.encode(
        contenido,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(obtener_db)
) -> models.Usuario:
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No fue posible validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise excepcion_credenciales

        usuario_id = int(usuario_id)

    except (InvalidTokenError, ValueError):
        raise excepcion_credenciales

    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise excepcion_credenciales

    return usuario