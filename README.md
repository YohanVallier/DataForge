# DataForge

A modular, production-oriented framework for building a **professional Data Science portfolio**. It provides reusable building blocks for data handling, machine learning, ETL pipelines, and visualization, so that individual portfolio projects can focus on the analytical problem rather than on boilerplate.

The framework is designed to demonstrate solid software engineering practices — modularity, separation of concerns, logging, exception handling, centralized configuration, and automated testing — while remaining lightweight enough to be used in small, focused projects.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Data Handling](#data-handling)
  - [Machine Learning Modeling](#machine-learning-modeling)
  - [ETL Pipelines](#etl-pipelines)
  - [Visualization](#visualization)
  - [Command-Line Entry Point](#command-line-entry-point)
- [Running Tests](#running-tests)
- [Continuous Integration](#continuous-integration)
- [Design Principles](#design-principles)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This repository is the **foundation** of a professional Data Science portfolio. Rather than a single monolithic notebook, it organizes reusable code into clearly separated modules:

- **`core`** — data manipulation and machine learning modeling.
- **`services`** — ETL pipelines for ingestion and transformation.
- **`utils`** — shared helpers (logging, path handling, validation).
- **`visualization`** — plotting utilities built on Matplotlib, Seaborn, and Plotly.

Each portfolio project can import these modules, extend them, and focus on the domain problem (sales analysis, churn prediction, demand forecasting, etc.) while inheriting consistent engineering standards.

---

## Features

- **Modular architecture** with explicit package boundaries.
- **Type hints and docstrings** throughout the public API.
- **Structured logging** (no `print` statements in library code).
- **Explicit exception handling** with informative error messages.
- **Centralized configuration** via `config/settings.py` and environment variables.
- **Reproducible environments** through `pyproject.toml` and `requirements.txt`.
- **Automated tests** with `pytest` and coverage reporting.
- **CI pipeline** via GitHub Actions.
- **No hardcoded secrets** — credentials are read from environment variables (see `.env.example`).

---

## Project Structure

```
.
├── config/
│   └── settings.py                 # Centralized configuration
├── src/
│   └── DataForge/
│       ├── __init__.py
│       ├── __main__.py             # CLI entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── data_handling.py    # Loading, cleaning, preprocessing
│       │   └── modeling.py         # Model training and evaluation
│       ├── services/
│       │   ├── __init__.py
│       │   └── etl.py              # ETL pipeline definitions
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py          # Shared utilities
│       └── visualization/
│           ├── __init__.py
│           └── plots.py            # Plotting utilities
├── tests/
│   ├── conftest.py                 # Pytest fixtures
│   └── test_main.py                # Unit tests
├── .github/
│   └── workflows/
│       └── tests.yml               # CI configuration
├── .env.example                    # Environment variable template
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## Requirements

- **Python** 3.10 or newer.
- The dependencies listed in `requirements.txt` (Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-learn, XGBoost, OpenPyXL, SQLAlchemy, Requests, BeautifulSoup4, PyArrow, Streamlit).
- Development dependencies: `pytest`, `pytest-cov`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/DataForge.git
cd DataForge
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

Install the package in editable mode together with development extras:

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

Alternatively, install only the runtime dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Configuration is centralized in `config/settings.py`. Sensitive values (database URLs, API keys) are **never** hardcoded — they are read from environment variables.

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Then export the variables (or use a tool such as `python-dotenv` in your own scripts):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
export LOG_LEVEL="INFO"
```

The `.env` file is excluded from version control by `.gitignore`.

---

## Usage

The package is importable as `DataForge`. The examples below illustrate the intended usage of each module.

### Data Handling

```python
from DataForge.core.data_handling import load_csv, clean_dataframe

df = load_csv("data/raw/sales.csv")
df_clean = clean_dataframe(df, drop_duplicates=True)
```

### Machine Learning Modeling

```python
from DataForge.core.modeling import train_model, evaluate_model

model = train_model(X_train, y_train, model_type="random_forest")
metrics = evaluate_model(model, X_test, y_test)
```

### ETL Pipelines

```python
from DataForge.services.etl import run_etl_pipeline

run_etl_pipeline(
    source="data/raw/transactions.csv",
    destination="data/processed/transactions.parquet",
)
```

### Visualization

```python
from DataForge.visualization.plots import plot_distribution

fig = plot_distribution(df, column="revenue", kind="hist")
fig.savefig("reports/revenue_distribution.png")
```

### Command-Line Entry Point

After installation, the package exposes a console script:

```bash
data-science-portfolio --help
```

Or run it as a module:

```bash
python -m DataForge --help
```

---

## Running Tests

Run the full test suite with coverage:

```bash
pytest
```

Or with explicit coverage reporting:

```bash
pytest --cov=src/DataForge --cov-report=term-missing
```

Tests are configured in `pyproject.toml` under `[tool.pytest.ini_options]` and use fixtures defined in `tests/conftest.py`.

---

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/tests.yml` runs the test suite on every push and pull request against the `main` branch, across supported Python versions. A failing test suite blocks merges, ensuring the framework remains stable as new projects are added.

---

## Design Principles

This framework follows a small set of non-negotiable engineering principles:

1. **Separation of concerns** — data handling, modeling, ETL, and visualization live in distinct modules.
2. **Explicit over implicit** — type hints, docstrings, and named exceptions.
3. **No `print` in library code** — use the `logging` module.
4. **No hardcoded secrets** — configuration is read from environment variables.
5. **Reproducibility** — pinned dependencies and deterministic pipelines.
6. **Proportional complexity** — the architecture scales with the problem, not ahead of it.

---

## Roadmap

The framework is intended to grow alongside the portfolio. Planned additions include:

- Additional ETL connectors (REST APIs, SQL databases).
- Extended model evaluation utilities (cross-validation, learning curves).
- Reusable Streamlit dashboard components.
- Example projects demonstrating end-to-end workflows.

See `CHANGELOG.md` for a detailed history of changes.

---

## Contributing

This is a personal portfolio project, but suggestions and issue reports are welcome. Please open an issue describing the proposed change before submitting a pull request.

---

## License

This project is distributed under the **MIT License**. See the `LICENSE` file for details.
