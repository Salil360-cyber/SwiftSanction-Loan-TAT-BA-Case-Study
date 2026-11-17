# 03_sql

PostgreSQL 16 (pgAdmin 4 or psql).

| File | What it does |
| --- | --- |
| [`01_schema.sql`](01_schema.sql) | Creates `loan_applications` and `stage_events` (primary key, foreign key) |
| [`02_load.sql`](02_load.sql) | Loads the two clean CSVs and counts rows |
| [`03_analysis.sql`](03_analysis.sql) | 12 business questions: status split, TAT and SLA, time per stage, close reasons, re-request rate and reasons, TAT cost of a re-request, withdrawal vs wait, low-risk underwriting, day of week, monthly MIS |
| [`results.md`](results.md) | Output of every query |

SQL used: `JOIN`, `GROUP BY`, `CASE WHEN`, CTEs (`WITH`), `SUM(...) OVER ()` for % of total, date functions (`EXTRACT(EPOCH ...)`, `TO_CHAR`), `NULLIF`.
