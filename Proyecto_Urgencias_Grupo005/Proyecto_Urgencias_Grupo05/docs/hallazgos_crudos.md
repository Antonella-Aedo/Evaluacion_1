# INFORME DE DIAGNÓSTICO: DATOS CRUDOS (ENTREGABLE 1)

## Introducción
Este análisis se realiza sobre la base de datos original sin ninguna modificación. El objetivo es identificar problemas de calidad, inconsistencias y errores de estructura antes de iniciar cualquier proceso de limpieza o transformación (ETL).

## Metodología de Diagnóstico

### Paso 1: Carga y Vista Previa (head y shape)
**¿Por qué se hizo?:** Para validar que el archivo se lee correctamente y conocer el volumen de datos.

**Hallazgo:** Trabajamos con un dataset de 29 columnas y aproximadamente 4,742 registros. Esto nos confirma que la base es manejable pero lo suficientemente compleja por su cantidad de variables.

### Paso 2: Análisis Estadístico Descriptivo (describe)
**¿Por qué se hizo?:** Para detectar anomalías matemáticas y entender la dispersión de los datos.

**Análisis del resultado:**

**Count (4742):** Al observar que algunas columnas tienen menos de 4742 (como el count de 4716 o 4676 en ciertos campos), confirmamos de inmediato la presencia de valores nulos.

**Variables Categóricas (Top/Freq):** Notamos que el Hospital "Dr. Gustavo Fricke" y la Región "Metropolitana" son los más frecuentes.

**Dispersión (Std/Min/Max):** Hay valores máximos en tiempos de espera o costos que se disparan (ej. max de 1.32e+06), lo que sugiere la presencia de outliers (valores atípicos) que podrían sesgar los promedios.

### Paso 3: Identificación de Valores Únicos
**¿Por qué se hizo?:** Para encontrar errores de digitación o falta de estándar en las categorías.

**Hallazgo Crítico:**

**SexoPaciente:** Mezcla de formatos (M/F, masculino/femenino) y valores inválidos ('X', 'SinDato').

**PrioridadTriage:** Presencia de basura visual (espacios en blanco, minúsculas, guiones mal puestos).

**FechaAtencionTexto:** Caos de formatos (puntos, barras y guiones) que impiden tratar la columna como una fecha real.

### Paso 4: Auditoría de Nulos (isnull)
**¿Por qué se hizo?:** Para cuantificar la pérdida de información y evaluar la integridad del dataset.

**Análisis:** Se generó un DataFrame de control que consolida el total y porcentaje de vacíos por columna. Para optimizar el diagnóstico, se filtraron únicamente las variables con incidencias (nulos > 0). La presencia de faltantes en columnas críticas como FechaAtencion o Sexo señala registros incompletos que comprometen la trazabilidad, por lo que se recomienda su depuración o revisión en origen.

### Paso 5: Detección de Duplicados (duplicated)
**¿Por qué se hizo?:** Para asegurar la integridad de los datos. Las filas duplicadas inflan las estadísticas y generan conclusiones falsas.

**Hallazgo:** Se detectaron registros idénticos que deben ser removidos para que cada fila represente una atención única y real.

## 3. Analisis Visual de los datos crudos

### Análisis Visual de los Datos Crudos

Para este diagnóstico, se generaron visualizaciones técnicas ubicadas en la ruta:

C:\Users\marti\Desktop\entregable_1\outputs\visualizaciones\diagnostico_crudo\

Es importante notar que estas visualizaciones presentan una estética irregular y dificultades de lectura intencionales. Esto es evidencia directa de los siguientes hallazgos:

**Impacto de Valores Nulos (NaN):** La falta de datos impide que las curvas de densidad (KDE) se dibujen de forma fluida, generando saltos visuales en los histogramas (1_histograma_...).

**Inconsistencia de Escalas:** Al existir valores "erroneos" (ej. costos de $0 o de millones), la escala del gráfico se estira. Esto hace que en los Boxplots la información real se vea pequeña e ilegible frente a los puntos atípicos.
