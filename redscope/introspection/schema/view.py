from redgiant.redscope.introspection.ddl import DDL


class View(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        super().__init__(name=name, schema=schema, ddl=ddl)

    def file_name(self) -> str:
        return f"{self.schema}.{self.name}.sql"

    def drop(self) -> str:
        pass

    def drop_if_exists(self) -> str:
        pass

    def drop_cascade(self) -> str:
        pass

    def create_external(self) -> str:
        pass

