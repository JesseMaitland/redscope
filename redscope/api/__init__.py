from redscope.config import FILE_ROOT
from redscope.introspection.tables import IntrospectTables
from redscope.env import load_redscope_env
from redscope.database.db_connections import get_db_connection
from redscope.project.project import Folders
from redscope.database.models import Catalog


def schema_catalog(env_file_name: str = '', db_connection_name: str = ''):
    load_redscope_env(env_file_name)
    db_conn = get_db_connection(db_connection_name)
    folders = Folders(FILE_ROOT)
    catalog = Catalog()
    return IntrospectTables(db_conn, catalog, folders).get_schema_catalog()
