# Hotel Booking Demand: Applied Data Processing Project

## Research question
What booking characteristics are associated with hotel reservation cancellations?

## Dataset
Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand  
Raw file: `data/raw/hotel_bookings.csv` (kept unchanged).

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python scripts/run_analysis.py
python scripts/benchmark_formats.py
pytest -q
```

## Project structure
- `hotel_booking/processing/`: reusable loading, validation and pipeline classes
- `hotel_booking/analysis.py`: analysis functions
- `scripts/`: reproducible analysis and format benchmark scripts
- `tests/`: automated tests
- `data/raw/`: immutable original CSV
- `outputs/figures/`: generated figures

## Data-quality policy
The pipeline reports exact duplicates and missing values before removing exact duplicate rows. Missing values are not silently imputed. Potentially unusual values (negative/zero ADR and zero-adult bookings) are flagged for investigation rather than automatically deleted.

## Important limitation
The benchmark results must be rerun on the student's own machine. Record Python, pandas, operating system, CPU and memory details in the report. Do not present timings from another machine as your own.
