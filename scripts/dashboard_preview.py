"""Static preview of the 2-page Power BI design, drawn from the same CSVs (numbers match SQL)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
A = pd.read_csv("01_data/loan_applications_clean.csv", parse_dates=["submitted_at"])
E = pd.read_csv("01_data/stage_events.csv", parse_dates=["start_time", "end_time"])
D = A[A.final_status == "Disbursed"]
INK, MUTED, GRID, BAR, KEY, BG = "#1b1f24", "#5b6470", "#e6e8eb", "#9db4d6", "#1f4e9a", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})

def card(ax, label, value):
    ax.axis("off"); ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#f3f5f8"))
    ax.text(.06, .62, value, fontsize=22, weight="bold", color=INK, transform=ax.transAxes)
    ax.text(.06, .22, label, fontsize=10, color=MUTED, transform=ax.transAxes)

def hbar(ax, labels, vals, title, fmt, key=None):
    y = np.arange(len(vals))
    cols = [KEY if (key is not None and i == key) else BAR for i in range(len(vals))]
    ax.barh(y, vals, color=cols, height=.6); ax.set_yticks(y, labels); ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v, i, " " + fmt.format(v), va="center", color=INK, fontsize=9)
    ax.set_title(title, loc="left", color=INK, fontsize=11, weight="bold"); ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)
    ax.set_xlim(0, max(vals) * 1.2)

def vbar(ax, labels, vals, title, fmt, key=None):
    x = np.arange(len(vals))
    cols = [KEY if (key is not None and i in key) else BAR for i in range(len(vals))]
    ax.bar(x, vals, color=cols, width=.6); ax.set_xticks(x, labels)
    for i, v in enumerate(vals):
        ax.text(i, v, fmt.format(v), ha="center", va="bottom", color=INK, fontsize=9)
    ax.set_title(title, loc="left", color=INK, fontsize=11, weight="bold"); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
    ax.set_ylim(0, max(vals) * 1.2)

def page(title):
    fig = plt.figure(figsize=(16, 9), facecolor=BG)
    fig.text(.03, .955, title, fontsize=18, weight="bold", color=INK)
    fig.text(.03, .925, "SwiftSanction · Godavari Finance (fictional) · personal loans, Jan-Jun 2026 · SLA = disbursed within 72 hours",
             fontsize=10, color=MUTED)
    return fig

# Page 1
fig = page("Loan TAT & SLA overview")
kp = [("Applications", f"{len(A):,}"), ("Disbursed", f"{len(D):,}"), ("Average TAT", f"{D.tat_hours.mean()/24:.1f} days"),
      ("Disbursed within SLA", f"{(D.tat_hours<=72).mean():.1%}")]
for i, (l, v) in enumerate(kp):
    card(fig.add_axes([.03 + i * .24, .76, .22, .12]), l, v)
g = E[E.application_id.isin(D.application_id)].groupby(["application_id", "stage_no", "stage_name"]).agg(s=("start_time", "min"), e=("end_time", "max")).reset_index()
g["h"] = (g.e - g.s).dt.total_seconds() / 3600
st = g.groupby(["stage_no", "stage_name"]).h.mean().reset_index()
hbar(fig.add_axes([.17, .40, .32, .30]), st.stage_name, st.h.round(1), "Average hours per stage (disbursed loans)", "{:.1f} h", key=int(st.h.idxmax()))
stt = A.final_status.value_counts()
hbar(fig.add_axes([.62, .40, .33, .30]), stt.index, stt.values, "How applications end", "{:,}")
mo = D.groupby(D.submitted_at.dt.month).tat_hours.apply(lambda x: (x <= 72).mean() * 100)
mo.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
vbar(fig.add_axes([.05, .07, .42, .24]), mo.index, mo.values.round(1), "% disbursed within SLA by month", "{:.1f}%")
dy = D.groupby("submit_day").tat_hours.apply(lambda x: (x <= 72).mean() * 100).reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
vbar(fig.add_axes([.55, .07, .42, .24]), dy.index, dy.values.round(1), "% within SLA by day the application was submitted", "{:.1f}%", key=[4, 5])
fig.savefig("04_powerbi/screenshots/page1_tat_overview.png", dpi=100); plt.close(fig)

# Page 2
fig = page("Root cause: re-requests, underwriting and lost customers")
ch = A.groupby("channel").doc_rerequests.apply(lambda x: (x > 0).mean() * 100).sort_values(ascending=False)
hbar(fig.add_axes([.10, .55, .34, .30]), ch.index, ch.values.round(1), "Document re-request % by channel", "{:.1f}%", key=0)
iss = E[E.outcome == "Re-requested"].issue.value_counts()
hbar(fig.add_axes([.62, .55, .33, .30]), iss.index, iss.values, "Why documents are re-requested", "{:,}", key=0)
s5 = E[E.stage_no == 5].merge(A[["application_id", "submitted_at"]], on="application_id")
dw = (s5.start_time - s5.submitted_at).dt.total_seconds() / 86400
b = pd.Series(np.select([dw < 2, dw < 4, dw < 6], ["0-2 days", "2-4 days", "4-6 days"], "6+ days"))
wd = (s5.outcome == "Withdrawn").groupby(b.values).mean() * 100
vbar(fig.add_axes([.05, .08, .40, .32]), wd.index, wd.values.round(1), "Customers who withdraw at sanction, by days already waited", "{:.1f}%", key=[3])
u = E[E.stage_no == 4].merge(A, on="application_id")
low = np.where((u.cibil_band == "750+") & (u.employment_type == "Salaried") & (u.loan_amount <= 500000), "Low risk", "Others")
uh = u.groupby(low).duration_hours.mean()
vbar(fig.add_axes([.55, .08, .19, .32]), uh.index, uh.values.round(1), "Underwriting hours", "{:.1f} h")
ur = (u.outcome == "Rejected").groupby(low).mean() * 100
vbar(fig.add_axes([.79, .08, .18, .32]), ur.index, ur.values.round(1), "Underwriting reject %", "{:.1f}%")
fig.savefig("04_powerbi/screenshots/page2_root_cause.png", dpi=100); plt.close(fig)
print("ok")
