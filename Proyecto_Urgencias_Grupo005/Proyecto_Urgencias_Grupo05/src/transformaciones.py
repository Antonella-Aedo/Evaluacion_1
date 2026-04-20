"""src.transformaciones

Funciones para transformaciones avanzadas: conversión de tipos, features temporales,
agrupaciones y pivot tables. Diseñado para pipelines y análisis exploratorio.
"""
from typing import List, Dict, Any, Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def convert_types(df: pd.DataFrame, dtype_map: Dict[str, Any]) -> pd.DataFrame:
    """Convierte tipos de columnas según un mapeo proporcionado.

    - Si la conversión falla para fechas, intenta `pd.to_datetime`.
    - Para numéricos usa `pd.to_numeric` con coerción.

    Args:
        df: DataFrame de entrada.
        dtype_map: {col: dtype}

    Returns:
        DataFrame con tipos convertidos.
    """
    for col, dtype in dtype_map.items():
        if col not in df.columns:
            logger.warning("Columna no encontrada para conversión: %s", col)
            continue
        try:
            df[col] = df[col].astype(dtype)
        except Exception:
            logger.debug("Conversión directa falló para %s, intentando coerción", col)
            if str(dtype).startswith("datetime") or dtype in ["datetime64[ns]", "datetime"]:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif dtype in [int, float, 'int', 'float']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                # dejar como está
                logger.debug("No se aplicó conversión adicional para %s", col)
    return df


def create_datetime_features(df: pd.DataFrame, col: str, tz: Optional[str] = None) -> pd.DataFrame:
    """Extrae features temporales de una columna datetime.

    Añade columnas: `{col}_year`, `{col}_month`, `{col}_day`, `{col}_weekday`, `{col}_hour`.
    """
    if col not in df.columns:
        logger.error("Columna datetime no encontrada: %s", col)
        raise KeyError(col)
    df[col] = pd.to_datetime(df[col], errors='coerce')
    if tz:
        try:
            df[col] = df[col].dt.tz_localize(tz)
        except Exception:
            logger.debug("No se pudo localizar zona horaria para %s", col)
    df[f"{col}_year"] = df[col].dt.year
    df[f"{col}_month"] = df[col].dt.month
    df[f"{col}_day"] = df[col].dt.day
    df[f"{col}_weekday"] = df[col].dt.weekday
    df[f"{col}_hour"] = df[col].dt.hour
    return df


def group_aggregate(df: pd.DataFrame, group_cols: List[str], agg_dict: Dict[str, List[str]]) -> pd.DataFrame:
    """Realiza agrupaciones y agregaciones múltiples.

    Args:
        df: DataFrame
        group_cols: columnas de agrupación
        agg_dict: {col: [funcs]}
    """
    missing = [c for c in group_cols if c not in df.columns]
    if missing:
        logger.warning("Columnas de agrupación no encontradas: %s", missing)
    return df.groupby(group_cols).agg(agg_dict).reset_index()


def pivot_table(df: pd.DataFrame, index: List[str], columns: str, values: str, aggfunc: str = 'mean') -> pd.DataFrame:
    """Crea una pivot table y aplana MultiIndex si corresponde."""
    table = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)
    if isinstance(table.columns, pd.MultiIndex):
        table.columns = ['_'.join(map(str, c)).strip() for c in table.columns.values]
    return table.reset_index()


def encode_categoricals(df: pd.DataFrame, cols: List[str], method: str = 'onehot') -> pd.DataFrame:
    """Codifica variables categóricas usando `onehot` o `label`.

    Requiere `scikit-learn` si se escoge `label`.
    """
    if method == 'onehot':
        return pd.get_dummies(df, columns=cols, drop_first=False)
    elif method == 'label':
        try:
            from sklearn.preprocessing import LabelEncoder
        except Exception:
            logger.error("scikit-learn requerido para 'label' encoding")
            raise
        le = LabelEncoder()
        for c in cols:
            df[c] = le.fit_transform(df[c].astype(str))
        return df
    else:
        raise ValueError("method debe ser 'onehot' o 'label'")

