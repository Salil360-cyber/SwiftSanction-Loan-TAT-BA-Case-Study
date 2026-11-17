# 1. Problem statement and goals

## Background

Godavari Finance (fictional) offers unsecured personal loans of Rs 50,000 to Rs 15 lakh through four channels: Mobile App, Website, Branch and DSA (Direct Selling Agents). Every application goes through 5 working stages after it is submitted: Document Verification → Credit Bureau Check → Underwriting → Sanction & Customer Acceptance → Disbursal. The operations team works Monday to Saturday, 10:00 to 18:00.

The bank's service promise (SLA) is to disburse an approved loan **within 72 hours (3 days)** of the application.

## Problem statement

> Of 9,914 personal loans disbursed from January to June 2026, only **23.1%** met the 72-hour SLA; the average turnaround time (TAT) was **4.3 days**. **Underwriting** takes the most time (**42.9 hours**, 41% of TAT), and **21.5%** of applications needed documents to be re-uploaded, which adds about **47 hours** per re-request. Slow loans cost the bank customers: at the sanction stage, **32.6%** of customers who had already waited 6+ days withdrew, against **3.7%** of those who waited under 2 days. In six months **1,269** customers who had been approved for sanction walked away. This affects loan applicants, the credit and operations teams, DSAs and the lending business head.

## Business goals (SMART)

1. Raise the share of loans disbursed within the 72-hour SLA from **23.1% to at least 35%** within 6 months of launch.
2. Cut the share of applications that need a document re-request from **21.5% to under 12%** within 6 months of launch.
3. Reduce customer withdrawals at the sanction stage by at least **10%** (from 1,269 per six months) in the same period.

## Scope

| In scope | Out of scope |
| --- | --- |
| Document checklist and upload quality check at application | Changing credit policy or CIBIL cut-offs |
| Fast-track underwriting lane for low-risk applications | Replacing the loan origination system |
| Daily TAT / SLA MIS report and breach alerts | Collections and repayment |
| DSA document quality feedback | Pricing and interest rates |
| Weekend ops cover (next phase) | Secured loans (home, gold, vehicle) |
