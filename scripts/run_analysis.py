from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hotel_booking.processing import CSVBookingLoader, BookingPipeline
from hotel_booking.analysis import cancellation_summary, cancellation_by_category

raw_path = ROOT / "data" / "raw" / "hotel_bookings.csv"
raw = CSVBookingLoader().load(raw_path)
pipeline = BookingPipeline()
data = pipeline.prepare(raw)

print("RAW QUALITY REPORT")
print(pipeline.quality_report)
print("\\nRAW ROWS:", len(raw), "CLEANED ROWS:", len(data))
print("\\nCANCELLATION SUMMARY")
summary = cancellation_summary(data)
print("Overall cancellation rate:", round(summary["overall_rate"] * 100, 2), "%")
print((summary["by_hotel"] * 100).round(2))
for col in ["deposit_type", "market_segment"]:
    print(f"\\nCancellation by {col}")
    print(cancellation_by_category(data, col))

# Derive month order explicitly for readable charting.
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
monthly = data.groupby("arrival_date_month")["is_canceled"].mean().reindex(month_order)
plt.figure()
(monthly * 100).plot(kind="bar")
plt.ylabel("Cancellation rate (%)")
plt.xlabel("Arrival month")
plt.title("Hotel booking cancellation rate by arrival month")
plt.tight_layout()
out = ROOT / "outputs" / "figures" / "cancellation_by_month.png"
plt.savefig(out, dpi=200)
print("\\nSaved figure:", out)
