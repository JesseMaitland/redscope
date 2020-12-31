from redgiant.redscope.introspection.ddl import DDL


class User(DDL):

    def __init__(self, name: str, ddl: str) -> None:
        super().__init__(name=name, ddl=ddl)

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def create(self) -> str:
        return f"CREATE USER {self.name} WITH PASSWORD xxxx;"

    def drop(self) -> str:
        return self.drop_if_exists()

    def drop_if_exists(self) -> str:
        return f"DROP USER IF EXISTS {self.name};"

    def drop_cascade(self) -> str:
        raise NotImplementedError("a USER cannot use the CASCADE option.")

    def create_external(self, prefix: str) -> str:
        raise NotImplementedError("a USER cannot be created externally.")
