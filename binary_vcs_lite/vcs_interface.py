from binary_vcs_lite.common.util import *
from binary_vcs_lite.core import workspace, repo


class LocalWorking(object):
    """Workspace and Repo at the same location.

    Attributes:
        _repo (core.repo.Repo):
        _workspace (core.workspace.Workspace):

    """

    def __init__(self, workspace_dir, init=0):
        super(LocalWorking, self).__init__()
        self._repo = repo.Repo(workspace_dir, init=init)
        self._workspace = workspace.Workspace(
            workspace_dir,
            self._repo,
            init=init
        )


class RemoteWorking(object):
    """Workspace and Repo at different locations.

    Attributes:
        _repo (core.repo.Repo):
        _workspace (core.workspace.Workspace):

    """

    def __init__(self, workspace_dir, repo_dir, init=0):
        super(RemoteWorking, self).__init__()
        self._repo = repo.Repo(repo_dir, init=init)
        self._workspace = workspace.Workspace(
            workspace_dir,
            self._repo,
            init=init
        )
