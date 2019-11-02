from pathlib import Path


class DDL:

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

    @property
    def insert(self):
        return self.insert_path.read_text()

    @property
    def delete(self):
        return self.delete_path.read_text()

    @property
    def select(self):
        return self.select_path.read_text()


class InitiateDb:

    def __init__(self, ddl: DDL, db_connection):
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


class Migration:

    def __init__(self, key: int, name: str, path: Path, dml: DML):
        self.key = key
        self.name = name
        self.path = path
        self.dml = dml

    def select(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(self.dml.select)
        cursor.fetchall()
        result = [r for r in cursor]
        result.sort()
        return result

    def insert(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(self.dml.insert, (self.key, self.name, self.path))
        db_connection.commit()
