"""Script ligero para ejecutar pipeline: cargar -> validar -> limpiar -> transformar -> exportar.

Uso:
    python run_pipeline.py
"""
import logging
import os
from pathlib import Path

from src.limpieza import load_csv, drop_duplicates_rows, impute_multiple, impute_column, save_csv
from src.transformaciones import convert_types, create_datetime_features, group_aggregate, pivot_table
from src.validacion import generate_quality_report
from src.visualizacion import save_histogram, save_boxplot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Buscar el archivo raw en varias ubicaciones posibles (compatibilidad con estructura previa)
POSSIBLE_LOCATIONS = [Path('data/raw/urgencias_noprocesados_grupo05.csv'), Path('data/urgencias_noprocesados_grupo05.csv')]
DATA_RAW = next((p for p in POSSIBLE_LOCATIONS if p.exists()), POSSIBLE_LOCATIONS[0])
DATA_PROCESSED = Path('data/processed/urgencias_procesadas_Limpio.csv')
OUTPUT_DIR = Path('outputs/visualizaciones')
QUALITY_PATH = Path('outputs/quality_report.json')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_csv(str(DATA_RAW))

    # Report antes
    report_before = generate_quality_report(df, out_path=str(QUALITY_PATH.with_name('quality_before.json')))
    logger.info('Reporte antes generado')

    # Limpieza: duplicados y filas sin fecha crítica
    n_before = df.shape[0]
    df = drop_duplicates_rows(df)

    # Detectar columna de fecha y columna de sexo/num
    date_candidates = ['fecha_ingreso', 'FechaAtencionTexto', 'fecha', 'Fecha']
    date_col = next((c for c in date_candidates if c in df.columns), None)
    if date_col:
        df = df.dropna(subset=[date_col])
    else:
        logger.warning('No se detectó columna de fecha en el dataset; no se eliminarán filas por fecha')

    n_after = df.shape[0]
    logger.info('Filas antes=%d, después=%d, eliminadas=%d', n_before, n_after, n_before - n_after)

    # Imputaciones: rellenar sexo si existe
    if 'SexoPaciente' in df.columns or 'sexo' in df.columns:
        sex_col = 'SexoPaciente' if 'SexoPaciente' in df.columns else 'sexo'
        df = impute_multiple(df, {sex_col: 'Desconocido'})

    # Conversión de tipos: fecha y números cuando existan
    dtype_map = {}
    if date_col:
        dtype_map[date_col] = 'datetime64[ns]'
    if 'NumTotal' in df.columns:
        dtype_map['NumTotal'] = 'float'
    df = convert_types(df, dtype_map)

    # Features temporales
    if date_col:
        try:
            df = create_datetime_features(df, date_col)
        except Exception:
            logger.warning('No se pudo crear features datetime para %s', date_col)

    # Agregaciones: agrupar por establecimiento y causa si existen
    group_cols = [c for c in ['EstablecimientoGlosa', 'Causa'] if c in df.columns]
    if group_cols and 'NumTotal' in df.columns:
        try:
            agg = group_aggregate(df, group_cols, {'NumTotal': ['mean', 'median', 'sum']})
            agg.to_csv(OUTPUT_DIR / 'agg_summary.csv', index=False)
        except Exception:
            logger.exception('Error al generar agregaciones')

    # Pivot ejemplo: por establecimiento y SexoPaciente
    if 'EstablecimientoGlosa' in df.columns and ('SexoPaciente' in df.columns or 'sexo' in df.columns) and 'NumTotal' in df.columns:
        try:
            sex_col = 'SexoPaciente' if 'SexoPaciente' in df.columns else 'sexo'
            pt = pivot_table(df, index=['EstablecimientoGlosa'], columns=sex_col, values='NumTotal', aggfunc='median')
            pt.to_csv(OUTPUT_DIR / 'pivot_median_NumTotal_by_sexo.csv', index=False)
        except Exception:
            logger.exception('Error al generar pivot')

    # Visualizaciones: NumTotal
    try:
        if 'NumTotal' in df.columns:
            save_histogram(df['NumTotal'], str(OUTPUT_DIR / 'hist_NumTotal.png'), title='Distribución NumTotal')
        if 'EstablecimientoGlosa' in df.columns and 'NumTotal' in df.columns:
            save_boxplot(df, 'EstablecimientoGlosa', 'NumTotal', str(OUTPUT_DIR / 'box_NumTotal_by_establecimiento.png'), title='NumTotal por establecimiento')
    except Exception:
        logger.exception('Error guardando visualizaciones')

    # Guardar procesado
    save_csv(df, str(DATA_PROCESSED))

    # Report después
    report_after = generate_quality_report(df, out_path=str(QUALITY_PATH.with_name('quality_after.json')))
    logger.info('Reporte después generado')

    # Resumen de métricas clave
    metrics = {
        'n_rows_before': report_before.get('n_rows'),
        'n_rows_after': report_after.get('n_rows'),
        'n_duplicates_before': report_before.get('n_duplicates'),
        'n_duplicates_after': report_after.get('n_duplicates')
    }
    import json

    with open('outputs/metrics_summary.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    logger.info('Metrics summary saved')


if __name__ == '__main__':
    main()
