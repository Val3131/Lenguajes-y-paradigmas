from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import DateTime



class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    edad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    peso: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    estatura: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    actividad: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )

    objetivo: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )

    sueno: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    habito_actividad: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    comentarios: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    condiciones = relationship(
    "CondicionSalud",
    back_populates="usuario",
    cascade="all, delete-orphan"
    )

    progresos = relationship(
    "Progreso",
    back_populates="usuario",
    cascade="all, delete-orphan"
    )
    correo: Mapped[str] = mapped_column(
    String(120),
    unique=True,
    index=True,
    nullable=False
    )

    contrasena_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

class CondicionSalud(Base):
    __tablename__ = "condiciones_salud"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="condiciones"
    )

class Progreso(Base):
    __tablename__ = "progresos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    peso_actual: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    sueno_actual: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    actividad_realizada: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    usuario = relationship(
        "Usuario",
        back_populates="progresos"
    )