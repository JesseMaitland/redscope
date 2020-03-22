from typing import Dict, Tuple
from redscope.terminal.tools.entry import EntryPoint
from redscope.features.unload import UnloadConfigManager
from redscope.env import DirContext

unload_args = {
    ('action', ): {
        'help': "the action you would like to perform",
        'choices': ['new', 'list']
    },

    ('--name', '-n'): {
        'help': "the name of the desired configuration"
    }
}


def get_unload_context() -> Tuple[DirContext, UnloadConfigManager]:
    dc = DirContext()
    ucm = UnloadConfigManager(dc.get_dir('unload_configs'))
    return dc, ucm


class UnloadEntryPoint(EntryPoint):

    def __init__(self, args_config: Dict):
        super().__init__(args_config=args_config)

    def call(self) -> None:
        func = getattr(self, self.cmd_args.action)
        func()
        exit()

    def new(self):
        dc, ucm = get_unload_context()
        ucm.new_config(self.cmd_args.name)

    def list(self):
        dc, ucm = get_unload_context()
        for c in ucm.list_configs():
            print(c)
