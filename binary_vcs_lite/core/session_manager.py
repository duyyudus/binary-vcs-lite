from binary_vcs_lite.common.util import *
from .session import Session


class SessionManager(object):
    """Manage sessions.

    Attributes:
        _session_dir (Path):
        _all_session (list of str):
        _session_data (dict of Session):
        _state_chain (StateChain):

    Properties:
        session_dir (Path):
        all_session (list of str):
        session_data (dict of Session):

    """

    def __init__(self, session_dir, state_chain):
        """
        Args:
            session_dir (str|Path): A folder store session data
            state_chain (StateChain):
        """
        super(SessionManager, self).__init__()

    @property
    def session_dir(self):
        return self._session_dir

    @property
    def all_session(self):
        return self._all_session

    @property
    def session_data(self):
        return self._session_data

    def load_session(self, session_file):
        """
        Args:
            session_file (Path):
        """
        pass

    def new_session(self, session_id):
        """
        Args:
            session_id (str):
        Returns:
            Session:
        """
        pass

    def sync_session(self, session_id):
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

        Returns:
            dict:
        """
        pass
