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
