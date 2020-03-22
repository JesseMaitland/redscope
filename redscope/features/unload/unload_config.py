import yaml
from typing import NamedTuple, List
from pathlib import Path
from datetime import date


class UnloadConfig(NamedTuple):
    schema:                 str
    table:                  str
    ts_column:              str
    frequency:              str
    starting_from:          date
    ending_at:              date
    partition_value:        str
    partition_keys:         List[str]
    create_external_schema: bool
    external_schema_name:   str


class UnloadConfigParser:

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = yaml.safe_load(config_path.open(mode='r'))['unload_config']

    def _convert_dates(self):
        date_att_names = ['starting_from', 'ending_at']
        for date_att_name in date_att_names:
            date_to_convert = self.config.get(date_att_name)

            if date_to_convert == 'today':
                converted_date = date.today()

            else:
                date_to_convert = date_to_convert.split('-')
                converted_date = date(int(date_to_convert[0]), int(date_to_convert[1]), int(date_to_convert[2]))

            self.config[date_att_name] = converted_date

    def parse(self) -> UnloadConfig:
        self._convert_dates()
        return UnloadConfig(**self.config)
