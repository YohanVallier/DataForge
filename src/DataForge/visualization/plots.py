"""Data visualization utilities.

This module provides reusable plotting helpers built on Matplotlib, Seaborn,
and Plotly. It is intentionally generic so that it can be shared across
portfolio projects, while still offering sensible defaults for common tasks
(distributions, correlations, and time series).

Public API
----------
- :func:`plot_distribution` — histogram, KDE, or box plot of a single column.
- :func:`plot_correlation_matrix` — heatmap of pairwise correlations.
- :func:`plot_time_series` — line plot of one or more series over time.
- :func:`plot_bar` — bar chart of aggregated values by category.
- :func:`save_figure` — persist a Matplotlib or Plotly figure to disk.

All Matplotlib-based functions return a :class:`matplotlib.figure.Figure` so
that callers can further customize or persist the result. Plotly-based
functions return a :class:`plotly.graph_objects.Figure`.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal, Sequence

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib.figure import Figure
from plotly.graph_objects import Figure as PlotlyFigure

logger = logging.getLogger(__name__)

__all__: list[str] = [
    "plot_bar",
    "plot_correlation_matrix",
    "plot_distribution",
    "plot_time_series",
    "save_figure",
]

DistributionKind = Literal["hist", "kde", "box"]
FigureType = Figure | PlotlyFigure

_VALID_DISTRIBUTION_KINDS: frozenset[str] = frozenset({"hist", "kde", "box"})


def _validate_dataframe(df: pd.DataFrame) -> None:
    """Validate that the input is a :class:`pandas.DataFrame`.

    Parameters
    ----------
    df:
        Object to validate.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")


def _validate_column(df: pd.DataFrame, column: str) -> None:
    """Validate that a column exists in a DataFrame.

    Parameters
    ----------
    df:
        DataFrame to inspect.
    column:
        Column name to validate.

    Raises
    ------
    KeyError
        If the column is not present in ``df``.
    """
    if column not in df.columns:
        raise KeyError(
            f"Column '{column}' not found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )


def _validate_distribution_kind(kind: str) -> None:
    """Validate that a distribution kind is supported.

    Parameters
    ----------
    kind:
        Distribution kind to validate.

    Raises
    ------
    ValueError
        If the kind is not recognized.
    """
    if kind not in _VALID_DISTRIBUTION_KINDS:
        raise ValueError(
            f"Unknown distribution kind: {kind!r}. "
            f"Expected one of {sorted(_VALID_DISTRIBUTION_KINDS)}."
        )


def plot_distribution(
    df: pd.DataFrame,
    column: str,
    *,
    kind: DistributionKind = "hist",
    bins: int = 30,
    hue: str | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = (10.0, 6.0),
    **kwargs: Any,
) -> Figure:
    """Plot the distribution of a single column.

    Parameters
    ----------
    df:
        Input DataFrame.
    column:
        Name of the column to plot.
    kind:
        Plot kind: ``"hist"``, ``"kde"``, or ``"box"``.
    bins:
        Number of histogram bins. Only used when ``kind="hist"``.
    hue:
        Optional column used to group the data by color.
    title:
        Optional plot title. Defaults to a descriptive title.
    figsize:
        Figure size in inches.
    **kwargs:
        Additional keyword arguments forwarded to the Seaborn plotting
        function.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    KeyError
        If ``column`` or ``hue`` is not present in ``df``.
    ValueError
        If ``kind`` is not recognized.
    """
    _validate_dataframe(df)
    _validate_column(df, column)
    _validate_distribution_kind(kind)
    if hue is not None:
        _validate_column(df, hue)

    fig, ax = plt.subplots(figsize=figsize)

    try:
        if kind == "hist":
            sns.histplot(
                data=df,
                x=column,
                hue=hue,
                bins=bins,
                kde=False,
                ax=ax,
                **kwargs,
            )
        elif kind == "kde":
            sns.kdeplot(
                data=df,
                x=column,
                hue=hue,
                fill=True,
                ax=ax,
                **kwargs,
            )
        elif kind == "box":
            sns.boxplot(
                data=df,
                x=hue,
                y=column,
                ax=ax,
                **kwargs,
            )
    except Exception as exc:
        plt.close(fig)
        raise ValueError(
            f"Failed to create {kind} distribution plot for column '{column}': {exc}"
        ) from exc

    ax.set_title(title or f"Distribution of '{column}'")
    ax.set_xlabel(column)
    fig.tight_layout()
    logger.info("Created %s distribution plot for column '%s'", kind, column)
    return fig


def plot_correlation_matrix(
    df: pd.DataFrame,
    *,
    method: Literal["pearson", "spearman", "kendall"] = "pearson",
    columns: Sequence[str] | None = None,
    annot: bool = True,
    cmap: str = "coolwarm",
    title: str | None = None,
    figsize: tuple[float, float] = (10.0, 8.0),
    **kwargs: Any,
) -> Figure:
    """Plot a heatmap of pairwise correlations between numeric columns.

    Parameters
    ----------
    df:
        Input DataFrame.
    method:
        Correlation method: ``"pearson"``, ``"spearman"``, or ``"kendall"``.
    columns:
        Optional subset of columns to include. Non-numeric columns are
        silently excluded.
    annot:
        Whether to annotate each cell with its correlation value.
    cmap:
        Matplotlib colormap name.
    title:
        Optional plot title.
    figsize:
        Figure size in inches.
    **kwargs:
        Additional keyword arguments forwarded to :func:`seaborn.heatmap`.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    ValueError
        If fewer than two numeric columns are available.
    """
    _validate_dataframe(df)

    subset = df[list(columns)] if columns else df
    numeric = subset.select_dtypes(include="number")

    if numeric.shape[1] < 2:
        raise ValueError(
            "At least two numeric columns are required to compute correlations"
        )

    corr = numeric.corr(method=method)
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        annot=annot,
        cmap=cmap,
        fmt=".2f",
        square=True,
        ax=ax,
        **kwargs,
    )
    ax.set_title(title or f"Correlation matrix ({method})")
    fig.tight_layout()
    logger.info("Created correlation matrix with shape %s", corr.shape)
    return fig


