# Initial findings from the supplied dataset

## Raw dataset profile
- 119,390 rows and 32 columns.
- 31,994 exact duplicate rows.
- Missing values: company 112,593 (94.31%); agent 16,340 (13.69%); country 488 (0.41%); children 4.
- Raw overall cancellation rate: 37.04%.
- Raw City Hotel cancellation rate: 41.73%; Resort Hotel: 27.76%.
- Raw median lead time: 69 days; cancelled bookings 113 days; non-cancelled bookings 45 days.

## Analytical copy after exact-duplicate removal
The project retains the raw file unchanged and creates a separate analytical copy by removing exact duplicate rows. This leaves 87,396 rows. All downstream rates must be labelled as based on this deduplicated analytical copy.
- Overall cancellation rate: 27.49%.
- City Hotel cancellation rate: 30.04%; Resort Hotel: 23.48%.
- Median lead time: 38 days for non-cancelled bookings and 80 days for cancelled bookings.
- Non-refundable deposit group cancellation rate: 94.70% (1,038 bookings).
- Online Travel Agent segment cancellation rate: 35.35% (51,618 bookings).
- August cancellation rate: 32.18%; January: 22.12%.

## Data-quality flags
- `company`: 112,593 missing (94.31%). Treat as unrecorded/not applicable unless source documentation confirms otherwise.
- `agent`: 16,340 missing (13.69%). Preserve missingness; do not invent agent IDs.
- `country`: 488 missing (0.41%). Preserve as unknown for country-level analysis.
- `children`: 4 missing. Investigate; do not silently replace.
- 1 negative ADR, 1,959 zero ADR, 403 zero-adult rows, and 180 rows with no adults, children or babies.
- 31,994 exact duplicate rows. The pipeline removes exact duplicate rows from the analytical copy, retaining the raw file unchanged.

## Interpretation caution
These are descriptive associations, not proof that any one factor causes cancellations. The difference between raw and deduplicated cancellation rates is substantial, so the report must justify duplicate handling and present both counts. Do not use `reservation_status` as a predictor of cancellation because it records the booking outcome and would cause target leakage.
