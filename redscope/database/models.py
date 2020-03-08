from pathlib import Path
from abc import ABC, abstractmethod
from psycopg2.extensions import connection
import pandas as pd


class QueryNotFoundError(Exception):
    pass


class MigrationDDL:

    def __init__(self):
        self.root: Path = Path(__file__).absolute().parent / "queries"
        self.schema_file_path: Path = self.root / "migrations" / "ddl" / "schema.sql"
        self.migration_table_path: Path = self.root / "migrations" / "ddl" / "migration_table.sql"

    @property
    def create_schema(self) -> str:
        return self.schema_file_path.read_text()

    @property
    def create_migration_table(self) -> str:
        return self.migration_table_path.read_text()


class MigrationQueries:

    insert = """INSERT INTO redscope.migrations(key, name, path, last_state, sql) VALUES (%s, %s, %s, %s, %s);"""
    update = """UPDATE redscope.migrations SET last_state = %s, sql = %s WHERE key = %s;"""
    delete = """DELETE FROM redscope.migrations WHERE key = %s"""
    select = """SELECT DISTINCT key, name, path FROM redscope.migrations ORDER BY key;"""


class QueryCatalog:

    def __init__(self, query_path: Path):
        self.query_path = query_path
        self.queries = {}

        for path in query_path.glob('**/*.sql'):
            self.queries[path.name.split('.')[0]] = path.read_text()

    def get_query(self, name: str) -> str:
        try:
            return self.queries[name]
        except KeyError:
            raise QueryNotFoundError(f'no query exists with name {name}')


class BaseQueries(ABC):

    def __init__(self, db_connection: connection):
        self.db_connection = db_connection

    @abstractmethod
    def call_query(self, name: str):
        pass

    def execute_query(self, query: str):
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


class IntrospectionQueries(BaseQueries):

    def __init__(self, db_connection: connection) -> None:
        super().__init__(db_connection)
        self.introspection_path: Path = Path(__file__).absolute().parent / "queries" / "introspection"
        self.db_queries = QueryCatalog(self.introspection_path)

    def call_query(self, name: str):
        query = self.db_queries.get_query(name)
        return self.execute_query(query)




class Catalog:

    def __init__(self):
        self.root_path: Path = Path(__file__).absolute().parent / "queries" / "catalog"
        query_paths = self.root_path.glob('**/*.sql')
        # set the query attributes
        for path in query_paths:
            name = path.name.split('.')[0]
            query_name = f"{name}_query"
            query_value = path.read_text()

            method_name = f"fetch_{name}"
            method_pointer = self._method_maker(query_value)
            setattr(self, query_name, query_value)
            setattr(self, method_name, method_pointer)

    def _method_maker(self, query):
        def get_data(db_connection) -> pd.DataFrame:
            return pd.read_sql(query, db_connection, parse_dates=True)

        return get_data


# TODO: duplication going on here, refactor and DRY it out.
class InitiateDb:

    def __init__(self, ddl: MigrationDDL, db_connection):
        self.ddl = ddl
        self.db_connection = db_connection

    def exe_create_schema(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(self.ddl.create_schema)
            self.db_connection.commit()
            return True
        except Exception:
            self.db_connection.rollback()
            raise Exception

    def exe_create_migration_table(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(self.ddl.create_migration_table)
            self.db_connection.commit()
            return True
        except Exception:
            self.db_connection.rollback()
            raise Exception


class DDL:

    def __init__(self, schema: str, db_object: str, ddl: str):
        self.schema = schema
        self.db_object = db_object
        self.ddl = ddl
