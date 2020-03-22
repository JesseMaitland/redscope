from pathlib import Path
from typing import List
from redscope.features.unload.unload_config import UnloadConfig, UnloadConfigParser


class UnloadConfigManager:

    template_path = Path(__file__).parent.absolute() / 'unload_config_template.yml'

    def __init__(self, unload_dir: Path):
        self.unload_dir = unload_dir

    @staticmethod
    def generate_file_name(name: str) -> str:
        return f"{name}.yml"

    def new_config(self, name: str) -> None:
        new_config_path = self.unload_dir / self.generate_file_name(name)
        new_config_path.touch(exist_ok=True)
        template = self.template_path.read_text()
        new_config_path.write_text(template)

    def list_configs(self) -> List[UnloadConfig]:
        configs = []
        for unload_config_path in self.unload_dir.glob('**/*.yml'):
            print(unload_config_path)
            configs.append(UnloadConfigParser(unload_config_path).parse())
        return configs
