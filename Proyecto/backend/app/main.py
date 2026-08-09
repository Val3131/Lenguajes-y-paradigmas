from fastapi import FastAPI
from app import models, prolog_engine
from app.database import engine
from app.routers import progresos, recomendaciones, usuarios, historial, auth
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Salud y Bienestar",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(progresos.router)
app.include_router(recomendaciones.router)
app.include_router(historial.router)


@app.on_event("startup")
def cargar_motor_prolog():
    # Carga hechos.pl y reglas.pl una sola vez al arrancar, para que
    # la primera peticion a /recomendaciones no pague ese costo.
    prolog_engine.preload()


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Salud y Bienestar funcionando"
    }


@app.get("/health")
def verificar_api():
    return {
        "estado": "ok"
    }
