from argparse import Namespace
from redscope.project.environment import PROJECT_ROOT, SCHEMA_DIR, REDSCOPE_CONFIG_PATH


def init(cmd: Namespace) -> None:
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    REDSCOPE_CONFIG_PATH.touch(exist_ok=True)
    print("Created Redscope Project Successfully.")
