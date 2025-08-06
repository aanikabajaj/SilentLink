CREATE TABLE IF NOT EXISTS user_keys (
    user_id TEXT PRIMARY KEY,
    identity_keys JSONB NOT NULL,
    one_time_keys JSONB NOT NULL,
    session_pickle TEXT NOT NULL,
    last_rotated TIMESTAMP NOT NULL,
    rotation_count INT DEFAULT 1
);
