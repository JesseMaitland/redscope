from pathlib import Path
from redscope.database.models import Migration
from datetime import datetime
from typing import List, Tuple


class Folders:

    def __init__(self):
        # root directory path
        self.root = Path.cwd() / "database"

        # project folders
        self.log_path = self.root / "logs"
        self.migrations_path = self.root / "migrations"
        self.ddl_path = self.root / "ddl"

        # file paths
        self.log_file = self.log_path / "redscope.log"


def create_file_name(name: str) -> str:
    timestamp = datetime.utcnow().timestamp()
    timestamp = str(timestamp).split('.')[0]
    return f"{timestamp}-{name}"


def parse_file_key_and_name(path: Path) -> Tuple[int, str]:
    parts = path.name.split('-')
    return int(parts[0]), parts[1]


def parse_file_key(path: Path) -> int:
    return int(path.name.split('-')[0])


def parse_file_name(path: Path) -> str:
    return str(path.name.split('-')[1])


def all_local_migrations(folders: Folders) -> List[Migration]:
    all_migrations = [p for p in folders.migrations_path.iterdir() if p.is_dir()]
    all_migrations = sorted(all_migrations, key=parse_file_key)
    return [Migration(
        key=parse_file_key(migration),
        name=parse_file_name(migration),
        path=migration
    ) for migration in all_migrations]


def all_outstanding_migrations(local_migrations: List[Migration], db_migrations: List[Migration]) -> List[Migration]:
    db_migration_keys = [m.key for m in db_migrations]
    outstanding_migrations = []
    for migration in local_migrations:
        if migration.key not in db_migration_keys:
            outstanding_migrations.append(migration)

    return outstanding_migrations


class Manager:

    def __init__(self, folders: Folders):
        self.folders = folders

    @staticmethod
    def file_name(name: str) -> str:
        timestamp = datetime.utcnow().timestamp()
        timestamp = str(timestamp).split('.')[0]
        return f"{timestamp}-{name}"

    @staticmethod
    def migration_key_and_name(name):
        parts = name.split('-')
        return int(parts[0]), parts[1]

    @staticmethod
    def migration_key(name) -> int:
        return int(name.split('-')[0])

    @staticmethod
    def migration_name(name) -> str:
        return str(name.split('-')[1])

    def create_new_migration(self, name):
        file_name = self.file_name(name)
        migration_dir = self.folders.migrations_path / file_name
        up_file = migration_dir / "up.sql"
        down_file = migration_dir / "down.sql"

        migration_dir.mkdir(parents=True, exist_ok=True)
        up_file.touch(exist_ok=True)
        down_file.touch(exist_ok=True)

    def all_local_migrations(self):
        all_migrations = [m for m in self.folders.migrations_path.iterdir() if
                          m.is_dir() and not m.name.startswith('.')]

        sorted_migrations = sorted(all_migrations, key=lambda x: int(x.name.split('-')[0]))

        return [Migration(
            key=self.migration_key(path.name),
            name=self.migration_name(path.name),
            path=path) for path in sorted_migrations]

    def all_db_migrations(self, db_connection):
        return Migration.select_all(db_connection)

    def compare_migrations(self, local_migrations: List[Migration], db_migrations: List[Migration]) -> List[Migration]:
        outstanding_migrations = []
        db_keys = [m.key for m in db_migrations]
        for migration in local_migrations:
            if migration.key not in db_keys:
                outstanding_migrations.append(migration)

        return outstanding_migrations
