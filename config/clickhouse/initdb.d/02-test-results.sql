USE coagent;

CREATE TABLE IF NOT EXISTS test_results (
    created_at DateTime64(3) DEFAULT now64(3),
    job_id Int64,
    session_id String,
    event_id String,
    trigger_pattern Nullable(String),
    has_trigger_value Bool,
    success Bool,
    test_results JSON,
    test_case_ids Array(String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (session_id, created_at, job_id);
