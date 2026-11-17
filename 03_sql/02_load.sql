-- Run in psql from the repo root. In pgAdmin: right-click each table > Import/Export Data,
-- choose the CSV, tick Header, and set NULL strings to blank.
\copy loan_applications FROM '01_data/loan_applications_clean.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy stage_events FROM '01_data/stage_events.csv' WITH (FORMAT csv, HEADER true, NULL '')

SELECT 'loan_applications' AS table_name, COUNT(*) FROM loan_applications
UNION ALL
SELECT 'stage_events', COUNT(*) FROM stage_events;
