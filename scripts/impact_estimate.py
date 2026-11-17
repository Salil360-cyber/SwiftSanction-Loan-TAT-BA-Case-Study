"""TO-BE impact estimate for SwiftSanction (6 months of data).
Method: shorten each application's wait by the saving each fix gives, then apply the
withdrawal rates already observed in SQL Q9 to the new wait. No new behaviour is invented."""
import pandas as pd, numpy as np
A = pd.read_csv("01_data/loan_applications_clean.csv", parse_dates=["submitted_at"])
E = pd.read_csv("01_data/stage_events.csv", parse_dates=["start_time"])
FAST_TRACK_HOURS = 4          # assumption: rule-based decision + spot check
REREQ_AVOIDED = 0.5           # assumption: checklist + upload quality check prevents half

# observed withdrawal rate at sanction by days already waited (same as SQL Q9)
s5 = E[E.stage_no == 5][["application_id", "start_time", "outcome"]].merge(A, on="application_id")
d = (s5.start_time - s5.submitted_at).dt.total_seconds() / 86400
bucket = lambda x: np.select([x < 2, x < 4, x < 6], [0, 1, 2], 3)
R = (s5.outcome == "Withdrawn").groupby(bucket(d)).mean().values
rate = lambda x: R[bucket(x)]
# hours one re-request adds (same as SQL Q8: TAT with 1 re-request minus TAT with 0)
D0 = A[A.final_status == "Disbursed"]
REREQ_HOURS = D0[D0.doc_rerequests == 1].tat_hours.mean() - D0[D0.doc_rerequests == 0].tat_hours.mean()
print("Withdrawal rates by days waited (0-2, 2-4, 4-6, 6+):", [f"{r:.1%}" for r in R], f"| one re-request adds {REREQ_HOURS:.1f} h")

uw = E[E.stage_no == 4].set_index("application_id").duration_hours
A["low_risk"] = (A.cibil_band == "750+") & (A.employment_type == "Salaried") & (A.loan_amount <= 500000)
A["save_fast"] = np.where(A.low_risk, (A.application_id.map(uw) - FAST_TRACK_HOURS).clip(lower=0), 0)
A["save_fast"] = A.save_fast.fillna(0)
A["save_doc"] = np.where(A.doc_rerequests > 0, REREQ_HOURS, 0)

s5 = s5.drop(columns=["low_risk", "save_fast", "save_doc"], errors="ignore").merge(
    A[["application_id", "save_fast", "save_doc"]], on="application_id")
base = rate(d).sum()
after_fast = rate(d - s5.save_fast / 24)
after_both_doc = rate(d - (s5.save_fast + s5.save_doc) / 24)
expected = (1 - REREQ_AVOIDED) * after_fast + REREQ_AVOIDED * after_both_doc
saved = base - expected.sum()

D = A[A.final_status == "Disbursed"]
t_fast = D.tat_hours - D.save_fast
sla_now = (D.tat_hours <= 72).mean()
sla_new = ((1 - REREQ_AVOIDED) * (t_fast <= 72) + REREQ_AVOIDED * (t_fast - D.save_doc <= 72)).mean()
tat_new = (t_fast - REREQ_AVOIDED * D.save_doc).mean()
avg_loan = D.loan_amount.mean()
print(f"Low-risk applications: {A.low_risk.sum():,}")
print(f"Expected withdrawals at sanction now: {base:,.0f}  after fixes: {expected.sum():,.0f}  avoided: {saved:,.0f}")
print(f"Average disbursed loan: Rs {avg_loan:,.0f}  extra disbursal: Rs {saved*avg_loan/1e7:,.2f} crore per 6 months")
print(f"Avg TAT: {D.tat_hours.mean():.1f} h -> {tat_new:.1f} h ; within 72h SLA: {sla_now:.1%} -> {sla_new:.1%}")
