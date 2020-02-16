from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.introspection.dbintro import DbIntro
import pandas as pd
from typing import Tuple


class IntrospectGroups(DbIntro):

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        super().__init__(db_connection, catalog, folders, "groups_path", "group_name")

    def fetch_data(self) -> Tuple[pd.DataFrame]:
        data = self.catalog.fetch_groups(self.db_connection)
        return data,

    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        groups = data_frames[0]
        groups['sql_string'] = groups['group_name'].apply(lambda x: f"CREATE GROUP {x};")
        return groups
