"""Utilidades de visualización y guardado de gráficos."""
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def save_histogram(series: pd.Series, path: str, bins: int = 50, title: Optional[str] = None) -> None:
    plt.figure(figsize=(8, 4))
    sns.histplot(series.dropna(), bins=bins, kde=True)
    if title:
        plt.title(title)
    plt.xlabel(series.name)
    plt.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    plt.close()


def save_boxplot(df: pd.DataFrame, x: str, y: str, path: str, title: Optional[str] = None) -> None:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df.dropna(subset=[x, y]), x=x, y=y)
    if title:
        plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    plt.close()
