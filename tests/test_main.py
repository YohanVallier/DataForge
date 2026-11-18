"""Unit tests for the core functionality of DataScienceProfessionalPortfolio.

This module exercises the public API of the framework's core, services,
utilities, and visualization modules. Tests are grouped by module and rely on
the fixtures defined in :mod:`tests.conftest`.

Coverage
--------
- :mod:`DataScienceProfessionalPortfolio.core.data_handling`
- :mod:`DataScienceProfessionalPortfolio.core.modeling`
- :mod:`DataScienceProfessionalPortfolio.services.etl`
- :mod:`DataScienceProfessionalPortfolio.utils.helpers`
- :mod:`DataScienceProfessionalPortfolio.visualization.plots`
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from DataScienceProfessionalPortfolio import __version__
from DataScienceProfessionalPortfolio.core.data_handling import (
    clean_dataframe,
    load_csv,
    load_parquet,
    save_dataframe,
    split_features_target,
    train_test_split_df,
)
from DataScienceProfessionalPortfolio.core.modeling import (
    cross_validate_model,
    evaluate_model,
    load_model,
    predict,
    save_model,
    train_model,
)
from DataScienceProfessionalPortfolio.services.etl import (
    ETLResult,
    extract,
    load,
    run_etl_pipeline,
    transform,
)
from DataScienceProfessionalPortfolio.utils.helpers import (
    chunked,
    ensure_directory,
    get_logger,
    resolve_path,
    safe_divide,
    timer,
    validate_columns,
)
from DataScienceProfessionalPortfolio.visualization.plots import (
    plot_bar,
    plot_correlation_matrix,
    plot_distribution,
    plot_time_series,
    save_figure,
)


# ---------------------------------------------------------------------------
# Package metadata
# ---------------------------------------------------------------------------


def test_package_version_is_string() -> None:
    """The package exposes a non-empty version string."""
    assert isinstance(__version__, str)
    assert __version__


# ---------------------------------------------------------------------------
# utils.helpers
# ---------------------------------------------------------------------------


def test_get_logger_returns_configured_logger() -> None:
    """``get_logger`` returns a logger with a stream handler attached."""
    logger = get_logger("test.helpers.logger", level="DEBUG")
    try:
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.DEBUG
        assert any(
            isinstance(handler, logging.StreamHandler)
            for handler in logger.handlers
        )
    finally:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()


def test_get_logger_rejects_invalid_level() -> None:
    """An invalid log level raises ``ValueError``."""
    with pytest.raises(ValueError):
        get_logger("test.helpers.invalid", level="NOT_A_LEVEL")


def test_ensure_directory_creates_nested_path(tmp_path: Path) -> None:
    """``ensure_directory`` creates nested directories and returns the path."""
    target = tmp_path / "a" / "b" / "c"
    result = ensure_directory(target)
    assert result == target
    assert target.is_dir()


def test_resolve_path_relative_to_base(tmp_path: Path) -> None:
    """Relative paths are resolved against the provided base directory."""
    resolved = resolve_path("data/file.csv", base=tmp_path)
    assert resolved == (tmp_path / "data" / "file.csv").resolve()


def test_resolve_path_absolute_unchanged(tmp_path: Path) -> None:
    """Absolute paths are returned unchanged."""
    absolute = tmp_path / "file.csv"
    assert resolve_path(absolute) == absolute


def test_validate_columns_passes(sample_dataframe: pd.DataFrame) -> None:
    """``validate_columns`` returns ``None`` when all columns are present."""
    assert validate_columns(sample_dataframe, ["revenue", "units"]) is None


def test_validate_columns_raises_on_missing(
    sample_dataframe: pd.DataFrame,
) -> None:
    """Missing columns raise ``KeyError`` with a descriptive message."""
    with pytest.raises(KeyError):
        validate_columns(sample_dataframe, ["revenue", "missing_column"])


def test_validate_columns_rejects_non_dataframe() -> None:
    """Non-DataFrame inputs raise ``TypeError``."""
    with pytest.raises(TypeError):
        validate_columns([1, 2, 3], ["a"])  # type: ignore[arg-type]


def test_timer_records_elapsed() -> None:
    """The ``timer`` context manager records elapsed time."""
    with timer("test") as result:
        pass
    assert "elapsed" in result
    assert result["elapsed"] >= 0.0


def test_chunked_splits_iterable() -> None:
    """``chunked`` yields lists of at most ``size`` items."""
    chunks = list(chunked(range(5), 2))
    assert chunks == [[0, 1], [2, 3], [4]]


def test_chunked_rejects_invalid_size() -> None:
    """A non-positive chunk size raises ``ValueError``."""
    with pytest.raises(ValueError):
        list(chunked(range(3), 0))


def test_safe_divide_handles_zero_denominator() -> None:
    """``safe_divide`` returns the default when the denominator is zero."""
    assert safe_divide(10.0, 2.0) == 5.0
    assert safe_divide(10.0, 0.0) == 0.0
    assert safe_divide(10.0, 0.0, default=-1.0) == -1.0


# ---------------------------------------------------------------------------
# core.data_handling
# ---------------------------------------------------------------------------


def test_load_csv_returns_dataframe(tmp_csv_file: Path) -> None:
    """``load_csv`` reads a CSV file into a DataFrame."""
    df = load_csv(tmp_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def test_load_csv_missing_file_raises(tmp_path: Path) -> None:
    """A missing CSV file raises ``FileNotFoundError``."""
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "does_not_exist.csv")


def test_load_parquet_returns_dataframe(tmp_parquet_file: Path) -> None:
    """``load_parquet`` reads a Parquet file into a DataFrame."""
    df = load_parquet(tmp_parquet_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def test_load_parquet_missing_file_raises(tmp_path: Path) -> None:
    """A missing Parquet file raises ``FileNotFoundError``."""
    with pytest.raises(FileNotFoundError):
        load_parquet(tmp_path / "does_not_exist.parquet")


def test_save_dataframe_csv_roundtrip(
    sample_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """A DataFrame saved as CSV can be read back unchanged."""
    dest = tmp_path / "out" / "data.csv"
    written = save_dataframe(sample_dataframe, dest)
    assert written == dest
    assert dest.is_file()
    reloaded = load_csv(dest)
    assert list(reloaded.columns) == list(sample_dataframe.columns)
    assert len(reloaded) == len(sample_dataframe)


def test_save_dataframe_parquet_roundtrip(
    sample_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """A DataFrame saved as Parquet can be read back unchanged."""
    dest = tmp_path / "out" / "data.parquet"
    written = save_dataframe(sample_dataframe, dest)
    assert written == dest
    assert dest.is_file()
    reloaded = load_parquet(dest)
    assert len(reloaded) == len(sample_dataframe)


def test_save_dataframe_rejects_unsupported_format(
    sample_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """An unsupported output format raises ``ValueError``."""
    with pytest.raises(ValueError):
        save_dataframe(sample_dataframe, tmp_path / "data.json")


def test_save_dataframe_rejects_non_dataframe(tmp_path: Path) -> None:
    """A non-DataFrame input raises ``TypeError``."""
    with pytest.raises(TypeError):
        save_dataframe([1, 2, 3], tmp_path / "data.csv")  # type: ignore[arg-type]


def test_clean_dataframe_normalizes_columns() -> None:
    """Column names are stripped, lowercased, and underscored."""
    df = pd.DataFrame({" Customer ID ": [1, 2], "Total Revenue": [10.0, 20.0]})
    cleaned = clean_dataframe(df)
    assert list(cleaned.columns) == ["customer_id", "total_revenue"]


def test_clean_dataframe_drops_duplicates() -> None:
    """Fully duplicated rows are removed."""
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    cleaned = clean_dataframe(df)
    assert len(cleaned) == 2


def test_clean_dataframe_does_not_mutate_input() -> None:
    """The input DataFrame is never mutated."""
    df = pd.DataFrame({"A": [1, 1, 2]})
    original = df.copy()
    clean_dataframe(df)
    pd.testing.assert_frame_equal(df, original)


def test_clean_dataframe_missing_strategy_mean() -> None:
    """The ``mean`` strategy fills numeric NaNs with the column mean."""
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    cleaned = clean_dataframe(df, missing_strategy="mean")
    assert cleaned["a"].isna().sum() == 0
    assert cleaned["a"].iloc[1] == pytest.approx(2.0)


def test_clean_dataframe_missing_strategy_drop() -> None:
    """The ``drop`` strategy removes rows with missing values."""
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    cleaned = clean_dataframe(df, missing_strategy="drop")
    assert len(cleaned) == 2


def test_clean_dataframe_invalid_strategy_raises() -> None:
    """An unknown missing-value strategy raises ``ValueError``."""
    df = pd.DataFrame({"a": [1.0, np.nan]})
    with pytest.raises(ValueError):
        clean_dataframe(df, missing_strategy="invalid")  # type: ignore[arg-type]


def test_split_features_target(sample_dataframe: pd.DataFrame) -> None:
    """``split_features_target`` separates features and target."""
    X, y = split_features_target(sample_dataframe, target="revenue")
    assert "revenue" not in X.columns
    assert y.name == "revenue"
    assert len(X) == len(y)


def test_split_features_target_missing_target_raises(
    sample_dataframe: pd.DataFrame,
) -> None:
    """A missing target column raises ``KeyError``."""
    with pytest.raises(KeyError):
        split_features_target(sample_dataframe, target="not_a_column")


def test_train_test_split_df(
    classification_dataframe: pd.DataFrame,
) -> None:
    """``train_test_split_df`` returns four aligned objects."""
    X_train, X_test, y_train, y_test = train_test_split_df(
        classification_dataframe,
        target="target",
        test_size=0.25,
        random_state=42,
    )
    assert len(X_train) + len(X_test) == len(classification_dataframe)
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)


# ---------------------------------------------------------------------------
# core.modeling
# ---------------------------------------------------------------------------


def test_train_model_classification(
    classification_dataframe: pd.DataFrame,
) -> None:
    """A classification model can be trained and used for prediction."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    model = train_model(X, y, model_type="logistic_regression", task="classification")
    predictions = predict(model, X)
    assert len(predictions) == len(y)


