"""Data manipulation and handling utilities.

This module provides reusable functions for loading, inspecting, cleaning, and
preprocessing tabular data with :mod:`pandas`. It is intentionally free of
domain-specific logic so that it can be shared across portfolio projects.

Public API
----------
- :func:`load_csv` — load a CSV file into a :class:`pandas.DataFrame`.
- :func:`load_parquet` — load a Parquet file into a :class:`pandas.DataFrame`.
- :func:`save_dataframe` — persist a DataFrame to CSV or Parquet.
- :func:`clean_dataframe` — normalize column names, drop duplicates, and
  handle missing values.
- :func:`split_features_target` — split a DataFrame into features and target.
- :func:`train_test_split_df` — convenience wrapper around scikit-learn's
  ``train_test_split`` that returns DataFrames.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal, Sequence

import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "clean_dataframe",
    "load_csv",
    "load_parquet",
    "save_dataframe",
    "split_features_target",
    "train_test_split_df",
]

_MissingStrategy = Literal["drop", "mean", "median", "zero", "ffill", "bfill"]


def load_csv(
    path: str | Path,
    *,
    sep: str = ",",
    encoding: str = "utf-8",
    dtype: dict[str, Any] | None = None,
    parse_dates: Sequence[str] | None = None,
    **read_csv_kwargs: Any,
) -> pd.DataFrame:
    """Load a CSV file into a :class:`pandas.DataFrame`.

    Parameters
    ----------
    path:
        Path to the CSV file.
    sep:
        Field delimiter. Defaults to ``","``.
    encoding:
        File encoding. Defaults to ``"utf-8"``.
    dtype:
        Optional mapping of column names to dtypes.
    parse_dates:
        Optional sequence of column names to parse as dates.
    **read_csv_kwargs:
        Additional keyword arguments forwarded to :func:`pandas.read_csv`.

    Returns
    -------
    pandas.DataFrame
        The loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be parsed as CSV.
    """
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info("Loading CSV file: %s", csv_path)
    try:
        df = pd.read_csv(
            csv_path,
            sep=sep,
            encoding=encoding,
            dtype=dtype,
            parse_dates=list(parse_dates) if parse_dates else None,
            **read_csv_kwargs,
        )
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to parse CSV file '{csv_path}': {exc}") from exc

    logger.info("Loaded CSV with shape %s", df.shape)
    return df


def load_parquet(
    path: str | Path,
    *,
    columns: Sequence[str] | None = None,
    **read_parquet_kwargs: Any,
) -> pd.DataFrame:
    """Load a Parquet file into a :class:`pandas.DataFrame`.

    Parameters
    ----------
    path:
        Path to the Parquet file.
    columns:
        Optional subset of columns to read.
    **read_parquet_kwargs:
        Additional keyword arguments forwarded to :func:`pandas.read_parquet`.

    Returns
    -------
    pandas.DataFrame
        The loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be parsed as Parquet.
    """
    parquet_path = Path(path)
    if not parquet_path.is_file():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    logger.info("Loading Parquet file: %s", parquet_path)
    try:
        df = pd.read_parquet(
            parquet_path,
            columns=list(columns) if columns else None,
            **read_parquet_kwargs,
        )
    except (OSError, ValueError) as exc:
        raise ValueError(
            f"Failed to read Parquet file '{parquet_path}': {exc}"
        ) from exc

    logger.info("Loaded Parquet with shape %s", df.shape)
    return df


def save_dataframe(
    df: pd.DataFrame,
    path: str | Path,
    *,
    fmt: Literal["csv", "parquet"] | None = None,
    index: bool = False,
    **to_kwargs: Any,
) -> Path:
    """Persist a DataFrame to disk as CSV or Parquet.

    Parameters
    ----------
    df:
        DataFrame to persist.
    path:
        Destination path. Parent directories are created if missing.
    fmt:
        Output format. If ``None``, inferred from the file suffix.
    index:
        Whether to write the DataFrame index. Defaults to ``False``.
    **to_kwargs:
        Additional keyword arguments forwarded to the writer.

    Returns
    -------
    pathlib.Path
        The path where the file was written.

    Raises
    ------
    ValueError
        If the format cannot be inferred or is unsupported.
    OSError
        If the file cannot be written.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")

    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    resolved_fmt = fmt or dest.suffix.lstrip(".").lower()
    if resolved_fmt not in {"csv", "parquet"}:
        raise ValueError(
            f"Unsupported output format '{resolved_fmt}'. "
            "Use 'csv' or 'parquet'."
        )

    logger.info("Saving DataFrame (%s) to %s as %s", df.shape, dest, resolved_fmt)
    try:
        if resolved_fmt == "csv":
            df.to_csv(dest, index=index, **to_kwargs)
        else:
            df.to_parquet(dest, index=index, **to_kwargs)
    except OSError as exc:
        raise OSError(f"Failed to write file '{dest}': {exc}") from exc

    return dest


