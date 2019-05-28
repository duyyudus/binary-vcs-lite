from binary_vcs_lite.common.util import *


class Session(object):
    """Handle session data and behavior.

    Attributes:
        _session_id (str):
        _session_file (Path):
        _revision_data (dict):
        _detail_version_data (dict):

    Properties:
        session_id (str):
        session_file (Path):
        revision_data (dict):
        all_revision (list of int):
        latest_revision (int):

    """

    def __init__(self, session_file):
        """
        Args:
            session_file (str|Path): A session file
        """
        super(Session, self).__init__()

    @property
    def session_id(self):
        return self._session_id

    @property
    def session_file(self):
        return self._session_file

    @property
    def revision_data(self):
        return self._revision_data

    @property
    def all_revision(self):
        """list of int: """
        pass

    @property
    def latest_revision(self):
        """int: """
        pass

    def sync_from_state_chain(self, state_chain):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def detail_file_version(self, revision, relative_path=None):
        """
        Args:
            revision (int):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        pass
