from redscope.features.schema_introspection.file_paths.file_paths import FilePaths


def init_project():
    file_paths = FilePaths()
    file_paths.dir_context.init_dirs()
