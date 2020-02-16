from typing import Tuple

from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.introspection.dbintro import DbIntro
import pandas as pd


class IntrospectUsers(DbIntro):

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        super().__init__(db_connection, catalog, folders, "users_path", "user_name")

    def fetch_data(self) -> Tuple[pd.DataFrame]:
        users = self.catalog.fetch_users(self.db_connection)
        return users,

    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        users = data_frames[0]
        users['sql_string'] = users['user_name'].apply(lambda x: f"CREATE USER {x} WITH PASSWORD xxxxx;")
        return users
