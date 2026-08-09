"""
Integracion con IA generativa (Groq - API gratuita, sin tarjeta de
credito requerida) para traducir las recomendaciones logicas que
produce el motor Prolog en consejos claros, motivadores y
personalizados en lenguaje natural.

Requisito del enunciado (seccion 4 y 6): el modelo debe ser gratuito
o local, y se debe documentar como se garantiza el costo cero. Groq
ofrece un free tier con limite de requests por minuto/dia mas que
suficiente para un proyecto de curso, sin necesidad de tarjeta.

Variable de entorno requerida:
  GROQ_API_KEY  (se lee desde backend/.env, que NO se sube al repo)
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_MODELO = "llama-3.1-8b-instant"  # modelo gratuito de Groq

_api_key = os.getenv("GROQ_API_KEY")
_cliente = Groq(api_key=_api_key) if _api_key else None


def _prompt_sistema() -> str:
    return (
        "Sos un asistente de bienestar y salud. Recibis una lista de "
        "recomendaciones estructuradas (generadas por un motor de "
        "reglas logicas) sobre alimentacion, ejercicio y descanso "
        "para un usuario. Tu trabajo es reescribirlas en un consejo "
        "breve, claro, motivador y personalizado en espanol, en "
        "prosa (no listas), de maximo 4 oraciones. Respondé "
        "directamente con el consejo, sin ningun saludo, "
        "introduccion, comillas ni frases como 'aqui te dejo' o "
        "'claro que si'. No inventes datos medicos ni "
        "recomendaciones que no esten en la lista original; solo "
        "humaniza y explica lo que ya se te dio."
    )


def generar_consejo(
    alimentacion: list[str],
    ejercicio: list[str],
    descanso: list[str],
) -> str:
    """Devuelve un consejo en lenguaje natural a partir del plan
    estructurado de Prolog. Si la IA no esta disponible (sin API key
    o error de red), devuelve una union simple del plan original en
    vez de fallar toda la peticion."""

    plan_texto = (
        "Alimentacion: " + " ".join(alimentacion) + "\n"
        "Ejercicio: " + " ".join(ejercicio) + "\n"
        "Descanso: " + " ".join(descanso)
    )

    if _cliente is None:
        return _consejo_de_respaldo(alimentacion, ejercicio, descanso)

    try:
        respuesta = _cliente.chat.completions.create(
            model=_MODELO,
            messages=[
                {"role": "system", "content": _prompt_sistema()},
                {"role": "user", "content": plan_texto},
            ],
            temperature=0.6,
            max_tokens=450,
        )
        return respuesta.choices[0].message.content.strip()
    except Exception:  # pylint: disable=broad-except
        # Si Groq falla (sin internet, rate limit, etc.) el sistema
        # sigue funcionando con el texto base de Prolog en vez de
        # tumbar el endpoint de recomendaciones.
        return _consejo_de_respaldo(alimentacion, ejercicio, descanso)


def _consejo_de_respaldo(
    alimentacion: list[str],
    ejercicio: list[str],
    descanso: list[str],
) -> str:
    partes = alimentacion + ejercicio + descanso
    return " ".join(partes)
