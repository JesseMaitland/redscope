from .terminal import init_redscope_env, get_terminal_logger
from redscope.database import Migration, DDL, InitiateDb
from redscope.project import project, logger_factory
from redscope import rambo_path
from rambo import provide_cmd_args

logger = get_terminal_logger(__name__)


@init_redscope_env
def init_db(db_conn):
    logger.info("creating database table and schema")
    ddl = DDL()
    initiate_db = InitiateDb(ddl, db_conn)
    initiate_db.exe_create_schema()
    initiate_db.exe_create_migration_table()
    logger.info("database tables created successfully")
    exit()


def init_project():
    folders = project.Folders()
    logger.info("creating redscope project directories")

    folders.root.mkdir(exist_ok=True, parents=True)
    folders.log_path.mkdir(exist_ok=True, parents=True)
    folders.migrations_path.mkdir(exist_ok=True, parents=True)
    folders.ddl_path.mkdir(exist_ok=True, parents=True)

    logger.info("project directories created successfully")
    exit()


@provide_cmd_args(rambo_path)
def new_migration(cmd_args):
    if not cmd_args.name:
        logger.info("the --name parameter must be provided when creating new migration")
        exit()

    folders = project.Folders()
    file_name = project.create_file_name(cmd_args.name)

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


@init_redscope_env
def migrate_up(db_conn):
    folders = project.Folders()
    local_migrations = project.all_local_migrations(folders)
    db_migrations = Migration.select_all(db_conn)
    migrations_to_apply = project.all_outstanding_migrations(local_migrations, db_migrations)

    if migrations_to_apply:

        for m in migrations_to_apply:
            logger.info(f"executing migrate up at {m.path.as_posix()}")
            m.execute_up(db_conn)
            m.insert(db_conn)
            logger.info(f"{m.path.as_posix()} executed successfully!")

    else:
        logger.info("all local migrations have been applied. Database is up to date")
    exit()


@init_redscope_env
def migrate_down(db_conn):
    last_applied_migration = Migration.select_last(db_conn)
    logger.info(f"migrating down from {last_applied_migration.path.as_posix()}")
    last_applied_migration.execute_down(db_conn)
    last_applied_migration.delete(db_conn)
    logger.info(f"migration down from {last_applied_migration.path.as_posix()} success!")
