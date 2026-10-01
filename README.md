# Desastres naturales 1970-2021 — Trabajo Práctico 1 (Procesamiento de Datos)

Pipeline ETL que procesa el dataset EM-DAT de desastres naturales (1970-2021), 
identificando patrones temporales y geográficos en su ocurrencia.

## Autor
Sol Josefina Mercado Jacobsen — Instituto Superior Santo Domingo

## Arquitectura

El proyecto sigue el enfoque de **ETL tradicional** (extract / transform / load), 
con tres módulos especializados:

- `extract/`: lectura del dataset (`pd.read_csv`) y exploración inicial de su 
  estructura (shape, tipos de dato, nulos).
- `transform/`: limpieza, imputación de nulos, estandarización de categorías, 
  unificación de la columna `fecha`, recorte a las últimas dos décadas (2002-2021), 
  y cálculo de los cruces analíticos (estacionalidad, tendencia, letalidad, etc.).
- `load/`: generación de los gráficos y su persistencia como imágenes en `outputs/`.

Se eligió este enfoque en lugar de Medallion por simplicidad, dado el volumen y la 
naturaleza del dataset (un único archivo fuente, sin necesidad de múltiples capas 
de almacenamiento intermedio).

## Estructura del proyecto

desastres_naturales_etl/
├── data/ # Dataset original (EM-DAT)
├── config/
│ └── config.yaml # Rutas y parámetros de configuración
├── extract/ # Lectura y exploración inicial
├── transform/ # Limpieza, curación y cruces analíticos

├── load/ # Generación de gráficos

├── notebook/
│ └── informe_final_modular.ipynb # Notebook de análisis y reporte
  └── informe.ipybn # notebook de EDA

├── outputs/ # Gráficos generados (PNG)
├── main.py # Orquesta el pipeline completo
├── utils / configuracion.py # Lee y carga el archivo config.yaml


└── requirements.txt


## Cómo ejecutar

1. Clonar el repositorio.
2. Crear el entorno virtual e instalar dependencias:

uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt

3. Ejecutar el pipeline completo:

python main.py