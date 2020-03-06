from redscope.features.schema_introspection.db_objects.ddl import DDL


class Group(DDL):

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        return f"CREATE GROUP {self.name};"

    @property
    def create_if_not_exist(self) -> str:
        return f"CREATE GROUP {self.name};"

    @property
    def drop(self) -> str:
        return f"DROP GROUP {self.name};"

    @property
    def drop_if_exist(self) -> str:
        return f"DROP GROUP {self.name};"
