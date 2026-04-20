"""src.limpieza

Funciones reutilizables para carga y limpieza básica de DataFrames.

Contiene:
- load_csv
- drop_columns
- impute_missing
- drop_duplicates_rows
- save_csv

Diseñado para uso en notebooks y scripts. Registra errores y valida entradas.
"""
from typing import List, Dict, Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_csv(path: str, **kwargs) -> pd.DataFrame:
    """Carga un CSV en un DataFrame de pandas.

    Args:
        path: Ruta al archivo CSV.
        **kwargs: Argumentos opcionales para `pd.read_csv`.

    Returns:
        pd.DataFrame

    Raises:
        IOError: si la lectura falla.
    """
    try:
        df = pd.read_csv(path, **kwargs)
        logger.info("Archivo cargado: %s — shape=%s", path, df.shape)
        return df
    except Exception as e:
        logger.exception("Error leyendo %s", path)
        raise IOError(f"No se pudo leer el archivo {path}: {e}")


def drop_columns(df: pd.DataFrame, cols: List[str], inplace: bool = False) -> Optional[pd.DataFrame]:
    """Elimina columnas especificadas.

    Args:
        df: DataFrame de entrada.
        cols: Lista de columnas a eliminar.
        inplace: Si True, modifica en sitio.

    Returns:
        DataFrame (si inplace=False) o None.
    """
    missing = [c for c in cols if c not in df.columns]
    if missing:
        logger.warning("Algunas columnas no existen y serán ignoradas: %s", missing)
    return df.drop(columns=[c for c in cols if c in df.columns], inplace=inplace)


def impute_missing(df: pd.DataFrame, strategy: str = "drop", fill_value: Optional[Dict[str, object]] = None) -> pd.DataFrame:
    """Manejo de valores faltantes con dos estrategias.

    Args:
        df: DataFrame de entrada.
        strategy: 'drop' o 'fill'
        fill_value: diccionario {col: value} para rellenar

    Returns:
        DataFrame limpio
    """
    if strategy == "drop":
        result = df.dropna()
        logger.info("Filas con nulos eliminadas. Nuevo shape=%s", result.shape)
        return result
    elif strategy == "fill":
        if fill_value is None:
            logger.error("fill_value no proporcionado para strategy='fill'")
            raise ValueError("fill_value debe proporcionarse cuando strategy='fill'")
        result = df.fillna(value=fill_value)
        logger.info("Valores nulos rellenados con map proporcionado")
        return result
    else:
        logger.error("Strategy desconocida: %s", strategy)
        raise ValueError("strategy debe ser 'drop' o 'fill'")


def impute_column(df: pd.DataFrame, column: str, strategy: str = 'median') -> pd.DataFrame:
    """Imputa una sola columna usando estrategia especificada.

    Args:
        df: DataFrame de entrada.
        column: nombre de la columna a imputar.
        strategy: 'mean', 'median', 'mode' o valor literal.

    Returns:
        DataFrame con la columna imputada.
    """
    if column not in df.columns:
        logger.warning("Columna no encontrada para imputación: %s", column)
        return df
    s = df[column]
    if strategy == 'mean':
        val = s.mean()
    elif strategy == 'median':
        val = s.median()
    elif strategy == 'mode':
        mode = s.mode()
        val = mode.iloc[0] if not mode.empty else None
    else:
        # usar valor literal proporcionado
        val = strategy
    df[column] = s.fillna(val)
    logger.info("Imputada columna %s con estrategia %s (val=%s)", column, strategy, str(val))
    return df


def impute_multiple(df: pd.DataFrame, strategy_map: Dict[str, object]) -> pd.DataFrame:
    """Imputa múltiples columnas según un mapeo {col: strategy}.

    strategy puede ser 'mean', 'median', 'mode' o un valor literal.
    """
    for col, strat in strategy_map.items():
        df = impute_column(df, col, strat)
    return df


def drop_duplicates_rows(df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = 'first') -> pd.DataFrame:
    """Elimina filas duplicadas y retorna el DataFrame resultante.

    Args:
        df: DataFrame de entrada.
        subset: columnas para identificar duplicados.
        keep: 'first', 'last' o False.
    """
    before = df.shape[0]
    result = df.drop_duplicates(subset=subset, keep=keep)
    after = result.shape[0]
    logger.info("Duplicados removidos: %d", before - after)
    return result


def save_csv(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """Guarda DataFrame a CSV.

    Args:
        df: DataFrame a guardar.
        path: Ruta destino.
        index: incluir índice
    """
    try:
        df.to_csv(path, index=index)
        logger.info("Archivo guardado: %s", path)
    except Exception as e:
        logger.exception("Error guardando %s", path)
        raise IOError(f"No se pudo guardar el archivo {path}: {e}")

