from typing import Tuple, Dict
from prettytable import PrettyTable
from psycopg2.extensions import connection
from redscope.env.project_context import DirContext
from redscope.terminal.tools.entry import EntryPoint
from redscope.features.migrations.migration_manager import MigrationManager


migration_args = {

    ('action',): {
        'help': "the migration action you want to preform",
        'choices': ['up', 'down', 'list', 'new']
    },

    ('--name', '-n'): {
        'help': "use to set the name of the new migration you wish to create, must be unique.",
        'default': None,
        'dest': 'name'
    },

    ('--all', '-a'): {
        'help': "set this flag when you want to run all not yet applied migrations. Only for use with 'up' ",
        'action': 'store_true',
        'dest': 'all'
    }
}


def get_migration_context(db_connection: connection = None) -> Tuple[DirContext, MigrationManager]:
    dc = DirContext()
    mm = MigrationManager(dc.get_dir('migrations'), db_connection=db_connection)
    return dc, mm


class MigrationsEntryPoint(EntryPoint):

    def __init__(self, args_config: Dict) -> None:
        super().__init__(args_config=args_config)

    def _validate_name(self, msg: str):
        if not self.cmd_args.name:
            raise ValueError(msg)

    def call(self) -> None:
        func = getattr(self, self.cmd_args.action)
        func()
        exit()

    def new(self):
        self._validate_name(f"--name, -n flag value must be provided to create a new migration file.")
        migration_name = self.cmd_args.name.replace(' ', '-')
        dc, mm = get_migration_context()
        migration_name = mm.generate_file_name(migration_name)
        mm.create_file(migration_name)

    def list(self):
        dc, mm = get_migration_context()
        migrations = mm.list_migrations()
        table = PrettyTable()
        table.field_names = ['key', 'name']
        for migration in migrations:
            table.add_row([migration.key, migration.name])
        print(table)

    def up(self):
        self.set_db_connection()
        dc, mm = get_migration_context(self.db_connection)

        if self.cmd_args.name:
            migration = mm.get_migration(self.cmd_args.name)
            mm.execute_migration(migration, mode='up')

        elif self.cmd_args.all:
            migrations = mm.list_outstanding_migrations()

            for migration in migrations:
                mm.execute_migration(migration, mode='up')

        else:
            raise ValueError(f"either --name, -n flag must be provided, or the --all, -a flag must be set to run up")

    def down(self):
        self.set_db_connection()
        self._validate_name(f"--name, -n flag value must be provided to run migrate down.")
        dc, mm = get_migration_context(self.db_connection)

        migration = mm.get_migration(self.cmd_args.name)
        mm.execute_migration(migration, mode='down')


# TODO: refactor into main migration entry
def list_applied_migrations(db_conn: connection):
    dc, mm = get_migration_context(db_conn)
    applied_migrations = mm.list_applied_migrations()
    for migration in applied_migrations:
        print(migration.full_name)


# TODO: refactor into main migration entry
def outstanding_migrations(db_conn: connection):
    dc, mm = get_migration_context(db_conn)
    outstanding = mm.list_outstanding_migrations()
    for out in outstanding:
        print(out.full_name)
