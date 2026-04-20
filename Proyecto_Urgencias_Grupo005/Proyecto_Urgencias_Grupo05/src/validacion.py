"""src.validacion

Funciones para reportes de calidad de datos: nulos, duplicados, validación de esquema
y rangos de valores.
"""
from typing import Dict, Any, Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def report_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna un DataFrame con conteos y porcentaje de valores faltantes por columna."""
    total = len(df)
    missing = df.isna().sum()
    report = pd.DataFrame({
        'column': missing.index,
        'missing_count': missing.values,
        'missing_pct': (missing.values / total) * 100
    })
    return report.sort_values('missing_pct', ascending=False)


def report_duplicates(df: pd.DataFrame, subset: Optional[list] = None) -> int:
    """Retorna el número de filas duplicadas (según subset si se da)."""
    count = int(df.duplicated(subset=subset).sum())
    logger.info("Duplicados detectados: %d (subset=%s)", count, subset)
    return count


def validate_dtypes(df: pd.DataFrame, expected_schema: Dict[str, Any]) -> pd.DataFrame:
    """Compara tipos reales con un esquema esperado y reporta discrepancias."""
    rows = []
    for col, expected in expected_schema.items():
        actual = 'MISSING'
        match = False
        if col in df.columns:
            actual = str(df[col].dtype)
            match = str(expected) == actual
        rows.append({'column': col, 'expected': str(expected), 'actual': actual, 'match': match})
    return pd.DataFrame(rows)


def check_value_ranges(df: pd.DataFrame, col_ranges: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Valida si los valores de columnas numéricas están dentro de rangos y reporta outliers."""
    outliers = {}
    for col, rng in col_ranges.items():
        if col not in df.columns:
            outliers[col] = {'missing_column': True}
            logger.warning("Columna para rango no encontrada: %s", col)
            continue
        s = df[col]
        mask = (~s.isna()) & ((s < rng.get('min', -float('inf'))) | (s > rng.get('max', float('inf'))))
        outliers[col] = {'outlier_count': int(mask.sum()), 'total': int(s.notna().sum())}
    return outliers


def summarize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen rápido de un DataFrame: tipos, nulos y elementos únicos."""
    summary = pd.DataFrame({
        'column': df.columns,
        'dtype': [str(dt) for dt in df.dtypes],
        'n_missing': df.isna().sum().values,
        'n_unique': df.nunique(dropna=True).values
    })
    return summary


def generate_quality_report(df: pd.DataFrame, expected_schema: Optional[Dict[str, Any]] = None, col_ranges: Optional[Dict[str, Dict[str, Any]]] = None, out_path: Optional[str] = None) -> Dict[str, Any]:
    """Genera un reporte de calidad y opcionalmente lo guarda.

    Retorna un diccionario con métricas clave.
    """
    missing_df = report_missing(df)
    dup_count = report_duplicates(df)
    summary = summarize_df(df)
    ranges = check_value_ranges(df, col_ranges) if col_ranges else {}
    dtype_report = validate_dtypes(df, expected_schema) if expected_schema else None

    report = {
        'n_rows': int(df.shape[0]),
        'n_columns': int(df.shape[1]),
        'n_duplicates': int(dup_count),
        'missing_by_column': missing_df.to_dict(orient='records'),
        'dtype_report': dtype_report.to_dict(orient='records') if dtype_report is not None else None,
        'range_checks': ranges
    }
    if out_path:
        import json
        import os

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    return report
