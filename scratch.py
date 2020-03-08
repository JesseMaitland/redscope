from pathlib import Path
from redscope.api import introspect_db
from redscope.env import load_redscope_env
from redscope.database.db_connections import get_db_connection


env_path = Path("/Users/jessemaitland/PycharmProjects/redscope/stg.env")
load_redscope_env(env_path)
db_connection = get_db_connection('REDSCOPE_DB_URL')
db_catalog = introspect_db(db_connection)


tables = db_catalog.get_tables_by_schema('dds')

for k, v in tables.items():
    print(k, v)
