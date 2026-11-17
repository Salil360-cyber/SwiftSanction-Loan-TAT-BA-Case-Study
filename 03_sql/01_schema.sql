-- SwiftSanction: PostgreSQL schema
DROP TABLE IF EXISTS stage_events;
DROP TABLE IF EXISTS loan_applications;

CREATE TABLE loan_applications (
    application_id   VARCHAR(10) PRIMARY KEY,
    submitted_at     TIMESTAMP NOT NULL,
    submit_day       VARCHAR(3),
    channel          VARCHAR(15),
    branch_city      VARCHAR(20),
    city_tier        VARCHAR(10),
    employment_type  VARCHAR(15),
    cibil_band       VARCHAR(12),
    loan_amount      INTEGER,
    last_stage_no    SMALLINT,
    last_stage_name  VARCHAR(40),
    final_status     VARCHAR(12),
    close_reason     VARCHAR(40),
    doc_rerequests   SMALLINT,
    tat_hours        NUMERIC(7,1)      -- only for Disbursed loans
);

CREATE TABLE stage_events (
    event_id        VARCHAR(10) PRIMARY KEY,
    application_id  VARCHAR(10) REFERENCES loan_applications(application_id),
    stage_no        SMALLINT,
    stage_name      VARCHAR(40),
    attempt_no      SMALLINT,
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    outcome         VARCHAR(15),       -- Passed / Re-requested / Rejected / Withdrawn
    issue           VARCHAR(40),
    duration_hours  NUMERIC(7,1)
);
