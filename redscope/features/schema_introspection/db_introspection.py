from importlib import import_module
from pathlib import Path
from typing import Tuple
from redscope.database.models import IntrospectionQueries
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter
from redscope.features.schema_introspection.db_objects.db_catalog import DbCatalog


class DbIntrospection:

    allowed_db_objects = ['groups', 'schemas', 'users', 'permissions', 'tables']

    def __init__(self, intro_queries: IntrospectionQueries, db_object: str):

        if db_object not in self.allowed_db_objects:
            raise ValueError(f'{db_object} is not a valid name. Allowed values are {self.allowed_db_objects}')

        self.intro_queries = intro_queries
        self.db_object = db_object
        self.formatter_path = Path(__file__).parent.relative_to(Path.cwd()) / "formatters" / db_object
        self.formatter_path = self.formatter_path.as_posix().replace('/', '.')

    def call(self):
        formatter = self.import_formatter()
        raw_ddl = self.execute_query()
        return formatter.format(raw_ddl)

    def execute_query(self) -> Tuple[str]:
        return self.intro_queries.call_query(self.db_object)

    def import_formatter(self) -> DDLFormatter:
        formatter_module = import_module(self.formatter_path, package=__name__)
        formatter = getattr(formatter_module, f"{self.db_object.capitalize().rstrip('s')}Formatter")
        return formatter()


def introspect_schemas(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'schemas')
    schemas = intro.call()
    return DbCatalog(schemas=schemas)


def introspect_groups(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'groups')
    groups = intro.call()
    return DbCatalog(groups=groups)
