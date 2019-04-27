from pathlib2 import Path
from common import util, hashing

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class Workspace(object):
    """
    Manage working directory.

    Controls which files to track 
    and handle workspace-related operations

    It must connect to a `core.repo.Repo`

    """

    def __init__(self, workspace_dir, repo, init=0):
        """
        Params
        ------
        workspace_dir : str or Path
            Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`
        repo : core.repo.Repo

        """

        super(Workspace, self).__init__()
        self.workspace_dir = Path(workspace_dir)
        self._repo = repo
        self._state_header = None
        self.deep_dir = Path(self.workspace_dir, VCS_FOLDER, WORKSPACE_FOLDER)

        if init:
            self._init_deep_dir()
        else:
            assert self.deep_dir.exists(), 'Invalid Workspace folder'

    def _init_deep_dir(self):
        if not self.deep_dir.exists():
            self.deep_dir.mkdir(parents=1)

    @property
    def workspace_hash(self):
        return hashing.hash_workspace(self.workspace_dir)

    @property
    def current_state(self):
        return self._state_header

    def absolute_path(self, relative_path):
        """
        Join relative path and working dir
        """

        return Path(self.workspace_dir, relative_path)
