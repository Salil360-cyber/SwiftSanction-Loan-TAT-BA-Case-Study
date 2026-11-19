# 1. Project charter

**Project:** SwiftSanction phase 1, faster personal-loan approvals · **Organisation:** Godavari Finance (fictional) · **Sponsor:** Head of Retail Lending · **Prepared by:** Salil Gokhale · **Version:** 1.0, 6 Jan 2027 (simulated)

## Why this project

Only 23.1% of personal loans meet the 72-hour SLA (average 4.3 days), and 1,269 approved customers withdrew at the sanction stage in six months. The BRD ([05_ba_docs/06_BRD.md](../05_ba_docs/06_BRD.md)) defines the fixes; this project delivers the four Must-have ones.

## Objectives (measured 6 months after go-live)

1. % of loans disbursed within 72 hours: 23.1% → at least 35%
2. Document re-request rate: 21.5% → under 12%
3. Withdrawals at sanction: at least 10% lower than 1,269 per six months

## Scope

| In scope (phase 1) | Out of scope |
| --- | --- |
| BR-01 document checklist by employment type | BR-05 DSA scorecard, BR-06 e-sign reminders (phase 2) |
| BR-02 upload quality check (app, web, DSA portal) | BR-07 Sunday verification shift (rostering decision) |
| BR-03 fast-track underwriting lane with 10% spot check | Credit policy and CIBIL cut-offs |
| BR-04 daily TAT / SLA report and alerts | Replacing the loan origination system |

## Timeline and milestones

| Milestone | Date |
| --- | --- |
| Charter signed | 6 Jan 2027 |
| BRD and fast-track rules signed off | 14 Jan 2027 |
| Sprint 1 done (checklist) | 28 Jan 2027 |
| Sprint 2 done (upload check) | 11 Feb 2027 |
| Sprint 3 done (fast-track lane) | 25 Feb 2027 |
| UAT sign-off | 8 Mar 2027 |
| Go-live | 9 Mar 2027 |
| Closure | 8 Apr 2027 |

Full schedule, Gantt and critical path: `SwiftSanction_Project_Plan.xlsx`.

## Team (RACI summary)

| Role | Person / team | RACI |
| --- | --- | --- |
| Sponsor | Head of Retail Lending | Accountable |
| Project lead | Loan Operations Manager | Responsible |
| Business Analyst | Salil Gokhale | Responsible |
| Build | IT / LOS team | Responsible |
| Rules approval | Credit Risk head | Consulted |
| Compliance check | Compliance | Consulted |
| Testing | QA lead + operations staff | Responsible |
| Users | Applicants, DSAs, ops staff | Informed |

## Budget (illustrative)

Rs 18 lakh for phase 1 (build, vendor API, testing, training). The expected gain is about 179 more loans disbursed per six months, worth about Rs 6.4 crore ([impact estimate](../05_ba_docs/10_ROI_estimate.md)).

## Top risks

Credit Risk approval of fast-track rules, vendor API timing for the upload check, DSA adoption, and fast-track credit quality. Full list with owners and scores: RAID_Log sheet.

## Approval (simulated)

Head of Retail Lending · Loan Operations Manager · Credit Risk head
