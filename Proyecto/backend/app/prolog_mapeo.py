"""
Capa de traduccion entre los valores en espanol que el frontend
guarda en la base de datos (ver frontend/pages/perfil.html y
backend/app/models.py) y los atomos que usan hechos.pl / reglas.pl.

Por que existe este archivo: el formulario de perfil manda literales
como "Diabetes tipo 2", "Levemente activo", "Perdida de peso", y asi
quedan guardados en la tabla `usuarios` / `condiciones_salud`. El
motor Prolog trabaja con atomos (diabetes_tipo2, levemente_activo,
perdida_peso). En vez de cambiar el frontend o la base de datos, se
traduce aqui, en un solo lugar.
"""

import unicodedata

# ---------------------------------------------------------------
# Mapas frontend (tal cual aparecen en perfil.html) -> atomos Prolog
# ---------------------------------------------------------------

CONDICIONES = {
    "diabetes tipo 2": "diabetes_tipo2",
    "hipertension": "hipertension",
    "obesidad": "obesidad",
    "anemia": "anemia",
    "intolerancia a la lactosa": "intolerancia_lactosa",
    "celiaquia": "celiaquia",
    # "Hipotiroidismo" no esta como checkbox en perfil.html todavia
    # (el motor Prolog si lo soporta) - se deja mapeado por si lo
    # agregan mas adelante.
    "hipotiroidismo": "hipotiroidismo",
}

NIVELES_ACTIVIDAD = {
    "sedentario": "sedentario",
    "levemente activo": "levemente_activo",
    "moderadamente activo": "moderadamente_activo",
    "muy activo": "muy_activo",
}

OBJETIVOS = {
    "perdida de peso": "perdida_peso",
    "ganancia muscular": "ganancia_muscular",
    "mantenimiento": "mantenimiento",
    "mejora cardiovascular": "mejora_cardiovascular",
    "reduccion del estres": "reduccion_estres",
}

# Valores por defecto para usuarios que aun no completaron su perfil
# (auth.py crea el usuario con actividad="Pendiente", objetivo="Pendiente").
NIVEL_ACTIVIDAD_POR_DEFECTO = "sedentario"
OBJETIVO_POR_DEFECTO = "mantenimiento"


def _normalizar(texto: str) -> str:
    """'Levemente activo' -> 'levemente activo';
    quita tildes para tolerar variantes de escritura."""
    texto = texto.strip().lower()
    sin_tildes = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sin_tildes if not unicodedata.combining(c))


def mapear_condiciones(nombres_condiciones: list[str]) -> list[str]:
    """Traduce la lista de nombres de CondicionSalud guardados en la
    BD a atomos Prolog. Los que no se reconocen (por ejemplo la opcion
    'Otra: especificar' del formulario, texto libre) se ignoran para
    el motor de reglas -- no hay forma de razonar sobre una condicion
    que no esta en la base de conocimiento -- pero se devuelven aparte
    para que el llamador decida si mostrarlos igual en la respuesta."""
    reconocidas = []
    for nombre in nombres_condiciones:
        atomo = CONDICIONES.get(_normalizar(nombre))
        if atomo:
            reconocidas.append(atomo)
    return reconocidas


def condiciones_no_reconocidas(nombres_condiciones: list[str]) -> list[str]:
    """Devuelve las condiciones que el usuario registro pero que el
    motor Prolog no puede usar (texto libre de 'Otra: especificar')."""
    return [
        nombre
        for nombre in nombres_condiciones
        if _normalizar(nombre) not in CONDICIONES
    ]


def mapear_nivel_actividad(valor: str) -> str:
    return NIVELES_ACTIVIDAD.get(_normalizar(valor), NIVEL_ACTIVIDAD_POR_DEFECTO)


def mapear_objetivo(valor: str) -> str:
    return OBJETIVOS.get(_normalizar(valor), OBJETIVO_POR_DEFECTO)


# ---------------------------------------------------------------
# Nombres legibles para mostrar en la respuesta (atomo -> texto bonito)
# ---------------------------------------------------------------

NOMBRES_ALIMENTOS = {
    "pollo_pechuga": "Pechuga de pollo",
    "salmon": "Salmón",
    "mariscos": "Mariscos",
    "carnes_rojas": "Carnes rojas",
    "embutidos": "Embutidos",
    "lentejas": "Lentejas",
    "garbanzos": "Garbanzos",
    "espinaca": "Espinaca",
    "brocoli": "Brócoli",
    "algas_yodadas": "Algas yodadas",
    "arroz_integral": "Arroz integral",
    "arroz_blanco": "Arroz blanco",
    "pan_blanco": "Pan blanco",
    "pan_integral": "Pan integral",
    "avena": "Avena",
    "quinoa": "Quinoa",
    "azucar_refinada": "Azúcar refinada",
    "leche_entera": "Leche entera",
    "yogur_natural": "Yogur natural",
    "queso_bajo_sodio": "Queso bajo en sodio",
    "leche_deslactosada": "Leche deslactosada",
    "aguacate": "Aguacate",
    "aceite_oliva": "Aceite de oliva",
    "nueces": "Nueces",
    "fritos": "Frituras",
    "platano": "Plátano",
    "manzana": "Manzana",
    "naranja": "Naranja",
    "sal_de_mesa": "Sal de mesa",
    "sal_yodada": "Sal yodada",
}

NOMBRES_ACTIVIDADES = {
    "caminata": "Caminata",
    "trote_suave": "Trote suave",
    "ciclismo": "Ciclismo",
    "natacion": "Natación",
    "hiit": "Entrenamiento HIIT",
    "spinning": "Spinning",
    "pesas_ligeras": "Pesas ligeras",
    "pesas_pesadas": "Pesas pesadas",
    "yoga": "Yoga",
    "pilates": "Pilates",
    "estiramientos": "Estiramientos",
}


def formatear_alimento(atomo: str) -> str:
    return NOMBRES_ALIMENTOS.get(atomo, atomo.replace("_", " ").capitalize())


def formatear_actividad(atomo: str) -> str:
    return NOMBRES_ACTIVIDADES.get(atomo, atomo.replace("_", " ").capitalize())
