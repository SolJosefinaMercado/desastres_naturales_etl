if __name__ == "__main__":
    from utils.configuracion import cargar_config

    config = cargar_config()
    ruta_silver = construir_silver(config["rutas"]["bronze"], config)
    print("Silver listo:", ruta_silver)

    rutas_gold = construir_gold(ruta_silver, config)
    print("Gold listo:", rutas_gold)