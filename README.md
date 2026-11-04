# Hotel Booking Demand: Data Processing, Storage Evaluation and Scalable Analysis

## 1. Project Overview

This project investigates hotel booking characteristics associated with reservation cancellations using the Hotel Booking Demand dataset.

The project was completed as part of the **Programming for Data Science** coursework for the MSc Data Science programme.

**Research question:** What booking characteristics are associated with hotel reservation cancellations?

The project covers:
- Reusable Python classes for data loading, validation and processing.
- Data-quality assessment and cleaning.
- Exploratory data analysis and visualisation.
- Cancellation prediction using machine learning.
- Storage format and performance comparisons.
- Pandas and PySpark performance evaluation.
- Reproducibility, version control and ethical considerations.

## 2. Dataset and Source

The dataset is obtained from Kaggle:

[Hotel Booking Demand Dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)

- **Dataset author:** Jesse Mostipak
- **Original research:** Antonio, N., de Almeida, A., and Nunes, L. (2019).
- **Original publication:** *Hotel booking demand datasets*, Data in Brief, 22, 41–49.
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0).

The original CSV is retained in `data/raw/` and is not modified by the cleaning pipeline.

## 3. Project Structure

```text
hotel_booking_coursework/
│
├── data/
│   ├── raw/
│   │   └── hotel_bookings.csv
│   └── processed/
│       ├── hotel_bookings_cleaned.csv
│       ├── storage_size_comparison.png
│       ├── storage_performance_comparison.png
│       ├── pandas_spark_benchmark.csv
│       └── other analysis outputs
│
├── hotel_booking/
│   └── processing/
│       └── reusable processing classes
│
├── scripts/
│   ├── clean_data.py
│   └── benchmark_formats.py
│
├── tests/
│   └── test_processing.py
│
├── outputs/
│   └── benchmark_results_local.json
│
├── report/
│   └── dataset_provenance.md
│
├── benchmark_pandas_spark.py
├── benchmark_compression.py
├── class_diagram.mmd
├── requirements.txt
├── README.md
└── .gitignore
```

## 4. Environment and Installation

The project was developed and tested using:

| Component | Version / Specification |
|---|---|
| Python | 3.12.10 |
| Pandas | 2.2.3 |
| PySpark | 4.3.0 |
| Java | 17 |
| Operating system | Windows 11 |
| Processor | Intel Core i5-1334U |
| RAM | 15.69 GB |

### Setup

Clone the repository:

```bash
git clone https://github.com/dilrudodawatta99/hotel-booking-demand-analysis.git
cd hotel-booking-demand-analysis
```

Create and activate a virtual environment:

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

PySpark execution also requires a compatible Java installation. This project was tested with Java 17.

## 5. Data Cleaning

The cleaning pipeline is implemented in:

```text
scripts/clean_data.py
```

Run it from the project root:

```bash
python scripts/clean_data.py
```

The original dataset contains 119,390 records and 32 columns.

The cleaning process applies the following rules:

| Data-quality issue | Treatment |
|---|---|
| Missing company values | Replaced with 0 |
| Missing agent values | Replaced with 0 |
| Missing country values | Replaced with `Unknown` |
| Missing children values | Replaced with 0 |
| Exact duplicate records | Removed |
| Negative ADR | Removed |
| Zero ADR | Retained |
| Zero-adult bookings | Retained |
| Records with no guests | Removed |

After cleaning, the dataset contains **87,229 records and 32 columns**, with no remaining missing values or exact duplicates.

The cleaned dataset is saved to:

```text
data/processed/hotel_bookings_cleaned.csv
```

## 6. Automated Testing

The project includes automated tests for data validation, exception handling and pipeline behaviour.

Run the tests from the project root:

```bash
python -m pytest -v
```

The current test suite contains eight tests, covering validation failures, custom exceptions and duplicate removal.

## 7. Storage Format Benchmarking

The storage benchmark is implemented in:

```text
scripts/benchmark_formats.py
```

Run:

```bash
python scripts/benchmark_formats.py
```

The benchmark compares CSV, JSON Lines and Pickle formats using:
- Uncompressed and GZIP-compressed file sizes.
- Full dataset write time.
- Full dataset read time.
- Single-column read time.
- Repeated measurements, with the first run discarded as a warm-up.

The results are saved in:

```text
outputs/benchmark_results_local.json
```

The benchmark charts are saved in:

```text
data/processed/
```

Results are hardware-dependent and should be interpreted in the context of the recorded environment.

## 8. Pandas and PySpark Comparison

The project compares Pandas and PySpark using the same cleaned dataset and a monthly booking aggregation.

Run:

```bash
python benchmark_pandas_spark.py
```

The benchmark uses repeated measurements and compares the resulting aggregations to confirm that both approaches produce equivalent results.

Results are saved in:

```text
data/processed/pandas_spark_benchmark.csv
```

PySpark is executed in local mode. Spark startup is excluded from the timed measurements.

## 9. Reproducibility and Data Integrity

- The original dataset is retained separately from processed data.
- The cleaning pipeline can be rerun from the project root.
- Dependencies are recorded in `requirements.txt`.
- Automated tests are available through `pytest`.
- Git is used to track project development and changes.
- Benchmark results are specific to the recorded hardware and software environment.

## 10. Ethical and Professional Considerations

The dataset source and licence are acknowledged. Data processing is limited to the academic research purpose.

Data-quality decisions are documented, and unusual values are assessed before removal. Model results are interpreted carefully, recognising that associations do not establish causation.

The project also considers relevant GDPR principles, including data minimisation, accuracy, purpose limitation and storage limitation.

## 11. Repository

GitHub repository:

[https://github.com/dilrudodawatta99/hotel-booking-demand-analysis](https://github.com/dilrudodawatta99/hotel-booking-demand-analysis)

