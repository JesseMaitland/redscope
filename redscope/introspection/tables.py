# flake8: noqa
from itertools import groupby
from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.introspection.dbintro import DbIntro
from typing import Tuple, List
import pandas as pd


class Table:

    def __init__(self, schema: str, name: str, ddl: str):
        self.schema = schema
        self.name = name
        self.ddl = ddl

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"

    @property
    def short_file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def long_file_name(self) -> str:
        return f"{self.full_name}.sql"

    @property
    def simple_ddl(self) -> str:
        lines_to_keep = []
        ddl_lines = self.ddl.split('\n')

        for line in ddl_lines:
            to_keep = line
            if 'CONSTRAINT' in line:
                continue

            elif 'DEFAULT' in line:
                to_keep = line.split('DEFAULT')[0].rstrip() + ','
                lines_to_keep.append(to_keep)

            elif 'NOT NULL' in line:
                to_keep = line.split('NOT NULL')[0].rstrip() + ','
                lines_to_keep.append(to_keep)

            else:
                lines_to_keep.append(to_keep)

        lines_to_keep[-2] = lines_to_keep[-2].rstrip(',')

        return '\n'.join(lines_to_keep)

    @property
    def drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.full_name};"

    @property
    def simple_ddl_drop(self) -> str:
        drop = self.drop_table + "\n"
        drop = drop + self.simple_ddl
        return drop

    @property
    def ddl_not_exist(self) -> str:
        ddl = self.simple_ddl
        ddl = ddl.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
        return ddl

    def get_external_table(self, schema: str) -> str:
        ddl = self.simple_ddl
        ddl = ddl.replace('CREATE TABLE', 'CREATE EXTERNAL TABLE')
        ddl = ddl.replace(f"{self.schema}.", f"{schema}.")
        return ddl


class Schema:

    def __init__(self, name: str, tables: List[Table]):
        self.name = name
        self.tables = tables

    @classmethod
    def create_schemas(cls, tables: List[Table]) -> List['Schema']:
        srt_key = lambda x: x.schema
        tables.sort(key=srt_key)
        gb = groupby(tables, key=srt_key)
        gb = {x[0]: [t for t in x[1]] for x in gb}
        return [cls(key, value) for key, value in gb.items()]


class SchemaCatalog:

    def __init__(self, schemas: List[Schema]):
        self._catalog = {s.name: {t.name: t for t in s.tables} for s in schemas}

    @property
    def schemas(self) -> List[str]:
        return [s for s in self._catalog.keys()]

    def get_table(self, schema: str, table: str) -> Table:
        return self._catalog[schema][table]

    def get_tables(self, schema: str):
        return self._catalog[schema]

    def get_table_list(self, schema: str):
        tables = self._catalog[schema]
        return [v for k, v in tables.items()]


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

    def get_schema_catalog(self):
        sql = self.construct_sql(*self.fetch_data())
        tables = sql.apply(lambda x: Table(schema=x.schema_name, name=x.table_name, ddl=x.sql_string), axis=1).to_list()
        schemas = Schema.create_schemas(tables)
        return SchemaCatalog(schemas)
