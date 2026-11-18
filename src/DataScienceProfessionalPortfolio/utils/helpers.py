"""Shared utility functions for DataScienceProfessionalPortfolio.

This module provides cross-cutting helpers used across the framework:

- :func:`get_logger` — configure and return a module-level logger.
- :func:`ensure_directory` — create a directory (and parents) if missing.
- :func:`resolve_path` — resolve a path relative to a base directory.
- :func:`validate_columns` — assert that required columns exist.
- :func:`timer` — context manager that measures elapsed time.
- :func:`chunked` — iterate over an iterable in fixed-size chunks.
- :func:`safe_divide` — division that returns a default on zero denominator.

All helpers are intentionally dependency-light and free of domain logic so
that they can be reused by every portfolio project.
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence, TypeVar

import pandas as pd

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "chunked",
    "ensure_directory",
    "get_logger",
    "resolve_path",
    "safe_divide",
    "timer",
    "validate_columns",
]

T = TypeVar("T")

_DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_VALID_LOG_LEVELS: frozenset[str] = frozenset(
    {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
)


class LoggerConfigurationError(OSError):
    """Raised when logger configuration fails due to file I/O errors."""

    pass


def get_logger(
    name: str | None = None,
    *,
    level: str | int | None = None,
    log_file: str | Path | None = None,
    fmt: str = _DEFAULT_LOG_FORMAT,
    datefmt: str = _DEFAULT_DATE_FORMAT,
) -> logging.Logger:
    """Return a configured logger.

    The logger is configured with a single :class:`logging.StreamHandler` (and
    optionally a :class:`logging.FileHandler`). Repeated calls for the same
    logger name are idempotent: handlers are only attached once.

    Parameters
    ----------
    name:
        Logger name. If ``None``, the root logger is used.
    level:
        Logging level as a string (e.g. ``"INFO"``) or an integer. If ``None``,
        the ``LOG_LEVEL`` environment variable is consulted, falling back to
        ``"INFO"``.
    log_file:
        Optional path to a log file. Parent directories are created if missing.
        If ``None``, the ``LOG_FILE`` environment variable is consulted.
    fmt:
        Log message format string.
    datefmt:
        Date format string.

    Returns
    -------
    logging.Logger
        The configured logger.

    Raises
    ------
    ValueError
        If ``level`` is a string that does not name a valid logging level.
    LoggerConfigurationError
        If the log file cannot be opened due to permission or I/O errors.
    """
    logger_ = logging.getLogger(name)

    resolved_level = _resolve_log_level(level)
    logger_.setLevel(resolved_level)

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    if not any(isinstance(h, logging.StreamHandler) for h in logger_.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger_.addHandler(stream_handler)

    resolved_file = log_file if log_file is not None else os.getenv("LOG_FILE")
    if resolved_file:
        file_path = Path(resolved_file)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise LoggerConfigurationError(
                f"Failed to create log directory '{file_path.parent}': {exc}"
            ) from exc

        already_attached = any(
            isinstance(h, logging.FileHandler)
            and Path(getattr(h, "baseFilename", "")) == file_path.resolve()
            for h in logger_.handlers
        )
        if not already_attached:
            try:
                file_handler = logging.FileHandler(file_path, encoding="utf-8")
            except OSError as exc:
                raise LoggerConfigurationError(
                    f"Failed to open log file '{file_path}': {exc}"
                ) from exc
            file_handler.setFormatter(formatter)
            logger_.addHandler(file_handler)

    return logger_


def _resolve_log_level(level: str | int | None) -> int:
    """Resolve a logging level from a string, integer, or environment variable.

    Parameters
    ----------
    level:
        Logging level as a string or integer, or ``None`` to consult the
        ``LOG_LEVEL`` environment variable.

    Returns
    -------
    int
        The numeric logging level.

    Raises
    ------
    ValueError
        If a string level is not recognized.
    """
    if isinstance(level, int):
        return level

    candidate = level if level is not None else os.getenv("LOG_LEVEL", "INFO")
    normalized = str(candidate).strip().upper()
    if normalized not in _VALID_LOG_LEVELS:
        raise ValueError(
            f"Invalid log level '{candidate}'. "
            f"Expected one of {sorted(_VALID_LOG_LEVELS)}."
        )
    return getattr(logging, normalized)


def ensure_directory(path: str | Path) -> Path:
    """Create a directory (and any missing parents) if it does not exist.

    Parameters
    ----------
    path:
        Directory path to create.

    Returns
    -------
    pathlib.Path
        The resolved directory path.

    Raises
    ------
    OSError
        If the directory cannot be created.
    """
    directory = Path(path)
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(f"Failed to create directory '{directory}': {exc}") from exc
    return directory


def resolve_path(path: str | Path, *, base: str | Path | None = None) -> Path:
    """Resolve a path, optionally relative to a base directory.

    Absolute paths are returned unchanged. Relative paths are joined to
    ``base`` when provided, otherwise resolved against the current working
    directory.

    Parameters
    ----------
    path:
        Path to resolve.
    base:
        Optional base directory for relative paths.

    Returns
    -------
    pathlib.Path
        The resolved absolute path.
    """
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    if base is not None:
        return (Path(base) / candidate).resolve()
    return candidate.resolve()


def validate_columns(
    df: pd.DataFrame,
    required: Sequence[str],
    *,
    context: str | None = None,
) -> None:
    """Validate that a DataFrame contains all required columns.

    Parameters
    ----------
    df:
        DataFrame to validate.
    required:
        Sequence of column names that must be present.
    context:
        Optional human-readable context included in the error message.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    KeyError
        If any required column is missing.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")

    missing = [col for col in required if col not in df.columns]
    if missing:
        prefix = f"{context}: " if context else ""
        raise KeyError(
            f"{prefix}missing required columns {missing}. "
            f"Available columns: {list(df.columns)}"
        )


