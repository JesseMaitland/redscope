from abc import ABC, abstractmethod
from typing import Tuple
from redscope.project.project import Folders
from redscope.database.models import Catalog
import pandas as pd


class DbIntro(ABC):

    def __init__(self, db_connection, catalog: Catalog, folders: Folders, root_path: str, sql_obj_name: str):
        self.catalog = catalog
        self.folders = folders
        self.db_connection = db_connection
        self.root_path = getattr(self.folders, root_path, None)
        self.sql_obj_name = sql_obj_name

    def introspect_and_save_files(self):
        frames = self.fetch_data()
        final_frame = self.construct_sql(*frames)
        final_frame = self.make_paths(final_frame)
        self.make_dirs(final_frame)
        self.save_files(final_frame)

    def get_sql(self):
        frames = self.fetch_data()
        return self.construct_sql(*frames)

    @abstractmethod
    def fetch_data(self) -> Tuple[pd.DataFrame]:
        pass

    @abstractmethod
    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        pass

    def make_paths(self, final_frame: pd.DataFrame) -> pd.DataFrame:
        final_frame['paths'] = final_frame[self.sql_obj_name].apply(lambda x: self.root_path / x)
        return final_frame

    @staticmethod
    def make_dirs(final_frame: pd.DataFrame):
        final_frame.paths.apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    @staticmethod
    def save_files(final_frame: pd.DataFrame):
        final_frame.apply(
            lambda x: x['paths'].joinpath(f"{x['paths'].name}.sql").write_text(x['sql_string']), axis=1)
