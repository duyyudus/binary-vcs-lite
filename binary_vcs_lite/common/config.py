import sys
from ruamel.yaml import YAML
if sys.version_info[0] == 3:
    from pathlib import Path
else:
    from pathlib2 import Path

_CONFIG_FILE = str(Path(__file__).resolve().parent.joinpath('config.yml'))
with open(_CONFIG_FILE, 'r') as cfg_file:
    CFG_DICT = YAML().load(cfg_file)

VCS_FOLDER = CFG_DICT['VCS_FOLDER']

WORKSPACE = CFG_DICT['WORKSPACE']
WORKSPACE_HASH = CFG_DICT['WORKSPACE_HASH']

REPO = CFG_DICT['REPO']
BLOB = CFG_DICT['BLOB']
STATE = CFG_DICT['STATE']
SESSION = CFG_DICT['SESSION']

DEFAULT_FILE_PATTERN = CFG_DICT['DEFAULT_FILE_PATTERN']

LOG_PREFIX = CFG_DICT['LOG_PREFIX']
LOG_FOLDER = CFG_DICT['LOG_FOLDER']
