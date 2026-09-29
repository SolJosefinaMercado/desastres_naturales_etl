import yaml
import pandas as pd

def cargar_config(ruta: str = "config/config.yaml") -> dict:
    # Lee el archivo YAML y lo devuelve como diccionario
    # with open abre el archivo y lo cierra solo
    with open(ruta, encoding="utf-8") as archivo:
        # convierte el texto YML en diccionario 
        return yaml.safe_load(archivo)
