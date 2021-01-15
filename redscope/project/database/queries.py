from pathlib import Path


class SqlManager:
    """
    Class is used to access the queries stored in the projects query directory. This approach
    removes the need to store SQL statements in raw python strings.
    """
    def __init__(self):
        self.root = Path(__file__).absolute().parent

    def get_query(self, name: str) -> str:
        path = self.root / "queries" / f"{name}.sql"
        return path.read_text()
