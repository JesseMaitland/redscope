from typing import List
from pathlib import Path
from datetime import datetime
from io import TextIOWrapper
from .migration import Migration
from psycopg2.extensions import connection


class MigrationNotFoundError(Exception):
    pass


class MigrationParser:

    up_mark = '--<migration: up>--'
    down_mark = '--<migration: down>--'

    def __init__(self, migration: Path) -> None:
        self.migration_path = migration

    def parse(self) -> Migration:
        with self.migration_path.open(mode='r') as file:
            up_script = self.get_migration_text(file, self.up_mark, self.down_mark)
            down_script = self.get_migration_text(file, self.down_mark, self.up_mark)

            up_script = ''.join(line for line in up_script)
            down_script = ''.join(line for line in down_script)

        return Migration(self.migration_path, up_script, down_script)

    def get_migration_text(self, text: TextIOWrapper, start_mark: str, stop_mark: str) -> str:
        line = text.readline()
        while line:
            if start_mark in line:
                while line and stop_mark not in line:
                    yield line
                    line = text.readline()
            else:
                line = text.readline()
        text.seek(0)


class MigrationManager:
    template_path = Path(__file__).absolute().parent / "migration_template.sql"

    def __init__(self, migration_dir: Path, db_connection: connection):
        self.migration_dir = migration_dir
        self.db_connection = db_connection

    @staticmethod
    def generate_file_name(name: str):
        timestamp = datetime.utcnow().timestamp()
        timestamp = str(timestamp).split('.')[0]
        return f"{timestamp}-{name}.sql"

    def create_file(self, file_name: str) -> None:
        new_file = self.migration_dir / file_name
        new_file.touch(exist_ok=True)
        new_file.write_text(self.template_path.read_text())

    def list_migrations(self) -> List[Migration]:
        migrations = self.migration_dir.glob('**/*.sql')
        migrations = [MigrationParser(m).parse() for m in migrations]
        self._sort_migrations(migrations)
        return migrations

    def list_applied_migrations(self) -> List[Migration]:
        applied_migrations = self._run_query(Migration.select)
        self._sort_migrations(applied_migrations)
        return applied_migrations

    def list_outstanding_migrations(self) -> List[Migration]:
        all_migrations = self.list_migrations()
        applied_migrations = self.list_applied_migrations()
        outstanding = [m for m in all_migrations if m.full_name not in [am.full_name for am in applied_migrations]]
        self._sort_migrations(outstanding)
        return outstanding

    def get_migration(self, name: str) -> Migration:
        migration = next((m for m in self.list_migrations() if m.name == name), None)
        if not migration:
            raise MigrationNotFoundError(f"no migration found with name {name}")
        else:
            return migration

    def execute_migration(self, migration: Migration, mode: str) -> None:
        allowed_modes = ['up', 'down']

        if mode not in allowed_modes:
            raise ValueError(f"allowed modes are only, up or down, not {mode}")

        if mode == 'up':
            try:
                self._run_ddl(migration.up)
                self._run_ddl(migration.insert, migration.key, migration.name, migration.path.as_posix(), mode, migration.up)
            except Exception:
                raise

        elif mode == 'down':
            try:
                self._run_ddl(migration.down)
                self._run_ddl(migration.insert, migration.key, migration.name, migration.path.as_posix(), mode, migration.down)
            except Exception:
                raise

    def _run_ddl(self, ddl: str, *values):
        with self.db_connection.cursor() as cursor:
            try:
                cursor.execute(ddl, values)
                self.db_connection.commit()
            except Exception:
                self.db_connection.rollback()
                raise

    def _run_query(self, query, *values) -> List[Migration]:
        with self.db_connection.cursor() as cursor:
            try:
                cursor.execute(query, values)
                results = cursor.fetchall()
            except Exception:
                self.db_connection.rollback()
                raise
        return [MigrationParser(Path(result[2]).absolute()).parse() for result in results]

    def _sort_migrations(self, migrations: List[Migration]) -> List[Migration]:
        migrations.sort(key=lambda x: x.key)
        return migrations
