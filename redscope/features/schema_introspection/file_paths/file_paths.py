from redscope.env.project_context import DirContext
from redscope.features.schema_introspection.db_objects.db_catalog import DbCatalog


class FilePaths:

    def __init__(self):
        self.dir_context = DirContext()

    def save_files(self, db_catalog: DbCatalog, *db_object_names):

        for name in db_object_names:
            ddl = db_catalog.get_db_objects(name)

            for d in ddl:

                if name == 'schemas':
                    path = self.dir_context.get_dir(name)
                    path = path / d.name
                    path.mkdir(exist_ok=True, parents=True)

                    path = path / d.file_name
                    path.touch(exist_ok=True)
                    path.write_text(d.create_if_not_exist)

                elif name in ['tables', 'views']:
                    path = self.dir_context.get_dir('schemas')
                    path = path / d.schema / name
                    path.mkdir(parents=True, exist_ok=True)

                    path = path / d.file_name
                    path.touch(exist_ok=True)
                    path.write_text(d.create_if_not_exist)

                elif name in ['groups', 'users']:
                    path = self.dir_context.get_dir('permissions')
                    path = path / name
                    path.mkdir(parents=True, exist_ok=True)

                    path = path / d.file_name
                    path.touch(exist_ok=True)
                    path.write_text(d.create_if_not_exist)


                else:
                    path = self.dir_context.get_dir(name)
                    path.mkdir(exist_ok=True, parents=True)
                    p = path / d.file_name
                    p.touch(exist_ok=True)
                    p.write_text(d.create_if_not_exist)
