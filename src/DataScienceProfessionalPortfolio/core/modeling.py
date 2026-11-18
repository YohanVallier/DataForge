"""Machine learning modeling utilities.

This module provides reusable helpers for training and evaluating machine
learning models with :mod:`scikit-learn`. It is intentionally generic so that
it can be shared across portfolio projects, while still offering sensible
defaults for common tasks (classification and regression).

Public API
----------
- :func:`train_model` — build and fit a model from a named preset.
- :func:`evaluate_model` — compute task-appropriate evaluation metrics.
- :func:`predict` — generate predictions from a fitted model.
- :func:`cross_validate_model` — run k-fold cross-validation.
- :func:`save_model` / :func:`load_model` — persist and restore models.
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "cross_validate_model",
    "evaluate_model",
    "load_model",
    "predict",
    "save_model",
    "train_model",
]

TaskType = Literal["classification", "regression"]
ModelType = Literal[
    "logistic_regression",
    "linear_regression",
    "decision_tree",
    "random_forest",
    "gradient_boosting",
]

_CLASSIFICATION_MODELS: dict[str, type[BaseEstimator]] = {
    "logistic_regression": LogisticRegression,
    "decision_tree": DecisionTreeClassifier,
    "random_forest": RandomForestClassifier,
    "gradient_boosting": GradientBoostingClassifier,
}

_REGRESSION_MODELS: dict[str, type[BaseEstimator]] = {
    "linear_regression": LinearRegression,
    "decision_tree": DecisionTreeRegressor,
    "random_forest": RandomForestRegressor,
    "gradient_boosting": GradientBoostingRegressor,
}


class ModelConfigurationError(ValueError):
    """Raised when a model/task combination is invalid or unsupported."""

    pass


def _resolve_model_class(model_type: ModelType, task: TaskType) -> type[BaseEstimator]:
    """Resolve a model class from a preset name and task type.

    Parameters
    ----------
    model_type:
        Name of the model preset.
    task:
        Either ``"classification"`` or ``"regression"``.

    Returns
    -------
    type[BaseEstimator]
        The scikit-learn estimator class.

    Raises
    ------
    ModelConfigurationError
        If the model preset is unknown or incompatible with the task.
    ValueError
        If the task is not recognized.
    """
    if task not in {"classification", "regression"}:
        raise ValueError(
            f"Unknown task: {task!r}. Expected 'classification' or 'regression'."
        )

    registry = (
        _CLASSIFICATION_MODELS if task == "classification" else _REGRESSION_MODELS
    )
    if model_type not in registry:
        raise ModelConfigurationError(
            f"Model '{model_type}' is not available for task '{task}'. "
            f"Available models: {sorted(registry)}"
        )
    return registry[model_type]


def train_model(
    X_train: pd.DataFrame | np.ndarray,
    y_train: pd.Series | np.ndarray,
    *,
    model_type: ModelType = "random_forest",
    task: TaskType = "classification",
    random_state: int | None = 42,
    **model_kwargs: Any,
) -> BaseEstimator:
    """Build and fit a model from a named preset.

    Parameters
    ----------
    X_train:
        Training features.
    y_train:
        Training target.
    model_type:
        Name of the model preset. See :data:`ModelType`.
    task:
        Either ``"classification"`` or ``"regression"``.
    random_state:
        Seed for reproducibility. Ignored by estimators that do not accept it.
    **model_kwargs:
        Additional keyword arguments forwarded to the estimator constructor.

    Returns
    -------
    sklearn.base.BaseEstimator
        The fitted estimator.

    Raises
    ------
    ModelConfigurationError
        If the model preset is unknown or incompatible with the task.
    ValueError
        If the task is not recognized or if X_train and y_train have
        mismatched lengths.
    TypeError
        If X_train or y_train have invalid types.
    """
    if not isinstance(X_train, (pd.DataFrame, np.ndarray)):
        raise TypeError(
            f"X_train must be a pandas.DataFrame or numpy.ndarray, "
            f"got {type(X_train).__name__}"
        )
    if not isinstance(y_train, (pd.Series, np.ndarray)):
        raise TypeError(
            f"y_train must be a pandas.Series or numpy.ndarray, "
            f"got {type(y_train).__name__}"
        )

    if len(X_train) != len(y_train):
        raise ValueError(
            "X_train and y_train must have the same number of samples "
            f"(got {len(X_train)} and {len(y_train)})"
        )

    try:
        model_class = _resolve_model_class(model_type, task)
    except (ModelConfigurationError, ValueError) as exc:
        logger.error(
            "Failed to resolve model '%s' for task '%s': %s",
            model_type,
            task,
            exc,
        )
        raise

    init_kwargs: dict[str, Any] = dict(model_kwargs)
    if "random_state" in model_class().get_params():
        init_kwargs.setdefault("random_state", random_state)

    logger.info("Training %s model (%s)", task, model_type)
    try:
        model = model_class(**init_kwargs)
        model.fit(X_train, y_train)
    except Exception as exc:
        logger.error(
            "Failed to train %s model (%s): %s", task, model_type, exc
        )
        raise

    logger.info("Model training complete")
    return model


def predict(
    model: BaseEstimator,
    X: pd.DataFrame | np.ndarray,
) -> np.ndarray:
    """Generate predictions from a fitted model.

    Parameters
    ----------
    model:
        A fitted scikit-learn estimator.
    X:
        Features to predict on.

    Returns
    -------
    numpy.ndarray
        Model predictions.

    Raises
    ------
    TypeError
        If ``model`` does not expose a ``predict`` method.
    """
    if not hasattr(model, "predict"):
        raise TypeError("model must implement a 'predict' method")
    return np.asarray(model.predict(X))


def evaluate_model(
    model: BaseEstimator,
    X_test: pd.DataFrame | np.ndarray,
    y_test: pd.Series | np.ndarray,
    *,
    task: TaskType = "classification",
) -> dict[str, float]:
    """Compute task-appropriate evaluation metrics.

    For classification, the returned metrics are ``accuracy``, ``precision``,
    ``recall``, ``f1``, and — when the model exposes ``predict_proba`` and the
    target is binary — ``roc_auc``.

    For regression, the returned metrics are ``mae``, ``rmse``, and ``r2``.

    Parameters
    ----------
    model:
        A fitted scikit-learn estimator.
    X_test:
        Test features.
    y_test:
        Test target.
    task:
        Either ``"classification"`` or ``"regression"``.

    Returns
    -------
    dict[str, float]
        Mapping of metric name to value.

    Raises
    ------
    ValueError
        If ``task`` is not recognized.
    """
    if task not in {"classification", "regression"}:
        raise ValueError(
            f"Unknown task: {task!r}. Expected 'classification' or 'regression'."
        )

    y_pred = predict(model, X_test)
    y_true = np.asarray(y_test)

    if task == "classification":
        metrics: dict[str, float] = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(
                precision_score(y_true, y_pred, average="weighted", zero_division=0)
            ),
            "recall": float(
                recall_score(y_true, y_pred, average="weighted", zero_division=0)
            ),
            "f1": float(
                f1_score(y_true, y_pred, average="weighted", zero_division=0)
            ),
        }
        if hasattr(model, "predict_proba") and len(np.unique(y_true)) == 2:
            try:
                proba = model.predict_proba(X_test)[:, 1]
                metrics["roc_auc"] = float(roc_auc_score(y_true, proba))
            except (ValueError, IndexError) as exc:
                logger.warning("Could not compute ROC AUC: %s", exc)
        logger.info("Classification metrics: %s", metrics)
        return metrics

    mse = float(mean_squared_error(y_true, y_pred))
    metrics = {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mse)),
        "r2": float(r2_score(y_true, y_pred)),
    }
    logger.info("Regression metrics: %s", metrics)
    return metrics


def cross_validate_model(
    model: BaseEstimator,
    X: pd.DataFrame | np.ndarray,
    y: pd.Series | np.ndarray,
    *,
    cv: int = 5,
    scoring: str | None = None,
) -> dict[str, float]:
    """Run k-fold cross-validation and return mean scores.

    Parameters
    ----------
    model:
        An unfitted scikit-learn estimator.
    X:
        Features.
    y:
        Target.
    cv:
        Number of folds.
    scoring:
        Optional scoring metric. If ``None``, the estimator's default scorer
        is used.

    Returns
    -------
    dict[str, float]
        Mapping of metric name to mean score across folds.
    """
    logger.info("Running %d-fold cross-validation", cv)
    results = cross_validate(model, X, y, cv=cv, scoring=scoring)
    summary = {
        key: float(np.mean(value))
        for key, value in results.items()
        if key.startswith("test_")
    }
    logger.info("Cross-validation summary: %s", summary)
    return summary


def save_model(model: BaseEstimator, path: str | Path) -> Path:
    """Persist a fitted model to disk using pickle.

    Parameters
    ----------
    model:
        The fitted estimator.
    path:
        Destination path. Parent directories are created if missing.

    Returns
    -------
    pathlib.Path
        The path where the model was written.

    Raises
    ------
    OSError
        If the file cannot be written.
    """
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Saving model to %s", dest)
    try:
        with dest.open("wb") as fh:
            pickle.dump(model, fh)
    except OSError as exc:
        raise OSError(f"Failed to save model to '{dest}': {exc}") from exc
    return dest


def load_model(path: str | Path) -> BaseEstimator:
    """Load a pickled model from disk.

    Parameters
    ----------
    path:
        Path to the pickled model.

    Returns
    -------
    sklearn.base.BaseEstimator
        The loaded estimator.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be unpickled.
    """
    model_path = Path(path)
    if not model_path.is_file():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    logger.info("Loading model from %s", model_path)
    try:
        with model_path.open("rb") as fh:
            model = pickle.load(fh)
    except (OSError, pickle.UnpicklingError) as exc:
        raise ValueError(
            f"Failed to load model from '{model_path}': {exc}"
        ) from exc
    return model