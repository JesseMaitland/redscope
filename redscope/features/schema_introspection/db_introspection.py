from importlib import import_module
from pathlib import Path
from typing import Tuple
from redscope.database.models import IntrospectionQueries
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter
from redscope.features.schema_introspection.db_objects.db_catalog import DbCatalog


class DbIntrospection:

    allowed_db_objects = ['groups', 'schemas', 'users', 'permissions', 'tables', 'views', 'constraints', 'usergroups']

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


def introspect_user_groups(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'usergroups')
    user_groups = intro.call()
    return DbCatalog(user_groups=user_groups)


def introspect_views(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'views')
    views = intro.call()
    return DbCatalog(views=views)


def introspect_constraints(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'constraints')
    constraints = intro.call()
    return DbCatalog(constraints=constraints)


def introspect_tables(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'tables')
    tables = intro.call()
    constraints = introspect_constraints(db_connection)

    for table in tables:
        for constraint in constraints.constraints:

            if constraint.schema == table.schema and constraint.table == table.name:
                table.add_constraint(constraint)

    return DbCatalog(tables=tables)


def introspect_users(db_connection) -> DbCatalog:
    queries = IntrospectionQueries(db_connection)
    intro = DbIntrospection(queries, 'users')
    users = intro.call()
    return DbCatalog(users=users)


def introspect_db(db_connection) -> DbCatalog:
    schemas = introspect_schemas(db_connection)
    groups = introspect_groups(db_connection)
    views = introspect_views(db_connection)
    tables = introspect_tables(db_connection)
    users = introspect_users(db_connection)
    user_groups = introspect_user_groups(db_connection)
    return DbCatalog(schemas=schemas.schemas,
                     groups=groups.groups,
                     views=views.views,
                     tables=tables.tables,
                     users=users.users,
                     user_groups=user_groups.user_groups)
