from pathlib import Path
from .project_logging import logger_factory
from datetime import datetime


class Folders:

    def __init__(self):
        self.root = Path.cwd() / "database"
        self.log_path = self.root / "logs"
        self.migrations_path = self.root / "migrations"
        self.ddl = self.root / "ddl"

        self.log_file = self.log_path / "redscope.log"

    def init_project_directories(self):
        logger.info("creating redscope project directories")
        self.root.mkdir(exist_ok=True, parents=True)
        self.log_path.mkdir(exist_ok=True, parents=True)
        self.migrations_path.mkdir(exist_ok=True, parents=True)
        self.ddl.mkdir(exist_ok=True, parents=True)
        logger.info("project directories created successfully")


logger = logger_factory(Folders().log_file, __name__)


class Migration:

    def __init__(self, key: int, path: Path):
        self.key = key
        self.path = path


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
    def migration_key(name):
        return int(name.split('-')[0])

    def create_new_migration(self, name):
        file_name = self.file_name(name)
        logger.info(f"creating migration {file_name}")
        migration_dir = self.folders.migrations_path / file_name
        up_file = migration_dir / "up.sql"
        down_file = migration_dir / "down.sql"

        migration_dir.mkdir(parents=True, exist_ok=True)
        up_file.touch(exist_ok=True)
        down_file.touch(exist_ok=True)
        logger.info(f"migration {file_name} created successfully")

    def all_migrations(self):
        all_migrations = [m for m in self.folders.migrations_path.iterdir() if m.is_dir() and not m.name.startswith('.')]
        sorted_migrations = sorted(all_migrations, key=lambda x: int(x.name.split('-')[0]))
        return [Migration(self.migration_key(path.name), path) for path in sorted_migrations]

    def compare_migrations(self, local_migrations, db_migrations):
        pass

    def
