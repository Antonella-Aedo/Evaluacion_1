# Estructura de Proyecto sugerida

Ejemplo de cómo debe quedar cada carpeta:

- data/
  - raw/
    - urgencias_noprocesados_grupo05.csv
  - processed/
    - urgencias_procesadas_Limpio.csv

- notebooks/
  - 00_cleaning_template.ipynb
  - analisis_datos_crudos.ipynb

- src/
  - limpieza.py
  - transformaciones.py
  - validacion.py

- outputs/
  - visualizaciones/
    - diagnostico_crudo/
    - diagnostico_limpio/

- docs/
  - informe_tecnico.md
  - Proceso de Limpieza y Transformación de Datos.md

Notas:
- Mantener `data/raw` inmutable: no editar los CSV originales.
- Guardar artefactos procesados en `data/processed` con nombres versionados.
