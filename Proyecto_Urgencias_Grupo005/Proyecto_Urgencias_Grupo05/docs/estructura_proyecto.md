# Estructura de Proyecto sugerida

Ejemplo de cómo debe quedar cada carpeta:

- data/
    - urgencias_procesadas_Limpio_sin pipeline
    - urgencias_noprocesados_grupo05.csv
  - processed/
    - urgencias_procesadas_Limpio.csv

- notebooks/
  - Analisis_Integridad_y_Visualizacion_Urgencias.ipynb
  - analisis_datos_crudos.ipynb

- src/
  - limpieza.py
  - transformaciones.py
  - validacion.py
  - visualizacion.py

- outputs/
  - visualizaciones/
    - diagnostico_crudo/
    - diagnostico_limpio/

- docs/
  - estructura_proyecto.md
  - hallazgos_crudos.md
  - Proceso de Limpieza y Transformación de Datos

Notas:
- Mantener `data/raw` inmutable: no editar los CSV originales.
- Guardar artefactos procesados en `data/processed` con nombres versionados.

Se implementó un pipeline de procesamiento de datos con el objetivo de organizar y automatizar las distintas etapas del análisis, incluyendo la limpieza, transformación y preparación de los datos. Este enfoque permitió aplicar de manera ordenada y reproducible técnicas como la normalización de variables numéricas, la codificación de variables categóricas y la creación de nuevas características, facilitando el trabajo y reduciendo posibles errores manuales.

El uso del pipeline asegura que todos los pasos se ejecuten en la secuencia correcta, permitiendo reutilizar el proceso en futuros análisis o con nuevos datos.

El trabajo fue desarrollado por los integrantes del equipo: Antonella Aedo, Benjamín Díaz y Manuel Pizarro.
