# 9. UAT test cases

| TC | Requirement | Steps | Expected result | Result |
| --- | --- | --- | --- | --- |
| TC-01 | BR-01 | Start application → select Salaried → open upload step | Salaried checklist shown (PAN, Aadhaar, 3 salary slips, 6 months' statement) | |
| TC-02 | BR-01 | Select Self-employed → open upload step | Self-employed checklist shown (PAN, Aadhaar, 2 years' ITR, 12 months' statement) | |
| TC-03 | BR-01 | Leave ITR blank → tap Submit | Submission blocked; "ITR missing" shown | |
| TC-04 | BR-02 | Upload a blurred PAN image | "Document not readable" shown within 5 seconds | |
| TC-05 | BR-02 | Upload a 4-month bank statement where 6 are needed | Message says 2 months are missing | |
| TC-06 | BR-03 | Submit: CIBIL 780, Salaried, Rs 3 lakh | File routed to fast-track; decision recorded within 4 working hours | |
| TC-07 | BR-03 | Submit: CIBIL 780, Self-employed, Rs 3 lakh | File routed to manual queue; reason "Not salaried" shown | |
| TC-08 | BR-03 | Run end of day with 50 fast-track decisions | 5 decisions listed for Credit Risk review | |
| TC-09 | BR-04 | Open 09:00 report | Yesterday's KPIs match a manual count from the data | |
| TC-10 | BR-04 | Keep a test file open for 60 hours | Alert received with file ID and current stage | |
| TC-11 | BR-05 | Open DSA scorecard for last month | Re-request % per DSA matches the data | |
| TC-12 | BR-06 | Send sanction letter → do not e-sign for 12 hours | SMS and app reminder received | |
| TC-13 | BR-07 | Submit a file on Saturday evening | File picked up for verification on Sunday | |

Result column is filled during UAT (Pass / Fail + defect ID).
