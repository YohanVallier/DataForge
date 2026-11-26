<<<<<<< HEAD
<div align="center">

# DataScienceProfessionalPortfolio
=======
# DataForge
>>>>>>> 49d003c263b8e76bec8dc63b988c9b6e532596c5

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](#) [![Pandas](https://img.shields.io/badge/Pandas-Data%20Handling-150458?style=flat-square&logo=pandas&logoColor=white)](#) [![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](#) [![XGBoost](https://img.shields.io/badge/XGBoost-Modeling-189FDD?style=flat-square)](#) [![Interface](https://img.shields.io/badge/Interface-Python%20Package%20%26%20CLI-4B5563?style=flat-square)](#)

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](#) [![Tests](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](#) [![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#) [![Documentation](https://img.shields.io/badge/Documentation-Bilingual-blue?style=flat-square)](#)

**Language / Idioma:** [English](#english) | [Português (Brasil)](#português-brasil)

</div>

---

## English

### Table of Contents

- [1.1. Project Overview](#11-project-overview)
- [1.2. Preview / Visual Showcase](#12-preview--visual-showcase)
- [1.3. Key Features](#13-key-features)
- [1.4. Architecture](#14-architecture)
- [1.5. Technologies Used](#15-technologies-used)
- [1.6. Project Structure](#16-project-structure)
- [1.7. Installation](#17-installation)
- [1.8. Configuration](#18-configuration)
- [1.9. Usage](#19-usage)
- [1.10. Workflow / Execution Flow](#110-workflow--execution-flow)
- [1.11. Testing](#111-testing)
- [1.12. Future Improvements](#112-future-improvements)
- [1.13. Contributing](#113-contributing)
- [1.14. License](#114-license)
- [1.15. Author](#115-author)

---

### 1.1. Project Overview

**DataScienceProfessionalPortfolio** is a modular, production-oriented framework designed as the foundation for building a professional Data Science portfolio. Rather than consolidating analysis into a single monolithic notebook, it organizes reusable components for data handling, machine learning modeling, ETL pipelines, and data visualization into distinct Python packages.

Individual portfolio projects—such as sales analysis, churn prediction, or demand forecasting—can import and extend these modules to focus on domain-specific analytical problems while inheriting consistent software engineering standards.

| Aspect | Summary |
| :--- | :--- |
| **Purpose** | Reusable foundational framework for modular Data Science portfolio projects |
| **Primary Domains** | Data Handling, Machine Learning Modeling, ETL Pipelines, Visualization |
| **Engineering Focus** | Modularity, separation of concerns, structured logging, explicit exception handling, centralized configuration, automated testing |
| **Execution Interfaces** | Importable Python package (`DataScienceProfessionalPortfolio`) and Command-Line Interface (`data-science-portfolio`) |

---

### 1.2. Preview / Visual Showcase

<div align="center">
  <img src="assets/images/project-banner.png" alt="DataScienceProfessionalPortfolio Banner" width="100%" />
</div>

> **Note:** No runtime screenshots, CLI terminal captures, or dashboard previews were provided in the original documentation. The banner above represents the modular architecture of the framework.

---

### 1.3. Key Features

- **Modular Architecture:** Explicit package boundaries separating core logic, ETL services, shared utilities, and visualization components.
- **Type Hints and Docstrings:** Explicit typing and documentation throughout the public API.
- **Structured Logging:** Uses Python's `logging` module with no `print` statements in library code.
- **Explicit Exception Handling:** Named exceptions with informative error messages.
- **Centralized Configuration:** Managed through `config/settings.py` and external environment variables.
- **No Hardcoded Secrets:** Credentials and sensitive values are loaded strictly from environment variables (template provided in `.env.example`).
- **Reproducible Environments:** Dependencies and packaging managed via `pyproject.toml` and `requirements.txt`.
- **Automated Testing and Coverage:** Unit test suite powered by `pytest` with coverage reporting via `pytest-cov`.
- **Continuous Integration:** Automated test execution via GitHub Actions on every push and pull request targeting `main`.

---

### 1.4. Architecture

The framework enforces six non-negotiable engineering principles: separation of concerns, explicitness over implicitness, structured logging instead of `print`, externalized secrets, reproducibility, and proportional complexity.

```mermaid
flowchart LR
    subgraph Entry["Entry Points"]
        API["Python Package Import<br/>(DataScienceProfessionalPortfolio)"]
        CLI["CLI Entry Point<br/>(__main__.py / data-science-portfolio)"]
    end

    subgraph Config["Configuration & Shared Layer"]
        ENV[".env / Environment Variables"]
        SET["config/settings.py"]
        UTL["utils/helpers.py<br/>(Logging, Paths, Validation)"]
    end

    subgraph Modules["Domain Modules"]
        CORE_DATA["core/data_handling.py<br/>(Loading, Cleaning, Preprocessing)"]
        CORE_ML["core/modeling.py<br/>(Training, Evaluation)"]
        SVC_ETL["services/etl.py<br/>(Ingestion, Transformation)"]
        VIZ["visualization/plots.py<br/>(Matplotlib, Seaborn, Plotly)"]
    end

    subgraph Quality["Verification & CI"]
        TESTS["tests/<br/>(conftest.py, test_main.py)"]
        CI[".github/workflows/tests.yml"]
    end

    ENV --> SET
    SET --> API
    SET --> CLI
    API --> CORE_DATA
    API --> CORE_ML
    API --> SVC_ETL
    API --> VIZ
    CLI --> Modules
    UTL --> CORE_DATA
    UTL --> CORE_ML
    UTL --> SVC_ETL
    UTL --> VIZ
    CORE_DATA --> CORE_ML
    SVC_ETL --> CORE_DATA
    CORE_DATA --> VIZ
    TESTS --> Modules
    CI --> TESTS
```

#### Module Responsibilities

| Module / Component | Path | Responsibility |
| :--- | :--- | :--- |
| **Configuration** | `config/settings.py` | Centralizes runtime settings and reads credentials from environment variables |
| **CLI Entry Point** | `src/DataScienceProfessionalPortfolio/__main__.py` | Exposes command-line execution (`data-science-portfolio` / `python -m`) |
| **Data Handling** | `src/DataScienceProfessionalPortfolio/core/data_handling.py` | Data loading, cleaning, and preprocessing (`load_csv`, `clean_dataframe`) |
| **ML Modeling** | `src/DataScienceProfessionalPortfolio/core/modeling.py` | Model training and evaluation (`train_model`, `evaluate_model`) |
| **ETL Services** | `src/DataScienceProfessionalPortfolio/services/etl.py` | Ingestion and transformation pipelines (`run_etl_pipeline`) |
| **Shared Utilities** | `src/DataScienceProfessionalPortfolio/utils/helpers.py` | Shared logging, path handling, and validation helpers |
| **Visualization** | `src/DataScienceProfessionalPortfolio/visualization/plots.py` | Plotting utilities built on Matplotlib, Seaborn, and Plotly (`plot_distribution`) |

---

### 1.5. Technologies Used

| Category | Technology / Tool | Role in Project |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core runtime language |
| **Data Manipulation** | Pandas, NumPy, PyArrow, OpenPyXL | Tabular processing, numerical operations, Parquet and spreadsheet I/O |
| **Machine Learning** | Scikit-learn, XGBoost | Model training and evaluation |
| **Data Visualization & UI** | Matplotlib, Seaborn, Plotly, Streamlit | Static/interactive plotting and dashboard components |
| **Data Ingestion & Storage** | SQLAlchemy, Requests, BeautifulSoup4 | Database access, HTTP requests, and HTML parsing |
| **Packaging & Dependencies** | `pyproject.toml`, `requirements.txt` | Package metadata, editable installation, and dependency management |
| **Testing** | `pytest`, `pytest-cov` | Unit test execution, fixtures, and coverage reporting |
| **CI/CD** | GitHub Actions | Automated testing pipeline on pushes and pull requests |

> **Note:** `python-dotenv` is mentioned as an optional helper for loading `.env` files in user scripts, though it is not listed among the core dependencies in the original `requirements.txt` summary.

---

### 1.6. Project Structure

```text
.
├── assets/
│   └── images/
│       └── project-banner.png      # Project banner for documentation showcase
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

> **Note:** The `assets/images/project-banner.png` directory and file were added to support the standardized documentation banner. Additionally, the usage examples reference `data/raw/`, `data/processed/`, and `reports/` paths, which are runtime directories not included in the base repository tree.

---

### 1.7. Installation

#### Prerequisites

- **Python 3.10 or newer**

#### 1. Clone the repository

```bash
<<<<<<< HEAD
git clone [https://github.com/](https://github.com/)<your-username>/DataScienceProfessionalPortfolio.git
cd DataScienceProfessionalPortfolio
=======
git clone https://github.com/<your-username>/DataForge.git
cd DataForge
>>>>>>> 49d003c263b8e76bec8dc63b988c9b6e532596c5
```

> **Note:** Replace `<your-username>` with the actual GitHub repository owner's username, as it was left as a placeholder in the original documentation.

#### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

#### 3. Install dependencies

Install the package in editable mode together with development extras (`pytest`, `pytest-cov`):

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

Alternatively, install only the runtime dependencies:

```bash
pip install -r requirements.txt
```

---

### 1.8. Configuration

Configuration is centralized in `config/settings.py`. Sensitive values—such as database URLs and API keys—are never hardcoded and must be supplied through environment variables. The `.env` file is excluded from version control via `.gitignore`.

#### Setup Steps

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Export the required variables in your shell (or load them with a tool such as `python-dotenv` in your own scripts):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
export LOG_LEVEL="INFO"
```

#### Documented Environment Variables

| Variable | Example Value | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://user:password@localhost:5432/mydb` | Database connection string |
| `LOG_LEVEL` | `INFO` | Controls structured logging verbosity |

> **Note:** The original documentation also mentions API keys as externalized credentials, but does not specify additional variable names, default values, or required flags defined inside `.env.example` or `config/settings.py`.

---

### 1.9. Usage

<<<<<<< HEAD
The package is importable as `DataScienceProfessionalPortfolio` and exposes a CLI console script after installation.
=======
The package is importable as `DataForge`. The examples below illustrate the intended usage of each module.
>>>>>>> 49d003c263b8e76bec8dc63b988c9b6e532596c5

#### Data Handling

```python
from DataForge.core.data_handling import load_csv, clean_dataframe

df = load_csv("data/raw/sales.csv")
df_clean = clean_dataframe(df, drop_duplicates=True)
```

#### Machine Learning Modeling

```python
from DataForge.core.modeling import train_model, evaluate_model

model = train_model(X_train, y_train, model_type="random_forest")
metrics = evaluate_model(model, X_test, y_test)
```

#### ETL Pipelines

```python
from DataForge.services.etl import run_etl_pipeline

run_etl_pipeline(
    source="data/raw/transactions.csv",
    destination="data/processed/transactions.parquet",
)
```

#### Visualization

```python
from DataForge.visualization.plots import plot_distribution

fig = plot_distribution(df, column="revenue", kind="hist")
fig.savefig("reports/revenue_distribution.png")
```

#### Command-Line Entry Point

Run using the installed console script:

```bash
data-science-portfolio --help
```

Or execute directly as a Python module:

```bash
python -m DataForge --help
```

#### Documented Data Formats and Interfaces

| Component | Input | Output |
| :--- | :--- | :--- |
| **Data Handling** | CSV file path (`data/raw/sales.csv`) | Cleaned DataFrame |
| **ML Modeling** | Training and test feature/target sets (`X_train`, `y_train`, `X_test`, `y_test`) | Trained model instance and evaluation metrics |
| **ETL Pipelines** | Source CSV file (`data/raw/transactions.csv`) | Processed Parquet file (`data/processed/transactions.parquet`) |
| **Visualization** | DataFrame, target column, plot kind (`hist`) | Figure object exportable to image (`reports/revenue_distribution.png`) |
| **CLI** | Command-line flags (e.g., `--help`) | Terminal output |

---

### 1.10. Workflow / Execution Flow

```mermaid
flowchart TD
    A["Start: Invoke Python API or CLI"] --> B["Load Centralized Config<br/>(config/settings.py & Environment Variables)"]
    B --> C{"Configuration & Inputs<br/>Valid?"}
    C -- No --> ERR["Raise Explicit Exception &<br/>Record Structured Log"]
    ERR --> Z["End with Error"]
    C -- Yes --> D{"Select Operation"}

    D -- "ETL Pipeline" --> E1["services/etl.py<br/>run_etl_pipeline()"]
    E1 --> E2["Read Raw Source (CSV) &<br/>Transform Data"]
    E2 --> E3["Write Processed Output (Parquet)"]

    D -- "Data Handling" --> F1["core/data_handling.py<br/>load_csv() -> clean_dataframe()"]
    F1 --> F2["Produce Cleaned DataFrame"]

    D -- "ML Modeling" --> G1["core/modeling.py<br/>train_model()"]
    G1 --> G2["evaluate_model()"]
    G2 --> G3["Return Model & Evaluation Metrics"]

    D -- "Visualization" --> H1["visualization/plots.py<br/>plot_distribution()"]
    H1 --> H2["Generate & Save Figure (PNG)"]

    E3 --> OK{"Execution<br/>Succeeded?"}
    F2 --> OK
    G3 --> OK
    H2 --> OK

    OK -- No --> ERR
    OK -- Yes --> DONE["Log Completion & Return Artifact"]
```

---

<<<<<<< HEAD
### 1.11. Testing
=======
```bash
pytest --cov=src/DataForge --cov-report=term-missing
```
>>>>>>> 49d003c263b8e76bec8dc63b988c9b6e532596c5

Automated tests are implemented with `pytest`, configured in `pyproject.toml` under `[tool.pytest.ini_options]`, and supported by shared fixtures in `tests/conftest.py` and unit tests in `tests/test_main.py`.

#### Test Commands

| Objective | Command |
| :--- | :--- |
| **Run full test suite** | `pytest` |
| **Run with terminal coverage report** | `pytest --cov=src/DataScienceProfessionalPortfolio --cov-report=term-missing` |

#### Continuous Integration

The GitHub Actions workflow defined in `.github/workflows/tests.yml` runs the test suite on every push and pull request targeting the `main` branch across supported Python versions. Failing tests block merges to preserve framework stability.

> **Note:** Specific code coverage percentages, total test counts, and the exact list of Python versions configured in `.github/workflows/tests.yml` were not specified in the original documentation.

---

### 1.12. Future Improvements

Planned roadmap additions documented for the framework include:

- Additional ETL connectors (REST APIs and SQL databases).
- Extended model evaluation utilities (cross-validation and learning curves).
- Reusable Streamlit dashboard components.
- Example projects demonstrating end-to-end workflows.

For a detailed history of changes, consult `CHANGELOG.md`.

---

### 1.13. Contributing

This repository is maintained as a personal portfolio project, but suggestions and issue reports are welcome.

1. Open an issue describing the proposed change or bug report before submitting a pull request.
2. Ensure all automated tests pass locally (`pytest`), as the CI workflow in `.github/workflows/tests.yml` blocks merges into `main` if any tests fail.

---

### 1.14. License

This project is distributed under the **MIT License**. See the `LICENSE` file for full terms.

---

### 1.15. Author

Author details (name, GitHub profile, and contact information) were not specified in the original documentation.

---

## Português (Brasil)

### Índice

- [2.1. Visão Geral do Projeto](#21-visão-geral-do-projeto)
- [2.2. Demonstração Visual](#22-demonstração-visual)
- [2.3. Principais Funcionalidades](#23-principais-funcionalidades)
- [2.4. Arquitetura](#24-arquitetura)
- [2.5. Tecnologias Utilizadas](#25-tecnologias-utilizadas)
- [2.6. Estrutura do Projeto](#26-estrutura-do-projeto)
- [2.7. Instalação](#27-instalação)
- [2.8. Configuração](#28-configuração)
- [2.9. Uso](#29-uso)
- [2.10. Fluxo de Execução](#210-fluxo-de-execução)
- [2.11. Testes](#211-testes)
- [2.12. Melhorias Futuras](#212-melhorias-futuras)
- [2.13. Contribuição](#213-contribuição)
- [2.14. Licença](#214-licença)
- [2.15. Autor](#215-autor)

---

### 2.1. Visão Geral do Projeto

O **DataScienceProfessionalPortfolio** é um framework modular e orientado à produção, projetado como base para a construção de um portfólio profissional de Ciência de Dados. Em vez de concentrar a análise em um único notebook monolítico, o projeto organiza componentes reutilizáveis de manipulação de dados, modelagem de machine learning, pipelines ETL e visualização de dados em pacotes Python separados.

Projetos individuais de portfólio — como análise de vendas, previsão de churn ou previsão de demanda — podem importar e estender esses módulos para focar no problema analítico de domínio, herdando padrões consistentes de engenharia de software.

| Aspecto | Resumo |
| :--- | :--- |
| **Propósito** | Framework base reutilizável para projetos modulares de portfólio em Ciência de Dados |
| **Domínios Principais** | Manipulação de Dados, Modelagem de Machine Learning, Pipelines ETL, Visualização |
| **Foco de Engenharia** | Modularidade, separação de responsabilidades, logging estruturado, tratamento explícito de exceções, configuração centralizada e testes automatizados |
| **Interfaces de Execução** | Pacote Python importável (`DataScienceProfessionalPortfolio`) e Interface de Linha de Comando (`data-science-portfolio`) |

---

### 2.2. Demonstração Visual

<div align="center">
  <img src="assets/images/project-banner.png" alt="Banner do DataScienceProfessionalPortfolio" width="100%" />
</div>

> **Nota:** Nenhuma captura de tela de execução, saída de terminal CLI ou prévia de dashboard foi fornecida na documentação original. O banner acima ilustra a arquitetura modular do framework.

---

### 2.3. Principais Funcionalidades

- **Arquitetura Modular:** Fronteiras explícitas entre pacotes, separando lógica central, serviços ETL, utilitários compartilhados e visualização.
- **Type Hints e Docstrings:** Tipagem e documentação explícitas em toda a API pública.
- **Logging Estruturado:** Uso do módulo `logging` do Python, sem instruções `print` no código de biblioteca.
- **Tratamento Explícito de Exceções:** Exceções nomeadas com mensagens de erro informativas.
- **Configuração Centralizada:** Gerenciada via `config/settings.py` e variáveis de ambiente externas.
- **Ausência de Segredos no Código:** Credenciais e valores sensíveis são lidos exclusivamente de variáveis de ambiente (modelo em `.env.example`).
- **Ambientes Reprodutíveis:** Dependências e empacotamento controlados por meio de `pyproject.toml` e `requirements.txt`.
- **Testes Automatizados e Cobertura:** Suíte de testes unitários com `pytest` e relatórios de cobertura com `pytest-cov`.
- **Integração Contínua:** Execução automatizada de testes via GitHub Actions a cada push e pull request para a branch `main`.

---

### 2.4. Arquitetura

O framework segue seis princípios de engenharia inegociáveis: separação de responsabilidades, explicitude acima de implicitude, ausência de `print` em código de biblioteca, segredos externalizados, reprodutibilidade e complexidade proporcional ao problema.

```mermaid
flowchart LR
    subgraph Entry["Pontos de Entrada"]
        API["Importação do Pacote Python<br/>(DataScienceProfessionalPortfolio)"]
        CLI["Ponto de Entrada CLI<br/>(__main__.py / data-science-portfolio)"]
    end

    subgraph Config["Configuração e Camada Compartilhada"]
        ENV[".env / Variáveis de Ambiente"]
        SET["config/settings.py"]
        UTL["utils/helpers.py<br/>(Logging, Caminhos, Validação)"]
    end

    subgraph Modules["Módulos de Domínio"]
        CORE_DATA["core/data_handling.py<br/>(Carga, Limpeza, Pré-processamento)"]
        CORE_ML["core/modeling.py<br/>(Treinamento, Avaliação)"]
        SVC_ETL["services/etl.py<br/>(Ingestão, Transformação)"]
        VIZ["visualization/plots.py<br/>(Matplotlib, Seaborn, Plotly)"]
    end

    subgraph Quality["Verificação e CI"]
        TESTS["tests/<br/>(conftest.py, test_main.py)"]
        CI[".github/workflows/tests.yml"]
    end

    ENV --> SET
    SET --> API
    SET --> CLI
    API --> CORE_DATA
    API --> CORE_ML
    API --> SVC_ETL
    API --> VIZ
    CLI --> Modules
    UTL --> CORE_DATA
    UTL --> CORE_ML
    UTL --> SVC_ETL
    UTL --> VIZ
    CORE_DATA --> CORE_ML
    SVC_ETL --> CORE_DATA
    CORE_DATA --> VIZ
    TESTS --> Modules
    CI --> TESTS
```

#### Responsabilidades dos Módulos

| Módulo / Componente | Caminho | Responsabilidade |
| :--- | :--- | :--- |
| **Configuração** | `config/settings.py` | Centraliza configurações de execução e lê credenciais de variáveis de ambiente |
| **Ponto de Entrada CLI** | `src/DataScienceProfessionalPortfolio/__main__.py` | Expõe a execução via linha de comando (`data-science-portfolio` / `python -m`) |
| **Manipulação de Dados** | `src/DataScienceProfessionalPortfolio/core/data_handling.py` | Carregamento, limpeza e pré-processamento de dados (`load_csv`, `clean_dataframe`) |
| **Modelagem ML** | `src/DataScienceProfessionalPortfolio/core/modeling.py` | Treinamento e avaliação de modelos (`train_model`, `evaluate_model`) |
| **Serviços ETL** | `src/DataScienceProfessionalPortfolio/services/etl.py` | Pipelines de ingestão e transformação (`run_etl_pipeline`) |
| **Utilitários Compartilhados** | `src/DataScienceProfessionalPortfolio/utils/helpers.py` | Funções auxiliares de logging, manipulação de caminhos e validação |
| **Visualização** | `src/DataScienceProfessionalPortfolio/visualization/plots.py` | Utilitários gráficos sobre Matplotlib, Seaborn e Plotly (`plot_distribution`) |

---

### 2.5. Tecnologias Utilizadas

| Categoria | Tecnologia / Ferramenta | Papel no Projeto |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.10+ | Linguagem principal de execução |
| **Manipulação de Dados** | Pandas, NumPy, PyArrow, OpenPyXL | Processamento tabular, operações numéricas e leitura/escrita em Parquet e planilhas |
| **Machine Learning** | Scikit-learn, XGBoost | Treinamento e avaliação de modelos |
| **Visualização de Dados e UI** | Matplotlib, Seaborn, Plotly, Streamlit | Gráficos estáticos/interativos e componentes de dashboard |
| **Ingestão e Armazenamento** | SQLAlchemy, Requests, BeautifulSoup4 | Acesso a bancos de dados, requisições HTTP e parsing HTML |
| **Empacotamento e Dependências** | `pyproject.toml`, `requirements.txt` | Metadados do pacote, instalação editável e controle de dependências |
| **Testes** | `pytest`, `pytest-cov` | Execução de testes unitários, fixtures e relatório de cobertura |
| **CI/CD** | GitHub Actions | Pipeline automatizado de testes em pushes e pull requests |

> **Nota:** A biblioteca `python-dotenv` é mencionada como recurso opcional para carregar arquivos `.env` em scripts do usuário, embora não figure na lista principal de dependências resumida para o `requirements.txt` original.

---

### 2.6. Estrutura do Projeto

```text
.
├── assets/
│   └── images/
│       └── project-banner.png      # Banner visual do projeto para documentação
├── config/
│   └── settings.py                 # Configuração centralizada
├── src/
│   └── DataScienceProfessionalPortfolio/
│       ├── __init__.py
│       ├── __main__.py             # Ponto de entrada CLI
│       ├── core/
│       │   ├── __init__.py
│       │   ├── data_handling.py    # Carregamento, limpeza e pré-processamento
│       │   └── modeling.py         # Treinamento e avaliação de modelos
│       ├── services/
│       │   ├── __init__.py
│       │   └── etl.py              # Definições de pipelines ETL
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py          # Utilitários compartilhados
│       └── visualization/
│           ├── __init__.py
│           └── plots.py            # Utilitários de visualização
├── tests/
│   ├── conftest.py                 # Fixtures do Pytest
│   └── test_main.py                # Testes unitários
├── .github/
│   └── workflows/
│       └── tests.yml               # Configuração de CI
├── .env.example                    # Modelo de variáveis de ambiente
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

> **Nota:** O caminho `assets/images/project-banner.png` foi adicionado para acomodar o banner visual da documentação padronizada. Além disso, os exemplos de uso referenciam os diretórios `data/raw/`, `data/processed/` e `reports/`, que são diretórios de tempo de execução ausentes na árvore base do repositório original.

---

### 2.7. Instalação

#### Pré-requisitos

- **Python 3.10 ou superior**

#### 1. Clonar o repositório

```bash
git clone [https://github.com/](https://github.com/)<your-username>/DataScienceProfessionalPortfolio.git
cd DataScienceProfessionalPortfolio
```

> **Nota:** Substitua `<your-username>` pelo nome de usuário real do proprietário do repositório no GitHub, mantido como placeholder conforme a documentação original.

#### 2. Criar e ativar um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

#### 3. Instalar as dependências

Instale o pacote em modo editável juntamente com os extras de desenvolvimento (`pytest`, `pytest-cov`):

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

Alternativamente, instale apenas as dependências de execução:

```bash
pip install -r requirements.txt
```

---

### 2.8. Configuração

A configuração é centralizada em `config/settings.py`. Valores sensíveis — como URLs de banco de dados e chaves de API — nunca são fixados no código e devem ser fornecidos via variáveis de ambiente. O arquivo `.env` é ignorado pelo controle de versão por meio do `.gitignore`.

#### Passos de Configuração

1. Copie o arquivo de modelo:

```bash
cp .env.example .env
```

2. Exporte as variáveis no shell (ou utilize uma ferramenta como `python-dotenv` nos seus próprios scripts):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
export LOG_LEVEL="INFO"
```

#### Variáveis de Ambiente Documentadas

| Variável | Valor de Exemplo | Finalidade |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://user:password@localhost:5432/mydb` | String de conexão com o banco de dados |
| `LOG_LEVEL` | `INFO` | Define o nível de verbosidade do logging estruturado |

> **Nota:** A documentação original menciona também chaves de API como credenciais externalizadas, mas não especifica outros nomes de variáveis, valores padrão ou obrigatoriedade definidos em `.env.example` ou `config/settings.py`.

---

### 2.9. Uso

O pacote pode ser importado como `DataScienceProfessionalPortfolio` e disponibiliza um script de console após a instalação.

#### Manipulação de Dados

```python
from DataScienceProfessionalPortfolio.core.data_handling import load_csv, clean_dataframe

df = load_csv("data/raw/sales.csv")
df_clean = clean_dataframe(df, drop_duplicates=True)
```

#### Modelagem de Machine Learning

```python
from DataScienceProfessionalPortfolio.core.modeling import train_model, evaluate_model

model = train_model(X_train, y_train, model_type="random_forest")
metrics = evaluate_model(model, X_test, y_test)
```

#### Pipelines ETL

```python
from DataScienceProfessionalPortfolio.services.etl import run_etl_pipeline

run_etl_pipeline(
    source="data/raw/transactions.csv",
    destination="data/processed/transactions.parquet",
)
```

#### Visualização

```python
from DataScienceProfessionalPortfolio.visualization.plots import plot_distribution

fig = plot_distribution(df, column="revenue", kind="hist")
fig.savefig("reports/revenue_distribution.png")
```

#### Ponto de Entrada via Linha de Comando (CLI)

Execute por meio do script de console instalado:

```bash
data-science-portfolio --help
```

Ou execute diretamente como módulo Python:

```bash
python -m DataScienceProfessionalPortfolio --help
```

#### Formatos e Interfaces Documentados

| Componente | Entrada | Saída |
| :--- | :--- | :--- |
| **Manipulação de Dados** | Caminho de arquivo CSV (`data/raw/sales.csv`) | DataFrame limpo |
| **Modelagem ML** | Conjuntos de treino e teste (`X_train`, `y_train`, `X_test`, `y_test`) | Modelo treinado e métricas de avaliação |
| **Pipelines ETL** | Arquivo CSV de origem (`data/raw/transactions.csv`) | Arquivo Parquet processado (`data/processed/transactions.parquet`) |
| **Visualização** | DataFrame, coluna alvo e tipo de gráfico (`hist`) | Objeto de figura exportável para imagem (`reports/revenue_distribution.png`) |
| **CLI** | Flags de linha de comando (ex.: `--help`) | Saída no terminal |

---

### 2.10. Fluxo de Execução

```mermaid
flowchart TD
    A["Início: Invocar API Python ou CLI"] --> B["Carregar Configuração Centralizada<br/>(config/settings.py e Variáveis de Ambiente)"]
    B --> C{"Configuração e Entradas<br/>Válidas?"}
    C -- Não --> ERR["Lançar Exceção Explícita e<br/>Registrar Log Estruturado"]
    ERR --> Z["Encerrar com Erro"]
    C -- Sim --> D{"Selecionar Operação"}

    D -- "Pipeline ETL" --> E1["services/etl.py<br/>run_etl_pipeline()"]
    E1 --> E2["Ler Origem Bruta (CSV) e<br/>Transformar Dados"]
    E2 --> E3["Gravar Saída Processada (Parquet)"]

    D -- "Manipulação de Dados" --> F1["core/data_handling.py<br/>load_csv() -> clean_dataframe()"]
    F1 --> F2["Gerar DataFrame Limpo"]

    D -- "Modelagem ML" --> G1["core/modeling.py<br/>train_model()"]
    G1 --> G2["evaluate_model()"]
    G2 --> G3["Retornar Modelo e Métricas de Avaliação"]

    D -- "Visualização" --> H1["visualization/plots.py<br/>plot_distribution()"]
    H1 --> H2["Gerar e Salvar Figura (PNG)"]

    E3 --> OK{"Execução<br/>Bem-sucedida?"}
    F2 --> OK
    G3 --> OK
    H2 --> OK

    OK -- Não --> ERR
    OK -- Sim --> DONE["Registrar Conclusão e Retornar Artefato"]
```

---

### 2.11. Testes

Os testes automatizados utilizam `pytest`, configurados em `pyproject.toml` sob `[tool.pytest.ini_options]`, com fixtures em `tests/conftest.py` e testes unitários em `tests/test_main.py`.

#### Comandos de Teste

| Objetivo | Comando |
| :--- | :--- |
| **Executar toda a suíte de testes** | `pytest` |
| **Executar com relatório de cobertura no terminal** | `pytest --cov=src/DataScienceProfessionalPortfolio --cov-report=term-missing` |

#### Integração Contínua

O workflow do GitHub Actions em `.github/workflows/tests.yml` executa a suíte de testes a cada push e pull request direcionado à branch `main`, nas versões suportadas do Python. Falhas nos testes bloqueiam o merge, garantindo a estabilidade do framework.

> **Nota:** Percentuais atuais de cobertura de código, quantidade total de testes e a lista exata de versões do Python configuradas em `.github/workflows/tests.yml` não foram especificados na documentação original.

---

### 2.12. Melhorias Futuras

As adições planejadas no roadmap do framework incluem:

- Conectores ETL adicionais (APIs REST e bancos de dados SQL).
- Utilitários estendidos de avaliação de modelos (validação cruzada e curvas de aprendizado).
- Componentes reutilizáveis de dashboard em Streamlit.
- Projetos de exemplo demonstrando workflows ponta a ponta.

Consulte `CHANGELOG.md` para o histórico detalhado de alterações.

---

### 2.13. Contribuição

Este é um projeto de portfólio pessoal, mas sugestões e relatos de problemas são bem-vindos.

1. Abra uma issue descrevendo a alteração proposta antes de enviar um pull request.
2. Certifique-se de que todos os testes passem localmente (`pytest`), pois o workflow de CI em `.github/workflows/tests.yml` bloqueia merges na branch `main` em caso de falha.

---

### 2.14. Licença

Este projeto é distribuído sob a **Licença MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

---

### 2.15. Autor

Os dados de autoria (nome, perfil no GitHub e informações de contacto) não foram especificados na documentação original.