# INFORME DE DIAGNÓSTICO: DATOS Limpio y procesados (ENTREGABLE 1)

Esta base de datos es un registro de gestión epidemiológica y financiera de atenciones de urgencia en Chile. Su objetivo principal es monitorear la demanda de salud, específicamente enfocada en enfermedades respiratorias, a través de la red asistencial.

## *1. ¿Qué representa cada fila?*
Cada registro (fila) representa el resumen semanal de atenciones para una causa específica en un establecimiento determinado. No es una lista de pacientes individuales, sino un "conteo agrupado" que detalla cuántas personas consultaron por una enfermedad en una semana, separándolas por edad.

## *2. Dimensiones que analiza:*
Clasifica los centros de salud por nombre, código, región y comuna. Además, incluye la georreferenciación (Latitud y Longitud).

**Jerarquía Administrativa:** Identifica quién administra el centro (Municipal o Servicio de Salud) y su Nivel de Atención (Primario como los SAPU/SAR, o Terciario como los Hospitales).

**Vigilancia Epidemiológica (¿Qué enfermedad?):** Se centra en causas respiratorias críticas como Influenza, Neumonía, Bronquitis Aguda y Crisis Asmática.

**Segmentación Demográfica (¿A quién?):** Es muy detallada en la edad. Divide el total de consultas en:

Lactantes (Menores de 1 año).

Preescolares y escolares (1 a 14 años).

Adultos (15 a 64 años).

Adultos Mayores (65 o más años).

**Estratificación de Gravedad:** Utiliza el sistema de Triage (C1, C2, C3, etc.) para indicar qué tan urgente fue la atención. C1 es riesgo vital, mientras que C4 o C5 son consultas no urgentes.

**Análisis Financiero:** Asigna un Costo en Pesos (CLP) a las atenciones, lo que permite medir el impacto económico del uso de recursos en la red de urgencia.

## *3. Temporalidad (2023 - 2024 - 2025):*
La base permite hacer un análisis comparativo interanual. Al incluir datos de 2023, 2024 y proyecciones o registros de 2025, su función es ayudar a predecir "peaks" o semanas de alta demanda (como la campaña de invierno) para que el sistema de salud pueda prepararse con más personal o medicamentos.

## Clasificación de Variables

Las variables del dataset fueron clasificadas en categóricas y cuantitativas según su naturaleza y uso en el análisis.

### Variables Categóricas
(Son cualitativas: representan categorías, nombres o etiquetas)

- EstablecimientoCodigo
- EstablecimientoGlosa  
- RegionCodigo  
- RegionGlosa  
- ComunaCodigo  
- ComunaGlosa  
- ServicioSaludCodigo  
- ServicioSaludGlosa  
- TipoEstablecimiento  
- DependenciaAdministrativa  
- NivelAtencion  
- TipoUrgencia  
- NivelComplejidad  
- OrdenCausa  
- Causa  
- FechaAtencionTexto  
- SexoPaciente  
- PrioridadTriage  

### Variables Cuantitativas
(Son numéricas: se pueden medir, sumar o promediar)

- Latitud  
- Longitud  
- Anio  
- SemanaEstadistica  

#### Conteos de atenciones
- NumTotal  
- NumMenor1Anio  
- Num1a4Anios  
- Num5a14Anios  
- Num15a64Anios  
- Num65oMas  

#### Variable económica
- CostoAtencionCLP  

### Observación
Cabe destacar que algunas variables numéricas corresponden a códigos (por ejemplo, EstablecimientoCodigo o RegionCodigo), por lo que fueron tratadas como variables categóricas, ya que no representan magnitudes medibles.

## Uso de estructuras de datos

Durante el desarrollo del análisis se utilizaron distintas estructuras de datos para facilitar la manipulación, organización y procesamiento de la información.

### DataFrame
El DataFrame (de la librería pandas) se utilizó como la estructura principal para trabajar con los datos. Permite almacenar la información en forma de tabla (filas y columnas), similar a una hoja de cálculo.

Su uso fue fundamental para:
- Cargar y visualizar los datos (head, shape).
- Limpiar datos (eliminación de nulos, estandarización de formatos).
- Realizar análisis estadístico.
- Filtrar, transformar y seleccionar columnas.
- Generar nuevas variables y preparar los datos para su análisis.

### Diccionarios
Los diccionarios se utilizaron para realizar mapeos y reemplazos de valores dentro de las columnas.

Su utilidad principal fue:
- Estandarizar categorías (por ejemplo, unificar valores como "M", "masculino").
- Corregir datos inconsistentes.
- Facilitar transformaciones rápidas mediante claves y valores.

### Listas y arrays
También se utilizaron listas y arrays para:
- Agrupar columnas (por ejemplo, columnas numéricas).
- Iterar sobre variables para aplicar procesos automáticos (como gráficos).
