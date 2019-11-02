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
    pass
