from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hotel_booking.processing import CSVBookingLoader, BookingPipeline
from hotel_booking.analysis import cancellation_summary, cancellation_by_category


# 1. Load the original raw dataset
raw_path = ROOT / "data" / "raw" / "hotel_bookings.csv"
raw = CSVBookingLoader().load(raw_path)


# 2. Run the reusable data-quality pipeline
pipeline = BookingPipeline()
deduplicated = pipeline.prepare(raw)


# 3. Load the fully cleaned dataset
cleaned_path = ROOT / "data" / "processed" / "hotel_bookings_cleaned.csv"

if not cleaned_path.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {cleaned_path}"
    )

data = pd.read_csv(cleaned_path)


# 4. Display data-quality information
print("\nRAW QUALITY REPORT")
print(pipeline.quality_report)

print("\nDATASET ROW COUNTS")
print("Original raw rows:", len(raw))
print("After duplicate removal:", len(deduplicated))
print("Final cleaned rows:", len(data))


# 5. Cancellation analysis
print("\nCANCELLATION SUMMARY")

summary = cancellation_summary(data)

print(
    "Overall cancellation rate:",
    round(summary["overall_rate"] * 100, 2),
    "%"
)

print("\nCancellation rate by hotel:")
print((summary["by_hotel"] * 100).round(2))


# 6. Cancellation by selected categories
for col in ["deposit_type", "market_segment"]:
    print(f"\nCANCELLATION BY {col.upper()}")
    print(cancellation_by_category(data, col))


# 7. Monthly cancellation analysis
month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly = (
    data.groupby("arrival_date_month")["is_canceled"]
    .mean()
    .reindex(month_order)
)


# 8. Generate monthly cancellation chart
plt.figure(figsize=(10, 6))

(monthly * 100).plot(kind="bar")

plt.ylabel("Cancellation rate (%)")
plt.xlabel("Arrival month")
plt.title("Hotel Booking Cancellation Rate by Arrival Month")
plt.xticks(rotation=45)
plt.tight_layout()

output_folder = ROOT / "outputs" / "figures"
output_folder.mkdir(parents=True, exist_ok=True)

output_path = output_folder / "cancellation_by_month.png"

plt.savefig(output_path, dpi=200)
plt.close()

print("\nSaved figure:", output_path)

print("\nAnalysis completed successfully.")