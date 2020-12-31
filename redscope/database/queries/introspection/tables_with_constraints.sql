WITH constraints AS
(
-- gets all column constraints
SELECT ns.nspname as schema_name,
       c.relname  as table_name,
       a.attname  as column_name,
       pg_get_constraintdef(cn.oid) as con_def,
       cn.conname as con_name
  FROM pg_constraint cn
       INNER JOIN pg_namespace ns
          ON ns.oid = cn.connamespace
       INNER JOIN pg_class c
          ON c.oid = cn.conrelid
       INNER JOIN pg_attribute a
          ON a.attnum = ANY(cn.conkey)
             AND a.attrelid = c.oid
), tables AS
(
-- gets all table names and data types
SELECT ns.nspname AS schema_name,
       c.relname AS table_name,
       a.attname AS column_name,
       a.attnum AS column_order,
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
       AND a.attnum >= 0)

SELECT t.schema_name,
       t.table_name,
       t.column_name,
       t.column_order,
       t.data_type,
       CASE WHEN t.default_value IS NOT NULL THEN 'DEFAULT ' || t.default_value ELSE '' END AS default_value,
       CASE WHEN t.not_null IS TRUE THEN 'NOT NULL' ELSE '' END AS not_null,
       CASE WHEN c.con_def IS NOT NULL THEN c.con_def ELSE '' END AS const
FROM tables t
       LEFT JOIN constraints c
          ON t.table_name = c.table_name
             AND t.schema_name = c.schema_name
             AND t.column_name = c.column_name
ORDER BY t.schema_name, t.table_name, t.column_order
;
