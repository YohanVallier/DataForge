# Changelog

All notable changes to **DataForge** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- Additional ETL connectors (REST APIs, SQL databases).
- Extended model evaluation utilities (cross-validation reports, learning curves).
- Reusable Streamlit dashboard components.
- Example end-to-end portfolio projects (sales analysis, churn prediction, demand forecasting).

---

## [0.1.0] - 2024-01-01

### Added

#### Project foundation

- Initial repository structure with `src/` layout and PEP 621 `pyproject.toml`.
- `requirements.txt` listing runtime and development dependencies.
- `.gitignore` covering Python artifacts, virtual environments, data files, logs, and secrets.
- `.env.example` documenting all supported environment variables (no secrets committed).
- `README.md` with overview, installation, configuration, usage examples, and design principles.
- `LICENSE` (MIT).
- `CHANGELOG.md` (this file).

#### Core package — `DataForge.core`

- `data_handling.py`:
  - `load_csv` — load CSV files with configurable separator, encoding, dtypes, and date parsing.
  - `load_parquet` — load Parquet files with optional column selection.
  - `save_dataframe` — persist DataFrames to CSV or Parquet with automatic format inference.
  - `clean_dataframe` — non-destructive cleaning pipeline (column normalization, duplicate removal, missing-value strategies).
  - `split_features_target` — split a DataFrame into features and target.
  - `train_test_split_df` — DataFrame-friendly wrapper around scikit-learn's `train_test_split`.
- `modeling.py`:
  - `train_model` — build and fit models from named presets (logistic/linear regression, decision tree, random forest, gradient boosting).
  - `predict` — generate predictions from a fitted estimator.
  - `evaluate_model` — task-appropriate metrics (classification: accuracy, precision, recall, F1, ROC AUC; regression: MAE, RMSE, R²).
  - `cross_validate_model` — k-fold cross-validation with mean score summary.
  - `save_model` / `load_model` — persist and restore fitted models via pickle.

#### Services package — `DataForge.services`

- `etl.py`:
  - `extract` — read data from CSV, Parquet, or SQL sources.
  - `transform` — configurable transformation pipeline with custom step support.
  - `load` — persist DataFrames to CSV, Parquet, or SQL destinations.
  - `run_etl_pipeline` — orchestrate extract → transform → load with structured results.
  - `ETLResult` — dataclass summarizing pipeline runs (rows extracted/loaded, columns, steps applied).

#### Utils package — `DataForge.utils`

- `helpers.py`:
  - `get_logger` — idempotent logger configuration with stream and optional file handlers.
  - `ensure_directory` — create directories (and parents) if missing.
  - `resolve_path` — resolve paths relative to an optional base directory.
  - `validate_columns` — assert required columns exist in a DataFrame.
  - `timer` — context manager measuring elapsed wall-clock time.
  - `chunked` — iterate over an iterable in fixed-size chunks.
  - `safe_divide` — division that returns a default on zero denominator.
  - `to_dict_safe` — best-effort conversion of objects to plain dictionaries.

#### Visualization package — `DataForge.visualization`

- `plots.py`:
  - `plot_distribution` — histogram, KDE, or box plot of a single column.
  - `plot_correlation_matrix` — heatmap of pairwise correlations.
  - `plot_time_series` — Matplotlib or Plotly line plot of one or more series.
  - `plot_bar` — bar chart of aggregated values by category.
  - `save_figure` — persist Matplotlib or Plotly figures to disk.

#### Configuration

- `config/settings.py` — centralized configuration reading from environment variables (application environment, logging, database URL, API credentials, data paths, random seed, Streamlit port).

#### Entry point

- `src/DataForge/__main__.py` — command-line entry point exposed as the `data-science-portfolio` console script.

#### Testing and CI

- `tests/conftest.py` — shared pytest fixtures (sample DataFrames, temporary CSV/Parquet files, SQLite database URL, configured logger).
- `tests/test_main.py` — unit tests covering the public API of core, services, utils, and visualization modules.
- `.github/workflows/tests.yml` — GitHub Actions workflow running the test suite across Python 3.10, 3.11, and 3.12, plus static checks (package import and CLI entry point verification).

### Engineering standards

- Type hints and docstrings throughout the public API.
- Structured logging via the `logging` module (no `print` statements in library code).
- Explicit exception handling with informative error messages.
- No hardcoded secrets — credentials are read from environment variables.
- Reproducible environments through pinned dependency ranges and deterministic pipelines.

---

## Versioning notes

- **MAJOR** — incompatible API changes.
- **MINOR** — backward-compatible functionality additions.
- **PATCH** — backward-compatible bug fixes.

[Unreleased]: https://github.com/<your-username>/DataForge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<your-username>/DataForge/releases/tag/v0.1.0