SELECT schemaname,
       viewname,
       pg_get_viewdef(schemaname || '.' || viewname, TRUE) AS definition
  FROM pg_views
 WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'admin');
