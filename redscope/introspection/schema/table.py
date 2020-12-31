from typing import List
from redgiant.redscope.introspection.ddl import DDL
from .constraint import Constraint


class Table(DDL):

    def __init__(self, schema: str, name: str, ddl: str, simple_ddl: str, constraints: List[Constraint] = None):
        super().__init__(name=name, schema=schema, ddl=ddl)
        self.simple_ddl = simple_ddl
        self.constraints = constraints or []

    def file_name(self) -> str:
        return f"{self.schema}.{self.name}.sql"

    def create(self):
        return f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.name}\n(\n{self.ddl}\n{self._constraint_ddl()});"

    def drop(self) -> str:
        return self.drop_if_exists()

    def drop_if_exists(self) -> str:
        return f"DROP TABLE IF EXISTS {self.schema}{self.name};"

    def drop_cascade(self) -> str:
        return f"{self.drop_if_exists().replace(';', '')} CASCADE;"

    def create_external(self, prefix: str) -> str:
        return f"CREATE EXTERNAL TABLE IF NOT EXISTS {prefix}_{self.schema}.{self.name}\n(\n{self.ddl}\n);"

    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def _constraint_ddl(self) -> str:
        return '\n'.join([c.create() for c in self.constraints])
