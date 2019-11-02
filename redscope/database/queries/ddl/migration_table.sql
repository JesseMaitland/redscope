CREATE TABLE IF NOT EXISTS redscope.migrations
(
    key        BIGINT PRIMARY KEY NOT NULL,
    name       VARCHAR(30)        NOT NULL,
    sql        VARCHAR(10000)     NULL,
    created_at TIMESTAMP   DEFAULT CURRENT_DATE,
    created_by VARCHAR(50) DEFAULT CURRENT_USER
);
