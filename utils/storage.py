import json
import os

RUTA_DATOS = "data.json"

def cargar_datos():
    if not os.path.exists(RUTA_DATOS):
        return []
    with open(RUTA_DATOS, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(RUTA_DATOS, "w") as f:
        json.dump(data, f, indent=4)
