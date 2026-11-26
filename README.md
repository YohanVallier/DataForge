<a id="top"></a>

<div align="center">

# 🧰 DataForge

### Modular Data Science Framework · Framework Modular de Ciência de Dados

<p>
  <a href="#english"><kbd> 🇺🇸 English Documentation </kbd></a>
  &nbsp;&nbsp;
  <a href="#portugues"><kbd> 🇧🇷 Documentação em Português </kbd></a>
</p>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3200&pause=1000&color=A855F7&center=true&vCenter=true&width=760&lines=Modular+Python+Foundation+for+Data+Science+Portfolios;ETL+Pipelines+%C2%B7+Data+Handling+%C2%B7+ML+Modeling+%C2%B7+Visualization;Clean+Architecture+%C2%B7+Pytest+Coverage+%C2%B7+GitHub+Actions+CI" alt="DataForge Typing Animation" />

<p>
  <kbd>🐍 Python 3.10+</kbd> &nbsp;
  <kbd>📊 Pandas · NumPy · PyArrow</kbd> &nbsp;
  <kbd>🤖 Scikit-learn · XGBoost</kbd> &nbsp;
  <kbd>🧪 Pytest + GitHub Actions CI</kbd> &nbsp;
  <kbd>📄 MIT License</kbd>
</p>

<p>
  <img src="https://skillicons.dev/icons?i=py,sklearn,postgres,git,github,githubactions&theme=dark" alt="DataForge Core Stack Icons" />
</p>

</div>

---

<a id="english"></a>

## 🇺🇸 English Documentation

> **Focus on the analytical problem — not on repetitive boilerplate.**

**DataForge** is a modular, production-oriented Python framework designed as the engineering foundation for a **professional Data Science portfolio**. It provides reusable building blocks for data handling, machine learning modeling, ETL pipelines, shared utilities, and data visualization — enforcing clean software engineering standards while staying lightweight enough for focused analytical projects.

<div align="center">

