"""
Capa de integracion con el motor Prolog via pyswip.

Se consultan varios predicados simples de reglas.pl (en vez del
termino compuesto plan_bienestar/4 de una sola vez) porque pyswip
desempaca mal los terminos anidados con pares Min-Max.

Requiere:
  - SWI-Prolog instalado en el sistema (paquete swi-prolog / swipl).
  - pip install pyswip
"""

import threading
from pathlib import Path
from typing import List, Tuple

from pyswip import Prolog


_PROLOG_DIR = Path(__file__).parent.parent.parent / "prolog"

# SWI-Prolog embebido no es reentrante de forma segura desde varios
# hilos a la vez, asi que se serializa el acceso con un lock. Para el
# trafico esperado de este proyecto de curso es mas que suficiente.
_lock = threading.Lock()
_prolog = Prolog()
_loaded = False


def _decode(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def _ruta_prolog(nombre_archivo: str) -> str:
    """Ruta con barras normales (/), que SWI-Prolog acepta sin
    problema incluso en Windows."""
    return (_PROLOG_DIR / nombre_archivo).as_posix()


def _consultar_archivo(nombre_archivo: str):
    """Carga un .pl ejecutando consult('...') directamente con
    Prolog.query(), en vez de usar Prolog.consult().

    Por que: Prolog.consult() de pyswip vuelve a envolver la ruta en
    un objeto pathlib.Path por dentro y le aplica str() otra vez antes
    de mandarla a Prolog. En Windows, str(Path(...)) SIEMPRE normaliza
    a contrabarras (C:\\Users\\...), sin importar que aqui ya le hayamos
    dado la ruta con barras normales - por eso as_posix() solo no
    alcanzaba. Prolog interpreta esas contrabarras como secuencias de
    escape (\\U, \\E...) y truena con 'Illegal \\u or \\U sequence'.
    Prolog.query() en cambio manda el texto tal cual, sin tocarlo, asi
    que armamos nosotros mismos la consulta consult('<ruta>') con la
    ruta ya en formato posix."""
    ruta = _ruta_prolog(nombre_archivo)
    list(_prolog.query(f"consult('{ruta}')"))


def _ensure_loaded():
    global _loaded
    if _loaded:
        return
    _consultar_archivo("hechos.pl")
    _consultar_archivo("reglas.pl")
    _loaded = True


def preload():
    """Llamar en el evento startup de FastAPI (ver main.py) para que
    la primera peticion HTTP no pague el costo de cargar los .pl."""
    with _lock:
        _ensure_loaded()


def _lista_prolog(atomos: List[str]) -> str:
    """['diabetes_tipo2','obesidad'] -> '[diabetes_tipo2,obesidad]'.
    Los atomos ya vienen filtrados por prolog_mapeo.py contra un
    diccionario fijo, asi que es seguro interpolarlos en la consulta."""
    return "[" + ",".join(atomos) + "]"


def obtener_plan(
    condiciones: List[str], nivel_actividad: str, objetivo: str
) -> dict:
    """condiciones/nivel_actividad/objetivo deben ser atomos Prolog
    validos (usar prolog_mapeo.mapear_* antes de llamar esto)."""
    with _lock:
        _ensure_loaded()

        lista_cond = _lista_prolog(condiciones)

        alimentos_rec = _consultar_lista(
            f"alimentos_recomendados_usuario({lista_cond}, R)"
        )
        alimentos_res = _consultar_lista(
            f"alimentos_restringidos_usuario({lista_cond}, R)"
        )
        rutina = _consultar_lista(
            f"rutina_para_objetivo_usuario({lista_cond}, {nivel_actividad}, "
            f"{objetivo}, R)"
        )
        min_h, max_h = _consultar_horas_sueno(nivel_actividad)
        habitos = _consultar_lista(f"habitos_descanso_texto({objetivo}, R)")

    return {
        "alimentos_recomendados": alimentos_rec,
        "alimentos_restringidos": alimentos_res,
        "rutina_ejercicio": rutina,
        "horas_sueno_min": min_h,
        "horas_sueno_max": max_h,
        "habitos_descanso": habitos,
    }


def _consultar_lista(consulta: str) -> List[str]:
    resultados = list(_prolog.query(consulta))
    if not resultados:
        return []
    return [_decode(v) for v in resultados[0]["R"]]


def _consultar_horas_sueno(nivel_actividad: str) -> Tuple[int, int]:
    resultados = list(
        _prolog.query(f"horas_sueno_recomendadas({nivel_actividad}, Min, Max)")
    )
    if not resultados:
        return 7, 9
    fila = resultados[0]
    return int(fila["Min"]), int(fila["Max"])
