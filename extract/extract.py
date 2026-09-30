
# Modulo extract.py
import pandas as pd 

def leer_dataset(ruta):
    df = pd.read_csv(ruta)
    return df 

def exploracion_inicial(df):
    informe = {
        "shape": df.shape,
        "nulos_por_columna": df.isnull().sum(),
        "tipos_por_columna": df.dtypes,
    }

    print("Shape: filas y columnas:", informe["shape"])
    print("\nInfo dataset crudo")
    print(df.info())
    print("\nConteo de nulos sobre el crudo")
    print(informe["nulos_por_columna"])

    return informe



