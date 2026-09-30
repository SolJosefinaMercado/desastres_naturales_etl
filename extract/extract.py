
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

    print("Shape: filas y columnas:", informe["shape"])
    print("\nInfo dataset crudo")
    print(df.info())
    print("\nConteo de nulos sobre el crudo")
    print(informe["nulos_por_columna"])
    print("\nEstadisticas descriptivas variables numericas", informe["estadisticas_col_numericas"])
    print("\nDescripcion variables categoricas", informe["descripcion_col_categoricas"])

    return informe

