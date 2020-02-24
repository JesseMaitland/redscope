from redscope.features.schema_introspection.db_objects.ddl import DDL


class Schema(DDL):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        return f"CREATE SCHEMA {self.name};"

    @property
    def create_if_not_exist(self) -> str:
        return f"CREATE SCHEMA IF NOT EXISTS {self.name};"

    @property
    def drop(self) -> str:
        return f"DROP SCHEMA {self.name};"

    @property
    def drop_if_exist(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.name};"

    @property
    def drop_if_exists_cascade(self) -> str:
        return f"{self.drop_if_exist} CASCADE;"
