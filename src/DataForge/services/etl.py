"""ETL pipeline definitions.

This module provides reusable building blocks for Extract-Transform-Load (ETL)
workflows. It is intentionally generic so that it can be shared across
portfolio projects, while still offering sensible defaults for common tasks
(reading CSV/Parquet/SQL sources, applying a cleaning step, and persisting the
result).

Public API
----------
- :func:`extract` — read data from a CSV, Parquet, or SQL source.
- :func:`transform` — apply a configurable transformation pipeline.
- :func:`load` — persist a DataFrame to CSV, Parquet, or a SQL database.
- :func:`run_etl_pipeline` — orchestrate extract → transform → load.
- :class:`ETLResult` — structured result of a pipeline run.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal, Sequence

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from DataForge.core.data_handling import (
    clean_dataframe,
    load_csv,
    load_parquet,
    save_dataframe,
)

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "ETLResult",
    "extract",
    "load",
    "run_etl_pipeline",
    "transform",
]

SourceType = Literal["csv", "parquet", "sql"]
DestinationType = Literal["csv", "parquet", "sql"]
MissingStrategy = Literal["drop", "mean", "median", "zero", "ffill", "bfill"]

TransformStep = Callable[[pd.DataFrame], pd.DataFrame]


class SourceTypeError(ValueError):
    """Raised when a source type cannot be determined or is unsupported."""

    pass


class DestinationTypeError(ValueError):
    """Raised when a destination type cannot be determined or is unsupported."""

    pass


@dataclass
class ETLResult:
    """Structured result of an ETL pipeline run.

    Attributes
    ----------
    source:
        Human-readable description of the data source.
    destination:
        Human-readable description of the data destination.
    rows_extracted:
        Number of rows read from the source.
    rows_loaded:
        Number of rows written to the destination.
    columns:
        Column names of the loaded DataFrame.
    steps_applied:
        Names of the transformation steps that were applied.
    """

    source: str
    destination: str
    rows_extracted: int
    rows_loaded: int
    columns: list[str] = field(default_factory=list)
    steps_applied: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        """Return the result as a plain dictionary.

        Returns
        -------
        dict[str, Any]
            A dictionary representation of the result.
        """
        return {
            "source": self.source,
            "destination": self.destination,
            "rows_extracted": self.rows_extracted,
            "rows_loaded": self.rows_loaded,
            "columns": list(self.columns),
            "steps_applied": list(self.steps_applied),
        }


def _build_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine from a connection string.

    Parameters
    ----------
    database_url:
        SQLAlchemy-compatible connection string.

    Returns
    -------
    sqlalchemy.engine.Engine
        The created engine.

    Raises
    ------
    ValueError
        If the connection string is empty or invalid.
    """
    if not database_url or not isinstance(database_url, str):
        raise ValueError("database_url must be a non-empty string")
    try:
        return create_engine(database_url, future=True)
    except SQLAlchemyError as exc:
        raise ValueError(
            f"Failed to create database engine for URL '{database_url}': {exc}"
        ) from exc


def _infer_source_type(source: str | Path) -> SourceType:
    """Infer the source type from a file path.

    Parameters
    ----------
    source:
        Path to a file.

    Returns
    -------
    SourceType
        The inferred source type.

    Raises
    ------
    SourceTypeError
        If the source type cannot be inferred from the file suffix.
    """
    suffix = Path(source).suffix.lstrip(".").lower()
    if suffix in {"csv", "parquet"}:
        return suffix  # type: ignore[return-value]
    raise SourceTypeError(
        f"Cannot infer source type from '{source}'. "
        f"File suffix '{suffix}' is not recognized. "
        f"Supported formats: csv, parquet. "
        f"For SQL sources, provide source_type explicitly."
    )


