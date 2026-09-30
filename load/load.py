import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

def crear_carpeta(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def guardar_grafico(fig, ruta_salida):
    fig.text(0.99, 0.01, "Fuente: EM-DAT", ha="right", fontsize=8, color="gray")
    fig.tight_layout()
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)


def plot_estacionalidad_mensual(tabla, ruta_salida):
    crear_carpeta(ruta_salida)
    promedio = tabla["cantidad_eventos"].mean()
    colores = ["tomato" if v > promedio else "steelblue" for v in tabla["cantidad_eventos"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    barras = ax.bar(tabla["mes"], tabla["cantidad_eventos"], color=colores)
    ax.bar_label(barras)

    ax.set_xticks(tabla["mes"])
    ax.set_xticklabels(MESES, rotation=0)
    ax.set_title("Distribución mensual de desastres naturales a nivel global (2002-2021)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad de eventos")
    guardar_grafico(fig, ruta_salida)


def plot_tendencia_anual(tabla, ruta_salida):
    crear_carpeta(ruta_salida)
    pendiente, ordenada = np.polyfit(tabla["anio"], tabla["cantidad_eventos"], 1)
    promedio = tabla["cantidad_eventos"].mean()
    colores = ["tomato" if v > promedio else "steelblue" for v in tabla["cantidad_eventos"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(tabla["anio"], tabla["cantidad_eventos"], color=colores)
    ax.plot(tabla["anio"], pendiente * tabla["anio"] + ordenada, color="black", linewidth=2,
            label=f"Tendencia: {pendiente*10:+.0f} eventos/década")
    ax.axhline(promedio, color="gray", linestyle="--", linewidth=1, label=f"Promedio: {promedio:.0f}")
    ax.legend()

    ax.set_title("Cantidad de desastres naturales por año (2002-2021)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de eventos")
    ax.tick_params(axis="x", rotation=45)
    guardar_grafico(fig, ruta_salida)


def plot_letalidad_por_disaster(tabla, ruta_salida):
    crear_carpeta(ruta_salida)
    fig, ax = plt.subplots(figsize=(8, 6))

    sns.scatterplot(data=tabla, x="promedio_muertes", y="cantidad_reportada", s=120, ax=ax)
    for _, fila in tabla.iterrows():
        ax.annotate(fila["disaster_type"], (fila["promedio_muertes"], fila["cantidad_reportada"]),
                    fontsize=8, xytext=(5, 5), textcoords="offset points")

    ax.set_yscale("log")
    ax.set_title("Promedio de muertes vs. cantidad de casos reportados")
    ax.set_xlabel("Promedio de muertes")
    ax.set_ylabel("Cantidad de casos reportados (escala logarítmica)")
    guardar_grafico(fig, ruta_salida)


def plot_estacionalidad_argentina(tabla, ruta_salida):
    crear_carpeta(ruta_salida)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(tabla, cmap="YlOrRd", annot=True, fmt="d", linewidths=0.5, ax=ax)
    ax.set_xticklabels(MESES, rotation=0)
    ax.set_title("Estacionalidad de desastres naturales por tipo, en Argentina (2002-2021)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Tipo de desastre")
    guardar_grafico(fig, ruta_salida)


def plot_tipo_predominante_por_pais(tabla, ruta_salida):
    # Usa plotly, no matplotlib: se guarda distinto (requiere kaleido)
    import plotly.express as px

    crear_carpeta(ruta_salida)
    fig = px.choropleth(
        tabla,
        locations="country",
        locationmode="country names",
        color="disaster_type",
        title="Tipo de desastre predominante por país (2002-2021)"
    )
    fig.write_image(ruta_salida, scale=2)

if __name__ == "__main__":
    from utils.configuracion import cargar_config
    from transform.transform import construir_silver, construir_gold
    import pandas as pd

    config = cargar_config()
    salida = config["rutas"]["graficos"]

    ruta_silver = construir_silver(config["rutas"]["bronze"], config)
    rutas_gold = construir_gold(ruta_silver, config)

    plot_estacionalidad_mensual(pd.read_parquet(rutas_gold["estacionalidad_mensual"]), f"{salida}/estacionalidad_mensual.png")
    plot_tendencia_anual(pd.read_parquet(rutas_gold["tendencia_anual"]), f"{salida}/tendencia_anual.png")
    plot_letalidad_por_disaster(pd.read_parquet(rutas_gold["letalidad_por_disaster"]), f"{salida}/letalidad_por_disaster.png")
    plot_estacionalidad_argentina(pd.read_parquet(rutas_gold["estacionalidad_argentina"]), f"{salida}/estacionalidad_argentina.png")
    plot_tipo_predominante_por_pais(pd.read_parquet(rutas_gold["tipo_predominante_por_pais"]), f"{salida}/tipo_predominante_por_pais.png")

    print("Gráficos guardados en", salida)