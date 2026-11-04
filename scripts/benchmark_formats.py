"""Benchmark CSV, JSON Lines and pickle on the supplied dataset.

Runs six times per operation: first run is treated as warm-up; report median
and range across the remaining five. Results depend on the execution machine.
"""
from pathlib import Path
import statistics
import tempfile
import time
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "raw" / "hotel_bookings.csv"
frame = pd.read_csv(SOURCE)

def measure(operation, repeats=6):
    durations = []
    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        durations.append((time.perf_counter() - start) * 1000)
    measured = durations[1:]  # discard warm-up
    return {
        "median_ms": round(statistics.median(measured), 2),
        "range_ms": [round(min(measured), 2), round(max(measured), 2)],
        "runs_ms": [round(x, 2) for x in durations]
    }

with tempfile.TemporaryDirectory() as directory:
    d = Path(directory)
    csv_path, json_path, pickle_path = d/"bookings.csv", d/"bookings.jsonl", d/"bookings.pkl"
    frame.to_csv(csv_path, index=False)
    frame.to_json(json_path, orient="records", lines=True)
    frame.to_pickle(pickle_path)

    results = {}
    specs = {
        "CSV": (lambda: frame.to_csv(d/"write.csv", index=False),
                lambda: pd.read_csv(csv_path),
                lambda: pd.read_csv(csv_path, usecols=["adr"]),
                csv_path),
        "JSON Lines": (lambda: frame.to_json(d/"write.jsonl", orient="records", lines=True),
                       lambda: pd.read_json(json_path, orient="records", lines=True),
                       lambda: pd.read_json(json_path, orient="records", lines=True)[["adr"]],
                       json_path),
        "Pickle": (lambda: frame.to_pickle(d/"write.pkl"),
                   lambda: pd.read_pickle(pickle_path),
                   lambda: pd.read_pickle(pickle_path)[["adr"]],
                   pickle_path)
    }
    for name, (write_fn, read_fn, column_fn, path) in specs.items():
        results[name] = {
            "size_bytes": path.stat().st_size,
            "write": measure(write_fn),
            "read_full": measure(read_fn),
            "read_one_column": measure(column_fn)
        }
    output = ROOT / "outputs" / "benchmark_results_local.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"Saved benchmark results to: {output}")
