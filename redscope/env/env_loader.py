import dotenv
from pathlib import Path

"""
if a file name is provided, use that file, otherwise use .env
if a var name is provided use that, otherwise use REDSCOPE_DB_URL
"""


def path_valid(env_file_path: Path) -> bool:
    if not env_file_path.exists():
        raise FileNotFoundError(f"no .env file found at {env_file_path.as_posix()}")
    return True


# TODO: Refactor these to single method which takes path argument
def load_default_env() -> bool:
    env_file_path = Path.cwd().absolute() / ".env"

    if path_valid(env_file_path):
        dotenv.load_dotenv(env_file_path)
        return True
    return False


def load_custom_env(file_name: str) -> bool:

    if not file_name:
        return False

    env_file_path = Path.cwd().absolute() / file_name
    if path_valid(env_file_path):
        dotenv.load_dotenv(env_file_path)
        return True
    return False
