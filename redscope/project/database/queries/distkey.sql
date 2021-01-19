SELECT n.nspname AS schema,
       c.relname AS "table",
      'DISTKEY (' + QUOTE_IDENT(a.attname) + ')' AS ddl
  FROM pg_namespace AS n
       INNER JOIN pg_class AS c ON n.oid = c.relnamespace
       INNER JOIN pg_attribute AS a ON c.oid = a.attrelid
  WHERE c.relkind = 'r'
        AND a.attisdistkey IS TRUE
        AND a.attnum > 0
        AND schema NOT IN ('pg_catalog', 'information_schema');
