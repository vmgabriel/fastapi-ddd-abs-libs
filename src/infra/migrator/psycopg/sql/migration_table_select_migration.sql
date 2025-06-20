CREATE TABLE IF NOT EXISTS migration
(
    id         SERIAL PRIMARY KEY,
    file_name  VARCHAR(200) NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT NOW()
);