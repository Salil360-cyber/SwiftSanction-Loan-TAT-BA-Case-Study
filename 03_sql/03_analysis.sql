-- SwiftSanction: business questions answered in SQL
-- SLA: a loan should be disbursed within 72 hours (3 days) of the application.

-- Q1. How do applications end?
SELECT final_status,
       COUNT(*) AS applications,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM loan_applications
GROUP BY final_status
ORDER BY applications DESC;

-- Q2. Turnaround time (TAT) of disbursed loans and SLA performance
SELECT COUNT(*) AS disbursed,
       ROUND(AVG(tat_hours), 1) AS avg_tat_hours,
       ROUND(AVG(tat_hours) / 24, 1) AS avg_tat_days,
       ROUND(100.0 * SUM(CASE WHEN tat_hours <= 72 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_within_sla
FROM loan_applications
WHERE final_status = 'Disbursed';

-- Q3. Where does the time go? Average hours per stage for disbursed loans
--     (first start to last end of the stage, so document re-requests are included)
WITH stage_time AS (
    SELECT e.application_id, e.stage_no, e.stage_name,
           EXTRACT(EPOCH FROM (MAX(e.end_time) - MIN(e.start_time))) / 3600 AS hours
    FROM stage_events e
    JOIN loan_applications a ON a.application_id = e.application_id
    WHERE a.final_status = 'Disbursed'
    GROUP BY e.application_id, e.stage_no, e.stage_name
)
SELECT stage_no, stage_name,
       ROUND(AVG(hours), 1) AS avg_hours,
       ROUND(100.0 * AVG(hours) / SUM(AVG(hours)) OVER (), 1) AS pct_of_tat
FROM stage_time
GROUP BY stage_no, stage_name
ORDER BY stage_no;

-- Q4. At which stage and why do applications close without a loan?
SELECT last_stage_name, final_status, close_reason, COUNT(*) AS applications
FROM loan_applications
WHERE final_status <> 'Disbursed'
GROUP BY last_stage_name, final_status, close_reason
ORDER BY applications DESC;

-- Q5. Document re-request rate by channel
SELECT channel,
       COUNT(*) AS applications,
       SUM(CASE WHEN doc_rerequests > 0 THEN 1 ELSE 0 END) AS with_rerequest,
       ROUND(100.0 * SUM(CASE WHEN doc_rerequests > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS rerequest_pct
FROM loan_applications
GROUP BY channel
ORDER BY rerequest_pct DESC;

-- Q6. Document re-request rate by employment type
SELECT employment_type,
       COUNT(*) AS applications,
       ROUND(100.0 * SUM(CASE WHEN doc_rerequests > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS rerequest_pct
FROM loan_applications
GROUP BY employment_type
ORDER BY rerequest_pct DESC;

-- Q7. Why are documents re-requested?
SELECT issue, COUNT(*) AS rerequests,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM stage_events
WHERE outcome = 'Re-requested'
GROUP BY issue
ORDER BY rerequests DESC;

-- Q8. How much does a re-request add to TAT?
SELECT doc_rerequests,
       COUNT(*) AS disbursed,
       ROUND(AVG(tat_hours), 1) AS avg_tat_hours,
       ROUND(AVG(tat_hours) / 24, 1) AS avg_tat_days
FROM loan_applications
WHERE final_status = 'Disbursed'
GROUP BY doc_rerequests
ORDER BY doc_rerequests;

-- Q9. Do customers walk away when the loan is slow?
--     Withdrawal rate at the sanction stage by how long the customer had already waited
WITH s5 AS (
    SELECT e.outcome,
           EXTRACT(EPOCH FROM (e.start_time - a.submitted_at)) / 86400 AS days_waited
    FROM stage_events e
    JOIN loan_applications a ON a.application_id = e.application_id
    WHERE e.stage_no = 5
)
SELECT CASE WHEN days_waited < 2 THEN '1) 0-2 days'
            WHEN days_waited < 4 THEN '2) 2-4 days'
            WHEN days_waited < 6 THEN '3) 4-6 days'
            ELSE '4) 6+ days' END AS waited_before_sanction,
       COUNT(*) AS reached_sanction,
       SUM(CASE WHEN outcome = 'Withdrawn' THEN 1 ELSE 0 END) AS withdrew,
       ROUND(100.0 * SUM(CASE WHEN outcome = 'Withdrawn' THEN 1 ELSE 0 END) / COUNT(*), 1) AS withdraw_pct
FROM s5
GROUP BY 1
ORDER BY 1;

-- Q10. Underwriting: do low-risk applications need the same manual review?
--      Low risk = CIBIL 750+, salaried, loan up to Rs 5 lakh
SELECT CASE WHEN a.cibil_band = '750+' AND a.employment_type = 'Salaried' AND a.loan_amount <= 500000
            THEN 'Low risk' ELSE 'Others' END AS risk_group,
       COUNT(*) AS underwritten,
       ROUND(AVG(e.duration_hours), 1) AS avg_underwriting_hours,
       ROUND(100.0 * SUM(CASE WHEN e.outcome = 'Rejected' THEN 1 ELSE 0 END) / COUNT(*), 1) AS reject_pct
FROM stage_events e
JOIN loan_applications a ON a.application_id = e.application_id
WHERE e.stage_no = 4
GROUP BY 1;

-- Q11. Does the day of application matter? (ops team works Mon-Sat, 10:00-18:00)
SELECT submit_day,
       COUNT(*) AS disbursed,
       ROUND(AVG(tat_hours), 1) AS avg_tat_hours,
       ROUND(100.0 * SUM(CASE WHEN tat_hours <= 72 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_within_sla
FROM loan_applications
WHERE final_status = 'Disbursed'
GROUP BY submit_day
ORDER BY avg_tat_hours DESC;

-- Q12. Monthly MIS report
SELECT TO_CHAR(submitted_at, 'YYYY-MM') AS month,
       COUNT(*) AS applications,
       SUM(CASE WHEN final_status = 'Disbursed' THEN 1 ELSE 0 END) AS disbursed,
       ROUND(100.0 * SUM(CASE WHEN final_status = 'Disbursed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disbursal_pct,
       ROUND(AVG(tat_hours), 1) AS avg_tat_hours,
       ROUND(100.0 * SUM(CASE WHEN tat_hours <= 72 THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN final_status = 'Disbursed' THEN 1 ELSE 0 END), 0), 1) AS pct_within_sla
FROM loan_applications
GROUP BY 1
ORDER BY 1;
