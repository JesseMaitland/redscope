from pathlib import Path
from redgiant.terminal.project import RedGiantProject
from redgiant.terminal import RedGiantSingleActionEntryPoint, RedGiantMultiActionEntryPoint


class RedScopeProject(RedGiantProject):

    def __init__(self, root_name: str) -> None:
        super().__init__(root_name)

        redscope = 'redscope'
        schemas = 'schemas'
        permissions = 'permissions'

        self.dirs = {
            redscope: self.root / redscope,
            schemas: self.root / redscope / schemas,
            permissions: self.root / redscope / permissions
        }

    def get_ddl_filepath(self, ddl: 'DDL') -> Path:

        if ddl.__class__.__name__ == 'Schema':
            return self.dirs['schemas'] / ddl.schema / ddl.file_name()

        elif ddl.__class__.__name__ in ['User', 'Group']:
            return self.dirs['permissions'] / f"{ddl.__class__.__name__.lower()}s" / ddl.file_name()

        elif ddl.__class__.__name__ == 'UserGroup':
            return self.dirs['permissions'] / 'membership' / ddl.file_name()

        else:
            return self.dirs['schemas'] / ddl.schema / f"{ddl.__class__.__name__.lower()}s" / ddl.file_name()

    def get_filepath(self, db_object: str, schema: str, name: str) -> Path:
        allowed_db_objects = ['schema', 'table', 'view', 'function', 'procedure']

        if db_object not in allowed_db_objects:
            raise ValueError(f"{db_object} not a valid value. choose from {allowed_db_objects}")

        return self.dirs['schemas'] / schema / f"{db_object}s" / f"{name}"

    def get_dir(self, name: str):
        return self.dirs[name]

    def make_subdir(self, name: str, *args):
        new_dir = Path(self.dirs[name].joinpath(args))
        new_dir.mkdir(exist_ok=True, parents=True)

    def init_project(self):
        for path in self.dirs.values():
            path.mkdir(parents=True, exist_ok=True)

    def clean_project(self):
        self.clean_dir('redscope')


class RedScopeSingleActionEntryPoint(RedGiantSingleActionEntryPoint):

    def __init__(self):
        super().__init__()
        self.project = RedScopeProject(self.config.get_project_root())

    def action(self) -> None:
        raise NotImplementedError


class RedScopeMultiActionEntryPoint(RedGiantMultiActionEntryPoint):

    def __init__(self):
        super().__init__()
        self.project = RedScopeProject(self.config.get_project_root())

