import pandas as pd
import pytest
from hotel_booking.processing import CSVBookingLoader, DataQualityChecker, DataQualityError, BookingPipeline


def sample():
    return pd.DataFrame({
        "hotel": ["City Hotel", "Resort Hotel", "City Hotel"],
        "is_canceled": [1, 0, 1],
        "lead_time": [100, 20, 100],
        "arrival_date_year": [2016, 2016, 2016],
        "arrival_date_month": ["July", "August", "July"],
        "adults": [2, 2, 2],
        "adr": [100.0, 80.0, 100.0],
        "market_segment": ["Online TA", "Direct", "Online TA"],
        "deposit_type": ["No Deposit", "No Deposit", "No Deposit"],
        "reservation_status": ["Canceled", "Check-Out", "Canceled"]
    })


def test_quality_checker_counts_duplicates():
    report = DataQualityChecker().check(sample())
    assert report["rows"] == 3
    assert report["duplicate_rows"] == 1


def test_quality_checker_rejects_non_dataframe():
    with pytest.raises(ValueError):
        DataQualityChecker().check(["not", "a", "dataframe"])


def test_quality_checker_rejects_empty_dataframe():
    with pytest.raises(DataQualityError):
        DataQualityChecker().check(pd.DataFrame())


def test_quality_checker_rejects_missing_columns():
    with pytest.raises(DataQualityError):
        DataQualityChecker().check(pd.DataFrame({"hotel": ["City Hotel"]}))


def test_pipeline_removes_exact_duplicates():
    cleaned = BookingPipeline().prepare(sample())
    assert len(cleaned) == 2


def test_csv_loader_rejects_wrong_extension(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("a,b\\n1,2")
    with pytest.raises(ValueError):
        CSVBookingLoader().load(path)


def test_quality_checker_rejects_non_numeric_adr():
    frame = sample().copy()
    frame["adr"] = frame["adr"].astype(object)
    frame.loc[0, "adr"] = "invalid"

    with pytest.raises(ValueError):
        DataQualityChecker().check(frame)


def test_quality_checker_rejects_invalid_cancellation_value():
    frame = sample().copy()
    frame.loc[0, "is_canceled"] = 2

    with pytest.raises(ValueError):
        DataQualityChecker().check(frame)


def test_quality_checker_rejects_non_numeric_adr():
    frame = sample().copy()
    frame["adr"] = frame["adr"].astype(object)
    frame.loc[0, "adr"] = "invalid"

    with pytest.raises(ValueError):
        DataQualityChecker().check(frame)


def test_quality_checker_rejects_invalid_cancellation_value():
    frame = sample().copy()
    frame.loc[0, "is_canceled"] = 2

    with pytest.raises(ValueError):
        DataQualityChecker().check(frame)
