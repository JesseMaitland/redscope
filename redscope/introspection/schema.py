from typing import Tuple
from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.introspection.dbintro import DbIntro
import pandas as pd


class IntrospectSchema(DbIntro):

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        super().__init__(db_connection, catalog, folders, "schema_path", "schema_name")

    def fetch_data(self) -> Tuple[pd.DataFrame]:
        data = self.catalog.fetch_schema(self.db_connection)
        return data,

    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        df = data_frames[0]
        df['sql_string'] = df[self.sql_obj_name].apply(lambda x: f"CREATE SCHEMA IF NOT EXISTS {x};")
        return df
