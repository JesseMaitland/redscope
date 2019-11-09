CREATE TABLE IF NOT EXISTS redscope.migrations
(
    key        BIGINT PRIMARY KEY NOT NULL,
    name       VARCHAR(30)        NOT NULL,
    path       VARCHAR(500)       NOT NULL,
    created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT CURRENT_USER
);
