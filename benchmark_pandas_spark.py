import time
import statistics
import platform
import os
from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

DATA_PATH = Path("data/processed/hotel_bookings_cleaned.csv")
OUTPUT_PATH = Path("data/processed/pandas_spark_benchmark.csv")

# Pandas: read the dataset and count bookings by month
def pandas_test():
    df = pd.read_csv(DATA_PATH)
    result = df.groupby("arrival_date_month").size().sort_index()
    return result.to_dict()

# PySpark: read the same dataset and count bookings by month
def spark_test(spark):
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(DATA_PATH))
    )

    rows = (
        df.groupBy("arrival_date_month")
        .count()
        .orderBy("arrival_date_month")
        .collect()
    )

    return {row["arrival_date_month"]: row["count"] for row in rows}

def measure(function, *args):
    start = time.perf_counter()
    result = function(*args)
    elapsed = time.perf_counter() - start
    return elapsed, result

def main():
    print("Starting benchmark...")
    print("Python:", platform.python_version())
    print("Processor:", platform.processor())
    print("Logical CPU cores:", os.cpu_count())

    # Spark startup is deliberately outside the timed tests.
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("HotelBookingBenchmark")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    print("\nRunning warm-up tests...")
    pandas_warmup = pandas_test()
    spark_warmup = spark_test(spark)

    if pandas_warmup != spark_warmup:
        raise ValueError("Pandas and PySpark results do not match!")

    print("Warm-up complete. Results match.")

    pandas_times = []
    spark_times = []

    print("\nRunning five measured tests for each method...")

    for run in range(1, 6):
        pandas_time, pandas_result = measure(pandas_test)
        spark_time, spark_result = measure(spark_test, spark)

        if pandas_result != spark_result:
            raise ValueError(f"Results do not match on run {run}!")

        pandas_times.append(pandas_time)
        spark_times.append(spark_time)

        print(
            f"Run {run}: "
            f"Pandas = {pandas_time:.4f}s | "
            f"PySpark = {spark_time:.4f}s"
        )

    records = []

    for method, times in [
        ("Pandas", pandas_times),
        ("PySpark", spark_times)
    ]:
        records.append({
            "Method": method,
            "Runs": len(times),
            "Median_seconds": statistics.median(times),
            "Minimum_seconds": min(times),
            "Maximum_seconds": max(times),
            "Range_seconds": max(times) - min(times)
        })

    summary = pd.DataFrame(records)
    summary.to_csv(OUTPUT_PATH, index=False)

    print("\nBENCHMARK SUMMARY")
    print(summary.to_string(index=False))
    print("\nResults saved to:", OUTPUT_PATH)
    print("Both methods produced matching monthly booking counts.")

    spark.stop()

if __name__ == "__main__":
    main()
