# Power BI build: model, Power Query step and DAX measures

## 1. Load

Get Data > Text/CSV:
- `loan_applications_clean.csv` → name the table `loans`
- `stage_events.csv` → name the table `events`

Check data types in Power Query: `submitted_at`, `start_time`, `end_time` = Date/Time; `loan_amount` = Whole number; `tat_hours`, `duration_hours` = Decimal number.

## 2. Power Query: build a `stage_time` table (hours spent in each stage)

A stage can have more than one attempt (document re-requests), so the time in a stage = first start to last end.

1. Right-click `events` > **Reference**. Rename the new query `stage_time`.
2. Home > **Group By** > Advanced: group by `application_id`, `stage_no`, `stage_name`.
   - New column `first_start` = Min of `start_time`
   - New column `last_end` = Max of `end_time`
3. Add Column > **Custom Column** `stage_hours` = `Duration.TotalHours([last_end] - [first_start])`, type Decimal.
4. Close & Apply.

## 3. Relationships (Model view)

- `loans[application_id]` 1 → * `events[application_id]`
- `loans[application_id]` 1 → * `stage_time[application_id]`

## 4. Calculated columns on `loans`

```
SLA Status =
IF(loans[final_status] <> "Disbursed", "Not disbursed",
   IF(loans[tat_hours] <= 72, "Within SLA", "Breached"))

Low Risk =
IF(loans[cibil_band] = "750+" && loans[employment_type] = "Salaried" && loans[loan_amount] <= 500000, "Yes", "No")

Day No = WEEKDAY(loans[submitted_at], 2)        -- Mon = 1 ... Sun = 7, use to sort submit_day
```

Sort `submit_day` by `Day No` (Column tools > Sort by column).

## 5. Measures

```
Applications = COUNTROWS(loans)

Disbursed = CALCULATE([Applications], loans[final_status] = "Disbursed")

Disbursal % = DIVIDE([Disbursed], [Applications])

Avg TAT (hours) = CALCULATE(AVERAGE(loans[tat_hours]), loans[final_status] = "Disbursed")

Avg TAT (days) = DIVIDE([Avg TAT (hours)], 24)

Within SLA = CALCULATE([Applications], loans[SLA Status] = "Within SLA")

SLA % = DIVIDE([Within SLA], [Disbursed])

Re-request % = DIVIDE(CALCULATE([Applications], loans[doc_rerequests] > 0), [Applications])

Avg Stage Hours =
CALCULATE(AVERAGE(stage_time[stage_hours]), loans[final_status] = "Disbursed")

Withdrawn = CALCULATE([Applications], loans[final_status] = "Withdrawn")
```

## 6. Expected values (check your cards against these)

| Measure | Value |
| --- | --- |
| Applications | 15,000 |
| Disbursed | 9,914 |
| Avg TAT (days) | 4.3 |
| SLA % | 23.1% |
| Re-request % | 21.5% |
| Avg Stage Hours, Underwriting | 42.9 |

These match `03_sql/results.md` and the Excel workbook.
