from redgiant.redscope.introspection.ddl import DDL


class Constraint(DDL):

    def __init__(self, name: str, schema: str, table: str, ddl: str):
        super().__init__(name=name, schema=schema, ddl=ddl)
        self.table = table

    def create(self) -> str:
        return f"CONSTRAINT {self.name} {self.ddl}"

    def file_name(self) -> str:
        raise NotImplementedError

    def drop(self) -> str:
        raise NotImplementedError

    def drop_if_exists(self) -> str:
        raise NotImplementedError

    def drop_cascade(self) -> str:
        raise NotImplementedError

    def create_external(self, prefix: str) -> str:
        raise NotImplementedError
