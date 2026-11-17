# 7. User stories and acceptance criteria

**Epic E1: Right documents the first time** · **Epic E2: Faster decisions** · **Epic E3: Visibility and follow-up**

| ID | Epic | User story | Priority |
| --- | --- | --- | --- |
| US-01 | E1 | As a loan applicant, I want to see the exact documents needed for my employment type, so that I upload everything the first time. | Must |
| US-02 | E1 | As a loan applicant, I want to be told immediately if my upload is blurred or incomplete, so that I can fix it before submitting. | Must |
| US-03 | E1 | As a DSA, I want the same checklist and upload check in my partner portal, so that my customers' files are not sent back. | Must |
| US-04 | E2 | As a credit officer, I want low-risk applications decided by approved rules, so that I can spend my time on risky files. | Must |
| US-05 | E2 | As a Credit Risk head, I want a random sample of fast-track decisions sent to me for review, so that I can confirm the rules are safe. | Must |
| US-06 | E3 | As an operations manager, I want a daily report of TAT and SLA by stage, channel and branch, so that I know where files are stuck. | Must |
| US-07 | E3 | As an operations manager, I want an alert when a file is close to breaching the SLA, so that I can act before the customer leaves. | Must |
| US-08 | E3 | As a DSA channel manager, I want a monthly re-request rate per DSA, so that I can coach the DSAs with the most bounced files. | Should |
| US-09 | E3 | As a loan applicant, I want a reminder to e-sign my sanction letter and a status tracker, so that I know what happens next. | Should |
| US-10 | E2 | As an operations manager, I want Sunday cover for document verification, so that weekend applications are not delayed. | Could |

## Acceptance criteria (Given-When-Then)

**US-01 Document checklist**
- Given I select "Salaried", when I reach the upload step, then I see: PAN, Aadhaar, last 3 salary slips, last 6 months' bank statement.
- Given I select "Self-employed", when I reach the upload step, then I see: PAN, Aadhaar, last 2 years' ITR, last 12 months' bank statement.
- Given a required document is missing, when I tap Submit, then submission is blocked and the missing document is named.

**US-02 Upload quality check**
- Given I upload a blurred image, when the check runs, then I see "Document not readable, please upload again" within 5 seconds.
- Given I upload a bank statement with fewer months than required, when the check runs, then I am told how many months are missing.

**US-04 Fast-track lane**
- Given CIBIL is 750+, employment is Salaried and the amount is up to Rs 5 lakh, when the bureau check passes, then the file goes to the fast-track lane.
- Given a file is in the fast-track lane, when all rules pass, then a sanction decision is recorded within 4 working hours.
- Given any rule fails, when the lane runs, then the file moves to the manual queue with the failed rule named.

**US-05 Spot check**
- Given fast-track decisions are made, when the day ends, then 10% of them, picked at random, are listed for Credit Risk review.

**US-06 Daily TAT report**
- Given it is 09:00 on a working day, when the report runs, then it shows yesterday's applications, disbursals, average TAT, % within SLA, and average hours per stage, filterable by channel and branch.

**US-07 SLA alert**
- Given a file has been open for 60 hours and is not disbursed, when the hourly check runs, then the operations manager gets an alert with the file ID and its current stage.

**US-09 Sanction reminder**
- Given a sanction letter has been sent, when 12 hours pass without e-sign, then the applicant gets an SMS and app reminder.
