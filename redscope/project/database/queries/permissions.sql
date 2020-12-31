SELECT relname as table_name,
       ns.nspname as schema_name,
       relacl as perms
  FROM pg_class c
       INNER JOIN pg_namespace ns
          ON c.relnamespace = ns.oid
 WHERE relname IN ('jobs', 'job_slots', 'companies')
ORDER BY table_name, schema_name
