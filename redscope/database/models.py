# flake8: noqa W291

from pathlib import Path
from abc import ABC, abstractmethod
from psycopg2.extensions import connection


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
    delete = """DELETE FROM redscope.migrations WHERE name = %s"""
    select = """SELECT key, name, path, last_state 
                  FROM redscope.migrations
                       INNER JOIN (SELECT MAX(created_at) as last_created, key as lkey, name as lname 
                                     FROM redscope.migrations
                                   GROUP BY key, name) AS last_records
                           ON last_records.last_created = redscope.migrations.created_at
                              AND last_records.lkey = redscope.migrations.key
                              AND last_records.lname = redscope.migrations.name 
              ORDER BY key;"""


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
