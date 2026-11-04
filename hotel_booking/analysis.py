"""Reproducible descriptive analysis functions."""
import pandas as pd


def cancellation_summary(frame):
    """Return overall and hotel-level cancellation rates."""
    if "is_canceled" not in frame.columns or "hotel" not in frame.columns:
        raise ValueError("Input must contain hotel and is_canceled columns.")
    return {
        "overall_rate": float(frame["is_canceled"].mean()),
        "by_hotel": frame.groupby("hotel")["is_canceled"].mean().sort_values(ascending=False)
    }


def cancellation_by_category(frame, column):
    """Return booking counts and cancellation rates for a categorical column."""
    if column not in frame.columns:
        raise ValueError(f"Unknown column: {column}")
    return frame.groupby(column, dropna=False)["is_canceled"].agg(
        bookings="count", cancellation_rate="mean"
    ).sort_values("cancellation_rate", ascending=False)
