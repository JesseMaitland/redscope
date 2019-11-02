from .terminal import init_redscope_env
from redscope.database import models


@init_redscope_env
def init_db(db_conn):
    ddl = models.DDL()
    initiate_db = models.InitiateDb(ddl, db_conn)
    initiate_db.exe_create_schema()
    initiate_db.exe_create_migration_table()

