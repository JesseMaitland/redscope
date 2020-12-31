SELECT nspname AS schema,
       NULL::VARCHAR AS name,
       pg_get_userbyid(nspowner) as owner,
       NULL::VARCHAR AS signature,
       'schema' AS db_obj_type
  FROM pg_namespace
 WHERE nspname NOT IN ('pg_toast', 'pg_internal', 'pg_catalog')
       AND nspname NOT LIKE 'pg_temp_%'

UNION ALL

SELECT schemaname,
       tablename,
       tableowner,
       NULL::VARCHAR,
       'table'
  FROM pg_tables
 WHERE schemaname NOT IN ('pg_catalog', 'information_schema')

UNION ALL

SELECT schemaname,
       viewname,
       viewowner,
       NULL::VARCHAR,
       'view'
  FROM pg_views
 WHERE schemaname NOT IN ('pg_catalog', 'information_schema')

UNION ALL

SELECT n.nspname,
       p.proname,
       pg_get_userbyid(proowner),
       '(' || oidvectortypes(proargtypes) || ')',
       CASE prokind WHEN 'f' THEN 'function'
                    WHEN 'p' THEN 'procedure'
                    WHEN 'a' THEN 'aggregate'
                    END
  FROM pg_proc_info p
       INNER JOIN pg_namespace n
          ON p.pronamespace = n.oid
 WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
       AND p.prokind IN ('f', 'p', 'a')
;
