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
        current_session (str):
        current_revision (int):
        is_dirty (bool):

    Methods:
        set_file_pattern(file_pattern)
        commit(session_list, data, add_only, fast_forward)
        checkout(session_id, revision, checkout_dir=None, overwrite=False)
        latest_revision(session_id)
        all_revision(session_id)
        all_session()
        detail_file_version(session_id, revision, relative_path)
        ls_changes()
        compare_revision(session_1, revision_1, session_2, revision_2)
    """

    def __init__(self, workspace_dir, repo_dir, session_id, init_workspace, init_repo):
        """
        Args:
            workspace_dir (str|Path):
            repo_dir (str|Path):
            session_id (str):
            init_workspace (bool):
            init_repo (bool):
        """
        super(VersioningInterface, self).__init__()
        check_type(workspace_dir, [str, Path])
        check_type(repo_dir, [str, Path])
        check_type(session_id, [str])

        self._repo = Repo(repo_dir, init_repo)
        self._workspace = Workspace(workspace_dir, self._repo, session_id, init_workspace)

    @property
    def repo(self):
        """Repo: """
        return self._repo

    @property
    def workspace(self):
        """Workspace: """
        return self._workspace

    @property
    def current_session(self):
        """str: return ID of current session in `self._workspace`."""
        return self._workspace.session_id

    @property
    def current_revision(self):
        """int: """
        return self._workspace.revision

    @property
    def is_dirty(self):
        """bool: check if there is any change between current workspace and current revision of current session."""
        return self._workspace.is_dirty

    def set_file_pattern(self, file_pattern):
        """Wrap same method in `self._workspace`

        Args:
            file_pattern (dict):
        """
        self._workspace.set_file_pattern(file_pattern)

    def commit(self, session_list, data, add_only, fast_forward):
        """Wrap same method in `self._workspace`

        For all files match file pattern in workspace folder, commit them to repository

        Args:
            session_list (list of str):
            data (dict):
            add_only (bool):
            fast_forward (bool):
        """
        self._workspace.commit(session_list, data, add_only, fast_forward)

    def checkout(self, session_id, revision, checkout_dir=None, overwrite=False):
        """Wrap same method in `self._workspace`

        Checkout all files belong to `session_id` and `revision` to workspace folder

        Args:
            session_id (str):
            revision (int|str):
            checkout_dir (Path, None by default):
            overwrite (bool, False by default):
        """
        self._workspace.checkout(session_id, revision, checkout_dir, overwrite)

    def latest_revision(self, session_id):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str)

        Returns:
            int:
        """
        return self._workspace.latest_revision(session_id)

    def all_revision(self, session_id):
        """Wrap same method in `self._workspace`

        All revisions of provided session

        Args:
            session_id (str):

        Returns:
            list of int:
        """
        return self._workspace.all_revision(session_id)

    def all_session(self):
        """Wrap same method in `self._workspace`

        All sessions in repo which we are connecting to

        Returns:
            list of str:
        """
        return self._workspace.all_session()

    def detail_file_version(self, session_id, revision=None, relative_path=None):
        """Wrap same method in `self._workspace`

        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        return self._workspace.detail_file_version(session_id, revision, relative_path)

    def ls_changes(self):
        """Wrap same method in `self._workspace`

        Detect changes between current workspace and latest revision of current session

        Returns:
            dict:
        """
        return self._workspace.ls_changes()

    def compare_revision(self, session_1, revision_1, session_2, revision_2):
        """Wrap same method in `self._workspace`

        Return difference from one revision of session 2 to another revision of session 1
        Equally as the transition from one revision of session 1 to one revision of session 2

        Args:
            session_1 (str): ID of session 1
            revision_1 (int): revision of session 1
            session_2 (str): ID of session 2
            revision_2 (int): revision of session 2

        Returns:
            dict:
        """
        return self._workspace.compare_revision(session_1, revision_1, session_2, revision_2)


class LocalVersioning(VersioningInterface):
    """Workspace and Repo at the same location.

    """

    def __init__(self, workspace_dir, session_id):
        """
        Args:
            workspace_dir (str|Path):
            session_id (str):
        """
        super(LocalVersioning, self).__init__(
            workspace_dir, workspace_dir, session_id, init_workspace=1, init_repo=1
        )


class RemoteVersioning(VersioningInterface):
    """Workspace and Repo at different locations.

    """

    def __init__(self, workspace_dir, repo_dir, session_id):
        """
        Args:
            workspace_dir (str|Path):
            repo_dir (str|Path):
            session_id (str):
        """
        super(RemoteVersioning, self).__init__(
            workspace_dir, repo_dir, session_id, init_workspace=1, init_repo=1
        )