def clean_dataframe(
    df: pd.DataFrame,
    *,
    normalize_columns: bool = True,
    drop_duplicates: bool = True,
    missing_strategy: _MissingStrategy | None = None,
    subset_columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Clean a DataFrame using a configurable, non-destructive pipeline.

    The function returns a new DataFrame; the input is never mutated.

    Parameters
    ----------
    df:
        Input DataFrame.
    normalize_columns:
        If ``True``, strip whitespace, lowercase, and replace spaces with
        underscores in column names.
    drop_duplicates:
        If ``True``, drop fully duplicated rows.
    missing_strategy:
        Strategy for handling missing values. One of ``"drop"``, ``"mean"``,
        ``"median"``, ``"zero"``, ``"ffill"``, ``"bfill"``, or ``None`` to
        leave missing values untouched.
    subset_columns:
        Optional subset of columns to apply the missing-value strategy to.
        If ``None``, all columns are considered.

    Returns
    -------
    pandas.DataFrame
        A cleaned copy of the input DataFrame.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    ValueError
        If ``missing_strategy`` is not recognized.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")

    cleaned = df.copy()

    if normalize_columns:
        cleaned.columns = [
            str(col).strip().lower().replace(" ", "_") for col in cleaned.columns
        ]

    if drop_duplicates:
        before = len(cleaned)
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        logger.debug("Dropped %d duplicate rows", before - len(cleaned))

    if missing_strategy is not None:
        cleaned = _apply_missing_strategy(
            cleaned, strategy=missing_strategy, subset=subset_columns
        )

    logger.info("Cleaned DataFrame with shape %s", cleaned.shape)
    return cleaned


def _apply_missing_strategy(
    df: pd.DataFrame,
    *,
    strategy: _MissingStrategy,
    subset: Sequence[str] | None,
) -> pd.DataFrame:
    """Apply a missing-value strategy to a DataFrame.

    Parameters
    ----------
    df:
        DataFrame to process (already a copy).
    strategy:
        Missing-value strategy.
    subset:
        Optional subset of columns to target.

    Returns
    -------
    pandas.DataFrame
        The processed DataFrame.

    Raises
    ------
    ValueError
        If the strategy is not recognized.
    """
    columns = list(subset) if subset else list(df.columns)

    if strategy == "drop":
        return df.dropna(subset=columns).reset_index(drop=True)
    if strategy == "mean":
        numeric_cols = df[columns].select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        return df
    if strategy == "median":
        numeric_cols = df[columns].select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        return df
    if strategy == "zero":
        df[columns] = df[columns].fillna(0)
        return df
    if strategy == "ffill":
        df[columns] = df[columns].ffill()
        return df
    if strategy == "bfill":
        df[columns] = df[columns].bfill()
        return df

    raise ValueError(f"Unknown missing-value strategy: {strategy!r}")


def split_features_target(
    df: pd.DataFrame,
    target: str,
    *,
    drop_columns: Sequence[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """Split a DataFrame into features (``X``) and target (``y``).

    Parameters
    ----------
    df:
        Input DataFrame containing the target column.
    target:
        Name of the target column.
    drop_columns:
        Optional additional columns to exclude from the features.

    Returns
    -------
    tuple[pandas.DataFrame, pandas.Series]
        A ``(X, y)`` tuple.

    Raises
    ------
    KeyError
        If the target column is not present in ``df``.
    """
    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found in DataFrame")

    excluded = {target, *(drop_columns or [])}
    feature_columns = [col for col in df.columns if col not in excluded]

    X = df[feature_columns].copy()
    y = df[target].copy()
    logger.debug("Split features %s and target '%s'", X.shape, target)
    return X, y


def train_test_split_df(
    df: pd.DataFrame,
    target: str,
    *,
    test_size: float = 0.2,
    random_state: int | None = 42,
    stratify: bool = False,
    drop_columns: Sequence[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split a DataFrame into train/test feature and target sets.

    Parameters
    ----------
    df:
        Input DataFrame.
    target:
        Name of the target column.
    test_size:
        Proportion of the dataset to include in the test split.
    random_state:
        Seed for reproducibility.
    stratify:
        If ``True``, stratify the split by the target column.
    drop_columns:
        Optional additional columns to exclude from the features.

    Returns
    -------
    tuple[pandas.DataFrame, pandas.DataFrame, pandas.Series, pandas.Series]
        ``(X_train, X_test, y_train, y_test)``.

    Raises
    ------
    KeyError
        If the target column is not present in ``df``.
    """
    if target not in df.columns:
        raise KeyError(
            f"Target column '{target}' not found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )

    X, y = split_features_target(df, target, drop_columns=drop_columns)
    stratify_arg = y if stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_arg,
    )
    logger.info(
        "Train/test split complete: train=%s, test=%s",
        X_train.shape,
        X_test.shape,
    )
    return X_train, X_test, y_train, y_test