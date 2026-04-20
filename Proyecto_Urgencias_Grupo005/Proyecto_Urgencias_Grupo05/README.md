# Proyecto Urgencias - Grupo 05

Descripción
- Repositorio para limpieza, validación y transformación de datos de urgencias. El flujo implementado es reproducible y modular, preparado para entrega académica.

Estructura principal
- `data/raw/` - Datos originales (no modificar)
- `data/processed/` - Datos procesados y listos para análisis
- `notebooks/` - Notebooks de análisis y templates
- `src/` - Código modular (limpieza, transformaciones, validación)
- `outputs/` - Artefactos resultantes (gráficos, tablas)
- `docs/` - Informe técnico y documentación

Requisitos
1. Crear y activar un entorno virtual (recomendado `venv`).
2. Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar el notebook template

```bash
jupyter notebook notebooks/00_cleaning_template.ipynb
```

Buenas prácticas
- No modificar archivos en `data/raw`.
- Versionar los datasets procesados en `data/processed`.

Ejecución del pipeline completo (genera datos procesados, reportes y visualizaciones):

```bash
python run_pipeline.py
```

Los resultados se guardan en `data/processed/` y `outputs/`.
