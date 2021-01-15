from argparse import Namespace
from redscope.project.environment import PROJECT_ROOT, SCHEMA_DIR, REDSCOPE_CONFIG_PATH


def init(cmd: Namespace) -> None:
    """
    Command initializes the redscope project where the config, and generated DDL files live.
    This command must be run as teh first step.
    """
    print("Creating redscope project....")
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    REDSCOPE_CONFIG_PATH.touch(exist_ok=True)
    print("Created Redscope Project Successfully.")
    print("Please fill in the .redscope config file with your .env file information.")