[Overview](#en-overview) · [Architecture](#en-architecture) · [Features](#en-features) · [Stack](#en-stack) · [Installation](#en-installation) · [Usage](#en-usage) · [Testing & CI](#en-testing) · [Principles](#en-principles) · [Roadmap](#en-roadmap) · [License](#en-license)

</div>

---

<a id="en-overview"></a>

### 🎯 Overview

Instead of scattering logic across monolithic notebooks, **DataForge** structures reusable Data Science code into clearly separated, importable Python subpackages under `src/DataForge/`. Any downstream project (sales analysis, churn prediction, demand forecasting, anomaly detection, etc.) can import and extend these building blocks while inheriting consistent engineering practices.

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>⚙️ <code>DataForge.core</code></h4>
      <p>Core analytical engines separated into <code>data_handling.py</code> (loading, cleaning, preprocessing) and <code>modeling.py</code> (ML training and evaluation workflows).</p>
    </td>
    <td width="50%" valign="top">
      <h4>🔄 <code>DataForge.services</code></h4>
      <p>Structured ETL pipeline definitions in <code>etl.py</code> for ingesting, transforming, and persisting datasets across storage formats.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4>📊 <code>DataForge.visualization</code></h4>
      <p>Reusable plotting utilities in <code>plots.py</code> built on top of <strong>Matplotlib</strong>, <strong>Seaborn</strong>, and <strong>Plotly</strong> for EDA and reporting.</p>
    </td>
    <td width="50%" valign="top">
      <h4>🛠️ <code>DataForge.utils</code> &amp; <code>config</code></h4>
      <p>Shared helpers (<code>helpers.py</code>) for logging, paths, and validation, paired with centralized environment configuration in <code>config/settings.py</code>.</p>
    </td>
  </tr>
</table>

---

<a id="en-architecture"></a>

### 🏗️ Architecture & Analytical Pipeline

```mermaid
flowchart TB
    subgraph Entry["Entry Points"]
        CLI["CLI Module<br/>(src/DataForge/__main__.py)"]
        PRJ["Portfolio Projects<br/>(Sales · Churn · Forecasting)"]
    end

    subgraph Domain["src/DataForge/ Subpackages"]
        ETL["services/etl.py<br/>ETL Pipelines"]
        DH["core/data_handling.py<br/>Loading, Cleaning & Preprocessing"]
        ML["core/modeling.py<br/>Training & Evaluation"]
        VIZ["visualization/plots.py<br/>Matplotlib · Seaborn · Plotly"]
    end

    subgraph Foundation["Shared Foundation"]
        CFG["config/settings.py<br/>Centralized Env Vars (.env)"]
        UTL["utils/helpers.py<br/>Logging · Paths · Validation"]
    end

    subgraph Quality["Quality & Audit"]
        TST["tests/ (conftest.py · test_main.py)"]
        CI["GitHub Actions (.github/workflows/tests.yml)"]
        AUD["AUDIT_REPORT.md"]
    end

    CLI --> ETL
    CLI --> DH
    PRJ --> ETL
    PRJ --> DH
    PRJ --> ML
    PRJ --> VIZ

    ETL --> DH
    DH --> ML
    DH --> VIZ
    ML --> VIZ

    ETL --> CFG
    DH --> CFG
    ML --> CFG
    ETL --> UTL
    DH --> UTL
    ML --> UTL
    VIZ --> UTL

    TST -.-> Domain
    CI -.-> TST
    AUD -.-> Domain
```

#### ⚡ End-to-End Data Flow

```mermaid
flowchart LR
    A[Raw Sources<br/>CSV · Excel · SQL · API] --> B[DataForge.services.etl<br/>Ingest & Transform]
    B --> C[DataForge.core.data_handling<br/>Clean & Preprocess]
    C --> D[DataForge.core.modeling<br/>Train & Evaluate ML]
    C --> E[DataForge.visualization.plots<br/>EDA & Visual Reports]
    D --> F[Deliverables<br/>Metrics · Parquet · Charts]
    E --> F
```

<details>
<summary><strong>📁 Project Directory Structure (Click to expand)</strong></summary>

```text
DataForge/
├── .github/
│   └── workflows/
│       └── tests.yml               # GitHub Actions CI pipeline
├── config/
│   └── settings.py                 # Centralized configuration settings
├── src/
│   └── DataForge/
│       ├── __init__.py             # Package metadata & public exports
│       ├── __main__.py             # CLI entry point (python -m DataForge)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── data_handling.py    # Data loading, cleaning & preprocessing
│       │   └── modeling.py         # ML model training & evaluation
│       ├── services/
│       │   ├── __init__.py
│       │   └── etl.py              # ETL pipeline definitions
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py          # Shared utility helpers
│       └── visualization/
│           ├── __init__.py
│           └── plots.py            # Data visualization utilities
├── tests/
│   ├── conftest.py                 # Pytest configuration & shared fixtures
│   └── test_main.py                # Unit tests for core functionality
├── .env.example                    # Environment variable template
├── .gitattributes                  # Cross-platform LF line-ending rules
├── .gitignore                      # Python & environment ignore rules
├── AUDIT_REPORT.md                 # Technical audit report
├── CHANGELOG.md                    # Version history
├── LICENSE                         # MIT License
├── pyproject.toml                  # Build system & pytest configuration
├── README.md                       # Bilingual documentation
└── requirements.txt                # Project dependencies
```

</details>

---

<a id="en-features"></a>

### ✨ Key Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>🧩 Software Engineering Standards</h4>
      <ul>
        <li><strong>Modular <code>src/</code> layout</strong> with explicit package boundaries.</li>
        <li><strong>Type hints &amp; docstrings</strong> across public modules and functions.</li>
        <li><strong>Structured logging</strong> — zero <code>print()</code> statements in library code.</li>
        <li><strong>Explicit exception handling</strong> with clear, actionable messages.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h4>🔐 Configuration, Reproducibility &amp; Quality</h4>
      <ul>
        <li><strong>Centralized settings</strong> in <code>config/settings.py</code> via environment variables.</li>
        <li><strong>No hardcoded secrets</strong> — template provided in <code>.env.example</code>.</li>
        <li><strong>Reproducible setup</strong> via <code>pyproject.toml</code>, <code>requirements.txt</code>, and <code>.gitattributes</code>.</li>
        <li><strong>Automated tests, CI &amp; Technical Audit</strong> (<code>pytest</code>, GitHub Actions, <code>AUDIT_REPORT.md</code>).</li>
      </ul>
    </td>
  </tr>
</table>

---

<a id="en-stack"></a>

### 🧰 Requirements & Technology Stack

> [!NOTE]
> Requires **Python 3.10 or newer** (`pandas>=2.0` ecosystem).

| Category | Tools & Libraries | Role in DataForge |
|---|---|---|
| **Data Manipulation & I/O** | `Pandas` · `NumPy` · `PyArrow` · `OpenPyXL` · `SQLAlchemy` | Tabular transformations, numerical computing, Parquet/Excel I/O, and SQL integration. |
| **Machine Learning** | `Scikit-learn` · `XGBoost` | Model training, feature pipelines, gradient boosting, and evaluation metrics. |
| **Visualization & Apps** | `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit` | Static/interactive visualizations and data application components. |
| **External Ingestion** | `Requests` · `BeautifulSoup4` | HTTP API requests and HTML data extraction. |
| **Testing & Automation** | `Pytest` · `pytest-cov` · `GitHub Actions` | Unit tests, shared fixtures, coverage reports, and automated CI checks. |

---

<a id="en-installation"></a>

### 🚀 Installation & Configuration

<table>
  <tr>
    <td width="55%" valign="top">
      <h4>💻 1. Clone &amp; Install Locally</h4>

```bash
# Clone the repository
git clone https://github.com/YohanVallier/DataForge.git
cd DataForge

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Install in editable mode with dev extras
pip install --upgrade pip
pip install -e ".[dev]"

# Or install runtime dependencies only
pip install -r requirements.txt
```

</td>
<td width="45%" valign="top">
  <h4>⚙️ 2. Environment Configuration</h4>
  <p>Settings are centralized in <code>config/settings.py</code> and read from environment variables. Sensitive values are <strong>never</strong> hardcoded.</p>

```bash
# Copy environment template
cp .env.example .env

# Export variables (or load via python-dotenv)
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
export LOG_LEVEL="INFO"
```

  <p><em>Note: <code>.env</code> is automatically excluded from version control via <code>.gitignore</code>.</em></p>
</td>
  </tr>
</table>

---

<a id="en-usage"></a>

### 💻 Usage Examples

The package is importable as **`DataForge`** and includes a command-line entry point (`src/DataForge/__main__.py`).

<details open>
<summary><strong>1. Data Handling — <code>DataForge.core.data_handling</code></strong></summary>

```python
from DataForge.core.data_handling import load_csv, clean_dataframe

df = load_csv("data/raw/sales.csv")
df_clean = clean_dataframe(df, drop_duplicates=True)
```

</details>

<details>
<summary><strong>2. Machine Learning Modeling — <code>DataForge.core.modeling</code></strong></summary>

```python
from DataForge.core.modeling import train_model, evaluate_model

model = train_model(X_train, y_train, model_type="random_forest")
metrics = evaluate_model(model, X_test, y_test)
```

</details>

<details>
<summary><strong>3. ETL Pipelines — <code>DataForge.services.etl</code></strong></summary>

```python
from DataForge.services.etl import run_etl_pipeline

run_etl_pipeline(
    source="data/raw/transactions.csv",
    destination="data/processed/transactions.parquet",
)
```

</details>

<details>
<summary><strong>4. Visualization — <code>DataForge.visualization.plots</code></strong></summary>

```python
from DataForge.visualization.plots import plot_distribution

fig = plot_distribution(df, column="revenue", kind="hist")
fig.savefig("reports/revenue_distribution.png")
```

</details>

<details>
<summary><strong>5. Command-Line Entry Point — <code>python -m DataForge</code></strong></summary>

```bash
# Run directly as a Python module
python -m DataForge --help
```

</details>

---

<a id="en-testing"></a>

### 🧪 Running Tests & Continuous Integration

```bash
# Run the full test suite (configured in pyproject.toml)
pytest

# Run with line-by-line coverage reporting
pytest --cov=src/DataForge --cov-report=term-missing
```

> [!TIP]
> **Continuous Integration & Technical Audit:** The workflow in `.github/workflows/tests.yml` automatically executes the test suite (`tests/conftest.py` & `tests/test_main.py`) on every push and pull request targeting `main`. Architectural and code-quality review notes are also documented in [`AUDIT_REPORT.md`](AUDIT_REPORT.md).

---

<a id="en-principles"></a>

### 🎯 Design Principles

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>1. Separation of Concerns</strong><br/>
      Data handling, modeling, ETL, utilities, and visualization live in isolated subpackages.
    </td>
    <td width="33%" valign="top">
      <strong>2. Explicit Over Implicit</strong><br/>
      Consistent type hints, docstrings, and descriptive named exceptions.
    </td>
    <td width="33%" valign="top">
      <strong>3. Structured Logging</strong><br/>
      Uses Python's <code>logging</code> module instead of <code>print()</code> in library code.
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <strong>4. Zero Hardcoded Secrets</strong><br/>
      All sensitive settings are injected via environment variables.
    </td>
    <td width="33%" valign="top">
      <strong>5. Reproducibility</strong><br/>
      Standardized dependencies, LF line endings (<code>.gitattributes</code>), and deterministic pipelines.
    </td>
    <td width="33%" valign="top">
      <strong>6. Proportional Complexity</strong><br/>
      Architecture scales alongside real analytical problems — never ahead of them.
    </td>
  </tr>
</table>

---

<a id="en-roadmap"></a>

### 🗺️ Roadmap & Contributing

<table>
  <tr>
    <td width="55%" valign="top">
      <h4>🛣️ Planned Enhancements</h4>
      <ul>
        <li>Additional ETL connectors (REST APIs, SQL databases).</li>
        <li>Extended model evaluation utilities (cross-validation, learning curves).</li>
        <li>Reusable Streamlit dashboard components.</li>
        <li>End-to-end example projects built on top of DataForge.</li>
      </ul>
      <p>See <a href="CHANGELOG.md"><code>CHANGELOG.md</code></a> for version history and <a href="AUDIT_REPORT.md"><code>AUDIT_REPORT.md</code></a> for technical audit findings.</p>
    </td>
    <td width="45%" valign="top">
      <h4>🤝 Contributing</h4>
      <p>This is a personal portfolio foundation, and constructive suggestions or issue reports are always welcome.</p>
      <p>Please open an issue describing your proposed improvement before submitting a pull request.</p>
    </td>
  </tr>
</table>

---

<a id="en-license"></a>

### 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full terms.

<div align="center">

**DataForge** — *Modular engineering foundation for Data Science projects.*

[⬆️ Back to top](#top) · [🇧🇷 Ir para a versão em Português](#portugues)

</div>

---

<a id="portugues"></a>

## 🇧🇷 Documentação em Português

> **Foque no problema analítico — não no código repetitivo.**

O **DataForge** é um framework modular em Python, orientado à produção, projetado como a base de engenharia para um **portfólio profissional de Ciência de Dados**. Ele reúne blocos reutilizáveis para manipulação de dados, modelagem de Machine Learning, pipelines de ETL, utilitários compartilhados e visualização — aplicando práticas sólidas de engenharia de software sem abrir mão da leveza necessária para projetos analíticos objetivos.

<div align="center">

[Visão Geral](#pt-overview) · [Arquitetura](#pt-architecture) · [Funcionalidades](#pt-features) · [Tecnologias](#pt-stack) · [Instalação](#pt-installation) · [Uso](#pt-usage) · [Testes & CI](#pt-testing) · [Princípios](#pt-principles) · [Roadmap](#pt-roadmap) · [Licença](#pt-license)

</div>

---

<a id="pt-overview"></a>

### 🎯 Visão Geral

Em vez de espalhar lógica em notebooks monolíticos, o **DataForge** organiza código reutilizável de Ciência de Dados em subpacotes Python claramente separados e importáveis dentro de `src/DataForge/`. Qualquer projeto derivado (análise de vendas, previsão de churn, previsão de demanda, detecção de anomalias, etc.) pode importar e estender esses módulos herdando padrões consistentes de engenharia.

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>⚙️ <code>DataForge.core</code></h4>
      <p>Núcleo analítico dividido em <code>data_handling.py</code> (carregamento, limpeza e pré-processamento) e <code>modeling.py</code> (treinamento e avaliação de modelos de ML).</p>
    </td>
    <td width="50%" valign="top">
      <h4>🔄 <code>DataForge.services</code></h4>
      <p>Definições estruturadas de pipelines de ETL em <code>etl.py</code> para ingestão, transformação e persistência de dados entre formatos.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4>📊 <code>DataForge.visualization</code></h4>
      <p>Utilitários reutilizáveis de visualização em <code>plots.py</code> construídos sobre <strong>Matplotlib</strong>, <strong>Seaborn</strong> e <strong>Plotly</strong> para AED e relatórios.</p>
    </td>
    <td width="50%" valign="top">
      <h4>🛠️ <code>DataForge.utils</code> &amp; <code>config</code></h4>
      <p>Helpers compartilhados (<code>helpers.py</code>) para logging, caminhos e validação, integrados à configuração centralizada em <code>config/settings.py</code>.</p>
    </td>
  </tr>
</table>

---

<a id="pt-architecture"></a>

### 🏗️ Arquitetura & Fluxo Analítico

```mermaid
flowchart TB
    subgraph Entry["Pontos de Entrada"]
        CLI["Módulo CLI<br/>(src/DataForge/__main__.py)"]
        PRJ["Projetos do Portfólio<br/>(Vendas · Churn · Demanda)"]
    end

    subgraph Domain["Subpacotes em src/DataForge/"]
        ETL["services/etl.py<br/>Pipelines de ETL"]
        DH["core/data_handling.py<br/>Carga, Limpeza & Pré-processamento"]
        ML["core/modeling.py<br/>Treinamento & Avaliação"]
        VIZ["visualization/plots.py<br/>Matplotlib · Seaborn · Plotly"]
    end

    subgraph Foundation["Base Compartilhada"]
        CFG["config/settings.py<br/>Variáveis de Ambiente (.env)"]
        UTL["utils/helpers.py<br/>Logging · Caminhos · Validação"]
    end

    subgraph Quality["Qualidade & Auditoria"]
        TST["tests/ (conftest.py · test_main.py)"]
        CI["GitHub Actions (.github/workflows/tests.yml)"]
        AUD["AUDIT_REPORT.md"]
    end

    CLI --> ETL
    CLI --> DH
    PRJ --> ETL
    PRJ --> DH
    PRJ --> ML
    PRJ --> VIZ

    ETL --> DH
    DH --> ML
    DH --> VIZ
    ML --> VIZ

    ETL --> CFG
    DH --> CFG
    ML --> CFG
    ETL --> UTL
    DH --> UTL
    ML --> UTL
    VIZ --> UTL

    TST -.-> Domain
    CI -.-> TST
    AUD -.-> Domain
```

#### ⚡ Fluxo de Dados Ponta a Ponta

```mermaid
flowchart LR
    A[Fontes Brutas<br/>CSV · Excel · SQL · API] --> B[DataForge.services.etl<br/>Ingestão & Transformação]
    B --> C[DataForge.core.data_handling<br/>Limpeza & Pré-processamento]
    C --> D[DataForge.core.modeling<br/>Treino & Avaliação de ML]
    C --> E[DataForge.visualization.plots<br/>AED & Relatórios Visuais]
    D --> F[Entregáveis<br/>Métricas · Parquet · Gráficos]
    E --> F
```

<details>
<summary><strong>📁 Estrutura de Diretórios do Projeto (Clique para expandir)</strong></summary>

```text
DataForge/
├── .github/
│   └── workflows/
│       └── tests.yml               # Pipeline de CI no GitHub Actions
├── config/
│   └── settings.py                 # Configurações centralizadas
├── src/
│   └── DataForge/
│       ├── __init__.py             # Metadados do pacote e exports públicos
│       ├── __main__.py             # Ponto de entrada CLI (python -m DataForge)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── data_handling.py    # Carregamento, limpeza e pré-processamento
│       │   └── modeling.py         # Treinamento e avaliação de modelos ML
│       ├── services/
│       │   ├── __init__.py
│       │   └── etl.py              # Definições de pipelines ETL
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py          # Funções utilitárias compartilhadas
│       └── visualization/
│           ├── __init__.py
│           └── plots.py            # Utilitários de visualização de dados
├── tests/
│   ├── conftest.py                 # Configuração do Pytest e fixtures
│   └── test_main.py                # Testes unitários das funcionalidades centrais
├── .env.example                    # Modelo de variáveis de ambiente
├── .gitattributes                  # Normalização multiplataforma de quebras de linha (LF)
├── .gitignore                      # Regras de exclusão para Python e ambientes
├── AUDIT_REPORT.md                 # Relatório de auditoria técnica
├── CHANGELOG.md                    # Histórico de versões
├── LICENSE                         # Licença MIT
├── pyproject.toml                  # Build system e configuração do Pytest
├── README.md                       # Documentação bilíngue
└── requirements.txt                # Dependências do projeto
```

</details>

---

<a id="pt-features"></a>

### ✨ Principais Funcionalidades

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>🧩 Padrões de Engenharia de Software</h4>
      <ul>
        <li><strong>Layout modular em <code>src/</code></strong> com fronteiras claras entre pacotes.</li>
        <li><strong>Type hints e docstrings</strong> nos módulos e funções públicas.</li>
        <li><strong>Logging estruturado</strong> — zero uso de <code>print()</code> no código da biblioteca.</li>
        <li><strong>Tratamento explícito de exceções</strong> com mensagens claras e informativas.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h4>🔐 Configuração, Reprodutibilidade &amp; Qualidade</h4>
      <ul>
        <li><strong>Configuração centralizada</strong> em <code>config/settings.py</code> via variáveis de ambiente.</li>
        <li><strong>Zero segredos no código</strong> — modelo pronto em <code>.env.example</code>.</li>
        <li><strong>Setup reproduzível</strong> via <code>pyproject.toml</code>, <code>requirements.txt</code> e <code>.gitattributes</code>.</li>
        <li><strong>Testes automatizados, CI &amp; Auditoria Técnica</strong> (<code>pytest</code>, GitHub Actions, <code>AUDIT_REPORT.md</code>).</li>
      </ul>
    </td>
  </tr>
</table>

---

<a id="pt-stack"></a>

### 🧰 Pré-requisitos & Stack Tecnológica

> [!NOTE]
> Requer **Python 3.10 ou superior** (ecossistema `pandas>=2.0`).

| Categoria | Ferramentas & Bibliotecas | Papel no DataForge |
|---|---|---|
| **Manipulação & I/O** | `Pandas` · `NumPy` · `PyArrow` · `OpenPyXL` · `SQLAlchemy` | Transformações tabulares, computação numérica, leitura/escrita Parquet/Excel e integração SQL. |
| **Machine Learning** | `Scikit-learn` · `XGBoost` | Treinamento de modelos, pipelines de features, gradient boosting e métricas de avaliação. |
| **Visualização & Apps** | `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit` | Gráficos estáticos/interativos e componentes para aplicações analíticas. |
| **Coleta Externa** | `Requests` · `BeautifulSoup4` | Requisições a APIs HTTP e extração de dados em HTML. |
| **Testes & Automação** | `Pytest` · `pytest-cov` · `GitHub Actions` | Testes unitários, fixtures compartilhadas, relatórios de cobertura e validações em CI. |

---

<a id="pt-installation"></a>

### 🚀 Instalação & Configuração

<table>
  <tr>
    <td width="55%" valign="top">
      <h4>💻 1. Clone e Instale Localmente</h4>

```bash
# Clone o repositório
git clone https://github.com/YohanVallier/DataForge.git
cd DataForge

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Instale em modo editável com dependências de desenvolvimento
pip install --upgrade pip
pip install -e ".[dev]"

# Ou instale apenas as dependências de execução
pip install -r requirements.txt
```

</td>
<td width="45%" valign="top">
  <h4>⚙️ 2. Configuração de Ambiente</h4>
  <p>As configurações ficam centralizadas em <code>config/settings.py</code> e são lidas por variáveis de ambiente. Dados sensíveis <strong>nunca</strong> ficam expostos no código.</p>

```bash
# Copie o modelo de variáveis
cp .env.example .env

# Exporte as variáveis (ou carregue via python-dotenv)
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
export LOG_LEVEL="INFO"
```

  <p><em>Nota: o arquivo <code>.env</code> já é ignorado pelo Git no <code>.gitignore</code>.</em></p>
</td>
  </tr>
</table>

---

<a id="pt-usage"></a>

### 💻 Exemplos de Uso

O pacote é importável como **`DataForge`** e disponibiliza um ponto de entrada via linha de comando (`src/DataForge/__main__.py`).

<details open>
<summary><strong>1. Manipulação de Dados — <code>DataForge.core.data_handling</code></strong></summary>

```python
from DataForge.core.data_handling import load_csv, clean_dataframe

df = load_csv("data/raw/sales.csv")
df_clean = clean_dataframe(df, drop_duplicates=True)
```

</details>

<details>
<summary><strong>2. Modelagem de Machine Learning — <code>DataForge.core.modeling</code></strong></summary>

```python
from DataForge.core.modeling import train_model, evaluate_model

model = train_model(X_train, y_train, model_type="random_forest")
metrics = evaluate_model(model, X_test, y_test)
```

</details>

<details>
<summary><strong>3. Pipelines de ETL — <code>DataForge.services.etl</code></strong></summary>

```python
from DataForge.services.etl import run_etl_pipeline

run_etl_pipeline(
    source="data/raw/transactions.csv",
    destination="data/processed/transactions.parquet",
)
```

</details>

<details>
<summary><strong>4. Visualização — <code>DataForge.visualization.plots</code></strong></summary>

```python
from DataForge.visualization.plots import plot_distribution

fig = plot_distribution(df, column="revenue", kind="hist")
fig.savefig("reports/revenue_distribution.png")
```

</details>

<details>
<summary><strong>5. Ponto de Entrada CLI — <code>python -m DataForge</code></strong></summary>

```bash
# Execute diretamente como módulo Python
python -m DataForge --help
```

</details>

---

<a id="pt-testing"></a>

### 🧪 Execução de Testes & Integração Contínua

```bash
# Executar toda a suíte de testes (configurada no pyproject.toml)
pytest

# Executar com relatório de cobertura linha a linha
pytest --cov=src/DataForge --cov-report=term-missing
```

> [!TIP]
> **Integração Contínua & Auditoria Técnica:** O workflow em `.github/workflows/tests.yml` executa automaticamente a suíte de testes (`tests/conftest.py` e `tests/test_main.py`) a cada push e pull request para a branch `main`. As notas de revisão técnica e qualidade também estão documentadas em [`AUDIT_REPORT.md`](AUDIT_REPORT.md).

---

<a id="pt-principles"></a>

### 🎯 Princípios de Design

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>1. Separação de Responsabilidades</strong><br/>
      Manipulação de dados, modelagem, ETL, utilitários e visualização vivem em subpacotes isolados.
    </td>
    <td width="33%" valign="top">
      <strong>2. Explícito Acima de Implícito</strong><br/>
      Type hints consistentes, docstrings e exceções nomeadas e claras.
    </td>
    <td width="33%" valign="top">
      <strong>3. Logging Estruturado</strong><br/>
      Uso do módulo <code>logging</code> do Python no lugar de <code>print()</code> na biblioteca.
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <strong>4. Zero Segredos no Código</strong><br/>
      Todas as configurações sensíveis são injetadas via variáveis de ambiente.
    </td>
    <td width="33%" valign="top">
      <strong>5. Reprodutibilidade</strong><br/>
      Dependências padronizadas, normalização LF (<code>.gitattributes</code>) e pipelines determinísticos.
    </td>
    <td width="33%" valign="top">
      <strong>6. Complexidade Proporcional</strong><br/>
      A arquitetura acompanha o crescimento real dos problemas — sem excessos antecipados.
    </td>
  </tr>
</table>

---

<a id="pt-roadmap"></a>

### 🗺️ Roadmap & Contribuição

<table>
  <tr>
    <td width="55%" valign="top">
      <h4>🛣️ Próximas Evoluções</h4>
      <ul>
        <li>Novos conectores de ETL (APIs REST e bancos SQL).</li>
        <li>Utilitários avançados de avaliação (validação cruzada, curvas de aprendizado).</li>
        <li>Componentes reutilizáveis para dashboards em Streamlit.</li>
        <li>Projetos de exemplo ponta a ponta construídos sobre o DataForge.</li>
      </ul>
      <p>Consulte <a href="CHANGELOG.md"><code>CHANGELOG.md</code></a> para o histórico de versões e <a href="AUDIT_REPORT.md"><code>AUDIT_REPORT.md</code></a> para o relatório de auditoria técnica.</p>
    </td>
    <td width="45%" valign="top">
      <h4>🤝 Contribuição</h4>
      <p>Este é um repositório pessoal de portfólio, mas sugestões construtivas e relatos de problemas são sempre bem-vindos.</p>
      <p>Abra uma <em>issue</em> descrevendo a proposta antes de enviar um <em>pull request</em>.</p>
    </td>
  </tr>
</table>

---

<a id="pt-license"></a>

### 📄 Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para os termos completos.

<div align="center">

**DataForge** — *Base modular de engenharia para projetos de Ciência de Dados.*

[⬆️ Voltar ao topo](#top) · [🇺🇸 Switch to English](#english)

</div>