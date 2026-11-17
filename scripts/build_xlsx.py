import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

F = "Arial"
a = pd.read_csv("01_data/loan_applications_clean.csv", keep_default_na=False)
raw_n = len(pd.read_csv("01_data/loan_applications_raw.csv"))
wb = Workbook()
H = Font(name=F, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3864")
B = Font(name=F, bold=True); N = Font(name=F); T = Font(name=F, bold=True, size=14); I = Font(name=F, italic=True)

def hdr(ws, r, vals):
    for i, x in enumerate(vals, 1):
        c = ws.cell(r, i, x); c.font = H; c.fill = HF; c.alignment = Alignment(horizontal="center", wrap_text=True)

def setn(ws, r1, r2, c1, c2):
    for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
        for c in row:
            if c.value is not None and not c.font.bold:
                c.font = N

ws = wb.active; ws.title = "About"
lines = [("SwiftSanction: Personal Loan Turnaround Time (TAT) Analysis", T),
         ("Godavari Finance (fictional) · synthetic data · Jan-Jun 2026", N), ("", N), ("Sheets", B),
         ("Cleaning_Log: what was cleaned in the raw file", N),
         ("Clean_Data: 15,000 cleaned applications (Excel Table 'loans') + 3 formula columns: TAT days, SLA status, low-risk flag", N),
         ("Summary: status, TAT and SLA KPIs (COUNTIF / AVERAGEIFS)", N),
         ("Analysis: re-request, TAT, day-of-week and low-risk tables (COUNTIFS / AVERAGEIFS)", N), ("", N),
         ("SLA = loan disbursed within 72 hours (3 days) of the application.", N),
         ("Stage-level timing (which stage takes longest) is done in SQL on stage_events.csv: see 03_sql.", N)]
for i, (t, f) in enumerate(lines, 1):
    ws.cell(i, 1, t).font = f
ws.column_dimensions["A"].width = 110

cl = wb.create_sheet("Cleaning_Log")
hdr(cl, 1, ["Step", "Issue in loan_applications_raw.csv", "Fix", "Rows affected"])
rows = [(1, "Exact duplicate rows", "Data > Remove Duplicates", 250),
        (2, "Inconsistent channel values (dsa, MOBILE APP, ' Branch ')", "TRIM + PROPER; 'Dsa' fixed to 'DSA'", 555),
        (3, "loan_amount stored as text with ₹ and commas", "SUBSTITUTE to remove ₹ and commas, then VALUE", 400),
        (4, "Blank employment_type", "Go To Special > Blanks > 'Unknown'", 200),
        (5, "Result", f"{raw_n:,} raw rows became 15,000 clean rows", 15000)]
for r, row in enumerate(rows, 2):
    for c, x in enumerate(row, 1):
        cl.cell(r, c, x).font = N
for col, w in zip("ABCD", [8, 55, 50, 15]):
    cl.column_dimensions[col].width = w

cd = wb.create_sheet("Clean_Data")
cols = list(a.columns) + ["tat_days", "sla_status", "low_risk"]
hdr(cd, 1, cols)
for i, r in enumerate(a.itertuples(index=False), 2):
    vals = list(r); vals[14] = float(vals[14]) if vals[14] != "" else None
    cd.append(vals)
    cd.cell(i, 16, f'=IF(O{i}="","",ROUND(O{i}/24,1))')
    cd.cell(i, 17, f'=IF(L{i}<>"Disbursed","Not disbursed",IF(O{i}<=72,"Within SLA","Breached"))')
    cd.cell(i, 18, f'=IF(AND(H{i}="750+",G{i}="Salaried",I{i}<=500000),"Yes","No")')
n = len(a) + 1
tab = Table(displayName="loans", ref=f"A1:R{n}"); tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
cd.add_table(tab)
for i, w in enumerate([13, 17, 10, 12, 12, 9, 15, 11, 12, 9, 28, 11, 28, 10, 10, 9, 14, 9], 1):
    cd.column_dimensions[get_column_letter(i)].width = w
for row in cd.iter_rows(min_row=2, max_row=n, min_col=9, max_col=9):
    row[0].number_format = "#,##0"
cd.freeze_panes = "A2"
C = lambda col: f"Clean_Data!${col}$2:${col}${n}"

su = wb.create_sheet("Summary"); su["A1"] = "Summary KPIs"; su["A1"].font = T
hdr(su, 3, ["Final status", "Applications", "% of total"])
for k, s in enumerate(["Disbursed", "Rejected", "Withdrawn"]):
    r = 4 + k; su.cell(r, 1, s)
    su.cell(r, 2, f'=COUNTIF({C("L")},A{r})').number_format = "#,##0"
    su.cell(r, 3, f"=B{r}/SUM($B$4:$B$6)").number_format = "0.0%"
su.cell(7, 1, "Total").font = B; c = su.cell(7, 2, "=SUM(B4:B6)"); c.font = B; c.number_format = "#,##0"
hdr(su, 9, ["KPI (disbursed loans)", "Value", ""])
kp = [("Average TAT (hours)", f'=AVERAGEIFS({C("O")},{C("L")},"Disbursed")', "0.0"),
      ("Average TAT (days)", "=B10/24", "0.0"),
      ("Disbursed within 72h SLA", f'=COUNTIF({C("Q")},"Within SLA")', "#,##0"),
      ("% within SLA", "=B12/B4", "0.0%"),
      ("Applications with a document re-request", f'=COUNTIF({C("N")},">0")', "#,##0"),
      ("% with a re-request", "=B14/B7", "0.0%")]
for k, (lab, f, nf) in enumerate(kp):
    r = 10 + k; su.cell(r, 1, lab); su.cell(r, 2, f).number_format = nf
setn(su, 4, 15, 1, 3)
for col, w in zip("ABC", [42, 14, 12]):
    su.column_dimensions[col].width = w

an = wb.create_sheet("Analysis"); an["A1"] = "Analysis tables"; an["A1"].font = T
r = 3
def block(title, heads):
    global r
    an.cell(r, 1, title).font = B; r += 1; hdr(an, r, heads); r += 1

def rr_table(title, col, vals):
    global r
    block(title, ["Value", "Applications", "With re-request", "Re-request %"])
    for s in vals:
        an.cell(r, 1, s)
        an.cell(r, 2, f'=COUNTIF({C(col)},A{r})').number_format = "#,##0"
        an.cell(r, 3, f'=COUNTIFS({C(col)},A{r},{C("N")},">0")').number_format = "#,##0"
        an.cell(r, 4, f"=C{r}/B{r}").number_format = "0.0%"; r += 1
    r += 1
rr_table("1. Document re-request rate by channel", "D", ["DSA", "Website", "Mobile App", "Branch"])
rr_table("2. Document re-request rate by employment type", "G", ["Self-employed", "Salaried", "Unknown"])

block("3. TAT by number of document re-requests (disbursed)", ["Re-requests", "Disbursed", "Avg TAT (h)", "Avg TAT (days)"])
for k in [0, 1, 2]:
    an.cell(r, 1, k)
    an.cell(r, 2, f'=COUNTIFS({C("N")},A{r},{C("L")},"Disbursed")').number_format = "#,##0"
    an.cell(r, 3, f'=AVERAGEIFS({C("O")},{C("N")},A{r},{C("L")},"Disbursed")').number_format = "0.0"
    an.cell(r, 4, f"=C{r}/24").number_format = "0.0"; r += 1
r += 1
block("4. TAT by day the application was submitted (disbursed)", ["Day", "Disbursed", "Avg TAT (h)", "% within SLA"])
day_start = r
for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
    an.cell(r, 1, d)
    an.cell(r, 2, f'=COUNTIFS({C("C")},A{r},{C("L")},"Disbursed")').number_format = "#,##0"
    an.cell(r, 3, f'=AVERAGEIFS({C("O")},{C("C")},A{r},{C("L")},"Disbursed")').number_format = "0.0"
    an.cell(r, 4, f'=COUNTIFS({C("C")},A{r},{C("Q")},"Within SLA")/B{r}').number_format = "0.0%"; r += 1
r += 1
block("5. Low-risk applications (CIBIL 750+, salaried, loan up to Rs 5 lakh)", ["Low risk", "Applications", "Rejected", "Reject %"])
for s in ["Yes", "No"]:
    an.cell(r, 1, s)
    an.cell(r, 2, f'=COUNTIF({C("R")},A{r})').number_format = "#,##0"
    an.cell(r, 3, f'=COUNTIFS({C("R")},A{r},{C("L")},"Rejected")').number_format = "#,##0"
    an.cell(r, 4, f"=C{r}/B{r}").number_format = "0.0%"; r += 1
setn(an, 3, r, 1, 4)
for col, w in zip("ABCD", [34, 14, 16, 14]):
    an.column_dimensions[col].width = w
ch = BarChart(); ch.type = "col"; ch.title = "Average TAT (hours) by submission day"; ch.style = 10
ch.add_data(Reference(an, min_col=3, min_row=day_start - 1, max_row=day_start + 6), titles_from_data=True)
ch.set_categories(Reference(an, min_col=1, min_row=day_start, max_row=day_start + 6))
ch.legend = None; ch.height = 8; ch.width = 15
ch.roundedCorners = False; ch.x_axis.delete = False; ch.y_axis.delete = False; ch.title.overlay = False
an.add_chart(ch, "F3")
wb.save("02_excel/SwiftSanction_Analysis.xlsx"); print("saved")
