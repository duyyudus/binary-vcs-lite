from pathlib2 import Path
from common import util
from core import workspace, repo

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class LocalWorking(object):
    """Workspace and Repo at the same location."""

    def __init__(self, workspace_dir, init=0):
        super(LocalWorking, self).__init__()
        self._repo = repo.Repo(workspace_dir, init=init)
        self._workspace = workspace.Workspace(
            workspace_dir,
            self._repo,
            init=init
        )


class RemoteWorking(object):
    """Workspace and Repo at different locations."""

    def __init__(self, workspace_dir, repo_dir, init=0):
        super(RemoteWorking, self).__init__()
        self._repo = repo.Repo(repo_dir, init=init)
        self._workspace = workspace.Workspace(
            workspace_dir,
            self._repo,
            init=init
        )
