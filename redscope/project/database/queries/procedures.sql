SELECT n.nspname AS schema,
       p.proname AS name,
       pg_get_functiondef(prooid) as ddl
  FROM pg_proc_info p
       INNER JOIN pg_namespace n
          ON p.pronamespace = n.oid
 WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
       AND p.prokind = 'p'
