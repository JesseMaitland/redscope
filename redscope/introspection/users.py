from redscope.project.project import Folders
from redscope.database.models import Catalog
import pandas as pd


class IntroUsers:

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        self.db_connection = db_connection
        self.data = pd.DataFrame()
        self.catalog = catalog
        self.folders = folders

    def execute(self):
        self.fetch_data()
        self._set_create_user()
        self._set_paths()
        self._make_dirs()
        self._make_files()

    def fetch_data(self):
        self.data = self.catalog.fetch_users(self.db_connection)

    def _set_create_user(self):
        self.data['create_user_sql'] = self.data['user_name'].apply(lambda x: f"CREATE USER {x} WITH PASSWORD xxxxx;")

    def _set_paths(self):
        self.data['paths'] = self.data['user_name'].apply(lambda x: self.folders.users_path / x)

    def _make_dirs(self):
        self.data['paths'].apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    def _make_files(self):
        self.data.apply(lambda x: x['paths'].joinpath(f"{x['paths'].name}.sql").write_text(x['create_user_sql']), axis=1)