def test_train_model_regression(regression_dataframe: pd.DataFrame) -> None:
    """A regression model can be trained and used for prediction."""
    X = regression_dataframe[["feature_a", "feature_b"]]
    y = regression_dataframe["target"]
    model = train_model(X, y, model_type="linear_regression", task="regression")
    predictions = predict(model, X)
    assert len(predictions) == len(y)


def test_train_model_incompatible_task_raises(
    classification_dataframe: pd.DataFrame,
) -> None:
    """An incompatible model/task combination raises ``ValueError``."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    with pytest.raises(ValueError):
        train_model(X, y, model_type="linear_regression", task="classification")


def test_train_model_length_mismatch_raises(
    classification_dataframe: pd.DataFrame,
) -> None:
    """Mismatched feature/target lengths raise ``ValueError``."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"].iloc[:-1]
    with pytest.raises(ValueError):
        train_model(X, y, model_type="logistic_regression", task="classification")


def test_evaluate_model_classification(
    classification_dataframe: pd.DataFrame,
) -> None:
    """Classification metrics include the expected keys."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    model = train_model(X, y, model_type="logistic_regression", task="classification")
    metrics = evaluate_model(model, X, y, task="classification")
    for key in ("accuracy", "precision", "recall", "f1"):
        assert key in metrics
        assert 0.0 <= metrics[key] <= 1.0


def test_evaluate_model_regression(regression_dataframe: pd.DataFrame) -> None:
    """Regression metrics include the expected keys."""
    X = regression_dataframe[["feature_a", "feature_b"]]
    y = regression_dataframe["target"]
    model = train_model(X, y, model_type="linear_regression", task="regression")
    metrics = evaluate_model(model, X, y, task="regression")
    for key in ("mae", "rmse", "r2"):
        assert key in metrics
    assert metrics["mae"] >= 0.0
    assert metrics["rmse"] >= 0.0


def test_evaluate_model_invalid_task_raises(
    classification_dataframe: pd.DataFrame,
) -> None:
    """An unknown task raises ``ValueError``."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    model = train_model(X, y, model_type="logistic_regression", task="classification")
    with pytest.raises(ValueError):
        evaluate_model(model, X, y, task="unknown")  # type: ignore[arg-type]


