import dotenv
from pathlib import Path

"""
if a file name is provided, use that file, otherwise use .env
if a var name is provided use that, otherwise use REDSCOPE_DB_URL
"""


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
