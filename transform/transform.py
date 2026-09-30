import pandas as pd
import os 
from extract.extract import leer_dataset


# ---- Limpieza y transformación (Silver) ----
def seleccionar_columnas(df):
    df = df[['Start Year',
             'Start Month',
             'Start Day',
             'Disaster Subgroup',
             'Disaster Type',
             'Country',
             'Region',
             'Continent',
             'Total Deaths' ]].copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df 
def normalizar_columnas(df):
    columnas_texto = ["disaster_subgroup", "disaster_type", "country", "region", "continent"]
    for columna in columnas_texto:
        df[columna] = df[columna].str.strip()
    return df 
def imputar_nulos(df):
    # imputacion de falores faltantes en mes de inicio 
    months = df["start_month"].dropna()
    mask = df["start_month"].isnull()
    df.loc[mask, "start_month"] = months.sample(n=mask.sum(), replace=True, random_state=42).values
    # imputacion de valores faltantes en dia de inicio 
    df["start_day"] = df["start_day"].fillna(1)
    return df
def unificar_fecha(df):
    df["fecha"] = pd.to_datetime(dict(year=df["start_year"],
                                      month=df["start_month"],
                                      day=df["start_day"]),
                                      errors="coerce")
    df = df.drop(columns=['start_year', 'start_month', 'start_day'])
    return df
def recortar_periodo(df):
    anio_max = df["fecha"].dt.year.max()
    return df[df["fecha"].dt.year >= anio_max - 19]
def guardar_silver(df, ruta_salida):
    # Guarda el dataset ya depurado como Parquet (conseva dtypes)
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_parquet(ruta_salida, index=False)
    return ruta_salida
def construir_silver(ruta_bronze, config):
    df = leer_dataset(ruta_bronze)
    df = seleccionar_columnas(df)
    df = normalizar_columnas(df)
    df = imputar_nulos(df)
    df = unificar_fecha(df)
    df = recortar_periodo(df)

    ruta_salida = guardar_silver(df, config["rutas"]["silver"])
    return ruta_salida

# ---- Análisis y cruces (Gold) ----
def estacionalidad_mensual(df):
    tabla = df.groupby(df["fecha"].dt.month).size().reset_index()
    tabla.columns = ["mes", "cantidad_eventos"]
    return tabla

def tendencia_anual(df):
    tabla = df.groupby(df["fecha"].dt.year).size().reset_index()
    tabla.columns = ["anio", "cantidad_eventos"]
    return tabla

def tipo_predominante_por_pais(df):
    tabla = (
        df.groupby("country")["disaster_type"]
        .value_counts()
        .reset_index(name="cantidad")
        .groupby("country")
        .head(1)
    )
    return tabla

def estacionalidad_argentina(df):
    argentina = df[df["country"] == "Argentina"]
    tabla = argentina.pivot_table(
        index="disaster_type",
        columns=argentina["fecha"].dt.month,
        values="fecha",
        aggfunc="count",
        fill_value=0
    )
    return tabla

def letalidad_por_disaster(df):
    tabla = (
        df.groupby("disaster_type")["total_deaths"]
        .agg(promedio_muertes="mean", cantidad_reportada="count")
        .sort_values("promedio_muertes", ascending=False)
        .reset_index()
    )
    return tabla

def construir_gold(ruta_silver, config):
    df = pd.read_parquet(ruta_silver)
    os.makedirs(config["rutas"]["gold"], exist_ok=True)

    tablas = {
        "estacionalidad_mensual": estacionalidad_mensual(df),
        "tendencia_anual": tendencia_anual(df),
        "letalidad_por_disaster": letalidad_por_disaster(df),
        "estacionalidad_argentina": estacionalidad_argentina(df),
        "tipo_predominante_por_pais": tipo_predominante_por_pais(df),
    }

    rutas = {}
    for nombre, tabla in tablas.items():
        ruta = f"{config['rutas']['gold']}/{nombre}.parquet"
        tabla.to_parquet(ruta, index=False)
        rutas[nombre] = ruta

    return rutas
