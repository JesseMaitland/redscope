SELECT
   n.nspname AS schema,
   c.relname AS "table",
   CASE WHEN c.reldiststyle = 0 THEN 'DISTSTYLE EVEN'
    WHEN c.reldiststyle = 1 THEN 'DISTSTYLE KEY'
    WHEN c.reldiststyle = 8 THEN 'DISTSTYLE ALL'
    WHEN c.reldiststyle = 9 THEN 'DISTSTYLE AUTO'
    ELSE ''
    END AS ddl
  FROM pg_namespace AS n
  INNER JOIN pg_class AS c ON n.oid = c.relnamespace
  WHERE c.relkind = 'r'
        AND schema NOT IN ('pg_catalog', 'information_schema');