def test_predict_rejects_object_without_predict() -> None:
    """An object without a ``predict`` method raises ``TypeError``."""
    with pytest.raises(TypeError):
        predict(object(), np.zeros((2, 2)))  # type: ignore[arg-type]


def test_cross_validate_model(classification_dataframe: pd.DataFrame) -> None:
    """Cross-validation returns mean test scores."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    model = train_model(X, y, model_type="logistic_regression", task="classification")
    summary = cross_validate_model(model, X, y, cv=3)
    assert any(key.startswith("test_") for key in summary)


def test_save_and_load_model_roundtrip(
    classification_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """A model can be persisted and restored."""
    X = classification_dataframe[["feature_a", "feature_b"]]
    y = classification_dataframe["target"]
    model = train_model(X, y, model_type="logistic_regression", task="classification")

    dest = tmp_path / "models" / "model.pkl"
    written = save_model(model, dest)
    assert written == dest
    assert dest.is_file()

    restored = load_model(dest)
    original_predictions = predict(model, X)
    restored_predictions = predict(restored, X)
    np.testing.assert_array_equal(original_predictions, restored_predictions)


def test_load_model_missing_file_raises(tmp_path: Path) -> None:
    """A missing model file raises ``FileNotFoundError``."""
    with pytest.raises(FileNotFoundError):
        load_model(tmp_path / "missing.pkl")


# ---------------------------------------------------------------------------
# services.etl
# ---------------------------------------------------------------------------


def test_extract_csv(tmp_csv_file: Path) -> None:
    """``extract`` reads a CSV source."""
    df = extract(tmp_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def test_extract_parquet(tmp_parquet_file: Path) -> None:
    """``extract`` reads a Parquet source."""
    df = extract(tmp_parquet_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def test_extract_unknown_suffix_raises(tmp_path: Path) -> None:
    """An unknown file suffix raises ``ValueError``."""
    with pytest.raises(ValueError):
        extract(tmp_path / "data.unknown")


def test_extract_sql_requires_database_url() -> None:
    """SQL extraction without a database URL raises ``ValueError``."""
    with pytest.raises(ValueError):
        extract("ignored", source_type="sql", query="SELECT 1")


def test_transform_applies_cleaning(sample_dataframe: pd.DataFrame) -> None:
    """``transform`` normalizes columns and drops duplicates."""
    df = sample_dataframe.copy()
    df.columns = [col.upper() for col in df.columns]
    df = pd.concat([df, df], ignore_index=True)

    transformed = transform(df)
    assert all(col == col.lower() for col in transformed.columns)
    assert len(transformed) == len(sample_dataframe)


def test_transform_custom_step(sample_dataframe: pd.DataFrame) -> None:
    """Custom transformation steps are applied in order."""
    def add_column(frame: pd.DataFrame) -> pd.DataFrame:
        frame = frame.copy()
        frame["revenue_x2"] = frame["revenue"] * 2
        return frame

    transformed = transform(sample_dataframe, steps=[("double_revenue", add_column)])
    assert "revenue_x2" in transformed.columns


def test_transform_rejects_non_dataframe_step(
    sample_dataframe: pd.DataFrame,
) -> None:
    """A step returning a non-DataFrame raises ``TypeError``."""
    def bad_step(frame: pd.DataFrame) -> pd.DataFrame:
        return [1, 2, 3]  # type: ignore[return-value]

    with pytest.raises(TypeError):
        transform(sample_dataframe, steps=[("bad", bad_step)])


def test_load_csv_destination(
    sample_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """``load`` writes a DataFrame to a CSV destination."""
    dest = tmp_path / "out" / "data.csv"
    result = load(sample_dataframe, dest)
    assert Path(result) == dest
    assert dest.is_file()


def test_load_sql_destination(
    sample_dataframe: pd.DataFrame, sqlite_database_url: str
) -> None:
    """``load`` writes a DataFrame to a SQL destination."""
    table = load(
        sample_dataframe,
        "ignored",
        destination_type="sql",
        table="customers",
        database_url=sqlite_database_url,
    )
    assert table == "customers"


def test_load_sql_requires_table(
    sample_dataframe: pd.DataFrame, sqlite_database_url: str
) -> None:
    """SQL loading without a table name raises ``ValueError``."""
    with pytest.raises(ValueError):
        load(
            sample_dataframe,
            "ignored",
            destination_type="sql",
            database_url=sqlite_database_url,
        )


def test_run_etl_pipeline_csv_to_parquet(
    tmp_csv_file: Path, tmp_path: Path
) -> None:
    """A full ETL pipeline runs from CSV to Parquet."""
    dest = tmp_path / "processed" / "data.parquet"
    result = run_etl_pipeline(tmp_csv_file, dest)
    assert isinstance(result, ETLResult)
    assert result.rows_extracted == 5
    assert result.rows_loaded == 5
    assert dest.is_file()


def test_etl_result_as_dict() -> None:
    """``ETLResult.as_dict`` returns a plain dictionary."""
    result = ETLResult(
        source="a",
        destination="b",
        rows_extracted=10,
        rows_loaded=8,
        columns=["x", "y"],
        steps_applied=["clean"],
    )
    payload = result.as_dict()
    assert payload["rows_extracted"] == 10
    assert payload["columns"] == ["x", "y"]


# ---------------------------------------------------------------------------
# visualization.plots
# ---------------------------------------------------------------------------


def test_plot_distribution_hist(sample_dataframe: pd.DataFrame) -> None:
    """``plot_distribution`` returns a Matplotlib figure."""
    fig = plot_distribution(sample_dataframe, column="revenue", kind="hist")
    try:
        assert isinstance(fig, plt.Figure)
    finally:
        plt.close(fig)


def test_plot_distribution_invalid_kind_raises(
    sample_dataframe: pd.DataFrame,
) -> None:
    """An unknown distribution kind raises ``ValueError``."""
    with pytest.raises(ValueError):
        plot_distribution(sample_dataframe, column="revenue", kind="invalid")  # type: ignore[arg-type]


def test_plot_distribution_missing_column_raises(
    sample_dataframe: pd.DataFrame,
) -> None:
    """A missing column raises ``KeyError``."""
    with pytest.raises(KeyError):
        plot_distribution(sample_dataframe, column="not_a_column")


def test_plot_correlation_matrix(numeric_dataframe: pd.DataFrame) -> None:
    """``plot_correlation_matrix`` returns a Matplotlib figure."""
    fig = plot_correlation_matrix(numeric_dataframe)
    try:
        assert isinstance(fig, plt.Figure)
    finally:
        plt.close(fig)


def test_plot_correlation_matrix_requires_numeric() -> None:
    """Fewer than two numeric columns raises ``ValueError``."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    with pytest.raises(ValueError):
        plot_correlation_matrix(df)


