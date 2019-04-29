from binary_vcs_lite.common.util import *


class Session(object):
    """Manage session info.

    Attributes:
        _session_dir (Path):

    Properties:
        session_dir (Path):

    """

    def __init__(self, session_dir):
        """
        Args:
            session_dir (str or Path): A folder store session data
        """

        super(Session, self).__init__()
        self._session_dir = Path(session_dir)

    @property
    def session_dir(self):
        """Path: """
        return self._session_dir