def plot_time_series(
    df: pd.DataFrame,
    x: str,
    y: str | Sequence[str],
    *,
    title: str | None = None,
    figsize: tuple[float, float] = (12.0, 6.0),
    interactive: bool = False,
    **kwargs: Any,
) -> FigureType:
    """Plot one or more series over a time axis.

    Parameters
    ----------
    df:
        Input DataFrame.
    x:
        Name of the column to use as the x-axis (typically a date column).
    y:
        Name of a single column or a sequence of columns to plot.
    title:
        Optional plot title.
    figsize:
        Figure size in inches. Ignored when ``interactive=True``.
    interactive:
        If ``True``, return a Plotly figure; otherwise return a Matplotlib
        figure.
    **kwargs:
        Additional keyword arguments forwarded to the plotting function.

    Returns
    -------
    matplotlib.figure.Figure | plotly.graph_objects.Figure
        The generated figure.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    KeyError
        If ``x`` or any of the ``y`` columns are not present in ``df``.
    """
    _validate_dataframe(df)
    _validate_column(df, x)

    y_columns = [y] if isinstance(y, str) else list(y)
    for column in y_columns:
        _validate_column(df, column)

    resolved_title = title or f"Time series of {', '.join(y_columns)}"

    if interactive:
        fig = px.line(
            df,
            x=x,
            y=y_columns,
            title=resolved_title,
            **kwargs,
        )
        logger.info("Created interactive time series plot for %s", y_columns)
        return fig

    fig, ax = plt.subplots(figsize=figsize)
    for column in y_columns:
        ax.plot(df[x], df[column], label=column, **kwargs)
    ax.set_title(resolved_title)
    ax.set_xlabel(x)
    ax.set_ylabel("value")
    if len(y_columns) > 1:
        ax.legend()
    fig.tight_layout()
    logger.info("Created time series plot for %s", y_columns)
    return fig


def plot_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    agg: Literal["sum", "mean", "count", "median"] = "sum",
    top_n: int | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = (10.0, 6.0),
    **kwargs: Any,
) -> Figure:
    """Plot a bar chart of aggregated values by category.

    Parameters
    ----------
    df:
        Input DataFrame.
    x:
        Categorical column used for the x-axis.
    y:
        Numeric column to aggregate.
    agg:
        Aggregation function: ``"sum"``, ``"mean"``, ``"count"``, or
        ``"median"``.
    top_n:
        Optional limit on the number of categories shown, sorted by the
        aggregated value in descending order.
    title:
        Optional plot title.
    figsize:
        Figure size in inches.
    **kwargs:
        Additional keyword arguments forwarded to :meth:`pandas.Series.plot`.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    KeyError
        If ``x`` or ``y`` is not present in ``df``.
    ValueError
        If ``agg`` is not recognized.
    """
    _validate_dataframe(df)
    _validate_column(df, x)
    _validate_column(df, y)

    if agg not in {"sum", "mean", "count", "median"}:
        raise ValueError(
            f"Unknown aggregation: {agg!r}. "
            "Expected one of 'sum', 'mean', 'count', 'median'."
        )

    grouped = df.groupby(x, observed=True)[y].agg(agg)
    grouped = grouped.sort_values(ascending=False)
    if top_n is not None:
        grouped = grouped.head(top_n)

    fig, ax = plt.subplots(figsize=figsize)
    grouped.plot(kind="bar", ax=ax, **kwargs)
    ax.set_title(title or f"{agg.capitalize()} of '{y}' by '{x}'")
    ax.set_xlabel(x)
    ax.set_ylabel(f"{agg}({y})")
    fig.tight_layout()
    logger.info("Created bar chart of '%s' by '%s' (%s)", y, x, agg)
    return fig


def save_figure(
    fig: FigureType,
    path: str | Path,
    *,
    dpi: int = 150,
    **kwargs: Any,
) -> Path:
    """Persist a Matplotlib or Plotly figure to disk.

    Parameters
    ----------
    fig:
        The figure to persist.
    path:
        Destination path. Parent directories are created if missing.
    dpi:
        Resolution for Matplotlib figures. Ignored for Plotly figures.
    **kwargs:
        Additional keyword arguments forwarded to the underlying save method.

    Returns
    -------
    pathlib.Path
        The path where the figure was written.

    Raises
    ------
    TypeError
        If ``fig`` is neither a Matplotlib nor a Plotly figure.
    OSError
        If the file cannot be written.
    """
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Saving figure to %s", dest)
    try:
        if isinstance(fig, Figure):
            fig.savefig(dest, dpi=dpi, bbox_inches="tight", **kwargs)
        elif isinstance(fig, PlotlyFigure):
            fig.write_image(str(dest), **kwargs)
        else:
            raise TypeError(
                "fig must be a matplotlib Figure or a plotly Figure, "
                f"got {type(fig).__name__}"
            )
    except OSError as exc:
        raise OSError(f"Failed to save figure to '{dest}': {exc}") from exc

    return dest