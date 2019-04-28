from common.util import *
from core import workspace, repo


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
