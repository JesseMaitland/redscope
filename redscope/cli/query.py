from configparser import ConfigParser
from argparse import Namespace

from redscope.project.database import fetch_and_map_query_result
from redscope.project.environment import init_redscope_env, SCHEMA_DIR


@init_redscope_env(provide_config=True)
def query(cmd: Namespace, config: ConfigParser) -> None:

    results = fetch_and_map_query_result(connection_name=config['redshift']['connection'], query_name=cmd.kind)

    for result in results:
        result.save_file(SCHEMA_DIR)
