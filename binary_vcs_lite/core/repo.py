from binary_vcs_lite.common.util import *
from .blob import Blob
from .state_chain import StateChain
from .session_manager import SessionManager


class Repo(object):
    """Manage version control system repository.

    Controls components::

        `core.blob.Blob`
        `core.state_chain.StateChain`
        `core.session_manager.SessionManager`

    Attributes:
        _repo_dir (Path):
        _deep_dir (Path):
        _repo_id (Path):
        _blob_dir (Path):
        _session_dir (Path):
        _state_dir (Path):
        _blob (core.blob.Blob):
        _session_manager (core.session_manager.SessionManager):
        _state_chain (core.state_chain.StateChain):

    Properties:
        repo_dir (Path):
        deep_dir (Path):
        repo_id (str):

    """

    def __init__(self, repo_dir, init=0):
        """
        Args:
            repo_dir (str|Path):
            init (bool):

        """

        super(Repo, self).__init__()

    @property
    def repo_dir(self):
        return self._repo_dir

    @property
    def deep_dir(self):
        return self._deep_dir

    @property
    def repo_id(self):
        """str: """
        pass

    def state_in(self,
                 workspace_hash,
                 session_list,
                 data,
                 current_session_id,
                 current_revision,
                 add_only):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_list (list of str):
            data (dict):
            current_session_id (str):
            current_revision (int):
            add_only (bool):
        """
        pass

    def state_out(self, workspace_hash, session_id, revision, overwrite):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_id (str):
            revision (int):
            overwrite (bool):
        """
        pass

    def save(self):
        pass

    def load(self):
        pass

    def latest_revision(self, session_id):
        """
        Args:
            session_id (str):

        Returns:
            int:
        """
        pass

    def all_revision(self, session_id):
        """
        Args:
            session_id (str):

        Returns:
            list of int:
        """
        pass

    def all_session(self):
        """
        Returns:
            list of str:
        """
        pass

    def detail_file_version(self, session_id, revision=None, relative_path=None):
        """
        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        pass
