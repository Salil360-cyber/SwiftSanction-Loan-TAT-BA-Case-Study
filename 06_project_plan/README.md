# 06_project_plan

The BRD says **what** to change; this folder plans **how and when** it gets delivered: phase 1 of SwiftSanction (BR-01 to BR-04) as a 14-task project from 4 Jan to 8 Apr 2027. Dates, team and budget are simulated.

| File | What it shows | PM skill |
| --- | --- | --- |
| [01_project_charter.md](01_project_charter.md) | Goal, scope, milestones, team, budget, top risks | Initiation |
| [SwiftSanction_Project_Plan.xlsx](SwiftSanction_Project_Plan.xlsx) | Schedule with forward and backward pass (`WORKDAY`, `NETWORKDAYS`), float and critical path; Gantt by conditional formatting; RAID log with scores and RAG; status summary | Planning, scheduling, risk |
| [03_sprint_backlog_jira.csv](03_sprint_backlog_jira.csv) | 15 backlog items, story points, 3 sprints of 19-20 points; imports into Jira (Issues > Import from CSV) | Agile / Scrum, Jira |
| [04_status_report_week6.md](04_status_report_week6.md) | Week-6 AMBER report: a late critical-path sprint, two recovery options, decision needed | Monitoring, escalation |

## Key numbers

| | |
| --- | --- |
| Tasks | 14, in 5 phases |
| Critical path | 69 working days: charter → kick-off → BRD sign-off → sprints 1-3 → UAT → go-live → hypercare → closure |
| Go-live | 9 Mar 2027 |
| Float | Backlog planning 2 days, training 4, TAT report 22, UAT plan 27 |
| RAID log | 5 risks, 3 assumptions, 1 issue, 3 dependencies |
| Week-6 status | 47% complete, 1 late critical task, AMBER |

## How to read the schedule

- **Early start** = the next working day after the latest predecessor finishes; **early finish** = start + duration − 1 working day.
- **Late finish / late start** come from a backward pass from the project finish.
- **Float** = how many days a task can slip without moving the finish. Float 0 = critical path (dark blue in the Gantt).
- Change any blue input (start date, a duration, % complete) and every date, the Gantt and the status update.
