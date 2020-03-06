from redscope.features.schema_introspection.db_objects.ddl import DDL


class Constraint(DDL):

    def __init__(self, name: str, schema: str, table: str, ddl: str):
        super().__init__(name)
        self.schema = schema
        self.table = table
        self._ddl = ddl

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        return f""

    @property
    def create_if_not_exist(self) -> str:
        return f""

    @property
    def drop(self) -> str:
        return f""

    @property
    def drop_if_exist(self) -> str:
        return f""

    @property
    def ddl(self) -> str:
        return f"CONSTRAINT {self.name} {self._ddl}"
