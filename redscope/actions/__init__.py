from redscope.terminal import entry_points
from redscope.config import RAMBO_CONFIG_PATH
from rambo import function_mapper, provide_func_key, provide_config


@provide_func_key(RAMBO_CONFIG_PATH)
@provide_config(RAMBO_CONFIG_PATH)
def get_action(func_key, config):
    actions = function_mapper(config, [entry_points])
    try:
        return actions[func_key]
    except KeyError:
        print(f"command {func_key} has not been implemented!")
        exit()
