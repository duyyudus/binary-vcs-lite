from pathlib2 import Path
from ruamel.yaml import YAML

_CONFIG_FILE = str(Path(__file__).parent.joinpath('config.yml'))
with open(_CONFIG_FILE, 'r') as cfg_file:
    CFG_DICT = YAML().load(cfg_file)
