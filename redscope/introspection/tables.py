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
        self._make_constraint_sql()

        self._format_sql()
        self._set_new_columns()
        self._set_default_and_null()
        self._nan_to_mt_string()
        self._make_column_sql()
        self._remove_whitespace()
        self._group_by_table()
        self._merge_tables_and_constraints()
        self._nan_to_mt_string()
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
        self.tables['data_type'] = self.tables['data_type'].str.replace('character varying', 'VARCHAR')
        self.tables['data_type'] = self.tables['data_type'].str.replace('character', 'CHAR')
        self.tables['data_type'] = self.tables['data_type'].str.replace('integer', 'INT')
        # self.table_const['data_type'] = self.table_const['data_type'].str.replace('timestamp without time zone',
        #                                                                           'TIMESTAMP')
        # self.table_const['data_type'] = self.table_const['data_type'].str.replace('timestamp with time zone',
        #                                                                           'TIMESTAMPZ')
        self.tables['data_type'] = self.tables['data_type'].str.upper()

    def _set_new_columns(self):
        self.tables['sql_null'] = pd.np.nan
        self.tables['dflt_sql'] = pd.np.nan
        self.tables['col_sql'] = pd.np.nan

    def _set_default_and_null(self):
        self.tables.loc[self.tables['not_null'] == True, 'sql_null'] = "NOT NULL"
        self.tables.loc[self.tables['has_default'] == True, 'dflt_sql'] = "DEFAULT"

    def _make_constraint_sql(self):
        self.const['const_sql'] = ",\nCONSTRAINT " + self.const['con_name'] + " " + self.const['con_def']

    def _nan_to_mt_string(self):
        self.tables = self.tables.fillna('')
        self.table_const = self.table_const.fillna('')

    def _remove_whitespace(self):
        self.tables['col_sql'] = self.tables['col_sql'].str.strip()
        self.const['const_sql'] = self.const['const_sql'].str.strip()

    def _make_column_sql(self):
        self.tables['col_sql'] = self.tables['column_name'] + ' ' + self.tables['data_type'] + ' ' + \
                                 self.tables['sql_null'] + ' ' + \
                                 self.tables['dflt_sql'] + ' ' + self.tables['default_value']

    def _group_by_table(self):
        print(self.tables.info())
        self.tables = self.tables.groupby(['schema_name', 'table_name'])['col_sql'].apply(
            ',\n'.join).reset_index()

    def _set_create_table(self):
        self.table_const['create_table'] = self.table_const.apply(
            lambda x: f"CREATE TABLE {x['schema_name']}.{x['table_name']}\n(\n{x['col_sql']} {x['const_sql']}\n);", axis=1)

    def _set_paths(self):
        self.table_const['paths'] = self.table_const['schema_name'].apply(
            lambda x: self.folders.schema_path / x / "tables")

    def _make_dirs(self):
        self.table_const['paths'].apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    def _make_files(self):
        self.table_const.apply(
            lambda x: x['paths'].joinpath(f"{x['schema_name']}.{x['table_name']}.sql").write_text(x['create_table']),
            axis=1)
