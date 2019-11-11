from redscope.project.project import Folders
from redscope.database.models import Catalog
from redscope.env import load_custom_env
from redscope.database import db_connections

load_custom_env("dev.env")
conn = db_connections.default()

catalog = Catalog()

schemas = catalog.fetch_schema_data(conn)
print(schemas.head())
