-- gets all table names and data types
SELECT ns.nspname AS schema,
       c.relname AS "table",
       a.attname AS name,
       a.attnum AS index,
       upper(format_type(a.atttypid, a.atttypmod)) AS data_type,
       CASE WHEN  ad.adsrc  IS NOT NULL THEN 'DEFAULT ' ||  ad.adsrc ELSE '' END AS "default",
       CASE WHEN a.attnotnull IS TRUE THEN 'NOT NULL' ELSE '' END AS not_null,
       CASE format_encoding(a.attencodingtype) WHEN 'none' THEN 'ENCODE RAW' ELSE 'ENCODE ' + upper(format_encoding(a.attencodingtype)) END as encoding
  FROM pg_namespace ns
       INNER JOIN pg_class c
          ON ns.oid = c.relnamespace
       INNER JOIN pg_attribute a
          ON c.oid = a.attrelid
       LEFT JOIN pg_attrdef ad
          ON ad.adrelid = a.attrelid
             AND ad.adnum = a.attnum
WHERE schema NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
       AND c.relkind = 'r'
       AND a.attnum >= 0
ORDER BY schema, "table", index;