def extract(
    source: str | Path,
    *,
    source_type: SourceType | None = None,
    query: str | None = None,
    table: str | None = None,
    database_url: str | None = None,
    **read_kwargs: Any,
) -> pd.DataFrame:
    """Extract data from a CSV, Parquet, or SQL source.

    Parameters
    ----------
    source:
        Path to a CSV/Parquet file, or a SQL query/table identifier when
        ``source_type="sql"``. For SQL sources, ``source`` is ignored in favor
        of ``query`` or ``table``.
    source_type:
        Explicit source type. If ``None``, inferred from the file suffix for
        file-based sources. SQL sources must be declared explicitly.
    query:
        SQL query to execute when ``source_type="sql"``.
    table:
        Table name to read when ``source_type="sql"`` and ``query`` is not
        provided.
    database_url:
        SQLAlchemy connection string, required for SQL sources.
    **read_kwargs:
        Additional keyword arguments forwarded to the underlying reader.

    Returns
    -------
    pandas.DataFrame
        The extracted DataFrame.

    Raises
    ------
    SourceTypeError
        If the source type cannot be inferred or is unsupported.
    ValueError
        If required arguments are missing for the selected source type.
    FileNotFoundError
        If a file-based source does not exist.
    """
    resolved_type = source_type
    if resolved_type is None:
        try:
            resolved_type = _infer_source_type(source)
        except SourceTypeError as exc:
            logger.error("Failed to infer source type: %s", exc)
            raise

    logger.info("Extracting data from %s source: %s", resolved_type, source)

    if resolved_type == "csv":
        try:
            return load_csv(source, **read_kwargs)
        except (FileNotFoundError, ValueError) as exc:
            logger.error("Failed to extract from CSV source: %s", exc)
            raise
    if resolved_type == "parquet":
        try:
            return load_parquet(source, **read_kwargs)
        except (FileNotFoundError, ValueError) as exc:
            logger.error("Failed to extract from Parquet source: %s", exc)
            raise
    if resolved_type == "sql":
        if database_url is None:
            raise ValueError("database_url is required for SQL sources")
        if query is None and table is None:
            raise ValueError(
                "Either 'query' or 'table' must be provided for SQL sources"
            )
        engine = _build_engine(database_url)
        try:
            if query is not None:
                with engine.connect() as conn:
                    df = pd.read_sql(text(query), conn, **read_kwargs)
            else:
                df = pd.read_sql_table(table, engine, **read_kwargs)  # type: ignore[arg-type]
        except SQLAlchemyError as exc:
            logger.error("Failed to read from SQL source: %s", exc)
            raise ValueError(f"Failed to read from SQL source: {exc}") from exc
        logger.info("Extracted SQL data with shape %s", df.shape)
        return df

    raise SourceTypeError(f"Unsupported source type: {resolved_type!r}")


