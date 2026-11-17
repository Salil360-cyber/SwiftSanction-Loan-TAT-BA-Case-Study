# 02_excel

`SwiftSanction_Analysis.xlsx`: every number on Summary and Analysis is a formula on `Clean_Data`, so it updates if the data changes.

| Sheet | What it shows |
| --- | --- |
| About | What each sheet contains, SLA definition |
| Cleaning_Log | 250 duplicates removed, 555 channel values fixed, 400 text amounts converted, 200 blank employment types set to Unknown |
| Clean_Data | 15,000 applications as an Excel Table (`loans`) + formula columns: `tat_days`, `sla_status` (nested IF), `low_risk` (IF + AND) |
| Summary | Final status split and TAT / SLA / re-request KPIs (COUNTIF, AVERAGEIFS) |
| Analysis | Re-request % by channel and employment type, TAT by re-requests, SLA % by submission day (with chart), low-risk reject % (COUNTIFS, AVERAGEIFS) |

Key results: average TAT **4.3 days**, only **23.1%** of disbursed loans within the 72-hour SLA, **21.5%** of applications needed a document re-request (DSA **33.8%**). The Excel and SQL results match.

Stage-level timing (which stage takes longest) is done in SQL on `stage_events.csv`, because it needs the event-level data.
