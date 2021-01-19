from configparser import ConfigParser
from argparse import Namespace

# Redscope Project deps
from redscope.project.database import fetch_and_map_query_result
from redscope.project.environment import init_redscope_env, SCHEMA_DIR
from redscope.project.database.models import Table


@init_redscope_env(provide_config=True)
def inspect(cmd: Namespace, config: ConfigParser) -> None:
    to_inspect = ['columns', 'views', 'functions', 'procedures'] if cmd.o == 'all' else [cmd.o]
    db_conn = config['redshift']['connection']
    for item in to_inspect:
        print(f"Introspecting ----- {item}")
        results = fetch_and_map_query_result(db_conn, item)

        if item == 'columns':
            results = Table.from_columns(results)
            constraints = fetch_and_map_query_result(db_conn, 'constraints')
            dist_style = fetch_and_map_query_result(db_conn, 'diststyle')
            dist_key = fetch_and_map_query_result(db_conn, 'distkey')

            for result in results:
                result.add_constraints(constraints)
                result.set_dist_style(dist_style)
                result.set_dist_keys(dist_key)
                result.save_file(SCHEMA_DIR)
            continue

        for result in results:
            result.save_file(SCHEMA_DIR)

    print("Introspection complete. Generated DDL files saved under /redshift/redscope/schema")
