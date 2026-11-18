"""Visualization subpackage for DataScienceProfessionalPortfolio.

This subpackage contains plotting utilities built on Matplotlib, Seaborn, and
Plotly:

- :mod:`DataScienceProfessionalPortfolio.visualization.plots` — reusable
  plotting functions for distributions, correlations, and time series.

The public API is re-exported here for convenience, so that consumers can
import directly from the subpackage::

    from DataScienceProfessionalPortfolio.visualization import plot_distribution
"""

from __future__ import annotations

from DataScienceProfessionalPortfolio.visualization.plots import (
    plot_correlation_matrix,
    plot_distribution,
    plot_time_series,
)

__all__: list[str] = [
    "plot_correlation_matrix",
    "plot_distribution",
    "plot_time_series",
]