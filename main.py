from utils.configuracion import cargar_config
from extract.extract import leer_dataset, exploracion_inicial
from transform.transform import construir_silver, construir_gold
from load.load import (
    plot_estacionalidad_mensual,
    plot_tendencia_anual,
    plot_letalidad_por_disaster,
    plot_estacionalidad_argentina,
    plot_tipo_predominante_por_pais,
)
import pandas as pd


if __name__ == "__main__":
    config = cargar_config()

    # 1) Extracción y exploración inicial
    df_crudo = leer_dataset(config["rutas"]["bronze"])
    informe = exploracion_inicial(df_crudo)
    print("Extracción completa.")

    # 2) Silver: limpieza y transformación
    ruta_silver = construir_silver(config["rutas"]["bronze"], config)
    print("Silver listo:", ruta_silver)

    # 3) Gold: cruces y agregaciones
    rutas_gold = construir_gold(ruta_silver, config)
    print("Gold listo:", rutas_gold)

    # 4) Gráficos
    salida = config["rutas"]["graficos"]
    plot_estacionalidad_mensual(pd.read_parquet(rutas_gold["estacionalidad_mensual"]), f"{salida}/estacionalidad_mensual.png")
    plot_tendencia_anual(pd.read_parquet(rutas_gold["tendencia_anual"]), f"{salida}/tendencia_anual.png")
    plot_letalidad_por_disaster(pd.read_parquet(rutas_gold["letalidad_por_disaster"]), f"{salida}/letalidad_por_disaster.png")
    plot_estacionalidad_argentina(pd.read_parquet(rutas_gold["estacionalidad_argentina"]), f"{salida}/estacionalidad_argentina.png")
    plot_tipo_predominante_por_pais(pd.read_parquet(rutas_gold["tipo_predominante_por_pais"]), f"{salida}/tipo_predominante_por_pais.png")
    print("Gráficos guardados en", salida)

    print("ETL completado.")