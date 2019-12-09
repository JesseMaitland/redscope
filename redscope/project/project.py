from pathlib import Path
from redscope.database.models import Migration
from datetime import datetime
from typing import List, Tuple


class Folders:

    def __init__(self, root_name: str):
        # root directory path
        self.root = Path.cwd() / root_name

        # project folders
        self.log_path = self.root / "logs"
        self.migrations_path = self.root / "migrations"
        self.ddl_path = self.root / "ddl"
        self.schema_path = self.ddl_path / "schema"
        self.permissions_path = self.ddl_path / "permissions"
        self.users_path = self.permissions_path / "users"
        self.groups_path = self.permissions_path / "groups"
        self.grants_path = self.permissions_path / "grants"

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
