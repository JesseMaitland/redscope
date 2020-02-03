from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.introspection import DbIntro
from typing import Tuple
import pandas as pd


class Table:

    def __init__(self, schema: str, table: str, ddl: str):
        self.schema = schema
        self.table = table
        self.ddl = ddl



class TableCatalog:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            super().__setattr__(key, value)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        else:
            raise AttributeError(f"{self.__class__.__name__} does not have attribute {item}")

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            self.__dict__[key] = value
        else:
            super().__setattr__(key, value)

    @classmethod
    def make_catalog(cls, ddl: pd.DataFrame) -> 'TableCatalog':
        Table(schema=ddl['schema_name'], table=ddl['table_name'], ddl=ddl['sql_string'])



# TODO: The column order is not always the same. Needs to be fixed.
class IntrospectTables(DbIntro):

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        super().__init__(db_connection, catalog, folders, "schema_path", "table_name")

    def fetch_data(self) -> Tuple[pd.DataFrame]:
        tables = self.catalog.fetch_tables(self.db_connection)
        constraints = self.catalog.fetch_constraints(self.db_connection)
        return tables, constraints

    def construct_sql(self, *data_frames: Tuple[pd.DataFrame]) -> pd.DataFrame:
        tables = data_frames[0]
        tables = self.format_table_dtypes(tables)
        tables = self.set_new_columns(tables)
        tables = self.set_default_and_null(tables)
        tables = tables.fillna('')
        tables = self.make_column_sql(tables)
        tables['col_sql'] = tables['col_sql'].str.strip()
        tables = self.group_by_table(tables)

        constraints = data_frames[1]
        constraints = self.make_constraint_sql(constraints)
        constraints = constraints.fillna('')
        constraints['constraint_sql'] = constraints['constraint_sql'].str.strip()

        tables = self.merge_tables_and_constraints(constraints, tables)
        tables = self.set_create_table(tables)
        return tables

    @staticmethod
    def merge_tables_and_constraints(tables: pd.DataFrame, constraints: pd.DataFrame):
        df = pd.merge(constraints, tables, how='left')
        df['constraint_sql'] = df['constraint_sql'].fillna('')
        return df

    @staticmethod
    def make_constraint_sql(constraints: pd.DataFrame) -> pd.DataFrame:
        constraints['constraint_sql'] = ",\nCONSTRAINT " + constraints['con_name'] + " " + constraints['con_def']
        return constraints

    @staticmethod
    def format_table_dtypes(tables: pd.DataFrame) -> pd.DataFrame:
        tables['data_type'] = tables['data_type'].str.replace('character varying', 'VARCHAR')
        tables['data_type'] = tables['data_type'].str.replace('character', 'CHAR')
        tables['data_type'] = tables['data_type'].str.replace('integer', 'INT')
        tables['data_type'] = tables['data_type'].str.upper()
        return tables

    @staticmethod
    def set_new_columns(tables: pd.DataFrame) -> pd.DataFrame:
        tables['sql_null'] = pd.np.nan
        tables['dflt_sql'] = pd.np.nan
        tables['col_sql'] = pd.np.nan
        tables['sql_string'] = pd.np.nan
        return tables

    @staticmethod
    def set_default_and_null(tables: pd.DataFrame) -> pd.DataFrame:
        tables.loc[tables['not_null'] == True, 'sql_null'] = "NOT NULL"
        tables.loc[tables['has_default'] == True, 'dflt_sql'] = "DEFAULT"
        return tables

    @staticmethod
    def make_column_sql(tables: pd.DataFrame) -> pd.DataFrame:
        tables['col_sql'] = tables['column_name'] + ' ' + tables['data_type'] + ' ' + \
                            tables['sql_null'] + ' ' + \
                            tables['dflt_sql'] + ' ' + tables['default_value']
        return tables

    @staticmethod
    def group_by_table(tables: pd.DataFrame) -> pd.DataFrame:
        tables = tables.groupby(['schema_name', 'table_name'])['col_sql'].apply(',\n'.join).reset_index()
        return tables

    @staticmethod
    def set_create_table(tables: pd.DataFrame) -> pd.DataFrame:
        tables['sql_string'] = tables.apply(
            lambda x: f"CREATE TABLE {x['schema_name']}.{x['table_name']}\n(\n{x['col_sql']} {x['constraint_sql']}\n);",
            axis=1)
        return tables

    def make_paths(self, tables: pd.DataFrame) -> pd.DataFrame:
        tables['paths'] = tables['schema_name'].apply(lambda x: self.root_path / x / "tables")
        return tables

    def save_files(self, tables: pd.DataFrame) -> pd.DataFrame:
        tables.apply(lambda x: x['paths'].joinpath(f"{x['table_name']}.sql").write_text(x['sql_string']), axis=1)
        return tables
