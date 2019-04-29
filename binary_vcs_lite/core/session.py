from binary_vcs_lite.common.util import *


class Session(object):
    """
    Manage session info.

    Internal attributes
        _session_dir : Path

    Exposed properties
        session_dir : Path

    """

    def __init__(self, session_dir):
        """
        Params
        ------
        session_dir : str or Path
            A folder store session data
        """

        super(Session, self).__init__()
        self._session_dir = Path(session_dir)

    @property
    def session_dir(self):
        """Safe way to get `self._session_dir` value without accidentally re-assign it."""

        return self._session_dir
