from binary_vcs_lite.common.util import *
from binary_vcs_lite.common import hashing


class Workspace(object):
    """Manage working directory.

    Controls which files to track using glob/regex file patterns
    and handle workspace-related operations

    It must connect to a `core.repo.Repo`

    Attributes:
        _file_pattern (dict):
        _workspace_dir (Path):
        _deep_dir (Path):
        _metadata_path (Path):
        _session_id (str):
        _revision (int):
        _repo (Repo):

    Properties:
        file_pattern (dict):
        workspace_dir (Path):
        deep_dir (Path):
        session_id (str):
        revision (int):
        repo_id (str):
        workspace_hash (common.hashing.WorkspaceHash):

    """

    def __init__(self, workspace_dir, repo, session_id, init=0):
        """
        Args:
            workspace_dir (str|Path): Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`
            repo (Repo):
            session_id (str):
            init (bool):

        """

        super(Workspace, self).__init__()

    @property
    def file_pattern(self):
        return self._file_pattern

    @property
    def workspace_dir(self):
        return self._workspace_dir

    @property
    def deep_dir(self):
        return self._deep_dir

    @property
    def session_id(self):
        return self._session_id

    @property
    def revision(self):
        return self._revision

    @property
    def repo_id(self):
        """str: """
        pass

    @property
    def workspace_hash(self):
        """WorkspaceHash: """
        pass

    def set_file_pattern(self, file_pattern):
        """
        Args:
            file_pattern (dict):
        """
        pass

    def connect_repo(self, repo, session_id):
        """
        Args:
            repo (Repo):
            session_id (str):
        """
        pass

    def absolute_path(self, hash_value):
        """
        Args:
            hash_value (str):
        """
        pass

    def commit(self, session_list, data, add_only, fast_forward):
        """
        Args:
            session_list (list of str):
            data (dict):
            add_only (bool):
            fast_forward (bool):
        """
        pass

    def checkout(self, session_id, revision, checkout_dir=None, overwrite=False):
        """
        Args:
            session_id (str):
            revision (int|str):
            checkout_dir (Path, None by default):
            overwrite (bool, False by default):
        """
        pass

    def save(self):
        pass

    def load(self):
        pass

    def detect_revision(self):
        """
        Returns:
            int:
        """
        pass

    def latest_revision(self, session_id):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):

        Returns:
            int:
        """
        pass

    def all_revision(self, session_id):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):

        Returns:
            list of int:
        """
        pass

    def all_session(self):
        """Wrap same method in `self._repo`

        Returns:
            list of str:
        """
        pass

    def detail_file_version(self, session_id, revision, relative_path):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        pass
