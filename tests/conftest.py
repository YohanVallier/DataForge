"""Pytest configuration and shared fixtures.

This module defines fixtures used across the test suite. Fixtures are kept
small, deterministic, and dependency-light so that tests remain fast and
reproducible.

Fixtures
--------
- :func:`sample_dataframe` — small mixed-type DataFrame for general tests.
- :func:`numeric_dataframe` — numeric-only DataFrame for modeling/plotting.
- :func:`classification_dataframe` — DataFrame suitable for classification.
- :func:`regression_dataframe` — DataFrame suitable for regression.
- :func:`tmp_csv_file` — CSV file written to a temporary directory.
- :func:`tmp_parquet_file` — Parquet file written to a temporary directory.
- :func:`sqlite_database_url` — SQLite connection string in a temp directory.
- :func:`configured_logger` — logger configured for tests.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd
import pytest

from DataScienceProfessionalPortfolio.utils.helpers import get_logger


@pytest.fixture()
def sample_dataframe() -> pd.DataFrame:
    """Return a small mixed-type DataFrame for general-purpose tests.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with numeric, categorical, and date columns.
    """
    return pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5],
            "region": ["North", "South", "North", "East", "South"],
            "revenue": [100.0, 250.5, 175.0, 300.0, 90.25],
            "units": [1, 3, 2, 4, 1],
            "signup_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-04",
                    "2024-01-05",
                ]
            ),
        }
    )


@pytest.fixture()
def numeric_dataframe() -> pd.DataFrame:
    """Return a numeric-only DataFrame with a fixed random seed.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with three numeric columns and 50 rows.
    """
    rng = np.random.default_rng(seed=42)
    return pd.DataFrame(
        {
            "feature_a": rng.normal(loc=0.0, scale=1.0, size=50),
            "feature_b": rng.normal(loc=5.0, scale=2.0, size=50),
            "feature_c": rng.uniform(low=0.0, high=10.0, size=50),
        }
    )


@pytest.fixture()
def classification_dataframe() -> pd.DataFrame:
    """Return a DataFrame suitable for binary classification tests.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two numeric features and a binary target column.
    """
    rng = np.random.default_rng(seed=7)
    n_samples = 100
    feature_a = rng.normal(size=n_samples)
    feature_b = rng.normal(size=n_samples)
    target = (feature_a + feature_b > 0).astype(int)
    return pd.DataFrame(
        {
            "feature_a": feature_a,
            "feature_b": feature_b,
            "target": target,
        }
    )


@pytest.fixture()
def regression_dataframe() -> pd.DataFrame:
    """Return a DataFrame suitable for regression tests.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two numeric features and a continuous target column.
    """
    rng = np.random.default_rng(seed=11)
    n_samples = 100
    feature_a = rng.normal(size=n_samples)
    feature_b = rng.normal(size=n_samples)
    target = 3.0 * feature_a - 2.0 * feature_b + rng.normal(scale=0.1, size=n_samples)
    return pd.DataFrame(
        {
            "feature_a": feature_a,
            "feature_b": feature_b,
            "target": target,
        }
    )


@pytest.fixture()
def tmp_csv_file(
    tmp_path: Path, sample_dataframe: pd.DataFrame
) -> Path:
    """Write the sample DataFrame to a temporary CSV file.

    Parameters
    ----------
    tmp_path:
        Pytest-provided temporary directory.
    sample_dataframe:
        DataFrame to persist.

    Returns
    -------
    pathlib.Path
        Path to the written CSV file.
    """
    csv_path = tmp_path / "sample.csv"
    sample_dataframe.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture()
def tmp_parquet_file(
    tmp_path: Path, sample_dataframe: pd.DataFrame
) -> Path:
    """Write the sample DataFrame to a temporary Parquet file.

    Parameters
    ----------
    tmp_path:
        Pytest-provided temporary directory.
    sample_dataframe:
        DataFrame to persist.

    Returns
    -------
    pathlib.Path
        Path to the written Parquet file.
    """
    parquet_path = tmp_path / "sample.parquet"
    sample_dataframe.to_parquet(parquet_path, index=False)
    return parquet_path


@pytest.fixture()
def sqlite_database_url(tmp_path: Path) -> str:
    """Return a SQLite connection string pointing to a temporary database.

    Parameters
    ----------
    tmp_path:
        Pytest-provided temporary directory.

    Returns
    -------
    str
        A SQLAlchemy-compatible SQLite connection string.
    """
    db_path = tmp_path / "test.db"
    return f"sqlite:///{db_path.as_posix()}"


@pytest.fixture()
def configured_logger() -> Iterator[logging.Logger]:
    """Provide a logger configured for tests and clean up handlers afterwards.

    Yields
    ------
    logging.Logger
        A logger named ``"tests"`` configured at ``DEBUG`` level.
    """
    logger = get_logger("tests", level="DEBUG")
    try:
        yield logger
    finally:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()