def test_plot_time_series_matplotlib(sample_dataframe: pd.DataFrame) -> None:
    """``plot_time_series`` returns a Matplotlib figure by default."""
    fig = plot_time_series(sample_dataframe, x="signup_date", y="revenue")
    try:
        assert isinstance(fig, plt.Figure)
    finally:
        plt.close(fig)


def test_plot_time_series_plotly(sample_dataframe: pd.DataFrame) -> None:
    """``plot_time_series`` returns a Plotly figure when interactive."""
    fig = plot_time_series(
        sample_dataframe, x="signup_date", y="revenue", interactive=True
    )
    assert hasattr(fig, "to_dict")


def test_plot_bar(sample_dataframe: pd.DataFrame) -> None:
    """``plot_bar`` returns a Matplotlib figure."""
    fig = plot_bar(sample_dataframe, x="region", y="revenue", agg="sum")
    try:
        assert isinstance(fig, plt.Figure)
    finally:
        plt.close(fig)


def test_plot_bar_invalid_agg_raises(sample_dataframe: pd.DataFrame) -> None:
    """An unknown aggregation raises ``ValueError``."""
    with pytest.raises(ValueError):
        plot_bar(sample_dataframe, x="region", y="revenue", agg="invalid")  # type: ignore[arg-type]


def test_save_figure_matplotlib(
    sample_dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    """A Matplotlib figure can be persisted to disk."""
    fig = plot_distribution(sample_dataframe, column="revenue")
    try:
        dest = tmp_path / "figures" / "dist.png"
        written = save_figure(fig, dest)
        assert written == dest
        assert dest.is_file()
    finally:
        plt.close(fig)


def test_save_figure_rejects_unknown_type(tmp_path: Path) -> None:
    """An unsupported figure type raises ``TypeError``."""
    with pytest.raises(TypeError):
        save_figure(object(), tmp_path / "fig.png")  # type: ignore[arg-type]