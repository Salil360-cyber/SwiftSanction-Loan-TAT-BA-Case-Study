"""Builds 06_project_plan/SwiftSanction_Project_Plan.xlsx: schedule with forward/backward pass formulas,
Gantt, RAID log and status summary. Every date and float is an Excel formula."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter as L

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3864")
N = Font(name=F); B = Font(name=F, bold=True); T = Font(name=F, bold=True, size=14); I = Font(name=F, italic=True, color="555555")
BLUE = Font(name=F, color="0000FF")
START = dt.date(2027, 1, 4); STATUS_DATE = dt.date(2027, 2, 12)

TASKS = [  # id, task, owner, duration (working days), predecessors, % complete at status date
 ("1.1", "Project charter and sponsor sign-off", "Business Analyst", 3, [], 100),
 ("1.2", "Stakeholder kick-off meeting", "Project lead", 1, ["1.1"], 100),
 ("2.1", "Final BRD and fast-track rules sign-off (Credit Risk)", "Business Analyst", 5, ["1.2"], 100),
 ("2.2", "Backlog, estimates and sprint plan", "Project lead", 3, ["1.2"], 100),
 ("2.3", "Test strategy and UAT plan", "QA lead", 3, ["2.1"], 100),
 ("3.1", "Sprint 1: document checklist (BR-01)", "IT / LOS team", 10, ["2.1", "2.2"], 100),
 ("3.2", "Sprint 2: upload quality check + DSA portal (BR-02)", "IT / LOS team", 10, ["3.1"], 70),
 ("3.3", "Sprint 3: fast-track underwriting lane (BR-03)", "IT / LOS team", 10, ["3.2"], 0),
 ("3.4", "Daily TAT / SLA report and alerts (BR-04)", "MIS / Business Analyst", 8, ["2.1"], 100),
 ("4.1", "User acceptance testing (13 test cases)", "Operations + QA", 7, ["3.3", "3.4", "2.3"], 0),
 ("4.2", "Training for ops staff and DSAs", "Operations manager", 3, ["3.3"], 0),
 ("4.3", "Go-live", "IT / LOS team", 1, ["4.1", "4.2"], 0),
 ("5.1", "Hypercare and benefits tracking (4 weeks)", "Business Analyst", 20, ["4.3"], 0),
 ("5.2", "Closure and lessons learned", "Project lead", 2, ["5.1"], 0),
]

def hdr(ws, r, vals):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = H; c.fill = HF; c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()
ab = wb.active; ab.title = "About"
for i, (t, f) in enumerate([
    ("SwiftSanction: Implementation Project Plan", T),
    ("Godavari Finance (fictional) · delivering the Must-have requirements BR-01 to BR-04 from the BRD", N), ("", N),
    ("Sheets", B),
    ("Schedule: tasks, owners, durations and dependencies; start, finish, late dates and float are WORKDAY / NETWORKDAYS formulas (forward and backward pass)", N),
    ("Gantt: weekly bars drawn by conditional formatting from the Schedule dates; critical-path tasks in dark blue", N),
    ("RAID_Log: risks, assumptions, issues and dependencies with owner, score (probability x impact) and RAG", N),
    ("Status: progress as of the status date, read by the weekly status report (06_project_plan/04_status_report_week6.md)", N), ("", N),
    ("Inputs in blue: project start date, durations, % complete, probability and impact. Everything else is calculated.", N),
    ("Working days are Monday to Friday; public holidays are not modelled.", I)], 1):
    ab.cell(i, 1, t).font = f
ab.column_dimensions["A"].width = 120

sc = wb.create_sheet("Schedule")
sc["A1"] = "Schedule"; sc["A1"].font = T
sc["A2"] = "Project start"; sc["A2"].font = B
sc["B2"] = START; sc["B2"].number_format = "dd-mmm-yyyy"; sc["B2"].font = BLUE
sc["D2"] = "Status date"; sc["D2"].font = B
sc["E2"] = STATUS_DATE; sc["E2"].number_format = "dd-mmm-yyyy"; sc["E2"].font = BLUE
heads = ["ID", "Task", "Owner", "Predecessors", "Duration (working days)", "Early start", "Early finish",
         "Late start", "Late finish", "Float (days)", "Critical path", "% complete", "Status"]
hdr(sc, 4, heads)
row = {t[0]: 5 + k for k, t in enumerate(TASKS)}
last = 4 + len(TASKS)
succ = {t[0]: [s[0] for s in TASKS if t[0] in s[4]] for t in TASKS}
for k, (tid, name, own, dur, pred, pct) in enumerate(TASKS):
    r = 5 + k
    sc.cell(r, 1, tid); sc.cell(r, 2, name); sc.cell(r, 3, own); sc.cell(r, 4, ", ".join(pred) or "-")
    c = sc.cell(r, 5, dur); c.font = BLUE
    sc.cell(r, 6, "=$B$2" if not pred else "=WORKDAY(MAX(" + ",".join(f"G{row[p]}" for p in pred) + "),1)")
    sc.cell(r, 7, f"=WORKDAY(F{r},E{r}-1)")
    sc.cell(r, 9, f"=MAX($G$5:$G${last})" if not succ[tid] else "=WORKDAY(MIN(" + ",".join(f"H{row[s]}" for s in succ[tid]) + "),-1)")
    sc.cell(r, 8, f"=WORKDAY(I{r},-(E{r}-1))")
    sc.cell(r, 10, f"=NETWORKDAYS(G{r},I{r})-1")
    sc.cell(r, 11, f'=IF(J{r}=0,"Yes","No")')
    c = sc.cell(r, 12, pct / 100); c.font = BLUE; c.number_format = "0%"
    sc.cell(r, 13, f'=IF(L{r}=1,"Done",IF(AND(G{r}<$E$2,L{r}<1),"Late",IF(L{r}>0,"In progress",IF(F{r}<=$E$2,"Should have started","Not started"))))')
    for col in (6, 7, 8, 9):
        sc.cell(r, col).number_format = "dd-mmm-yy"
    for col in range(1, 14):
        if sc.cell(r, col).font != BLUE:
            sc.cell(r, col).font = N if col not in (5, 12) else BLUE
sc.cell(last + 2, 1, "Project finish").font = B
c = sc.cell(last + 2, 6, f"=MAX(G5:G{last})"); c.number_format = "dd-mmm-yyyy"; c.font = B
sc.cell(last + 3, 1, "Go-live").font = B
c = sc.cell(last + 3, 6, f"=F{row['4.3']}"); c.number_format = "dd-mmm-yyyy"; c.font = B
sc.cell(last + 4, 1, "Critical path length (working days)").font = B
c = sc.cell(last + 4, 6, f'=SUMIF(K5:K{last},"Yes",E5:E{last})'); c.font = B
sc.cell(last + 6, 1, "Late start / late finish come from a backward pass from the project finish; float = days a task can slip without moving the finish. Float 0 = critical path.").font = I
for col, w in zip("ABCDEFGHIJKLM", [6, 48, 22, 13, 12, 12, 12, 12, 12, 9, 9, 10, 18]):
    sc.column_dimensions[col].width = w
sc.freeze_panes = "C5"

gt = wb.create_sheet("Gantt")
gt["A1"] = "Gantt chart (weeks starting Monday)"; gt["A1"].font = T
hdr(gt, 3, ["ID", "Task"])
weeks = 15
for w in range(weeks):
    col = 3 + w
    c = gt.cell(3, col, f"=Schedule!$B$2+{7 * w}"); c.number_format = "dd-mmm"; c.font = H; c.fill = HF
    c.alignment = Alignment(horizontal="center", text_rotation=90)
    gt.column_dimensions[L(col)].width = 4.2
gt.row_dimensions[3].height = 48
for k, t in enumerate(TASKS):
    r = 4 + k; sr = 5 + k
    gt.cell(r, 1, f"=Schedule!A{sr}").font = N; gt.cell(r, 2, f"=Schedule!B{sr}").font = N
gt.column_dimensions["A"].width = 6; gt.column_dimensions["B"].width = 48
rng = f"C4:{L(2 + weeks)}{3 + len(TASKS)}"
crit = 'AND(C$3<=INDEX(Schedule!$G$5:$G$18,ROW()-3),C$3+4>=INDEX(Schedule!$F$5:$F$18,ROW()-3),INDEX(Schedule!$K$5:$K$18,ROW()-3)="Yes")'
norm = 'AND(C$3<=INDEX(Schedule!$G$5:$G$18,ROW()-3),C$3+4>=INDEX(Schedule!$F$5:$F$18,ROW()-3))'
gt.conditional_formatting.add(rng, FormulaRule(formula=[crit], fill=PatternFill("solid", fgColor="1F3864"), stopIfTrue=True))
gt.conditional_formatting.add(rng, FormulaRule(formula=[norm], fill=PatternFill("solid", fgColor="9DB4D6")))
gt.cell(5 + len(TASKS), 2, "Dark blue = critical path · light blue = has float").font = I
gt.freeze_panes = "C4"

rd = wb.create_sheet("RAID_Log")
rd["A1"] = "RAID log"; rd["A1"].font = T
hdr(rd, 3, ["ID", "Type", "Description", "Owner", "Probability (1-5)", "Impact (1-5)", "Score", "RAG", "Response / action", "Status", "Due"])
RAID = [
 ("R1", "Risk", "Credit Risk does not approve the fast-track rules in time for sprint 3", "Business Analyst", 3, 5, "Share the data early (low-risk reject rate 3.5%); rules workshop in week 2", "Closed", "2027-01-14"),
 ("R2", "Risk", "Vendor upload-check API is not ready for sprint 2", "IT lead", 3, 4, "Ask for sandbox access by week 3; fallback: basic size and resolution check", "Occurred (see I1)", "2027-01-25"),
 ("R3", "Risk", "DSAs keep sending incomplete files after go-live", "DSA channel manager", 4, 3, "Training before go-live; monthly re-request scorecard per DSA", "Open", "2027-03-02"),
 ("R4", "Risk", "Fast-track lane approves a loan that later defaults", "Credit Risk head", 2, 5, "10% daily spot check; monthly review of fast-track defaults", "Open", "2027-03-09"),
 ("R5", "Risk", "Ops staff keep using the old manual checks", "Operations manager", 3, 3, "Involve ops in UAT; short training and cheat sheet", "Open", "2027-03-02"),
 ("A1", "Assumption", "The loan system can route files by rule without a new platform", "IT lead", None, None, "Confirmed in sprint planning", "Closed", "2027-01-12"),
 ("A2", "Assumption", "Applicants' phone cameras give readable uploads", "Business Analyst", None, None, "Check with UAT samples", "Open", "2027-03-08"),
 ("A3", "Assumption", "Phase 1 budget of Rs 18 lakh is approved (illustrative)", "Sponsor", None, None, "Confirmed in charter sign-off", "Closed", "2027-01-06"),
 ("I1", "Issue", "Upload-check API access arrived 4 days late; sprint 2 is behind and it is on the critical path", "IT lead", 5, 4, "Proposed: release BR-02 for app and web on time; move the DSA portal piece after go-live (sponsor decision due 15 Feb)", "Open", "2027-02-15"),
 ("D1", "Dependency", "Credit Risk sign-off (task 2.1) is needed before sprint 3 builds the rules", "Business Analyst", None, None, "Signed off 14 Jan", "Closed", "2027-01-14"),
 ("D2", "Dependency", "Vendor API for document quality checks (BR-02)", "IT lead", None, None, "Linked to I1", "Open", "2027-02-15"),
 ("D3", "Dependency", "Read access to loan-system stage data for the TAT report (BR-04)", "IT database admin", None, None, "Granted 18 Jan", "Closed", "2027-01-18"),
]
for k, (rid, typ, desc, own, p, im, resp, st, due) in enumerate(RAID):
    r = 4 + k
    vals = [rid, typ, desc, own, p, im]
    for c, v in enumerate(vals, 1):
        cell = rd.cell(r, c, v); cell.font = BLUE if c in (5, 6) else N
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    rd.cell(r, 7, f'=IF(E{r}="","",E{r}*F{r})').font = N
    rd.cell(r, 8, f'=IF(G{r}="","",IF(G{r}>=15,"Red",IF(G{r}>=8,"Amber","Green")))').font = N
    for c, v in ((9, resp), (10, st)):
        cell = rd.cell(r, c, v); cell.font = N; cell.alignment = Alignment(wrap_text=True, vertical="top")
    cell = rd.cell(r, 11, dt.date.fromisoformat(due)); cell.number_format = "dd-mmm-yy"; cell.font = N
red_rng = f"H4:H{3 + len(RAID)}"
rd.conditional_formatting.add(red_rng, FormulaRule(formula=['H4="Red"'], fill=PatternFill("solid", fgColor="F4CCCC")))
rd.conditional_formatting.add(red_rng, FormulaRule(formula=['H4="Amber"'], fill=PatternFill("solid", fgColor="FCE5CD")))
rd.conditional_formatting.add(red_rng, FormulaRule(formula=['H4="Green"'], fill=PatternFill("solid", fgColor="D9EAD3")))
for col, w in zip("ABCDEFGHIJK", [5, 12, 52, 20, 12, 10, 8, 8, 52, 16, 11]):
    rd.column_dimensions[col].width = w
rd.cell(5 + len(RAID), 1, "Score = probability x impact. RAG: 15+ Red, 8-14 Amber, below 8 Green. Assumptions and dependencies are tracked by status, not scored.").font = I

st = wb.create_sheet("Status")
st["A1"] = "Status as of the status date"; st["A1"].font = T
S = lambda c: f"Schedule!${c}$5:${c}${last}"
rows = [
 ("Status date", "=Schedule!E2", "dd-mmm-yyyy"),
 ("Tasks done", f'=COUNTIF({S("M")},"Done")', "0"),
 ("Tasks late", f'=COUNTIF({S("M")},"Late")', "0"),
 ("Overall % complete (weighted by duration)", f'=SUMPRODUCT({S("E")},{S("L")})/SUM({S("E")})', "0%"),
 ("Late tasks on the critical path", f'=COUNTIFS({S("M")},"Late",{S("K")},"Yes")', "0"),
 ("Open risks scored Amber or Red", f'=COUNTIFS(RAID_Log!$B$4:$B$15,"Risk",RAID_Log!$J$4:$J$15,"Open",RAID_Log!$G$4:$G$15,">=8")', "0"),
 ("Open issues", f'=COUNTIFS(RAID_Log!$B$4:$B$15,"Issue",RAID_Log!$J$4:$J$15,"Open")', "0"),
 ("Planned go-live", "=Schedule!F" + str(last + 3), "dd-mmm-yyyy"),
 ("Overall RAG", '=IF(B7>0,IF(B9>0,"Amber","Red"),IF(B6>0,"Amber","Green"))', "@"),
]
hdr(st, 3, ["Measure", "Value"])
for k, (lab, f, nf) in enumerate(rows):
    r = 4 + k
    st.cell(r, 1, lab).font = N
    c = st.cell(r, 2, f); c.number_format = nf; c.font = B if lab == "Overall RAG" else N
st.cell(14, 1, "Overall RAG rule: a late critical-path task with an open issue and recovery plan = Amber; late critical task without one = Red; other late tasks = Amber; else Green.").font = I
st.column_dimensions["A"].width = 46; st.column_dimensions["B"].width = 16
wb.save("06_project_plan/SwiftSanction_Project_Plan.xlsx"); print("saved")
