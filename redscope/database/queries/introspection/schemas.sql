-- query used to retrieve unique schema names
SELECT DISTINCT nspname AS schema_name
  FROM pg_namespace ns
       INNER JOIN pg_class cl
          ON ns.oid = cl.relnamespace
 WHERE cl.relkind = 'r'
       AND relnamespace <> 11;

