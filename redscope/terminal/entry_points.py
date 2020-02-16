from .terminal import init_terminal_env, get_terminal_logger
from redscope.config import RAMBO_CONFIG_PATH, FILE_ROOT
from redscope.database import Migration, MigrationDDL, InitiateDb
from redscope.database.models import Catalog
from redscope.project import Folders, create_file_name, all_outstanding_migrations, all_local_migrations
from redscope.introspection import IntrospectUsers, IntroUserGroup, IntrospectGroups, IntrospectSchema, IntrospectTables
from rambo import provide_cmd_args

logger = get_terminal_logger(__name__)


@init_terminal_env
def init_db(db_conn):
    logger.info("creating database table and schema")
    ddl = MigrationDDL()
    initiate_db = InitiateDb(ddl, db_conn)
    initiate_db.exe_create_schema()
    initiate_db.exe_create_migration_table()
    logger.info("database tables created successfully")
    exit()


def init_project():
    folders = Folders(FILE_ROOT)
    logger.info("creating redscope project directories")

    for k, v in folders.__dict__.items():
        if not v.suffix:
            v.mkdir(exist_ok=True, parents=True)
        else:
            v.touch(exist_ok=True)

    logger.info("project directories created successfully")
    exit()


@provide_cmd_args(RAMBO_CONFIG_PATH)
def new_migration(cmd_args):
    if not cmd_args.name:
        logger.info("the --name parameter must be provided when creating new migration")
        exit()

    folders = Folders(FILE_ROOT)
    file_name = create_file_name(cmd_args.name)

    logger.info(f"Creating migration {file_name}")

    # set up the paths for the folders and files to create the migration
    migration_dir = folders.migrations_path / file_name
    up_file = migration_dir / "up.sql"
    down_file = migration_dir / "down.sql"

    # create the objects on disk, if they exist just ignore errors
    migration_dir.mkdir(parents=True, exist_ok=True)
    up_file.touch(exist_ok=True)
    down_file.touch(exist_ok=True)

    logger.info(f"Successfully created migration {file_name}")
    exit()


@init_terminal_env
def migrate_up(db_conn):
    folders = Folders(FILE_ROOT)
    local_migrations = all_local_migrations(folders)
    db_migrations = Migration.select_all(db_conn)
    migrations_to_apply = all_outstanding_migrations(local_migrations, db_migrations)

    if migrations_to_apply:

        for m in migrations_to_apply:
            logger.info(f"executing migrate up at {m.path.as_posix()}")
            m.execute_up(db_conn)
            m.insert(db_conn)
            logger.info(f"{m.path.as_posix()} executed successfully!")

    else:
        logger.info("all local migrations have been applied. Database is up to date")
    exit()


@init_terminal_env
def migrate_down(db_conn):
    last_applied_migration = Migration.select_last(db_conn)
    logger.info(f"migrating down from {last_applied_migration.path.as_posix()}")
    last_applied_migration.execute_down(db_conn)
    last_applied_migration.delete(db_conn)
    logger.info(f"migration down from {last_applied_migration.path.as_posix()} success!")


@init_terminal_env
def show_migrations(db_conn):
    folders = Folders(FILE_ROOT)
    local_migrations = all_local_migrations(folders)
    db_migrations = Migration.select_all(db_conn)
    migrations_to_apply = all_outstanding_migrations(local_migrations, db_migrations)

    if migrations_to_apply:
        logger.info(f'the following migrations would be applied with "redscope migrate up"')
        for migration in migrations_to_apply:
            logger.info(migration.path.as_posix())
        exit()
    else:
        logger.info("No migrations to apply, database is up to date")
        exit()


@init_terminal_env
def intro_db(db_conn):
    folders = Folders(FILE_ROOT)
    catalog = Catalog()

    intro_users = IntrospectUsers(db_conn, catalog, folders)
    intro_users.introspect_and_save_files()

    intro_schema = IntrospectSchema(db_conn, catalog, folders)
    intro_schema.introspect_and_save_files()

    intro_tables = IntrospectTables(db_conn, catalog, folders)
    intro_tables.introspect_and_save_files()

    intro_groups = IntrospectGroups(db_conn, catalog, folders)
    intro_groups.introspect_and_save_files()

    intro_user_groups = IntroUserGroup(db_conn, catalog, folders)
    intro_user_groups.execute()
