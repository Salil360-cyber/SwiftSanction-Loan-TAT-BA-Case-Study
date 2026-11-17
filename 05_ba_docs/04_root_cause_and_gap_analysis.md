# 4. Root cause and gap analysis

## 5 Whys: why do customers withdraw at the sanction stage?

1. **Why do customers withdraw?** They have waited too long and take a loan elsewhere: withdrawal rises from 3.7% (under 2 days) to 32.6% (6+ days).
2. **Why do they wait so long?** Average TAT is 4.3 days against a 3-day SLA.
3. **Why is TAT 4.3 days?** Underwriting takes 42.9 hours and document verification 24.3 hours on average.
4. **Why does document verification take so long?** 21.5% of files are sent back for re-upload (blurred, missing bank statement, missing salary slip / ITR), adding about 47 hours each.
5. **Why are files incomplete?** Customers and DSAs are not told exactly which documents their profile needs, and nothing checks quality at upload.

**Root causes:** no profile-based document checklist or upload check; one manual underwriting queue for every risk level; no TAT monitoring.

## Fishbone (cause categories)

| Category | Causes found |
| --- | --- |
| Process | Every file gets full manual underwriting; re-requests go back to the end of the queue |
| People | DSAs submit incomplete files (33.8% re-request rate vs 12.3% at branches) |
| Technology | No upload quality check; no checklist by employment type |
| Data / reporting | No daily TAT or SLA breach report |
| Environment | No ops cover on Sunday; Friday / Saturday files wait over the weekend |

## Gap analysis

| Area | AS-IS | TO-BE | Gap to close |
| --- | --- | --- | --- |
| Document collection | Generic upload, checked 1-2 days later | Profile checklist + instant quality check | Checklist rules, upload validation (BR-01, BR-02) |
| Underwriting | One queue, full manual review for all | Fast-track lane for low-risk files | Fast-track rules approved by Credit Risk (BR-03) |
| Monitoring | No TAT view | Daily TAT / SLA report + alerts | Report and alert rules (BR-04) |
| DSA quality | No feedback | Monthly re-request scorecard per DSA | Scorecard (BR-05) |
| Customer follow-up | No nudges after sanction | E-sign reminders and status tracker | Notifications (BR-06) |
| Weekend | Closed Sunday | Sunday cover for verification | Rostering decision (BR-07) |
