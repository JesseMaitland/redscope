from redgiant.redscope.introspection.ddl import DDL


class Ownership(DDL):

    def __init__(self, name: str, schema: str, signature: str, owner: str, db_obj_type=str):
        super().__init__(name=name, schema=schema, ddl='')
        self.owner = owner
        self.signature = signature or ''
        self.db_obj_type = db_obj_type

        if self.db_obj_type == 'view':
            self.alter_type = 'TABLE'

        elif self.db_obj_type == 'function':
            self.alter_type = 'PROCEDURE'

        else:
            self.alter_type = self.db_obj_type

    def file_name(self) -> str:
        return f"{self.schema}.{self.name}.sql"

    def create(self) -> str:
        return f"ALTER {self.alter_type.upper()} {self.schema}.{self.name}{self.signature} OWNER TO {self.owner};"

    def drop(self) -> str:
        pass

    def drop_if_exists(self) -> str:
        pass

    def drop_cascade(self) -> str:
        pass

    def create_external(self, prefix: str) -> str:
        pass
