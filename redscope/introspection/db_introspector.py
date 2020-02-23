import pandas as pd
from typing import Tuple
from .base_db_intro import BaseDbIntro
from redscope.database.models import Catalog
from redscope.project import Folders


class DBIntrospection(BaseDbIntro):

    db_object_names = ['groups', 'users', 'schema']

    def __init__(self, db_connection, catalog: Catalog, folders: Folders, object_name: str, sql_template: str):
        path = f"{object_name}_path"
        name = f"{object_name}_name"
        self.sql_template = sql_template
        super().__init__(db_connection, catalog, folders, path, name)

    def fetch_data(self) -> Tuple[pd.DataFrame]:
        data = self.catalog.fetch_groups(self.db_connection)
        return data,

    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        sql_df = data_frames[0]
        sql_df['sql_string'] = sql_df['group_name'].apply(lambda x: self.sql_template.format(x))
        return sql_df

