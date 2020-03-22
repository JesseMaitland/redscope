from pathlib import Path

args_config = {
    ('--env-file', '-ef'): {
        'help': "the name of the .env file you would like to load. Must be located in the project root. Defaults to .env",
        'default': Path.cwd() / ".env",
        'dest': 'env_file'
    },

    ('--env-var', '-ev'): {
        'help': "The environment variable which contains your database connection string. Defaults to REDSCOPE_DB_URL",
        'default': "REDSCOPE_DB_URL",
        'dest': 'env_var'
    }
}


def main_introspection():
    from redscope.features.schema_introspection.entrypoints import intro_args, IntrospectDbEntryPoint
    args_config.update(intro_args)
    IntrospectDbEntryPoint(args_config=args_config).call()


def main_migration():
    from redscope.features.migrations.entrypoints import migration_args, MigrationsEntryPoint
    args_config.update(migration_args)
    MigrationsEntryPoint(args_config=args_config).call()


def main_project_init():
    from redscope.features.project.entrypoints import project_args, InitProjectEntryPoint
    args_config.update(project_args)
    InitProjectEntryPoint(args_config=args_config).call()
