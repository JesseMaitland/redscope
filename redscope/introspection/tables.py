from redscope.project.project import Folders
from redscope.database.models import Catalog
import pandas as pd


class IntroTables:

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        self.db_connection = db_connection
        self.tables = pd.DataFrame()
        self.const = pd.DataFrame()
        self.table_const = pd.DataFrame()
        self.catalog = catalog
        self.folders = folders

    def execute(self):
        self.fetch_data()
        self._merge_tables_and_constraints()
        self._format_sql()
        self._set_new_columns()
        self._set_default_and_null()
        self._nan_to_mt_string()
        self._make_column_sql()
        self._remove_whitespace()
        self._group_by_table()
        self._set_create_table()
        self._set_paths()
        self._make_dirs()
        self._make_files()

    def fetch_data(self):
        self.tables = self.catalog.fetch_tables(self.db_connection)
        self.const = self.catalog.fetch_constraints(self.db_connection)

    def _merge_tables_and_constraints(self):
        self.table_const = self.tables.merge(self.const, how='left')

    def _format_sql(self):
        self.table_const['data_type'] = self.table_const['data_type'].str.replace('character varying', 'VARCHAR')
        self.table_const['data_type'] = self.table_const['data_type'].str.replace('character', 'CHAR')
        self.table_const['data_type'] = self.table_const['data_type'].str.replace('integer', 'INT')
        self.table_const['data_type'] = self.table_const['data_type'].str.replace('timestamp without time zone',
                                                                                  'TIMESTAMP')
        self.table_const['data_type'] = self.table_const['data_type'].str.replace('timestamp with time zone',
                                                                                  'TIMESTAMPZ')
        self.table_const['data_type'] = self.table_const['data_type'].str.upper()

    def _set_new_columns(self):
        self.table_const['sql_null'] = pd.np.nan
        self.table_const['dflt_sql'] = pd.np.nan
        self.table_const['col_sql'] = pd.np.nan

    def _set_default_and_null(self):
        self.table_const.loc[self.table_const['not_null'] == True, 'sql_null'] = "NOT NULL"
        self.table_const.loc[self.table_const['has_default'] == True, 'dflt_sql'] = "DEFAULT"

    def _nan_to_mt_string(self):
        self.table_const = self.table_const.fillna('')

    def _remove_whitespace(self):
        self.table_const['col_sql'] = self.table_const['col_sql'].str.strip()

    def _make_column_sql(self):
        self.table_const['col_sql'] = self.table_const['column_name'] + ' ' + self.table_const['data_type'] + ' ' + \
                                      self.table_const['sql_null'] + ' ' + \
                                      self.table_const['dflt_sql'] + ' ' + self.table_const['default_value'] + ' ' + \
                                      self.table_const['con_def']

    def _group_by_table(self):
        self.table_const = self.table_const.groupby(['schema_name', 'table_name'])['col_sql'].apply(
            ',\n'.join).reset_index()

    def _set_create_table(self):
        self.table_const['create_table'] = self.table_const.apply(
            lambda x: f"CREATE TABLE {x['schema_name']}.{x['table_name']}(\n{x['col_sql']});", axis=1)

    def _set_paths(self):
        self.table_const['paths'] = self.table_const['schema_name'].apply(lambda x: self.folders.schema_path / x / "tables")

    def _make_dirs(self):
        self.table_const['paths'].apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    def _make_files(self):
        self.table_const.apply(
            lambda x: x['paths'].joinpath(f"{x['schema_name']}.{x['table_name']}.sql").write_text(x['create_table']), axis=1)
