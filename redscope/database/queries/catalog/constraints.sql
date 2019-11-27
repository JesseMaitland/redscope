-- gets all column constraints
SELECT ns.nspname as schema_name,
       c.relname  as table_name,
       a.attname  as column_name,
       pg_get_constraintdef(cn.oid) as con_def,
       cn.conname as con_name
  FROM pg_constraint cn
       INNER JOIN pg_namespace ns
          ON ns.oid = cn.connamespace
       INNER JOIN pg_class c
          ON c.oid = cn.conrelid
       INNER JOIN pg_attribute a
          ON a.attnum = ANY(cn.conkey)
             AND a.attrelid = c.oid
