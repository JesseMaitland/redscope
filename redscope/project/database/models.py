import sqlparse
from abc import ABC, abstractmethod
from typing import List, Tuple
from itertools import groupby
from pathlib import Path


class DDL(ABC):

    def __init__(self, schema: str, name: str) -> None:
        self._schema = schema
        self._name = name

    @property
    def schema(self) -> str:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @property
    def qualified_name(self) -> str:
        return f"{self._schema}.{self._name}"

    @property
    def file_path(self) -> Path:
        return Path(self._schema) / f"{self.__class__.__name__.lower()}s" / f"{self.qualified_name}.sql"

    @abstractmethod
    def ddl(self) -> str:
        pass

    def save_file(self, root_path: Path) -> None:
        path = root_path / self.file_path.as_posix()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(self.ddl())


class Schema(DDL):

    def __init__(self, name: str) -> None:
        super(Schema, self).__init__(name=name, schema=name)

    @property
    def qualified_name(self) -> str:
        return self._name

    @property
    def file_path(self) -> Path:
        return Path(self._schema) / f"{self.qualified_name}.sql"

    def ddl(self) -> str:
        return f"CREATE SCHEMA IF NOT EXISTS {self.name};"


class UserDefinedObject(DDL):

    def __init__(self, schema: str, name: str, ddl: str) -> None:
        super(UserDefinedObject, self).__init__(schema=schema, name=name)
        self._ddl = ddl

    def ddl(self) -> str:
        return self._ddl


class View(UserDefinedObject):

    def ddl(self) -> str:
        if 'CREATE VIEW' in self._ddl:
            return sqlparse.format(self._ddl, reindent_aligned=True)
        else:
            return sqlparse.format(f"CREATE VIEW {self.qualified_name} \n AS \n {self._ddl}", reindent_aligned=True)


class Procedure(UserDefinedObject):
    pass


class Function(UserDefinedObject):
    pass


class Column(DDL):

    def __init__(self, schema: str, name: str, table: str, index: int, data_type: str, default: str, not_null: str,
                 encoding: str) -> None:
        super(Column, self).__init__(schema=schema, name=name)
        self.table = table
        self.index = index
        self.data_type = data_type
        self.default = default
        self.not_null = not_null
        self.encoding = encoding

    @property
    def offset(self) -> int:
        return len(self.name)

    def ddl(self) -> str:
        return f"{self.name} {self.data_type} {self.not_null} {self.default} {self.encoding}"

    def format_ddl(self, padding: int) -> str:
        return f"   {self.name} {' ' * (padding - self.offset)}" \
               f"{self.data_type} {self.not_null} {self.default} {self.encoding}"


class Constraint(DDL):

    def __init__(self, name: str, schema: str, table: str, column: str, ddl: str):
        super(Constraint, self).__init__(name=name, schema=schema)
        self.table = table
        self._ddl = ddl
        self._column = column

    def ddl(self) -> str:
        return f"CONSTRAINT {self.name} {self._ddl}"

    def format_ddl(self) -> str:
        return f"   CONSTRAINT {self.name} {self._ddl}"


class Table(DDL):

    def __init__(self, schema: str, name: str, columns: List[Column] = None,
                 constraints: List[Constraint] = None) -> None:
        super(Table, self).__init__(schema=schema, name=name)
        self.columns = columns or []
        self.format_offset = max(columns, key=lambda x: x.offset).offset
        self.constraints = constraints or []

    def column_ddl(self) -> str:
        return ',\n'.join([c.format_ddl(self.format_offset) for c in self.columns])

    def constraint_ddl(self) -> str:
        return ',\n'.join([c.format_ddl() for c in self.constraints])

    def ddl(self) -> str:
        column_ddl = self.column_ddl()

        if self.constraints:
            constraints = self.constraint_ddl() + '\n'
            column_ddl = column_ddl + ','
        else:
            constraints = ''

        return f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.name}\n(\n{column_ddl}\n{constraints});"

    @classmethod
    def from_columns(cls, columns: List[Column]) -> List['Table']:
        columns = cls.group_columns(columns)
        tables = []
        for table, cols in columns.items():
            schema, name = table.split('.')[:2]
            tables.append(cls(schema, name, cols))
        return tables

    @staticmethod
    def grouping_key(column: Column) -> Tuple[str]:
        return column.schema, column.table

    @staticmethod
    def group_columns(columns: List[Column]):

        sorted_ddl = sorted(columns, key=Table.grouping_key)
        groups = {}
        for key, group in groupby(sorted_ddl, key=Table.grouping_key):
            groups[f"{key[0]}.{key[1]}"] = list(group)

        # keeps the column order as defined in the db
        for group in groups.values():
            group.sort(key=lambda x: x.index)
        return groups

    def add_constraints(self, constraints: List[Constraint]) -> None:
        for constraint in constraints:
            if constraint.schema == self.schema and constraint.table == self.name:
                self.constraints.append(constraint)
