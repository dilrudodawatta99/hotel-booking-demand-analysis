import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parents[1]

with open(root / "outputs" / "benchmark_results_local.json", encoding="utf-8") as f:
    results = json.load(f)

formats = ["CSV", "JSON Lines", "Pickle"]
compressed_mb = [1.159828, 1.749820, 1.065375]

# Chart 1: File sizes
uncompressed_mb = [
    results[name]["size_bytes"] / 1_000_000
    for name in formats
]

x = np.arange(len(formats))
width = 0.35

plt.figure(figsize=(9, 5))
plt.bar(x - width/2, uncompressed_mb, width, label="Uncompressed")
plt.bar(x + width/2, compressed_mb, width, label="GZIP")
plt.xticks(x, formats)
plt.ylabel("File size (MB)")
plt.title("Storage Size Comparison: Uncompressed vs GZIP")
plt.legend()
plt.tight_layout()
plt.savefig(root / "data" / "processed" / "storage_size_comparison.png", dpi=300)
plt.close()

# Chart 2: Median operation times
operations = ["write", "read_full", "read_one_column"]
labels = ["Write", "Full read", "Single-column read"]

plt.figure(figsize=(10, 5))

for name in formats:
    values = [results[name][operation]["median_ms"] for operation in operations]
    plt.plot(labels, values, marker="o", linewidth=2, label=name)

plt.ylabel("Median time (milliseconds)")
plt.title("Storage Format Performance Comparison")
plt.legend()
plt.tight_layout()
plt.savefig(root / "data" / "processed" / "storage_performance_comparison.png", dpi=300)
plt.close()

print("Both charts created successfully.")
print("storage_size_comparison.png")
print("storage_performance_comparison.png")
