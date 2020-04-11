from typing import Tuple, Dict
from prettytable import PrettyTable
from psycopg2.extensions import connection
from redscope.env.project_context import DirContext
from redscope.terminal.tools.entry import EntryPoint
from redscope.features.migrations.migration_manager import MigrationManager


migration_args = {

    ('action',): {
        'help': "the migration action you want to preform",
        'choices': ['up', 'down', 'list', 'new', 'remove']
    },

    ('--name', '-n'): {
        'help': "use to set the name of the new migration you wish to preform an action on.",
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

        if '-' in [char for char in migration_name]:
            print("the - char is not allowed in migration names, please use the _ instead")
            return

        dc, mm = get_migration_context()

        if migration_name in [lm.name for lm in mm.list_local_migrations()]:
            print(f"migration names must be unique, name {migration_name} already exists.")
            return

        migration_name = mm.generate_file_name(migration_name)
        mm.create_file(migration_name)
        print(f"successfully created migration {migration_name}")

    def list(self):
        self.set_db_connection()
        dc, mm = get_migration_context(self.db_connection)
        migrations = mm.list_migrations()
        table = PrettyTable()
        table.field_names = ['key', 'name', 'last state', 'file']
        for migration in migrations:
            table.add_row([migration.key, migration.name, migration.run_state, migration.file_name])
        print(table)

    def up(self):
        self.set_db_connection()
        dc, mm = get_migration_context(self.db_connection)

        if self.cmd_args.name:
            migration = mm.get_migration(self.cmd_args.name)
            print(f"running migration {migration.full_name} up")
            mm.execute_migration(migration, mode='up')

        elif self.cmd_args.all:
            migrations = [m for m in mm.list_migrations() if m.run_state != 'up']

            for migration in migrations:
                print(f"running migration {migration.full_name} up")
                mm.execute_migration(migration, mode='up')

        else:
            raise ValueError(f"either a value for the -n flag must be provided, or the -a flag must be set")

    def down(self):
        self.set_db_connection()
        self._validate_name(f"--name, -n flag value must be provided to run migrate down.")
        dc, mm = get_migration_context(self.db_connection)

        migration = mm.get_migration(self.cmd_args.name)
        print(f"running migration {migration.full_name} down")
        mm.execute_migration(migration, mode='down')

    def remove(self):
        self.set_db_connection()

        # try to rollback the migration first, if it is already in the down state, it is likely to fail.
        try:
            self.down()
        except Exception:
            pass

        dc, mm = get_migration_context(self.db_connection)
        migration = mm.get_migration(self.cmd_args.name)
        mm.delete_migration(migration)
