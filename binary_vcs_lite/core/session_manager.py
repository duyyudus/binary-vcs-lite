from binary_vcs_lite.common.util import *
from .session import Session


class SessionNotFound(VcsLiteError):
    """Session not found."""


class ClashingSession(VcsLiteError):
    """Session IDs are the same."""


class InvalidSession(VcsLiteError):
    """Session file is neither valid nor exist."""


class InvalidRepoSession(VcsLiteError):
    """There is no `session` folder in `.repo` folder."""


class MissingStateChain(VcsLiteError):
    """An instance of `StateChain` must be provided."""


class SessionManager(object):
    """Manage sessions.

    Attributes:
        _session_dir (Path):
        _all_session_id (list of str):
        _session_data (dict of Session):
        _state_chain (StateChain):

    Properties:
        session_dir (Path):
        all_session_id (list of str):
        session_data (dict of Session):

    Methods:
        load_session(session_file)
        new_session(session_id)
        update_session(session_id)
        detail_file_version(session_id, revision=None, relative_path=None)

    """

    def __init__(self, session_dir, state_chain):
        """
        Args:
            session_dir (str|Path): A folder store session data
            state_chain (StateChain):
        Raises:
            InvalidRepoSession:
            MissingStateChain:
        """
        super(SessionManager, self).__init__()

    def _reset(self):
        """For unit test only."""
        self._all_session_id = []
        self._session_data = {}

    @property
    def session_dir(self):
        """Path: """
        return self._session_dir

    @property
    def all_session_id(self):
        """list of str: """
        return self._all_session_id

    @property
    def session_data(self):
        """dict of Session: """
        return self._session_data

    def load_session(self, session_file):
        """
        Args:
            session_file (str|Path):
        Raises:
            InvalidSession:
        """
        pass

    def new_session(self, session_id):
        """
        Args:
            session_id (str):
        Raises:
            ClashingSession:
        Returns:
            Session:
        """
        pass

    def update_session(self, session_id):
        """
        Args:
            session_id (str):
        """
        pass

    def detail_file_version(self, session_id, revision=None, relative_path=None):
        """
        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):
        Raises:
            SessionNotFound:
        Returns:
            dict:
        """
        pass
