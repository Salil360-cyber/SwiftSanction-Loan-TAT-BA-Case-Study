# Business Requirements Document (BRD)

**Project:** SwiftSanction: Personal Loan Turnaround Time (TAT) Reduction · **Organisation:** Godavari Finance (fictional) · **Version:** 1.0 (Draft) · **Prepared by:** Salil Gokhale, Business Analyst

> Case study on synthetic data. Stakeholders and sign-offs are simulated.

## 1. Background

Godavari Finance sells unsecured personal loans (Rs 50,000 to Rs 15 lakh) through its Mobile App, Website, Branches and DSAs. After submission, every application passes 5 stages: Document Verification, Credit Bureau Check, Underwriting, Sanction & Customer Acceptance, and Disbursal. The service promise is disbursal within 72 hours.

## 2. Problem statement

From January to June 2026, only 23.1% of 9,914 disbursed loans met the 72-hour SLA, and the average TAT was 4.3 days. Underwriting (42.9 hours) and document verification (24.3 hours) take the most time; 21.5% of applications needed a document re-upload. Slow loans lose customers: 1,269 customers withdrew at the sanction stage, and withdrawal rises from 3.7% (waited under 2 days) to 32.6% (waited 6+ days).

## 3. Objectives

1. Raise % of loans disbursed within 72 hours from 23.1% to at least 35%.
2. Cut the document re-request rate from 21.5% to under 12%.
3. Reduce withdrawals at sanction by at least 10%.

All within 6 months of launch.

## 4. Scope

**In scope:** document checklist and upload check; fast-track underwriting lane for low-risk files; daily TAT / SLA report and alerts; DSA scorecard; sanction reminders; Sunday verification cover (next phase).
**Out of scope:** credit policy and CIBIL cut-offs; loan origination system replacement; pricing; collections; secured loans.

## 5. Stakeholders

Head of Retail Lending (sponsor, Accountable); Loan Operations Manager, IT / LOS team and Business Analyst (Responsible); Credit Risk head, Compliance, DSA channel manager, QA (Consulted); Customer service and applicants (Informed). Full RACI: [02_stakeholders_raci.md](02_stakeholders_raci.md).

## 6. Current process (AS-IS)

Applicant uploads documents → ops checks them (often 1-2 days later) and re-requests if blurred or missing → bureau check → every file waits in one queue for full manual underwriting → sanction letter → customer e-signs → disbursal. Ops works Monday to Saturday, 10:00-18:00. Flow: [03_process_flows.md](03_process_flows.md).

## 7. Data findings

| # | Finding | Value |
| --- | --- | --- |
| 1 | Loans disbursed within 72-hour SLA | 23.1% (avg TAT 4.3 days) |
| 2 | Slowest stage | Underwriting, 42.9 h (41% of TAT) |
| 3 | Applications with a document re-request | 21.5% (DSA 33.8%, Branch 12.3%) |
| 4 | Top re-request reason | Blurred document, 34.5% |
| 5 | Time added by one re-request | about 47 hours |
| 6 | Withdrawal at sanction: under 2 days vs 6+ days waited | 3.7% vs 32.6% |
| 7 | Low-risk files: underwriting time and rejection | 29.9 h, 3.5% rejected (others: 50.7 h, 15.3%) |
| 8 | SLA met for Friday / Saturday applications | 6.8% / 5.0% (Mon-Wed: 35.6-37.7%) |

Source: [03_sql/results.md](../03_sql/results.md), matched in the Excel workbook.

## 8. Business requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| BR-01 | The system shall show applicants and DSAs a document checklist based on employment type and block submission until all required documents are uploaded. | Must |
| BR-02 | The system shall check each upload for readability and completeness and tell the applicant immediately what to fix. | Must |
| BR-03 | Applications with CIBIL 750+, salaried employment and loan amount up to Rs 5 lakh shall go to a rule-based fast-track lane, with 10% of decisions sent daily for Credit Risk review. | Must |
| BR-04 | Operations shall receive a daily TAT / SLA report by stage, channel and branch, and an alert when a file is open for 60 hours. | Must |
| BR-05 | The DSA channel manager shall receive a monthly re-request rate per DSA. | Should |
| BR-06 | Applicants shall get an e-sign reminder 12 hours after the sanction letter and see their loan status. | Should |
| BR-07 | Document verification shall be staffed on Sundays. | Could |

User stories and acceptance criteria: [07_user_stories.md](07_user_stories.md).

## 9. Non-functional requirements

| Area | Requirement |
| --- | --- |
| Performance | Upload check result within 5 seconds; fast-track decision within 4 working hours |
| Availability | Upload and checklist available 24x7 |
| Security | Documents encrypted at rest and in transit; role-based access to reports |
| Audit | Every fast-track decision logs the rules applied and the result |
| Reporting | Daily report ready by 09:00 on working days |

## 10. Assumptions

- Credit Risk approves the fast-track rules before launch.
- The loan origination system can route files by rule and send SMS / app notifications.
- Applicants have a smartphone camera good enough for a readable upload.

## 11. Constraints

- RBI KYC and fair-lending rules apply to every change.
- Phase 1 budget and timeline are set by the sponsor; credit policy stays unchanged.

## 12. Risks and mitigation

| Risk | Mitigation |
| --- | --- |
| Fast-track approves a bad loan | Strict rules, 10% daily spot check, monthly review of fast-track defaults |
| Upload check rejects good documents | Manual override by ops; track false rejections in UAT and after launch |
| DSAs resist the scorecard | Share it as coaching, not penalty; start with the top 10 DSAs |
| Sunday shift costs too much | Pilot in two cities first (Could priority) |

## 13. Success KPIs

% disbursed within 72 hours · average TAT · document re-request % · withdrawals at sanction · fast-track spot-check findings.

## 14. Expected impact

Counting only the fast-track lane and half of re-requests avoided: about 179 fewer withdrawals per 6 months (about Rs 6.4 crore more disbursed), average TAT from 4.3 to about 3.8 days, and SLA from 23.1% to about 36%. Details: [10_ROI_estimate.md](10_ROI_estimate.md).

## 15. Appendix

RTM: [08_RTM.csv](08_RTM.csv) · UAT: [09_UAT_test_cases.md](09_UAT_test_cases.md) · Data dictionary: [01_data/DATA_DICTIONARY.md](../01_data/DATA_DICTIONARY.md)

**Sign-off (simulated):** Head of Retail Lending · Loan Operations Manager · Credit Risk head
