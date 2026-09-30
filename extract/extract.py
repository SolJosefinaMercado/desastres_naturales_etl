
# Modulo extract.py
import pandas as pd 

def leer_dataset(ruta):
    df = pd.read_csv(ruta)
    return df 

def exploracion_inicial(df):
    informe = {
        "shape": df.shape,
        "nulos_por_columna": df.isnull().sum().sort_values(ascending=True),
        "tipos_por_columna": df.dtypes,
        "estadisticas_col_numericas" : df.describe(),
        "descripcion_col_categoricas" : df.describe(include=str)
    }
    print('Scroll ↓ (shape, info, nulls, describe numerico y categorico)')
    print('-' * 100)
    print("Shape: filas y columnas:", informe["shape"])
    print('-' * 100)
    print("\nInfo dataset crudo")
    print('-' * 100)
    print(df.info())
    print('-' * 100)
    print("\nConteo de nulos sobre el crudo")
    print('-' * 100)
    print(informe["nulos_por_columna"])
    print('-' * 100)
    print("\nEstadisticas descriptivas variables numericas", informe["estadisticas_col_numericas"])
    print('-' * 100)
    print("\nDescripcion variables categoricas", informe["descripcion_col_categoricas"])

    return informe

