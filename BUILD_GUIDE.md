# Build guide

Build the Excel, SQL and Power BI parts yourself, then compare your numbers with the **expected values** given at each step.

## Part A: Excel (start from `01_data/loan_applications_raw.csv`)

**A1. Open and save**
1. Open the CSV in Excel → File > Save As → `SwiftSanction_Analysis.xlsx` (Excel Workbook).
2. Rename the sheet `Raw_Data`. Right-click the tab > Move or Copy > tick Create a copy → rename the copy `Clean_Data`. Work only on `Clean_Data`.

**A2. Remove duplicates**
1. Click any cell in the data → Data > Remove Duplicates → Select All → OK.
2. Expected: **250** duplicates removed, **15,000** rows remain.

**A3. Fix `channel`**
1. Insert a new column next to `channel` named `channel_clean`.
2. Formula: `=PROPER(TRIM(D2))` and double-click the fill handle.
3. `PROPER` turns "DSA" into "Dsa": Ctrl+H on the new column, Find `Dsa`, Replace `DSA`, Options > tick Match entire cell contents > Replace All.
4. Copy the column → Paste Special > Values over `channel`, then delete `channel_clean`.
5. Check: filter `channel` shows only Mobile App, Website, Branch, DSA. (**555** values were fixed.)

**A4. Fix `loan_amount`**
1. New column `amount_clean`: `=VALUE(SUBSTITUTE(SUBSTITUTE(I2,UNICHAR(8377),""),",",""))` (`UNICHAR(8377)` is the ₹ sign, so you do not have to type it).
2. Paste as values over `loan_amount`, delete the helper column, format as Number with 1000 separator. (**400** text amounts fixed.)

**A5. Fill blank `employment_type`**
1. Select the `employment_type` column → Home > Find & Select > Go To Special > Blanks → OK.
2. Type `Unknown` and press **Ctrl+Enter**. (**200** blanks.)

**A6. Make it a Table and add formula columns**
1. Click inside the data → Ctrl+T → My table has headers → OK. Table Design > Table Name: `loans`.
2. Add three columns at the right:
   - `tat_days`: `=IF([@tat_hours]="","",ROUND([@tat_hours]/24,1))`
   - `sla_status`: `=IF([@final_status]<>"Disbursed","Not disbursed",IF([@tat_hours]<=72,"Within SLA","Breached"))`
   - `low_risk`: `=IF(AND([@cibil_band]="750+",[@employment_type]="Salaried",[@loan_amount]<=500000),"Yes","No")`
3. Add a `Cleaning_Log` sheet listing the 4 fixes and row counts above.

**A7. Summary sheet (formulas)**

| Cell | Formula | Expected |
| --- | --- | --- |
| Disbursed | `=COUNTIF(loans[final_status],"Disbursed")` | 9,914 |
| Rejected | `=COUNTIF(loans[final_status],"Rejected")` | 3,382 |
| Withdrawn | `=COUNTIF(loans[final_status],"Withdrawn")` | 1,704 |
| Avg TAT (hours) | `=AVERAGEIFS(loans[tat_hours],loans[final_status],"Disbursed")` | 104.2 |
| Within SLA | `=COUNTIF(loans[sla_status],"Within SLA")` | 2,290 |
| % within SLA | Within SLA / Disbursed | 23.1% |
| % with re-request | `=COUNTIF(loans[doc_rerequests],">0")/15000` | 21.5% |

**A8. Pivot tables (Insert > PivotTable > From table `loans` > New sheet `Analysis`)**
1. Re-request by channel: first add a column `has_rerequest` to the table: `=IF([@doc_rerequests]>0,1,0)`. In the pivot: Rows `channel`; Values Average of `has_rerequest`, formatted as %. Expected: DSA **33.8%**, Website 23.9%, Mobile App 20.0%, Branch **12.3%**.
2. TAT by re-requests: Filter `final_status` = Disbursed; Rows `doc_rerequests`; Values Average of `tat_hours`. Expected: 0 → **93.3**, 1 → **139.9**, 2 → **185.9**.
3. SLA by day: Filter Disbursed; Rows `submit_day`; Columns `sla_status`; Values Count, Show Values As > % of Row Total. Expected: Sat **5.0%**, Fri **6.8%** within SLA.
4. Low risk: Rows `low_risk`; Columns `final_status`; Values Count, Show Values As > % of Row Total. Expected Rejected (any stage): Yes **5.2%**, No **27.8%**. (SQL Q10 shows the underwriting stage only: 3.5% vs 15.3%.)
5. Insert > Column chart from the SLA-by-day pivot. Add a title.

## Part B: SQL (pgAdmin 4)

1. Create database `swiftsanction`.
2. Query Tool → open and run `03_sql/01_schema.sql`.
3. Right-click `loan_applications` > Import/Export Data → Import → file `loan_applications_clean.csv` → Options: Header ON, Delimiter `,`, NULL Strings empty → OK. Repeat for `stage_events` with `stage_events.csv`.
4. Expected counts: **15,000** and **67,346**.
5. Run each query in `03_analysis.sql` one by one and compare with `results.md`. For each one, write in your own words what business question it answers.

## Part C: Power BI Desktop

Follow [`04_powerbi/DAX_measures.md`](04_powerbi/DAX_measures.md): load, Power Query `stage_time` table, relationships, calculated columns, measures.

**Page 1: TAT & SLA overview**
1. 4 Card visuals: Applications, Disbursed, Avg TAT (days), SLA %.
2. Clustered bar: Y-axis `stage_time[stage_name]`, X-axis `Avg Stage Hours`. Sort by `stage_no`.
3. Clustered bar: Y-axis `loans[final_status]`, X-axis `Applications`.
4. Column chart: X-axis month of `submitted_at`, Y-axis `SLA %`.
5. Column chart: X-axis `submit_day` (sorted by `Day No`), Y-axis `SLA %`.
6. Slicers: `channel`, `employment_type`, `city_tier` in one row at the top.

**Page 2: Root cause**
1. Bar: `channel` vs `Re-request %`.
2. Bar: `events[issue]` vs count of `events[event_id]`, with a visual filter `outcome` = Re-requested.
3. Underwriting: bar of `Low Risk` vs average of `events[duration_hours]` (visual filter `stage_no` = 4).
4. Withdrawal by days waited: use SQL Q9 results as a small table, or add a Power Query step on `events` (stage 5 rows, merge `submitted_at`, add `days_waited` and a bucket column).

Check your cards against the expected values, then File > Save as `SwiftSanction_Dashboard.pbix` and add it to `04_powerbi/`.
