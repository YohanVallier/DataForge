"""Centralized configuration settings for DataForge.

This module provides a single, importable source of truth for configuration
values used across the framework. All values are read from environment
variables (with sensible defaults) so that no secrets are ever hardcoded and
the same code can run in development, staging, and production.

Public API
----------
- :class:`Settings` — immutable configuration container.
- :func:`get_settings` — return the cached :class:`Settings` instance.
- :func:`reload_settings` — clear the cache and re-read the environment.

Environment variables
---------------------
- ``APP_ENV`` — ``development`` | ``staging`` | ``production``.
- ``LOG_LEVEL`` — ``DEBUG`` | ``INFO`` | ``WARNING`` | ``ERROR`` | ``CRITICAL``.
- ``LOG_FILE`` — optional path to a log file.
- ``DATABASE_URL`` — SQLAlchemy-compatible connection string.
- ``API_BASE_URL`` — base URL for external APIs.
- ``API_KEY`` — API key for external services (never commit real values).
- ``API_TIMEOUT_SECONDS`` — request timeout in seconds.
- ``DATA_RAW_DIR`` — directory for raw data.
- ``DATA_INTERIM_DIR`` — directory for interim data.
- ``DATA_PROCESSED_DIR`` — directory for processed data.
- ``REPORTS_DIR`` — directory for generated reports and figures.
- ``RANDOM_SEED`` — seed for reproducibility.
- ``STREAMLIT_SERVER_PORT`` — port for local Streamlit dashboards.

Usage
-----
>>> from config.settings import get_settings
>>> settings = get_settings()
>>> settings.log_level
'INFO'
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Final, Literal

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "Settings",
    "get_settings",
    "reload_settings",
]

AppEnv = Literal["development", "staging", "production"]

_VALID_APP_ENVS: Final[frozenset[str]] = frozenset(
    {"development", "staging", "production"}
)
_VALID_LOG_LEVELS: Final[frozenset[str]] = frozenset(
    {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
)

_PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent


def _get_env(name: str, default: str | None = None) -> str | None:
    """Read an environment variable, treating empty strings as unset.

    Parameters
    ----------
    name:
        Name of the environment variable.
    default:
        Value returned when the variable is unset or empty.

    Returns
    -------
    str | None
        The resolved value, or ``default``.
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _get_int_env(name: str, default: int) -> int:
    """Read an integer environment variable.

    Parameters
    ----------
    name:
        Name of the environment variable.
    default:
        Value returned when the variable is unset or empty.

    Returns
    -------
    int
        The parsed integer value.

    Raises
    ------
    ValueError
        If the variable is set but cannot be parsed as an integer.
    """
    raw = _get_env(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable '{name}' must be an integer, got {raw!r}"
        ) from exc


def _get_float_env(name: str, default: float) -> float:
    """Read a float environment variable.

    Parameters
    ----------
    name:
        Name of the environment variable.
    default:
        Value returned when the variable is unset or empty.

    Returns
    -------
    float
        The parsed float value.

    Raises
    ------
    ValueError
        If the variable is set but cannot be parsed as a float.
    """
    raw = _get_env(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable '{name}' must be a number, got {raw!r}"
        ) from exc


def _resolve_path(raw: str | None, default: str) -> Path:
    """Resolve a path relative to the project root when not absolute.

    Parameters
    ----------
    raw:
        Raw path string from the environment, or ``None``.
    default:
        Default relative path used when ``raw`` is ``None``.

    Returns
    -------
    pathlib.Path
        The resolved absolute path.
    """
    candidate = Path(raw if raw is not None else default)
    if candidate.is_absolute():
        return candidate
    return (_PROJECT_ROOT / candidate).resolve()


