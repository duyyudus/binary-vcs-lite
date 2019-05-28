from binary_vcs_lite.common.util import *
from binary_vcs_lite.core.workspace import Workspace
from binary_vcs_lite.core.repo import Repo


class VersioningInterface(object):
    """Main interface to run version control operations.

    Attributes:
        _repo (core.repo.Repo):
        _workspace (core.workspace.Workspace):

    Properties:
        repo (core.repo.Repo):
        workspace (core.workspace.Workspace):
    """

    def __init__(self, workspace_dir, repo_dir, init_workspace, init_repo):
        """
        Args:
            workspace_dir (Path):
            repo_dir (Path):
            init_workspace (bool):
            init_repo (bool):
        """
        super(VersioningInterface, self).__init__()

    @property
    def repo(self):
        return self._repo

    @property
    def workspace(self):
        return self._workspace

    def set_file_pattern(self, file_pattern):
        """Wrap same method in `self._workspace`

        Args:
            file_pattern (dict):
        """
        pass

    def commit(self, session_list, data, add_only, fast_forward):
        """Wrap same method in `self._workspace`

        Args:
            session_list (list of str):
            data (dict):
            add_only (bool):
            fast_forward (bool):
        """
        pass

    def checkout(self, session_id, revision, checkout_dir=None, overwrite=False):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str):
            revision (int|str):
            checkout_dir (Path, None by default):
            overwrite (bool, False by default):
        """
        pass

    def latest_revision(self, session_id):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str)

        Returns:
            int:
        """
        pass

    def all_revision(self, session_id):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str):

        Returns:
            list of int:
        """
        pass

    def all_session(self):
        """Wrap same method in `self._workspace`

        Returns:
            list of str:
        """
        pass

    def detail_file_version(self, session_id, revision, relative_path):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        pass


class LocalVersioning(VersioningInterface):
    """Workspace and Repo at the same location.

    """

    def __init__(self, workspace_dir):
        super(LocalVersioning, self).__init__(
            workspace_dir, workspace_dir, init_workspace=1, init_repo=1
        )


class RemoteVersioning(VersioningInterface):
    """Workspace and Repo at different locations.

    """

    def __init__(self, workspace_dir, repo_dir):
        super(RemoteVersioning, self).__init__(
            workspace_dir, repo_dir, init_workspace=1, init_repo=1
        )
