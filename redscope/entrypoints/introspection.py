from redgiant.redscope.project import RedScopeSingleActionEntryPoint
from redgiant.redscope.introspection import introspect_redshift, ALL_INTROSPECTION_OBJECTS


class Introspect(RedScopeSingleActionEntryPoint):

    discover = True

    entry_point_args = {
        ('--entity', '-e'): {
            'help': 'the name of the database object you would like to introspect. Default will introspect everything',
            'choices': ALL_INTROSPECTION_OBJECTS,
            'default': None
        }
    }

    def action(self) -> None:
        db_connection = self.config.get_db_connection('redshift')
        redshift_schema = introspect_redshift(db_connection, self.args.entity, True)

        for schema in redshift_schema.schemas().values():
            self._create_files(schema)

            for ddl in schema.items():
                if ddl.__class__.__name__.lower() != 'constraint':
                    self._create_files(ddl)

        for permission in redshift_schema.permissions().ddl():
            self._create_files(permission)

    def _create_files(self, ddl) -> None:
        path = self.project.get_ddl_filepath(ddl)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(ddl.create())
