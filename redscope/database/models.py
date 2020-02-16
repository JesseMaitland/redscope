from pathlib import Path
import pandas as pd


class MigrationDDL:

    def __init__(self):
        self.root: Path = Path(__file__).absolute().parent / "queries" / "ddl"
        self.schema_file_path: Path = self.root / "schema.sql"
        self.migration_table_path: Path = self.root / "migration_table.sql"

    @property
    def create_schema(self) -> str:
        return self.schema_file_path.read_text()

    @property
    def create_migration_table(self) -> str:
        return self.migration_table_path.read_text()


class DML:

    def __init__(self):
        self.root: Path = Path(__file__).absolute().parent / "queries" / "dml"
        self.insert_path = self.root / "insert.sql"
        self.delete_path = self.root / "delete.sql"
        self.select_path = self.root / "select.sql"
        self.select_last_path = self.root / "select_last.sql"

    @property
    def insert(self):
        return self.insert_path.read_text()

    @property
    def delete(self):
        return self.delete_path.read_text()

    @property
    def select(self):
        return self.select_path.read_text()

    @property
    def select_last(self):
        return self.select_last_path.read_text()


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


# TODO: lots of duplication going on here. Can probably be refactored.
class Migration:
    dml: DML = DML()

    def __init__(self, key: int, name: str, path: Path):
        self.key = key
        self.name = name
        self.path = path

    @classmethod
    def select_all(cls, db_connection):
        cursor = db_connection.cursor()
        try:
            cursor.execute(cls.dml.select)
            result = [Migration(
                key=r[0],
                name=r[1],
                path=Path(r[2]).absolute()
            ) for r in cursor.fetchall()]

            return result
        except Exception:
            db_connection.rollback()
            raise

    def insert(self, db_connection):
        cursor = db_connection.cursor()
        try:
            relative_path = self.path.relative_to(Path.cwd().as_posix()).as_posix()
            cursor.execute(self.dml.insert, [self.key, self.name, relative_path])
            db_connection.commit()
        except Exception:
            db_connection.rollback()
            raise

    def delete(self, db_connection):
        cursor = db_connection.cursor()
        try:
            cursor.execute(self.dml.delete, [self.key])
            db_connection.commit()
        except Exception:
            db_connection.rollback()
            raise

    @classmethod
    def select_last(cls, db_connection) -> 'Migration':
        cursor = db_connection.cursor()
        try:
            cursor.execute(cls.dml.select_last)
            result = cursor.fetchone()

            return Migration(
                key=result[0],
                name=result[1],
                path=Path(result[2]).absolute())

        except Exception:
            db_connection.rollback()
            raise

    def execute_up(self, db_connection):
        cursor = db_connection.cursor()
        try:
            migration = self.path.joinpath('up.sql').read_text()
            cursor.execute(migration)
            db_connection.commit()
        except Exception:
            db_connection.rollback()
            raise

    def execute_down(self, db_connection):
        cursor = db_connection.cursor()
        try:
            migration = self.path.joinpath('down.sql').read_text()
            cursor.execute(migration)
            db_connection.commit()
        except Exception:
            db_connection.rollback()
            raise


class DDL:

    def __init__(self, schema: str, db_object: str, ddl: str):
        self.schema = schema
        self.db_object = db_object
        self.ddl = ddl
