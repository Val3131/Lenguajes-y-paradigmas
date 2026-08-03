from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    edad: int = Field(ge=1, le=120)
    peso: float = Field(ge=3, le=300)
    estatura: float = Field(ge=0.50, le=2.50)
    condiciones: list[str] = []
    actividad: str
    objetivo: str
    sueno: float = Field(ge=1, le=24)
    habitoActividad: str = Field(min_length=3, max_length=80)
    comentarios: str | None = None

class UsuarioActualizar(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    edad: int = Field(ge=1, le=120)
    peso: float = Field(ge=3, le=300)
    estatura: float = Field(ge=0.50, le=2.50)
    condiciones: list[str] = []
    actividad: str
    objetivo: str
    sueno: float = Field(ge=1, le=24)
    habitoActividad: str = Field(min_length=3, max_length=80)
    comentarios: str | None = None

class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    edad: int
    peso: float
    estatura: float
    actividad: str
    objetivo: str
    sueno: float
    habito_actividad: str
    comentarios: str | None
    fecha_creacion: datetime
    condiciones: list[CondicionRespuesta] = []

class CondicionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str

class ProgresoCrear(BaseModel):
    pesoActual: float = Field(ge=3, le=300)
    suenoActual: float = Field(ge=1, le=24)
    actividadRealizada: str = Field(min_length=3, max_length=100)

class ProgresoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    peso_actual: float
    sueno_actual: float
    actividad_realizada: str
    fecha: datetime

class RecomendacionRespuesta(BaseModel):
    alimentacion: list[str]
    ejercicio: list[str]
    descanso: list[str]

class RecomendacionSemana(BaseModel):
    alimentacion: str
    ejercicio: str
    descanso: str


class HistorialRespuesta(BaseModel):
    semanaAnterior: RecomendacionSemana
    semanaActual: RecomendacionSemana

class RegistroUsuario(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=72)


class LoginUsuario(BaseModel):
    correo: EmailStr
    contrasena: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    nombre: str


class UsuarioAutenticado(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr