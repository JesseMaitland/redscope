from redgiant.redscope.introspection.ddl import DDL


class Group(DDL):

    def __init__(self, name: str, ddl: str):
        super().__init__(name=name, ddl=ddl)

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def drop(self) -> str:
        pass

    def drop_if_exists(self) -> str:
        pass

    def drop_cascade(self) -> str:
        pass

    def create_external(self, prefix: str) -> str:
        pass
