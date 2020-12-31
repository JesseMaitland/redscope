from redgiant.redscope.introspection.ddl import DDL


class Procedure(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        super().__init__(name=name, schema=schema, ddl=ddl)

    def file_name(self) -> str:
        return f"{self.schema}.{self.name}.sql"

    def drop(self) -> str:
        return self.drop_if_exists()

    def drop_if_exists(self) -> str:
        return f"DROP PROCEDURE IF EXISTS {self.schema}.{self.name}"

    def drop_cascade(self) -> str:
        raise NotImplementedError("dropping a PROCEDURE has no CASCADE option.")

    def create_external(self, prefix: str) -> str:
        raise NotImplementedError("a PROCEDURE cannot be created externally.")

