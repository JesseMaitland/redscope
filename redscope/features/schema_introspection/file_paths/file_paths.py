from redscope.env.project_context import DirContext
from redscope.features.schema_introspection.db_objects.db_catalog import DbCatalog


class FilePaths:

    def __init__(self):
        self.dir_context = DirContext()

    def save_files(self, db_catalog: DbCatalog, *db_object_names):

        for name in db_object_names:
            ddl = db_catalog.get_db_objects(name)
            print(ddl)
            path = self.dir_context.get_dir(name)

            for d in ddl:
                p = path / d.file_name
                p.touch(exist_ok=True)
                p.write_text(d.create_if_not_exist)
