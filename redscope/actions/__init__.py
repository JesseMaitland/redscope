from redscope import terminal
from rambo import function_mapper, provide_func_key, provide_config


@provide_func_key()
@provide_config()
def get_action(func_key, config):
    actions = function_mapper(config, [terminal])
    try:
        return actions[func_key]
    except KeyError:
        print(f"command {func_key} has not been implemented!")
        exit()
