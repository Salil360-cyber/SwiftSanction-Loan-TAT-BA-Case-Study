"""Generate SwiftSanction synthetic data (Godavari Finance is fictional).
One row per personal-loan application + one row per stage attempt."""
import numpy as np, pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(7)
N = 15000
WORK_START, WORK_END = 10, 18          # bank ops work Mon-Sat 10:00-18:00

def next_work(t):
    """Move t to the next moment the ops team is working."""
    while True:
        if t.weekday() == 6:  # Sunday
            t = (t + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0); continue
        if t.hour < WORK_START:
            return t.replace(hour=WORK_START, minute=0, second=0)
        if t.hour >= WORK_END:
            t = (t + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0); continue
        return t

def work(t, hours):
    """Ops work of `hours` working hours starting at t (pauses outside working time)."""
    t = next_work(t); left = hours
    while left > 1e-9:
        end_today = t.replace(hour=WORK_END, minute=0, second=0)
        avail = (end_today - t).total_seconds() / 3600
        if left <= avail:
            return t + timedelta(hours=left)
        left -= avail
        t = next_work(end_today + timedelta(minutes=1))
    return t

cities = {"Mumbai": "Tier 1", "Pune": "Tier 1", "Bengaluru": "Tier 1", "Hyderabad": "Tier 1",
          "Nagpur": "Tier 2", "Nashik": "Tier 2", "Indore": "Tier 2",
          "Gondia": "Tier 3", "Wardha": "Tier 3", "Latur": "Tier 3"}
city_p = [.14, .12, .13, .11, .11, .09, .09, .07, .07, .07]
STAGES = {2: "Document Verification", 3: "Credit Bureau Check", 4: "Underwriting",
          5: "Sanction & Customer Acceptance", 6: "Disbursal"}
doc_issue = ["Blurred document", "Missing bank statement", "Salary slip / ITR missing", "Address proof mismatch"]

apps, events = [], []
start = datetime(2026, 1, 1)
for i in range(1, N + 1):
    aid = f"SS{i:05d}"
    channel = rng.choice(["Mobile App", "Website", "Branch", "DSA"], p=[.40, .15, .25, .20])
    emp = rng.choice(["Salaried", "Self-employed"], p=[.65, .35])
    cibil = rng.choice(["750+", "700-749", "650-699", "Below 650"], p=[.45, .28, .17, .10])
    city = rng.choice(list(cities), p=city_p)
    amt = int(np.clip(round(np.exp(rng.normal(12.6, .6)) / 5000) * 5000, 50000, 1500000))
    # submission: any day, weighted towards daytime
    day = start + timedelta(days=int(rng.integers(0, 181)))
    hour = int(rng.choice(range(24), p=np.array([1,1,1,1,1,1,2,3,5,7,8,8,8,8,8,8,7,7,6,5,4,3,2,1]) / 106))
    sub = day + timedelta(hours=hour, minutes=int(rng.integers(0, 60)))
    t = sub; status, reason, last = None, "", 2

    # Stage 2: document verification with re-requests
    p_rr = {"Mobile App": .18, "Website": .22, "Branch": .10, "DSA": .34}[channel] + (.12 if emp == "Self-employed" else 0)
    attempt = 1
    while True:
        s = t; e = work(s, rng.gamma(2, 1.6))
        if attempt < 3 and rng.random() < (p_rr if attempt == 1 else .25):
            iss = rng.choice(doc_issue, p=[.30, .30, .25, .15] if emp == "Self-employed" else [.40, .20, .25, .15])
            events.append([aid, 2, STAGES[2], attempt, s, e, "Re-requested", iss])
            wait = rng.gamma(2, 16)                           # customer takes time to re-upload
            if rng.random() < .10:
                status, reason = "Withdrawn", "Did not re-upload documents"
                break
            t = e + timedelta(hours=wait); attempt += 1; continue
        events.append([aid, 2, STAGES[2], attempt, s, e, "Passed", ""]); t = e; break
    if status is None:
        last = 3
        s = t; e = work(s, rng.gamma(2, .6))
        p_rej = {"750+": .02, "700-749": .04, "650-699": .15, "Below 650": .85}[cibil]
        if rng.random() < p_rej:
            events.append([aid, 3, STAGES[3], 1, s, e, "Rejected", "Low credit score / bureau flag"])
            status, reason = "Rejected", "Low credit score / bureau flag"
        else:
            events.append([aid, 3, STAGES[3], 1, s, e, "Passed", ""]); t = e
    if status is None:
        last = 4
        low_risk = cibil == "750+" and emp == "Salaried" and amt <= 500000
        hrs = rng.gamma(2, 2.5 if low_risk else 5.5) + (6 if amt > 1000000 else 0)
        s = t; e = work(s + timedelta(hours=rng.gamma(2, 4)), hrs)    # queue wait + review
        p_rej = {"750+": .04, "700-749": .10, "650-699": .30, "Below 650": .30}[cibil] + (.05 if emp == "Self-employed" else 0)
        if rng.random() < p_rej:
            events.append([aid, 4, STAGES[4], 1, s, e, "Rejected", "Income / repayment capacity"])
            status, reason = "Rejected", "Income / repayment capacity"
        else:
            events.append([aid, 4, STAGES[4], 1, s, e, "Passed", ""]); t = e
    if status is None:
        last = 5
        s = t; letter = work(s, rng.gamma(2, .7))
        e = letter + timedelta(hours=rng.gamma(1.5, 8))              # customer e-signs any time
        elapsed = (s - sub).total_seconds() / 3600
        p_wd = .04 if elapsed < 48 else .10 if elapsed < 96 else .20 if elapsed < 144 else .32
        if rng.random() < p_wd:
            events.append([aid, 5, STAGES[5], 1, s, e, "Withdrawn", "Took loan elsewhere"])
            status, reason = "Withdrawn", "Took loan elsewhere"
        else:
            events.append([aid, 5, STAGES[5], 1, s, e, "Passed", ""]); t = e
    if status is None:
        last = 6
        s = t; e = work(s, rng.gamma(2, 1.8))
        events.append([aid, 6, STAGES[6], 1, s, e, "Passed", ""]); t = e
        status = "Disbursed"
    end = events[-1][5] if status != "Withdrawn" or reason == "Took loan elsewhere" else t
    apps.append([aid, sub, sub.strftime("%a"), channel, city, cities[city], emp, cibil, amt,
                 last, STAGES[last], status, reason, attempt - 1,
                 round((end - sub).total_seconds() / 3600, 1) if status == "Disbursed" else None])

