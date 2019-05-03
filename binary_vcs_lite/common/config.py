import sys
from ruamel.yaml import YAML
if sys.version_info[0] == 3:
    from pathlib import Path
else:
    from pathlib2 import Path

_CONFIG_FILE = str(Path(__file__).parent.joinpath('config.yml'))
with open(_CONFIG_FILE, 'r') as cfg_file:
    CFG_DICT = YAML().load(cfg_file)
