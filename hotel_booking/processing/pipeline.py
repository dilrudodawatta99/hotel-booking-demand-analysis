"""Orchestration of loading, quality checking and cleaning."""
import pandas as pd
from .quality import DataQualityChecker


class BookingPipeline:
    """Run a repeatable preparation pipeline.

    Contract: prepare(frame) validates a DataFrame and returns a cleaned copy.
    Exact duplicate rows are removed; missing values are not silently imputed.
    """
    def __init__(self, checker=None):
        self._checker = checker or DataQualityChecker()
        self._quality_report = None

    @property
    def quality_report(self):
        """Return the raw-data quality report from the latest run."""
        return self._quality_report

    def prepare(self, frame):
        """Check input, remove exact duplicates, and parse the reservation date."""
        self._quality_report = self._checker.check(frame)
        cleaned = frame.drop_duplicates().copy()
        if "reservation_status_date" in cleaned.columns:
            cleaned["reservation_status_date"] = pd.to_datetime(
                cleaned["reservation_status_date"], errors="coerce"
            )
        return cleaned
