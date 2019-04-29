from binary_vcs_lite.common.util import *
from binary_vcs_lite.common import hashing
from binary_vcs_lite.core import blob, state, session


class Repo(object):
    """Manage version control system repository.

    Controls components::

        `core.blob.Blob`
        `core.state.StateChain`
        `core.session.Session`

    Attributes:
        _repo_dir (Path):
        _deep_dir (Path):
        _repo_id (Path):
        _blob_dir (Path):
        _state_dir (Path):
        _session_dir (Path):
        _blob (core.blob.Blob):
        _state_chain (core.state.StateChain):
        _session (core.session.Session):

    Properties:
        deep_dir (Path):
        repo_dir (Path):
        repo_id (str):
        latest_state (str):

    """

    def __init__(self, repo_dir, init=0):
        """
        Args:
            repo_dir (str or Path):

        """

        super(Repo, self).__init__()
        self._repo_dir = Path(repo_dir)
        self._deep_dir = Path(self._repo_dir, VCS_FOLDER, REPO['REPO_FOLDER'])
        self._repo_id = self._calculate_repo_id()

        if init:
            self._init_deep_dir()
        else:
            assert self._deep_dir.exists(), 'Invalid Repo folder'

        self._blob_dir = Path(self._deep_dir, REPO['BLOB_FOLDER'])
        self._state_dir = Path(self._deep_dir, REPO['STATE_FOLDER'])
        self._session_dir = Path(self._deep_dir, REPO['SESSION_FOLDER'])

        self._blob = blob.Blob(self._blob_dir)
        self._state_chain = state.StateChain(self._state_dir)
        self._session = session.Session(self._session_dir)

    @property
    def deep_dir(self):
        """Path: """
        return self._deep_dir

    @property
    def repo_dir(self):
        """Path: """
        return self._repo_dir

    @property
    def repo_id(self):
        """str: """
        return self._repo_id

    @property
    def latest_state(self):
        """str: """
        return self._state_chain.latest_state

    def _init_deep_dir(self):
        if not self._deep_dir.exists():
            self._deep_dir.mkdir(parents=1)

    def _calculate_repo_id(self):
        return hashing.hash_str(self._deep_dir.as_posix())

    def store_blob(self, workspace_hash):
        """Interface to Blob.store_blob()

        Args:
            workspace_hash (common.hashing.WorkspaceHash):

        """

        return self._blob.store_blob(workspace_hash)

    def extract_blob(self, workspace_hash):
        """Interface to Blob.extract_blob()

        Args:
            workspace_hash (common.hashing.WorkspaceHash):

        """

        return self._blob.extract_blob(workspace_hash)
