# SQL results

Run on PostgreSQL 16 against the clean data (15,000 applications, 67,346 stage events).

## Q1. How do applications end?

```
 final_status | applications | pct  
--------------+--------------+------
 Disbursed    |         9914 | 66.1
 Rejected     |         3382 | 22.5
 Withdrawn    |         1704 | 11.4
(3 rows)
```

## Q2. Turnaround time (TAT) of disbursed loans and SLA performance

```
 disbursed | avg_tat_hours | avg_tat_days | pct_within_sla 
-----------+---------------+--------------+----------------
      9914 |         104.2 |          4.3 |           23.1
(1 row)
```

## Q3. Where does the time go? Average hours per stage for disbursed loans

```
 stage_no |           stage_name           | avg_hours | pct_of_tat 
----------+--------------------------------+-----------+------------
        2 | Document Verification          |      24.3 |       23.4
        3 | Credit Bureau Check            |       3.0 |        2.9
        4 | Underwriting                   |      42.9 |       41.2
        5 | Sanction & Customer Acceptance |      16.6 |       15.9
        6 | Disbursal                      |      17.3 |       16.6
(5 rows)
```

## Q4. At which stage and why do applications close without a loan?

```
        last_stage_name         | final_status |          close_reason          | applications 
--------------------------------+--------------+--------------------------------+--------------
 Credit Bureau Check            | Rejected     | Low credit score / bureau flag |         1831
 Underwriting                   | Rejected     | Income / repayment capacity    |         1551
 Sanction & Customer Acceptance | Withdrawn    | Took loan elsewhere            |         1269
 Document Verification          | Withdrawn    | Did not re-upload documents    |          435
(4 rows)
```

## Q5. Document re-request rate by channel

```
  channel   | applications | with_rerequest | rerequest_pct 
------------+--------------+----------------+---------------
 DSA        |         3039 |           1026 |          33.8
 Website    |         2298 |            549 |          23.9
 Mobile App |         6008 |           1199 |          20.0
 Branch     |         3655 |            449 |          12.3
(4 rows)
```

## Q6. Document re-request rate by employment type

```
 employment_type | applications | rerequest_pct 
-----------------+--------------+---------------
 Self-employed   |         5159 |          28.8
 Unknown         |          200 |          20.0
 Salaried        |         9641 |          17.6
(3 rows)
```

## Q7. Why are documents re-requested?

```
           issue           | rerequests | pct  
---------------------------+------------+------
 Blurred document          |       1513 | 34.5
 Salary slip / ITR missing |       1112 | 25.4
 Missing bank statement    |       1110 | 25.3
 Address proof mismatch    |        650 | 14.8
(4 rows)
```

## Q8. How much does a re-request add to TAT?

```
 doc_rerequests | disbursed | avg_tat_hours | avg_tat_days 
----------------+-----------+---------------+--------------
              0 |      7997 |          93.3 |          3.9
              1 |      1499 |         139.9 |          5.8
              2 |       418 |         185.9 |          7.7
(3 rows)
```

## Q9. Do customers walk away when the loan is slow?

```
 waited_before_sanction | reached_sanction | withdrew | withdraw_pct 
------------------------+------------------+----------+--------------
 1) 0-2 days            |             3466 |      129 |          3.7
 2) 2-4 days            |             5047 |      503 |         10.0
 3) 4-6 days            |             1936 |      398 |         20.6
 4) 6+ days             |              734 |      239 |         32.6
(4 rows)
```

## Q10. Underwriting: do low-risk applications need the same manual review?

```
 risk_group | underwritten | avg_underwriting_hours | reject_pct 
------------+--------------+------------------------+------------
 Low risk   |         3320 |                   29.9 |        3.5
 Others     |         9414 |                   50.7 |       15.3
(2 rows)
```

## Q11. Does the day of application matter? (ops team works Mon-Sat, 10:00-18:00)

```
 submit_day | disbursed | avg_tat_hours | pct_within_sla 
------------+-----------+---------------+----------------
 Sat        |      1407 |         114.8 |            5.0
 Fri        |      1386 |         113.0 |            6.8
 Thu        |      1414 |         107.3 |           20.5
 Sun        |      1366 |         106.0 |           17.4
 Wed        |      1389 |         101.3 |           37.7
 Tue        |      1457 |          95.5 |           37.1
 Mon        |      1495 |          93.0 |           35.6
(7 rows)
```

## Q12. Monthly MIS report

```
  month  | applications | disbursed | disbursal_pct | avg_tat_hours | pct_within_sla 
---------+--------------+-----------+---------------+---------------+----------------
 2026-01 |         2575 |      1726 |          67.0 |         104.5 |           22.8
 2026-02 |         2265 |      1454 |          64.2 |         103.9 |           23.4
 2026-03 |         2546 |      1696 |          66.6 |         102.2 |           22.9
 2026-04 |         2588 |      1758 |          67.9 |         105.8 |           23.5
 2026-05 |         2598 |      1714 |          66.0 |         105.5 |           20.9
 2026-06 |         2428 |      1566 |          64.5 |         103.3 |           25.3
(6 rows)
```
