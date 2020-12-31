from importlib import import_module
from pathlib import Path
from typing import Tuple, List, Union
from psycopg2.extensions import connection
from redgiant.redscope.database.models import IntrospectionQueries
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter
from redgiant.redscope.introspection.schema import RedshiftSchema
from redgiant.redscope.introspection.ddl import DDL

#  allowed_db_objects = ['groups', 'schemas', 'users', 'tables', 'views', 'constraints', 'membership', 'udfs', 'ownership']

BASE_INTROSPECTION_OBJECTS = [
    'schemas'
]

SCHEMA_INTROSPECTION_OBJECTS = [
    'tables',
    'views',
    'procedures',
    'udfs',
    'constraints',
    'ownership'
]

PERMISSION_INTROSPECTION_OBJECTS = [
    'users',
    'groups',
    'membership'
]

ALL_INTROSPECTION_OBJECTS = []
ALL_INTROSPECTION_OBJECTS.extend(BASE_INTROSPECTION_OBJECTS)
ALL_INTROSPECTION_OBJECTS.extend(SCHEMA_INTROSPECTION_OBJECTS)
ALL_INTROSPECTION_OBJECTS.extend(PERMISSION_INTROSPECTION_OBJECTS)


class IntrospectionController:

    def __init__(self, introspection_queries: IntrospectionQueries, db_object: str = ''):

        self.introspection_queries = introspection_queries
        self.db_object = None
        self.formatter_path = None

        if db_object:
            self.set_introspection_path(db_object)

    def set_introspection_path(self, db_object: str):
        self.validate_db_object(db_object)
        self.db_object = db_object
        self.formatter_path = Path("redgiant/redscope/introspection/formatters") / db_object
        self.formatter_path = self.formatter_path.as_posix().replace('/', '.')

    def __call__(self, db_object: str) -> List[DDL]:
        self.set_introspection_path(db_object)
        formatter = self._import_formatter()
        raw_ddl = self._execute_query()
        return formatter.format(raw_ddl)

    def _execute_query(self) -> Tuple[str]:
        return self.introspection_queries.call_query(self.db_object)

    def _import_formatter(self) -> DDLFormatter:
        formatter_module = import_module(self.formatter_path)
        formatter = getattr(formatter_module, f"{self.db_object.capitalize().rstrip('s')}Formatter")
        return formatter()

    def validate_db_object(self, db_object: str):
        if db_object not in ALL_INTROSPECTION_OBJECTS:
            raise ValueError(f'{db_object} is not a valid name. Allowed values are {ALL_INTROSPECTION_OBJECTS}')


def introspect_redshift(db_connection: connection, object_type: Union[str, List[str]] = None,
                        verbose: bool = False) -> RedshiftSchema:
    """
    Function used to introspect redshift database objects
    Args:
        db_connection: psycopg2 connection object to a running instance of redshift.
        object_type: str or list the type of redshift object to introspect
        verbose: When True, will print out the introspection steps to the terminal

    Returns: DbCatalog: This is a dictionary like object which contains the requested ddl

    """

    # first figure out if we are introspecting 1 database object, or all of them.
    if type(object_type) == str:
        objects_to_introspect = [object_type]
    else:
        objects_to_introspect = ALL_INTROSPECTION_OBJECTS

    queries = IntrospectionQueries(db_connection)
    introspect = IntrospectionController(queries)
    introspected_objects = {}

    for object_to_introspect in objects_to_introspect:

        if verbose:
            print(f"Introspecting Redshift ........ {object_to_introspect}")

        db_objects = introspect(object_to_introspect)

        introspected_objects[object_to_introspect] = db_objects

    redshift_schema = RedshiftSchema(**{key: introspected_objects[key] for key in RedshiftSchema.allowed_kwargs})

    redshift_schema.map_schemas(**{key: introspected_objects[key]
                                   for key in objects_to_introspect
                                   if key in SCHEMA_INTROSPECTION_OBJECTS})

    redshift_schema.map_permissions(**{key: introspected_objects[key]
                                       for key in objects_to_introspect
                                       if key in PERMISSION_INTROSPECTION_OBJECTS})

    return redshift_schema
