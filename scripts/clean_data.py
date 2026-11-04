from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = ROOT / "data" / "raw" / "hotel_bookings.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "hotel_bookings_cleaned.csv"


def clean_hotel_bookings():
    """Clean hotel booking records and save a separate analytical dataset."""

    data = pd.read_csv(RAW_PATH)
    original_rows = len(data)

    print("Original rows:", original_rows)

    duplicate_count = int(data.duplicated().sum())
    data = data.drop_duplicates().copy()

    data["company"] = data["company"].fillna(0)
    data["agent"] = data["agent"].fillna(0)
    data["country"] = data["country"].fillna("Unknown")
    data["children"] = data["children"].fillna(0)

    negative_adr_count = int((data["adr"] < 0).sum())
    data = data[data["adr"] >= 0].copy()

    guest_columns = ["adults", "children", "babies"]
    no_guest_count = int((data[guest_columns].sum(axis=1) == 0).sum())

    data = data[data[guest_columns].sum(axis=1) > 0].copy()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)

    print("\nCLEANING SUMMARY")
    print("Duplicates removed:", duplicate_count)
    print("Negative ADR removed:", negative_adr_count)
    print("Zero-guest records removed:", no_guest_count)
    print("Final rows:", len(data))
    print("Final columns:", len(data.columns))
    print("Missing values:", int(data.isna().sum().sum()))
    print("Remaining duplicates:", int(data.duplicated().sum()))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    clean_hotel_bookings()
