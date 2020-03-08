CREATE TABLE IF NOT EXISTS redscope.migrations
(
    id         BIGINT IDENTITY(1, 1) PRIMARY KEY NOT NULL,
    key        BIGINT             NOT NULL,
    name       VARCHAR(30)        NOT NULL,
    path       VARCHAR(500)       NOT NULL,
    last_state VARCHAR(25),
    sql        VARCHAR(MAX),
    created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT CURRENT_USER
);