def transform(
    df: pd.DataFrame,
    *,
    normalize_columns: bool = True,
    drop_duplicates: bool = True,
    missing_strategy: MissingStrategy | None = None,
    subset_columns: Sequence[str] | None = None,
    steps: Sequence[tuple[str, TransformStep]] | None = None,
) -> pd.DataFrame:
    """Apply a configurable transformation pipeline to a DataFrame.

    The function first applies the standard cleaning step from
    :func:`DataForge.core.data_handling.clean_dataframe`,
    then applies any additional custom transformation steps in order.

    Parameters
    ----------
    df:
        Input DataFrame.
    normalize_columns:
        Whether to normalize column names.
    drop_duplicates:
        Whether to drop fully duplicated rows.
    missing_strategy:
        Strategy for handling missing values.
    subset_columns:
        Optional subset of columns to target for missing-value handling.
    steps:
        Optional sequence of ``(name, callable)`` transformation steps. Each
        callable receives a DataFrame and must return a DataFrame.

    Returns
    -------
    pandas.DataFrame
        The transformed DataFrame.

    Raises
    ------
    TypeError
        If a transformation step does not return a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")

    transformed = clean_dataframe(
        df,
        normalize_columns=normalize_columns,
        drop_duplicates=drop_duplicates,
        missing_strategy=missing_strategy,
        subset_columns=subset_columns,
    )

    for name, step in steps or []:
        logger.info("Applying transformation step: %s", name)
        result = step(transformed)
        if not isinstance(result, pd.DataFrame):
            raise TypeError(
                f"Transformation step '{name}' must return a pandas.DataFrame, "
                f"got {type(result).__name__}"
            )
        transformed = result

    logger.info("Transformation complete with shape %s", transformed.shape)
    return transformed


def _infer_destination_type(destination: str | Path) -> DestinationType:
    """Infer the destination type from a file path.

    Parameters
    ----------
    destination:
        Path to a file.

    Returns
    -------
    DestinationType
        The inferred destination type.

    Raises
    ------
    DestinationTypeError
        If the destination type cannot be inferred from the file suffix.
    """
    suffix = Path(destination).suffix.lstrip(".").lower()
    if suffix in {"csv", "parquet"}:
        return suffix  # type: ignore[return-value]
    raise DestinationTypeError(
        f"Cannot infer destination type from '{destination}'. "
        f"File suffix '{suffix}' is not recognized. "
        f"Supported formats: csv, parquet. "
        f"For SQL destinations, provide destination_type explicitly."
    )


def load(
    df: pd.DataFrame,
    destination: str | Path,
    *,
    destination_type: DestinationType | None = None,
    table: str | None = None,
    database_url: str | None = None,
    if_exists: Literal["fail", "replace", "append"] = "replace",
    index: bool = False,
    **write_kwargs: Any,
) -> Path | str:
    """Persist a DataFrame to a CSV, Parquet, or SQL destination.

    Parameters
    ----------
    df:
        DataFrame to persist.
    destination:
        File path for file-based destinations. Ignored for SQL destinations.
    destination_type:
        Explicit destination type. If ``None``, inferred from the file suffix
        for file-based destinations. SQL destinations must be declared
        explicitly.
    table:
        Target table name for SQL destinations.
    database_url:
        SQLAlchemy connection string, required for SQL destinations.
    if_exists:
        Behavior when the SQL table already exists.
    index:
        Whether to write the DataFrame index for file-based destinations.
    **write_kwargs:
        Additional keyword arguments forwarded to the underlying writer.

    Returns
    -------
    pathlib.Path | str
        The file path for file-based destinations, or the table name for SQL
        destinations.

    Raises
    ------
    DestinationTypeError
        If the destination type cannot be inferred or is unsupported.
    ValueError
        If required arguments are missing for the selected destination type.
    """
    resolved_type = destination_type
    if resolved_type is None:
        try:
            resolved_type = _infer_destination_type(destination)
        except DestinationTypeError as exc:
            logger.error("Failed to infer destination type: %s", exc)
            raise

    logger.info("Loading data into %s destination: %s", resolved_type, destination)

    if resolved_type in {"csv", "parquet"}:
        try:
            return save_dataframe(
                df,
                destination,
                fmt=resolved_type,  # type: ignore[arg-type]
                index=index,
                **write_kwargs,
            )
        except (OSError, ValueError) as exc:
            logger.error("Failed to load to file destination: %s", exc)
            raise

    if resolved_type == "sql":
        if database_url is None:
            raise ValueError("database_url is required for SQL destinations")
        if table is None:
            raise ValueError("table is required for SQL destinations")
        engine = _build_engine(database_url)
        try:
            df.to_sql(
                table,
                engine,
                if_exists=if_exists,
                index=index,
                **write_kwargs,
            )
        except SQLAlchemyError as exc:
            logger.error("Failed to write to SQL destination: %s", exc)
            raise ValueError(f"Failed to write to SQL destination: {exc}") from exc
        logger.info("Loaded %d rows into table '%s'", len(df), table)
        return table

    raise DestinationTypeError(f"Unsupported destination type: {resolved_type!r}")


def run_etl_pipeline(
    source: str | Path,
    destination: str | Path,
    *,
    source_type: SourceType | None = None,
    destination_type: DestinationType | None = None,
    source_query: str | None = None,
    source_table: str | None = None,
    source_database_url: str | None = None,
    destination_table: str | None = None,
    destination_database_url: str | None = None,
    if_exists: Literal["fail", "replace", "append"] = "replace",
    normalize_columns: bool = True,
    drop_duplicates: bool = True,
    missing_strategy: MissingStrategy | None = None,
    subset_columns: Sequence[str] | None = None,
    steps: Sequence[tuple[str, TransformStep]] | None = None,
    read_kwargs: dict[str, Any] | None = None,
    write_kwargs: dict[str, Any] | None = None,
) -> ETLResult:
    """Run a complete extract → transform → load pipeline.

    Parameters
    ----------
    source:
        Data source (file path or SQL identifier).
    destination:
        Data destination (file path or SQL identifier).
    source_type:
        Explicit source type. Inferred from the file suffix when ``None``.
    destination_type:
        Explicit destination type. Inferred from the file suffix when ``None``.
    source_query:
        SQL query for SQL sources.
    source_table:
        SQL table name for SQL sources.
    source_database_url:
        SQLAlchemy connection string for SQL sources.
    destination_table:
        SQL table name for SQL destinations.
    destination_database_url:
        SQLAlchemy connection string for SQL destinations.
    if_exists:
        Behavior when the SQL destination table already exists.
    normalize_columns:
        Whether to normalize column names during transformation.
    drop_duplicates:
        Whether to drop fully duplicated rows during transformation.
    missing_strategy:
        Strategy for handling missing values during transformation.
    subset_columns:
        Optional subset of columns to target for missing-value handling.
    steps:
        Optional sequence of custom ``(name, callable)`` transformation steps.
    read_kwargs:
        Additional keyword arguments forwarded to the extractor.
    write_kwargs:
        Additional keyword arguments forwarded to the loader.

    Returns
    -------
    ETLResult
        Structured summary of the pipeline run.

    Raises
    ------
    SourceTypeError
        If the source type cannot be inferred or is unsupported.
    DestinationTypeError
        If the destination type cannot be inferred or is unsupported.
    ValueError
        If any stage fails due to invalid configuration.
    """
    logger.info("Starting ETL pipeline: %s -> %s", source, destination)

    try:
        raw_df = extract(
            source,
            source_type=source_type,
            query=source_query,
            table=source_table,
            database_url=source_database_url,
            **(read_kwargs or {}),
        )
    except (SourceTypeError, ValueError, FileNotFoundError) as exc:
        logger.error("ETL pipeline failed at extract stage: %s", exc)
        raise

    rows_extracted = len(raw_df)

    try:
        transformed_df = transform(
            raw_df,
            normalize_columns=normalize_columns,
            drop_duplicates=drop_duplicates,
            missing_strategy=missing_strategy,
            subset_columns=subset_columns,
            steps=steps,
        )
    except (TypeError, ValueError) as exc:
        logger.error("ETL pipeline failed at transform stage: %s", exc)
        raise

    try:
        load(
            transformed_df,
            destination,
            destination_type=destination_type,
            table=destination_table,
            database_url=destination_database_url,
            if_exists=if_exists,
            **(write_kwargs or {}),
        )
    except (DestinationTypeError, ValueError, OSError) as exc:
        logger.error("ETL pipeline failed at load stage: %s", exc)
        raise

    result = ETLResult(
        source=str(source),
        destination=str(destination),
        rows_extracted=rows_extracted,
        rows_loaded=len(transformed_df),
        columns=list(transformed_df.columns),
        steps_applied=[name for name, _ in (steps or [])],
    )
    logger.info(
        "ETL pipeline complete: extracted=%d, loaded=%d",
        result.rows_extracted,
        result.rows_loaded,
    )
    return result