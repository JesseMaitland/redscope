from pathlib import Path
from redscope.api import introspect_tables, load_redscope_env, get_db_connection

env_path = Path("stg.env")
load_redscope_env(env_path)

db_connection = get_db_connection('redscope_db_url')

db_catalog = introspect_tables(db_connection)


t = db_catalog.get_table('dds.companies')

print(t.simple_ddl)
print(t.create_if_not_exist)
