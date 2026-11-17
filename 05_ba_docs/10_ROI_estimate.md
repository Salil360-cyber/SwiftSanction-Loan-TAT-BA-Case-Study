# 10. Impact estimate

Script: [`scripts/impact_estimate.py`](../scripts/impact_estimate.py). It changes no customer behaviour: it only shortens each application's wait by what a fix saves, then applies the withdrawal rates already seen in the data (SQL Q9) to the new wait.

## Assumptions (only two fixes counted)

| Fix | Assumption |
| --- | --- |
| BR-03 Fast-track lane | Low-risk files (CIBIL 750+, salaried, up to Rs 5 lakh) get a decision in **4 hours** instead of today's underwriting time |
| BR-01 + BR-02 Checklist and upload check | **Half** of document re-requests are avoided; each avoided re-request saves **46.6 hours** (SQL Q8: 139.9 h with one re-request vs 93.3 h with none) |

## Inputs from the data

| Input | Value |
| --- | --- |
| Withdrawal at sanction by days already waited | 0-2 days 3.7% · 2-4 days 10.0% · 4-6 days 20.6% · 6+ days 32.6% |
| Withdrawals at sanction (Jan-Jun 2026) | 1,269 |
| Average disbursed loan | Rs 3.55 lakh |

## Result (per 6 months)

| Measure | Today | After the two fixes |
| --- | --- | --- |
| Withdrawals at sanction | 1,269 | about **1,090** (about **179** fewer) |
| Extra loans disbursed | - | about **179**, worth about **Rs 6.4 crore** |
| Average TAT (disbursed) | 4.3 days (104.2 h) | about **3.8 days** (92.1 h) |
| % disbursed within 72-hour SLA | 23.1% | about **36%** |

## Notes

- The estimate is deliberately modest: the MIS alerts, DSA scorecard, e-sign reminders and Sunday cover are not counted.
- Rupee ROI needs two inputs from the bank: the cost to build the features and the margin earned per loan. With those, ROI = (extra loans × margin per loan − cost) / cost.
- After launch, track: % within SLA, average TAT, re-request %, withdrawals at sanction, and fast-track spot-check findings.
