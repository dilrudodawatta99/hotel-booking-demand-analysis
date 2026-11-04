# Initial Findings and Updated Analytical Results

## 1. Raw Dataset Profile

The original Hotel Booking Demand dataset contains 119,390 records and 32 columns.

Initial data-quality checks identified:

| Data-quality issue | Count |
|---|---:|
| Exact duplicate records | 31,994 |
| Missing company values | 112,593 |
| Missing agent values | 16,340 |
| Missing country values | 488 |
| Missing children values | 4 |
| Negative ADR records | 1 |
| Zero ADR records | 1,959 |
| Zero-adult records | 403 |
| Records with no adults, children or babies | 180 |

The raw overall cancellation rate was 37.04%. The raw cancellation rate was 41.73% for City Hotel and 27.76% for Resort Hotel.

The original raw CSV is retained unchanged. Its SHA-256 checksum is recorded in `dataset_provenance.md`.

## 2. Data Cleaning and Final Analytical Dataset

The data was processed in separate stages to preserve the original source and make cleaning decisions traceable.

| Processing stage | Records |
|---|---:|
| Original raw dataset | 119,390 |
| After exact duplicate removal | 87,396 |
| Final cleaned analytical dataset | 87,229 |

The 31,994 exact duplicate records were removed from the analytical copy. Further cleaning removed one record with a negative ADR and 166 records with no guests.

Missing values were handled using documented cleaning rules. Missing country values were labelled as `Unknown`, and missing children values were replaced with zero. Missing company and agent values were handled without inventing individual identifiers.

Zero ADR and zero-adult records were retained for investigation rather than automatically removed. These values may represent unusual but potentially valid booking circumstances.

The final cleaned dataset contains 87,229 records and 32 columns, with no remaining missing values, exact duplicates, negative ADR values or zero-guest records.

## 3. Cancellation Analysis

All results in this section refer to the final cleaned dataset unless otherwise stated.

The overall cancellation rate is 27.52%.

| Hotel type | Bookings | Cancellation rate |
|---|---:|---:|
| City Hotel | 53,274 | 30.10% |
| Resort Hotel | 33,955 | 23.48% |

City Hotel has a higher cancellation rate than Resort Hotel. This difference may be associated with differences in customer behaviour, booking patterns and hotel characteristics. It does not establish a causal relationship.

### 3.1 Deposit Type

| Deposit type | Bookings | Cancellation rate |
|---|---:|---:|
| Non Refund | 1,038 | 94.70% |
| No Deposit | 86,084 | 26.72% |
| Refundable | 107 | 24.30% |

The Non Refund category has a notably high cancellation rate. However, it represents a relatively small proportion of bookings, so the result should be interpreted with caution. The relationship may also reflect the circumstances under which non-refundable deposits are applied.

### 3.2 Market Segment

| Market segment | Bookings | Cancellation rate |
|---|---:|---:|
| Online TA | 51,553 | 35.38% |
| Groups | 4,921 | 27.07% |
| Aviation | 226 | 19.91% |
| Offline TA/TO | 13,855 | 14.85% |
| Direct | 11,780 | 14.75% |
| Complementary | 692 | 12.28% |
| Corporate | 4,200 | 12.12% |
| Undefined | 2 | 100.00% |

Online Travel Agents account for the largest number of bookings and have a higher cancellation rate than most other market segments. The Undefined category has only two records and should not be used for broad conclusions.

### 3.3 Lead Time

Cancellation rates increase across the observed lead-time groups:

| Lead-time group | Cancellation rate |
|---|---:|
| 0–7 days | 8.42% |
| 8–30 days | 25.39% |
| 31–90 days | 32.04% |
| 91–180 days | 35.01% |
| 181–365 days | 39.69% |
| More than 365 days | 40.78% |

Bookings made further in advance are associated with higher cancellation rates. This is a descriptive association and does not demonstrate that longer lead times cause cancellations.

### 3.4 Other Observations

Returning guests have a lower cancellation rate than new guests:

