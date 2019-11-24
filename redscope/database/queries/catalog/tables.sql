-- gets all table names and data types
SELECT ns.nspname AS schema_name,
       c.relname AS table_name,
       a.attname AS column_name,
       format_type(a.atttypid, a.atttypmod) AS data_type,
       a.atthasdef AS has_default,
       a.attnotnull AS not_null,
       ad.adsrc AS default_value
  FROM pg_namespace ns
       INNER JOIN pg_class c
          ON ns.oid = c.relnamespace
       INNER JOIN pg_attribute a
          ON c.oid = a.attrelid
       LEFT JOIN pg_attrdef ad
          ON ad.adrelid = a.attrelid
             AND ad.adnum = a.attnum
 WHERE schema_name NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
       AND c.relkind = 'r'
       AND a.attnum >= 0;
