from redscope.terminal import entry_points
from redscope import rambo_path
from rambo import function_mapper, provide_func_key, provide_config


@provide_func_key(rambo_path)
@provide_config(rambo_path)
def get_action(func_key, config):
    actions = function_mapper(config, [entry_points])
    try:
        return actions[func_key]
    except KeyError:
        print(f"command {func_key} has not been implemented!")
        exit()