A = pd.DataFrame(apps, columns=["application_id", "submitted_at", "submit_day", "channel", "branch_city", "city_tier",
                                "employment_type", "cibil_band", "loan_amount", "last_stage_no", "last_stage_name",
                                "final_status", "close_reason", "doc_rerequests", "tat_hours"])
E = pd.DataFrame(events, columns=["application_id", "stage_no", "stage_name", "attempt_no", "start_time",
                                  "end_time", "outcome", "issue"])
E["duration_hours"] = ((E.end_time - E.start_time).dt.total_seconds() / 3600).round(1)
E.insert(0, "event_id", [f"EV{i:06d}" for i in range(1, len(E) + 1)])
A["submitted_at"] = A.submitted_at.dt.strftime("%Y-%m-%d %H:%M")
for c in ["start_time", "end_time"]:
    E[c] = E[c].dt.strftime("%Y-%m-%d %H:%M")
blank_idx = rng.choice(len(A), 200, replace=False)
true_emp = A.employment_type.copy()
A.loc[blank_idx, "employment_type"] = "Unknown"      # what cleaning can recover: nothing, so 'Unknown'
A.to_csv("01_data/loan_applications_clean.csv", index=False)
E.to_csv("01_data/stage_events.csv", index=False)

# raw file with deliberate quality issues
R = A.copy()
R["loan_amount"] = R.loan_amount.astype(object)
idx = rng.choice(len(R), 400, replace=False)
R.loc[idx, "loan_amount"] = ["₹" + f"{v:,}" for v in A.loan_amount.iloc[idx]]          # text amounts
idx = rng.choice(len(R), 600, replace=False)
R.loc[idx, "channel"] = [rng.choice([c.lower(), c.upper(), " " + c + " "]) for c in R.channel.iloc[idx]]
R.loc[blank_idx, "employment_type"] = ""
dups = R.sample(250, random_state=7)
R = pd.concat([R, dups]).sample(frac=1, random_state=11).reset_index(drop=True)
R.to_csv("01_data/loan_applications_raw.csv", index=False, encoding="utf-8-sig")   # BOM so Excel shows ₹ correctly
print(len(R), len(A), len(E))
