"""Dataset validation and quality reporting."""
import pandas as pd


class DataQualityError(Exception):
    """Raised when a dataset cannot satisfy the pipeline's minimum contract."""


class DataQualityChecker:
    """Validate and profile a hotel-booking DataFrame.

    Contract: check(frame) requires a pandas DataFrame with required columns.
    """

    REQUIRED_COLUMNS = {
        "hotel", "is_canceled", "lead_time", "arrival_date_year",
        "arrival_date_month", "adults", "adr", "market_segment",
        "deposit_type", "reservation_status"
    }

    def __init__(self):
        self._last_report = None

    @property
    def last_report(self):
        """Return the most recent quality report, or None before checking."""
        return self._last_report

    def check(self, frame):
        """Validate the dataset and return its quality statistics."""

        if not isinstance(frame, pd.DataFrame):
            raise ValueError("frame must be a pandas DataFrame.")

        if frame.empty:
            raise DataQualityError("The input dataset contains no records.")

        missing_columns = self.REQUIRED_COLUMNS.difference(frame.columns)

        if missing_columns:
            raise DataQualityError(
                "Required columns are missing: " +
                ", ".join(sorted(missing_columns))
            )

        # Validate numeric columns while allowing missing values.
        for column in ["adr", "adults", "is_canceled"]:
            numeric_values = pd.to_numeric(frame[column], errors="coerce")
            invalid_values = frame[column].notna() & numeric_values.isna()

            if invalid_values.any():
                raise ValueError(
                    f"Column '{column}' contains non-numeric values."
                )

        # Cancellation must contain only 0 or 1.
        cancellation_values = pd.to_numeric(
            frame["is_canceled"], errors="coerce"
        ).dropna()

        if not cancellation_values.isin([0, 1]).all():
            raise ValueError(
                "Column 'is_canceled' must contain only 0 and 1."
            )

        adr_values = pd.to_numeric(frame["adr"], errors="coerce")
        adult_values = pd.to_numeric(frame["adults"], errors="coerce")

        report = {
            "rows": int(len(frame)),
            "columns": int(len(frame.columns)),
            "duplicate_rows": int(frame.duplicated().sum()),
            "missing_by_column": frame.isna().sum().astype(int).to_dict(),
            "negative_adr_rows": int((adr_values < 0).sum()),
            "zero_adr_rows": int((adr_values == 0).sum()),
            "zero_adult_rows": int((adult_values == 0).sum()),
        }

        self._last_report = report
        return report
