from abc import ABC, abstractmethod
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
            return self._ddl
        else:
            return f"CREATE VIEW {self.qualified_name} \n AS \n {self._ddl}"


class Procedure(UserDefinedObject):
    pass


class Function(UserDefinedObject):
    pass
