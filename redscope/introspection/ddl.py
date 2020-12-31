
class DDL:

    def __init__(self, name: str, ddl: str, schema: str = None):

        self.name = name
        self.schema = schema
        self.ddl = ddl

    def __bool__(self) -> bool:
        return True if self.name else False

    @classmethod
    def empty(cls):
        return cls('', '', '')

    def file_name(self) -> str:
        raise NotImplementedError

    def create(self) -> str:
        return self.ddl

    def drop(self) -> str:
        raise NotImplementedError

    def drop_if_exists(self) -> str:
        raise NotImplementedError

    def drop_cascade(self) -> str:
        raise NotImplementedError

    def create_external(self, prefix: str) -> str:
        raise NotImplementedError
