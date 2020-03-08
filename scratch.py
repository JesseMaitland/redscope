from redscope.env.project_context import DirContext
from redscope.features.migrations.migration_manager import MigrationManager, MigrationParser


dc = DirContext()
mm = MigrationManager(dc.get_dir('migrations'))
mig = mm.get_migration('foo')

print(mig.up)
print(mig.down)
