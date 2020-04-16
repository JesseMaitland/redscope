-- gets all table names and data types
SELECT ns.nspname AS schema_name,
       c.relname AS table_name,
       a.attname AS column_name,
       a.attnum AS column_order,
       format_type(a.atttypid, a.atttypmod) AS data_type,
       CASE WHEN  ad.adsrc  IS NOT NULL THEN 'DEFAULT ' ||  ad.adsrc ELSE '' END AS default_value,
       CASE WHEN a.attnotnull IS TRUE THEN 'NOT NULL' ELSE '' END AS not_null,
       CASE format_encoding(a.attencodingtype) WHEN 'none' THEN 'ENCODE RAW' ELSE 'ENCODE ' + format_encoding(a.attencodingtype) END as encoding
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
       AND a.attnum >= 0
ORDER BY schema_name, table_name, column_order;
