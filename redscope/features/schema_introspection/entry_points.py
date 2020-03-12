from redscope.features.schema_introspection.db_introspection import introspect_db
from redscope.features.terminal.env_tools import init_terminal_env
from redscope.features.schema_introspection.file_paths.file_paths import FilePaths


@init_terminal_env(provide_db=True, provide_cmd=False)
def intro_db(db_conn):
    db_catalog = introspect_db(db_conn)
    file_paths = FilePaths()
    file_paths.save_files(db_catalog, 'schemas', 'groups', 'views', 'tables', 'users', 'usergroups')