@dataclass(frozen=True)
class Settings:
    """Immutable configuration container.

    Attributes
    ----------
    app_env:
        Application environment (``development``, ``staging``, ``production``).
    log_level:
        Logging level name (e.g. ``"INFO"``).
    log_file:
        Optional path to a log file. ``None`` when logging to stderr only.
    database_url:
        SQLAlchemy-compatible connection string.
    api_base_url:
        Base URL for external APIs, or ``None`` when not configured.
    api_key:
        API key for external services, or ``None`` when not configured.
    api_timeout_seconds:
        Request timeout in seconds for external APIs.
    data_raw_dir:
        Directory for raw data.
    data_interim_dir:
        Directory for interim data.
    data_processed_dir:
        Directory for processed data.
    reports_dir:
        Directory for generated reports and figures.
    random_seed:
        Seed used for reproducibility across experiments.
    streamlit_server_port:
        Port used when running Streamlit dashboards locally.
    project_root:
        Absolute path to the project root directory.
    """

    app_env: AppEnv
    log_level: str
    log_file: Path | None
    database_url: str
    api_base_url: str | None
    api_key: str | None
    api_timeout_seconds: float
    data_raw_dir: Path
    data_interim_dir: Path
    data_processed_dir: Path
    reports_dir: Path
    random_seed: int
    streamlit_server_port: int
    project_root: Path = field(default=_PROJECT_ROOT)

    @property
    def is_production(self) -> bool:
        """Return ``True`` when running in the production environment."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Return ``True`` when running in the development environment."""
        return self.app_env == "development"

    def as_dict(self) -> dict[str, object]:
        """Return a dictionary representation of the settings.

        Sensitive values (``api_key``) are redacted.

        Returns
        -------
        dict[str, object]
            A dictionary representation with secrets redacted.
        """
        return {
            "app_env": self.app_env,
            "log_level": self.log_level,
            "log_file": str(self.log_file) if self.log_file else None,
            "database_url": self.database_url,
            "api_base_url": self.api_base_url,
            "api_key": "***" if self.api_key else None,
            "api_timeout_seconds": self.api_timeout_seconds,
            "data_raw_dir": str(self.data_raw_dir),
            "data_interim_dir": str(self.data_interim_dir),
            "data_processed_dir": str(self.data_processed_dir),
            "reports_dir": str(self.reports_dir),
            "random_seed": self.random_seed,
            "streamlit_server_port": self.streamlit_server_port,
            "project_root": str(self.project_root),
        }


def _build_settings() -> Settings:
    """Build a :class:`Settings` instance from the current environment.

    Returns
    -------
    Settings
        The constructed settings object.

    Raises
    ------
    ValueError
        If any environment variable has an invalid value.
    """
    app_env_raw = (_get_env("APP_ENV", "development") or "development").lower()
    if app_env_raw not in _VALID_APP_ENVS:
        raise ValueError(
            f"Invalid APP_ENV '{app_env_raw}'. "
            f"Expected one of {sorted(_VALID_APP_ENVS)}."
        )

    log_level_raw = (_get_env("LOG_LEVEL", "INFO") or "INFO").upper()
    if log_level_raw not in _VALID_LOG_LEVELS:
        raise ValueError(
            f"Invalid LOG_LEVEL '{log_level_raw}'. "
            f"Expected one of {sorted(_VALID_LOG_LEVELS)}."
        )

    log_file_raw = _get_env("LOG_FILE")
    log_file = _resolve_path(log_file_raw, "logs/app.log") if log_file_raw else None

    database_url = _get_env("DATABASE_URL", "sqlite:///./data/local.db")
    if not database_url:
        raise ValueError("DATABASE_URL must be a non-empty string")

    settings = Settings(
        app_env=app_env_raw,  # type: ignore[arg-type]
        log_level=log_level_raw,
        log_file=log_file,
        database_url=database_url,
        api_base_url=_get_env("API_BASE_URL"),
        api_key=_get_env("API_KEY"),
        api_timeout_seconds=_get_float_env("API_TIMEOUT_SECONDS", 30.0),
        data_raw_dir=_resolve_path(_get_env("DATA_RAW_DIR"), "data/raw"),
        data_interim_dir=_resolve_path(_get_env("DATA_INTERIM_DIR"), "data/interim"),
        data_processed_dir=_resolve_path(
            _get_env("DATA_PROCESSED_DIR"), "data/processed"
        ),
        reports_dir=_resolve_path(_get_env("REPORTS_DIR"), "reports"),
        random_seed=_get_int_env("RANDOM_SEED", 42),
        streamlit_server_port=_get_int_env("STREAMLIT_SERVER_PORT", 8501),
    )

    logger.debug("Settings loaded: %s", settings.as_dict())
    return settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached :class:`Settings` instance.

    The settings are read from the environment on first call and cached for
    the lifetime of the process. Use :func:`reload_settings` to force a
    re-read.

    Returns
    -------
    Settings
        The cached settings object.

    Raises
    ------
    ValueError
        If any environment variable has an invalid value.
    """
    return _build_settings()


def reload_settings() -> Settings:
    """Clear the settings cache and re-read the environment.

    Returns
    -------
    Settings
        The freshly loaded settings object.

    Raises
    ------
    ValueError
        If any environment variable has an invalid value.
    """
    get_settings.cache_clear()
    logger.info("Settings cache cleared; reloading from environment")
    return get_settings()
</｜｜DSML｜｜>