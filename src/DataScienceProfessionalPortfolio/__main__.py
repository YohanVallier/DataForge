"""Command-line entry point for DataScienceProfessionalPortfolio.

This module exposes a small, dependency-light CLI that lets users inspect the
framework configuration and run a demonstration ETL pipeline. It is intended
as a smoke-test entry point and as a template for project-specific scripts.

The CLI is exposed as the ``data-science-portfolio`` console script (see
``pyproject.toml``) and can also be invoked as a module::

    python -m DataScienceProfessionalPortfolio --help

Public API
----------
- :func:`main` — parse arguments and dispatch to the selected command.
- :func:`build_parser` — construct the :class:`argparse.ArgumentParser`.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from DataScienceProfessionalPortfolio import __version__
from DataScienceProfessionalPortfolio.services.etl import run_etl_pipeline
from DataScienceProfessionalPortfolio.utils.helpers import get_logger

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "build_parser",
    "main",
]


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser.

    Returns
    -------
    argparse.ArgumentParser
        The configured parser with all supported subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="data-science-portfolio",
        description=(
            "DataScienceProfessionalPortfolio command-line interface. "
            "Inspect configuration and run demonstration workflows."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    subparsers.add_parser(
        "info",
        help="Print framework version and resolved configuration.",
    )

    etl_parser = subparsers.add_parser(
        "etl",
        help="Run a demonstration ETL pipeline from a source to a destination.",
    )
    etl_parser.add_argument(
        "source",
        type=Path,
        help="Path to the source file (CSV or Parquet).",
    )
    etl_parser.add_argument(
        "destination",
        type=Path,
        help="Path to the destination file (CSV or Parquet).",
    )
    etl_parser.add_argument(
        "--missing-strategy",
        default=None,
        choices=["drop", "mean", "median", "zero", "ffill", "bfill"],
        help="Strategy for handling missing values during transformation.",
    )
    etl_parser.add_argument(
        "--no-drop-duplicates",
        action="store_true",
        help="Keep fully duplicated rows instead of dropping them.",
    )

    return parser


def _configure_logging(level: str | None) -> None:
    """Configure the root logger for CLI usage.

    Parameters
    ----------
    level:
        Optional logging level name. When ``None``, the ``LOG_LEVEL``
        environment variable is consulted, falling back to ``"INFO"``.

    Raises
    ------
    ValueError
        If ``level`` is not a recognized logging level.
    """
    try:
        get_logger("DataScienceProfessionalPortfolio", level=level)
    except ValueError as exc:
        raise ValueError(f"Invalid log level: {exc}") from exc


def _run_info() -> int:
    """Print framework version and resolved configuration.

    Returns
    -------
    int
        Process exit code (``0`` on success).
    """
    from config.settings import get_settings

    try:
        settings = get_settings()
    except ValueError as exc:
        logger.error("Failed to load settings: %s", exc)
        return 1

    print(f"DataScienceProfessionalPortfolio {__version__}")
    for key, value in settings.as_dict().items():
        print(f"  {key}: {value}")
    return 0


def _run_etl(args: argparse.Namespace) -> int:
    """Run a demonstration ETL pipeline.

    Parameters
    ----------
    args:
        Parsed command-line arguments for the ``etl`` subcommand.

    Returns
    -------
    int
        Process exit code (``0`` on success, ``1`` on failure).
    """
    try:
        result = run_etl_pipeline(
            args.source,
            args.destination,
            drop_duplicates=not args.no_drop_duplicates,
            missing_strategy=args.missing_strategy,
        )
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("ETL pipeline failed: %s", exc)
        return 1

    print("ETL pipeline completed successfully.")
    for key, value in result.as_dict().items():
        print(f"  {key}: {value}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and dispatch to the selected command.

    Parameters
    ----------
    argv:
        Optional sequence of command-line arguments. When ``None``,
        :data:`sys.argv` is used.

    Returns
    -------
    int
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        _configure_logging(args.log_level)
    except ValueError as exc:
        parser.error(str(exc))

    if args.command == "info":
        return _run_info()
    if args.command == "etl":
        return _run_etl(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())