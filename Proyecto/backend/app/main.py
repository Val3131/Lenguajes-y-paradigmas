from fastapi import FastAPI
from app import models
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

