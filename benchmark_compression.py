from pathlib import Path
import gzip
import pickle
import platform
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "raw" / "hotel_bookings.csv"
OUTPUT = ROOT / "outputs" / "compression_results.txt"

df = pd.read_csv(SOURCE)
results = []

with gzip.open(ROOT / "outputs" / "bookings.csv.gz", "wt", encoding="utf-8") as f:
    df.to_csv(f, index=False)

with gzip.open(ROOT / "outputs" / "bookings.jsonl.gz", "wt", encoding="utf-8") as f:
    df.to_json(f, orient="records", lines=True)

with gzip.open(ROOT / "outputs" / "bookings.pkl.gz", "wb") as f:
    pickle.dump(df, f)

files = [
    ("CSV", ROOT / "outputs" / "bookings.csv.gz"),
    ("JSON Lines", ROOT / "outputs" / "bookings.jsonl.gz"),
    ("Pickle", ROOT / "outputs" / "bookings.pkl.gz")
]

for name, compressed_path in files:
    compressed_size = compressed_path.stat().st_size
    results.append(
        f"{name}: {compressed_size:,} bytes "
        f"({compressed_size / 1024:.2f} KB)"
    )

original_size = SOURCE.stat().st_size

report = [
    "GZIP COMPRESSION RESULTS",
    f"Original CSV size: {original_size:,} bytes",
    "",
    *results,
    "",
    f"Python version: {platform.python_version()}",
    f"Pandas version: {pd.__version__}",
    f"Operating system: {platform.platform()}",
    f"Processor: {platform.processor()}"
]

OUTPUT.write_text("\n".join(report), encoding="utf-8")
print("\n".join(report))
print(f"\nSaved to: {OUTPUT}")
