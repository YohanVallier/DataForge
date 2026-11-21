"""Services subpackage for DataForge.

This subpackage contains higher-level orchestration components that combine
the building blocks from :mod:`DataForge.core` into
end-to-end workflows:

- :mod:`DataForge.services.etl` — ETL pipeline
  definitions for data ingestion, transformation, and loading.

The public API is re-exported here for convenience, so that consumers can
import directly from the subpackage::

    from DataForge.services import run_etl_pipeline
"""

from __future__ import annotations

from DataForge.services.etl import run_etl_pipeline

__all__: list[str] = [
    "run_etl_pipeline",
]