- New guests: 28.32%.
- Returning guests: 7.73%.

Cancellation rates also differ across customer types. Transient bookings have a 30.14% cancellation rate, compared with 16.33% for Contract, 15.25% for Transient-Party and 9.80% for Group bookings.

The number of special requests is also associated with cancellation behaviour. Bookings with no special requests have a 33.25% cancellation rate, while bookings with one or more requests generally have lower rates. Small groups, particularly those with five requests, should be interpreted cautiously.

## 4. Average Daily Rate and Booking Value

The overall mean Average Daily Rate (ADR) is 106.52.

| Hotel type | Mean ADR | Median ADR |
|---|---:|---:|
| City Hotel | 111.27 | 105.30 |
| Resort Hotel | 99.06 | 79.50 |

The City Hotel has a higher average daily rate, while Resort Hotel bookings have a longer average stay.

An estimated booking-value measure can be calculated by multiplying ADR by the number of booked nights. This is only a proxy based on booking information. It should not be interpreted as realised revenue because cancelled bookings are included and actual payments are not established by this calculation.

The ADR distribution contains high-value observations. These were investigated using the interquartile range method. Statistical outliers were not automatically removed because an outlier is not necessarily an error.

## 5. Predictive Modelling

The target variable is `is_canceled`, which identifies whether a booking was cancelled.

The dataset was divided into training and testing sets using an 80:20 split, with stratification and a fixed random state of 42.

Three modelling approaches were evaluated:

| Model | Accuracy | Cancellation precision | Cancellation recall | Cancellation F1 |
|---|---:|---:|---:|---:|
| Logistic Regression, 24 features | 79% | 0.71 | 0.40 | 0.51 |
| Random Forest, 24 features | 76% | 0.54 | 0.78 | 0.64 |
| Random Forest, 20 features | 69% | 0.46 | 0.77 | 0.58 |

Logistic Regression achieved the highest accuracy, but it detected only 40% of cancelled bookings. The 24-feature Random Forest achieved a higher cancellation recall of 78%, identifying more cancelled bookings at the cost of more false positives.

The 20-feature Random Forest excludes booking information that may become available only after the initial reservation, including booking changes and deposit type. It provides a more cautious scenario for considering cancellation risk using information available closer to booking time.

The model comparison demonstrates that accuracy alone is not sufficient when evaluating cancellation prediction. Precision, recall and F1-score are also important.

The feature importance analysis identifies variables that contribute to the Random Forest's decisions. These importance scores indicate predictive contribution, not causation or the direction of an effect.

## 6. Interpretation and Limitations

The findings indicate that cancellation behaviour differs by hotel type, lead time, market segment, deposit type and customer characteristics.

The analysis is descriptive and predictive. It identifies patterns and evaluates the ability of models to classify cancellation outcomes. It does not establish why customers cancel or prove that changing a particular booking characteristic will reduce cancellations.

Potential target leakage must be considered when selecting predictive features. `reservation_status` and `reservation_status_date` are excluded because they contain information about the booking outcome. Other variables may also be unavailable at the exact time a reservation is first created.

The dataset represents historical hotel booking observations. Its patterns and model performance may not generalise to every hotel, market or future period. Further validation on newer data would be needed before operational use.

## 7. Analytical Direction

The project progresses through the OSEMN process:

- **Obtain:** acquire and document the original Hotel Booking Demand dataset.
- **Scrub:** inspect missing values, duplicates and invalid records, then create a cleaned analytical dataset.
- **Explore:** examine cancellation patterns and relationships using descriptive statistics and visualisations.
- **Model:** compare Logistic Regression and Random Forest models using classification metrics.
- **Interpret:** evaluate the findings, model limitations and possible implications for hotel booking management.

The descriptive findings can support further diagnostic investigation into the reasons behind cancellation differences. Predictive modelling provides an estimate of cancellation risk. A future prescriptive stage could evaluate possible interventions, such as targeted booking reminders or changes to deposit policies, but these would require further testing before implementation.

