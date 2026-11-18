"""Services subpackage for DataScienceProfessionalPortfolio.

This subpackage contains higher-level orchestration components that combine
the building blocks from :mod:`DataScienceProfessionalPortfolio.core` into
end-to-end workflows:

- :mod:`DataScienceProfessionalPortfolio.services.etl` — ETL pipeline
  definitions for data ingestion, transformation, and loading.

The public API is re-exported here for convenience, so that consumers can
import directly from the subpackage::

    from DataScienceProfessionalPortfolio.services import run_etl_pipeline
"""

from __future__ import annotations

from DataScienceProfessionalPortfolio.services.etl import run_etl_pipeline

__all__: list[str] = [
    "run_etl_pipeline",
]