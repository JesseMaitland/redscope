from configparser import ConfigParser
from argparse import Namespace

# Redscope Project deps
from redscope.project.database import fetch_and_map_query_result
from redscope.project.environment import init_redscope_env, SCHEMA_DIR
from redscope.project.database.models import Table


@init_redscope_env(provide_config=True)
def inspect(cmd: Namespace, config: ConfigParser) -> None:
    to_inspect = ['columns', 'views', 'functions', 'procedures'] if cmd.o == 'all' else [cmd.o]

    for item in to_inspect:
        print(f"Introspecting ----- {item}")
        results = fetch_and_map_query_result(config['redshift']['connection'], item)

        if item == 'columns':
            results = Table.from_columns(results)
            constraints = fetch_and_map_query_result(config['redshift']['connection'], 'constraints')

            for result in results:
                result.add_constraints(constraints)
                result.save_file(SCHEMA_DIR)
            continue

        for result in results:
            result.save_file(SCHEMA_DIR)

    print("Introspection complete. Generated DDL files saved under /redshift/redscope/schema")
