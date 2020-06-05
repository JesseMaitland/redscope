from typing import List
from redscope.features.schema_introspection.db_objects.ddl import DDL
from .constraint import Constraint


class Table(DDL):

    def __init__(self, schema: str, name: str, ddl: str, constraints: List[Constraint] = None):
        super().__init__(name)
        self.schema = schema
        self.ddl = ddl
        self.constraints = constraints or []

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        if self.constraints:
            return f"CREATE TABLE {self.full_name} \n(\n{self.ddl},\n {self.constraint_ddl}\n);"
        else:
            return f"CREATE TABLE {self.full_name} \n(\n{self.ddl}\n);"

    @property
    def create_if_not_exist(self) -> str:
        if self.constraints:
            return f"CREATE TABLE IF NOT EXISTS {self.full_name} \n(\n{self.ddl},\n {self.constraint_ddl}\n);"
        else:
            return f"CREATE TABLE IF NOT EXISTS {self.full_name} \n(\n{self.ddl}\n);"

    def create_external_table(self, schema: str = None) -> str:
        schema = schema or self.schema
        return f"CREATE EXTERNAL TABLE IF NOT EXISTS {schema}.{self.name} \n(\n{self.simple_ddl}\n);"

    @property
    def drop(self) -> str:
        return f"DROP TABLE {self.full_name};"

    @property
    def drop_if_exist(self) -> str:
        return f"DROP TABLE IF EXISTS {self.full_name};"

    @property
    def constraint_ddl(self) -> str:
        return '\n'.join([c.ddl for c in self.constraints])

    @property
    def simple_ddl(self) -> str:
        lines_to_keep = []
        ddl_lines = self.ddl.split('\n')

        for line in ddl_lines:
            to_keep = line
            to_keep = to_keep.rstrip(',')

            if 'CONSTRAINT' in to_keep:
                continue

            to_keep = to_keep.split('DEFAULT')[0].rstrip()
            to_keep = to_keep.split('NOT NULL')[0].rstrip()
            to_keep = to_keep.split('ENCODE')[0].rstrip()

            lines_to_keep.append(to_keep)

        lines_to_keep = [l + ',' if i < len(lines_to_keep) - 1 else l for i, l in enumerate(lines_to_keep)]
        columns = '\n'.join(lines_to_keep)
        return f"CREATE TABLE IF NOT EXISTS {self.full_name}\n(\n{columns}\n);"

    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)
