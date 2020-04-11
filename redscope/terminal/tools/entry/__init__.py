import dotenv
import os
import psycopg2
from configparser import ConfigParser
from typing import Dict
from pathlib import Path
from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser
from redscope.config import DEFAULT_DB_URL


def parse_redscope_config() -> Dict:
    redscope_config = Path.cwd().absolute() / ".redscope"

    if redscope_config.exists():
        config = ConfigParser()
        config.read(redscope_config)
        return config


def parse_terminal_args(args_config: Dict) -> Namespace:
    arg_parser = ArgumentParser()

    for command, options in args_config.items():
        arg_parser.add_argument(*command, **options)
    return arg_parser.parse_args()


def env_path_valid(env_file_path: Path) -> bool:
    if not env_file_path.exists():
        raise FileNotFoundError(f"no .env file found at {env_file_path.as_posix()}")
    return True


def load_redscope_env(file_name: str = ''):
    env_file_path = Path.cwd().absolute()
    if file_name:
        env_file_path = env_file_path / file_name
    else:
        env_file_path = env_file_path / '.env'

    if env_path_valid(env_file_path):
        dotenv.load_dotenv(env_file_path)


def db_connection_exists(db_connection_string: str, connection_name: str = DEFAULT_DB_URL) -> bool:
    if not db_connection_string:
        raise EnvironmentError(f"no connection string found in .env for {connection_name}")
    return True


def get_db_connection(connection_name: str = '') -> psycopg2.connect:
    db_connection_string = os.getenv(connection_name) or os.getenv(DEFAULT_DB_URL)
    if db_connection_exists(db_connection_string, connection_name):
        return psycopg2.connect(db_connection_string)


class EntryPoint(ABC):

    def __init__(self, args_config: Dict):
        self.cmd_args: Namespace = parse_terminal_args(args_config)
        self.config = parse_redscope_config() or {}
        self.db_connection = None

        try:
            self.env_file_name = self.config['environment']['env_file_name']
        except KeyError:
            self.env_file_name = self.cmd_args.env_file

        try:
            self.env_var_name = self.config['environment']['env_var_name']
        except KeyError:
            self.env_var_name = self.cmd_args.env_var

        load_redscope_env(Path.cwd() / self.env_file_name)

    @abstractmethod
    def call(self) -> None:
        pass

    def set_db_connection(self):
        self.db_connection = get_db_connection(self.env_var_name)
