from typing import Dict
from redscope.features.schema_introspection.file_paths.file_paths import FilePaths
from redscope.terminal.tools.entry import EntryPoint
from redscope.features.schema_introspection.db_introspection import introspect_db, introspect_tables, \
    introspect_user_groups, introspect_schemas, introspect_groups, introspect_views, introspect_users

inspection_mapping = {
    'schemas': introspect_schemas,
    'tables': introspect_tables,
    'views': introspect_views,
    'usergroups': introspect_user_groups,
    'users': introspect_users,
    'groups': introspect_groups,
    'all': introspect_db
}


class IntrospectDbEntryPoint(EntryPoint):

    def __init__(self, args_config: Dict):
        super().__init__(args_config=args_config)
        self.set_db_connection()

    def call(self) -> None:
        introspect_function = inspection_mapping[self.cmd_args.db_object]
        db_catalog = introspect_function(self.db_connection)
        file_paths = FilePaths()

        if self.cmd_args.db_object == 'all':
            objects_to_save = [key for key in inspection_mapping.keys() if key != 'all']
        else:
            objects_to_save = [self.cmd_args.db_object]

        file_paths.save_files(db_catalog, *objects_to_save)
        exit()


intro_args = {
    ('db_object',): {
        'help': "The database object you would like to introspect, default is 'all'. ",
        'default': 'all',
        'choices': list(inspection_mapping.keys())
    }
}
