from typing import Dict
from redscope.env import DirContext
from redscope.database.models import MigrationDDL
from redscope.terminal.tools.entry import EntryPoint

project_args = {
    ('action',): {
        'help': "the action you would like to take",
        'choices': ['init', 'drop']
    },

    ('--database', '-d'): {
        'help': "pass this flag to also initiate the database tables",
        'action': 'store_true',
        'dest': 'db'
    },

    ('--project', '-p'): {
        'help': "pass this flag if you want to initiate the project only",
        'action': 'store_true',
        'dest': 'project'
    },

    ('--all', '-a'): {
        'help': "pass this flag to init both the db, and the project directories",
        'action': 'store_true',
        'dest': 'all'
    }
}


class InitProjectEntryPoint(EntryPoint):

    def __init__(self, args_config: Dict) -> None:
        super().__init__(args_config=args_config)

    def _validate_params(self):
        if not self.cmd_args.all and not self.cmd_args.db and not self.cmd_args.project:
            raise ValueError(
                f"at least one --project, --database, --all, (-p, -d, -a) flags must be passed to either the drop or init command.")

    def call(self) -> None:
        func = getattr(self, self.cmd_args.action)
        func()
        exit()

    def init(self):
        self._validate_params()

        if self.cmd_args.project or self.cmd_args.all:
            dc = DirContext()
            dc.init_dirs()

        if self.cmd_args.db or self.cmd_args.all:
            self.set_db_connection()
            ddl = MigrationDDL()
            cursor = self.db_connection.cursor()

            try:
                cursor.execute(ddl.create_schema)
                cursor.execute(ddl.create_migration_table)
                self.db_connection.commit()

            except Exception:
                self.db_connection.rollback()
                raise

    def drop(self):
        raise NotImplementedError("the drop feature has not been yet implemented.")
