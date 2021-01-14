-- gets all column constraints
SELECT DISTINCT
       ns.nspname as schema,
       c.relname  as "table",
       a.attname  as "column",
       pg_get_constraintdef(cn.oid) as ddl,
       cn.conname as name
  FROM pg_constraint cn
       INNER JOIN pg_namespace ns
          ON ns.oid = cn.connamespace
       INNER JOIN pg_class c
          ON c.oid = cn.conrelid
       INNER JOIN pg_attribute a
          ON a.attnum = ANY(cn.conkey)
             AND a.attrelid = c.oid
