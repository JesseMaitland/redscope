from redscope.project.project import Folders
from redscope.database.models import Catalog
import pandas as pd


# TODO: refactor to inherit from DBIntro
class IntroUserGroup:

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        self.db_connection = db_connection
        self.data = pd.DataFrame()
        self.catalog = catalog
        self.folders = folders

    def execute(self):
        self.fetch_data()
        self._set_add_user_groups()
        self._group_statements()
        self._set_paths()
        self._make_dirs()
        self._make_files()

    def fetch_data(self):
        self.data = self.catalog.fetch_user_groups(self.db_connection)

    def _set_add_user_groups(self):
        self.data['add_group_sql'] = self.data.apply(lambda x: f"ALTER GROUP {x.group_name} ADD USER {x.user_name};",
                                                     axis=1)
        self.data = self.data.sort_values(by='user_name').reset_index(drop=True).reindex()

    def _group_statements(self):
        self.data = self.data.groupby(["user_name"])['add_group_sql'].apply(lambda x: '\n'.join(x)).reset_index()

    def _set_paths(self):
        self.data['paths'] = self.data['user_name'].apply(lambda x: self.folders.users_path / x)

    def _make_dirs(self):
        self.data['paths'].apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    def _make_files(self):
        self.data.apply(lambda x: x['paths'].joinpath('groups.sql').write_text(x['add_group_sql']),
                        axis=1)
