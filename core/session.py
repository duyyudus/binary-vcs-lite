from pathlib2 import Path
from common import util

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class Session(object):
    """
    Manage session info.

    """

    def __init__(self, session_dir):
        """
        Params
        ------
        session_dir : str or Path
            A folder store session data
        """

        super(Session, self).__init__()
        self.session_dir = Path(session_dir)
