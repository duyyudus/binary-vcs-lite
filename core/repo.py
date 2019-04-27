from pathlib2 import Path
from common import util
from core import blob, state, session

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class Repo(object):
    """
    Manage version control system repository.

    Controls components
        `core.blob.Blob`
        `core.state.StateChain`
        `core.session.Session`

    """

    def __init__(self, repo_dir, init=0):
        """
        Params
        ------
        repo_dir : str or Path

        """

        super(Repo, self).__init__()
        self.repo_dir = Path(repo_dir)
        self.deep_dir = Path(self.repo_dir, VCS_FOLDER, REPO_FOLDER)

        if init:
            self._init_deep_dir()
        else:
            assert self.deep_dir.exists(), 'Invalid Repo folder'

        self.blob_dir = Path(self.deep_dir, BLOB_FOLDER)
        self.state_dir = Path(self.deep_dir, STATE_FOLDER)
        self.session_dir = Path(self.deep_dir, SESSION_FOLDER)

        self._blob = blob.Blob(self.blob_dir)
        self._state = state.StateChain(self.state_dir)
        self._session = session.Session(self.session_dir)

    def _init_deep_dir(self):
        if not self.deep_dir.exists():
            self.deep_dir.mkdir(parents=1)
