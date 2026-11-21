"""Core subpackage for DataForge.

This subpackage contains the fundamental building blocks of the framework:

- :mod:`DataForge.core.data_handling` — data loading,
  cleaning, and preprocessing utilities.
- :mod:`DataForge.core.modeling` — machine learning
  model training and evaluation utilities.

The public API is re-exported here for convenience, so that consumers can
import directly from the subpackage::

    from DataForge.core import load_csv, train_model
"""

from __future__ import annotations

from DataForge.core.data_handling import (
    clean_dataframe,
    load_csv,
)
from DataForge.core.modeling import (
    evaluate_model,
    train_model,
)

__all__: list[str] = [
    "clean_dataframe",
    "evaluate_model",
    "load_csv",
    "train_model",
]