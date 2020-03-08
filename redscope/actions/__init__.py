import redscope.features.terminal.entry_points as terminal_entry_points
import redscope.features.schema_introspection.entry_points as intro_entry_points
import redscope.features.migrations.entry_points as migration_entry_points
from redscope.config import RAMBO_CONFIG_PATH
from rambo import function_mapper, provide_func_key, provide_config


@provide_func_key(RAMBO_CONFIG_PATH)
@provide_config(RAMBO_CONFIG_PATH)
def get_action(func_key, config):
    actions = function_mapper(config, [terminal_entry_points, intro_entry_points, migration_entry_points])
    try:
        return actions[func_key]
    except KeyError:
        print(f"command {func_key} has not been implemented!")
        exit()
