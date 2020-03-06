SELECT schemaname,
       viewname,
       definition
  FROM pg_views
 WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'admin');