@contextmanager
def timer(label: str = "operation") -> Iterator[dict[str, float]]:
    """Context manager that measures elapsed wall-clock time.

    The yielded dictionary is populated with the ``elapsed`` key (in seconds)
    when the context exits, and the duration is logged at ``INFO`` level.

    Parameters
    ----------
    label:
        Human-readable label used in the log message.

    Yields
    ------
    dict[str, float]
        A dictionary that receives the ``elapsed`` duration on exit.

    Examples
    --------
    >>> with timer("load") as t:
    ...     pass
    >>> "elapsed" in t
    True
    """
    result: dict[str, float] = {}
    start = time.perf_counter()
    try:
        yield result
    finally:
        elapsed = time.perf_counter() - start
        result["elapsed"] = elapsed
        logger.info("%s completed in %.4f seconds", label, elapsed)


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists of at most ``size`` items from an iterable.

    Parameters
    ----------
    iterable:
        Source iterable.
    size:
        Maximum chunk size. Must be a positive integer.

    Yields
    ------
    list[T]
        Chunks of the input iterable.

    Raises
    ------
    ValueError
        If ``size`` is not a positive integer.
    """
    if not isinstance(size, int) or size <= 0:
        raise ValueError(f"size must be a positive integer, got {size!r}")

    chunk: list[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def safe_divide(
    numerator: float,
    denominator: float,
    *,
    default: float = 0.0,
) -> float:
    """Divide two numbers, returning ``default`` when the denominator is zero.

    Parameters
    ----------
    numerator:
        Numerator value.
    denominator:
        Denominator value.
    default:
        Value returned when ``denominator`` is zero.

    Returns
    -------
    float
        The quotient, or ``default`` when division is undefined.
    """
    if denominator == 0:
        return default
    return numerator / denominator


def to_dict_safe(obj: Any) -> dict[str, Any]:
    """Best-effort conversion of an object to a plain dictionary.

    Parameters
    ----------
    obj:
        Object to convert. If it exposes ``as_dict`` or ``to_dict``, that
        method is used. If it is already a mapping, a shallow copy is returned.

    Returns
    -------
    dict[str, Any]
        A dictionary representation of ``obj``.

    Raises
    ------
    TypeError
        If ``obj`` cannot be converted to a dictionary.
    """
    if isinstance(obj, dict):
        return dict(obj)
    for method_name in ("as_dict", "to_dict"):
        method = getattr(obj, method_name, None)
        if callable(method):
            result = method()
            if isinstance(result, dict):
                return result
    raise TypeError(f"Cannot convert object of type {type(obj).__name__} to dict")