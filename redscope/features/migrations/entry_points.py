from argparse import Namespace
from typing import Tuple
from redscope.features.terminal.env_tools import init_terminal_env
from redscope.env.project_context import DirContext
from redscope.features.migrations.migration_manager import MigrationManager
from redscope.database.models import MigrationDDL


def get_migration_context(db_connection=None) -> Tuple[DirContext, MigrationManager]:
    dc = DirContext()
    mm = MigrationManager(dc.get_dir('migrations'), db_connection=db_connection)
    return dc, mm


@init_terminal_env(provide_db=False, provide_cmd=True)
def new_migration(cmd_args: Namespace):
    migration_name = cmd_args.name.replace(' ', '-')
    dc, mm = get_migration_context()
    migration_name = mm.generate_file_name(migration_name)
    mm.create_file(migration_name)
    exit()


@init_terminal_env(provide_db=False, provide_cmd=False)
def list_migrations():
    dc, mm = get_migration_context()
    migrations = mm.list_migrations()
    for migration in migrations:
        print(migration.full_name)
    exit()


@init_terminal_env(provide_db=True, provide_cmd=True)
def migrate_up(db_conn, cmd_args):
    dc, mm = get_migration_context(db_conn)

    if cmd_args.name:
        migration = mm.get_migration(cmd_args.name)
        mm.execute_migration(migration, mode='up')

    else:
        migrations = mm.list_outstanding_migrations()

        for migration in migrations:
            mm.execute_migration(migration, mode='up')


@init_terminal_env(provide_db=True, provide_cmd=True)
def migrate_down(db_conn, cmd_args):
    dc, mm = get_migration_context(db_conn)

    if cmd_args.name:
        migration = mm.get_migration(cmd_args.name)
        mm.execute_migration(migration, 'down')

    else:
        raise NotImplementedError


@init_terminal_env(provide_db=True, provide_cmd=False)
def applied_migrations(db_conn):
    dc, mm = get_migration_context(db_conn)
    applied_migs = mm.list_applied_migrations()
    for migration in applied_migs:
        print(migration.full_name)


@init_terminal_env(provide_db=True, provide_cmd=False)
def outstanding_migrations(db_conn):
    dc, mm = get_migration_context(db_conn)
    outstanding = mm.list_outstanding_migrations()
    for out in outstanding:
        print(out.full_name)


@init_terminal_env(provide_db=True, provide_cmd=False)
def init_db(db_conn):
    with db_conn.cursor() as cursor:
        migration_ddl = MigrationDDL()
        try:
            cursor.execute(migration_ddl.create_schema)
            cursor.execute(migration_ddl.create_migration_table)
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            raise
