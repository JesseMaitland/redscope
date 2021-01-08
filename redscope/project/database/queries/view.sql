SELECT schemaname AS schema,
       viewname AS name,
       pg_get_viewdef(schemaname || '.' || viewname, TRUE) AS ddl
  FROM pg_views
 WHERE schemaname = %s AND viewname = %s;
