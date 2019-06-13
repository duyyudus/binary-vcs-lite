from binary_vcs_lite.common.util import *
from .session import Session
from .state_chain import StateChain

_vcs_logger = VcsLogger()
log_info = _vcs_logger.log_info
log_debug = _vcs_logger.log_debug
log_error = _vcs_logger.log_error


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
        check_type(session_dir, [str, Path])

        session_dir = Path(session_dir)
        if not session_dir.exists():
            raise InvalidRepoSession()
        self._session_dir = session_dir
        self._all_session_id = []
        self._session_data = {}

        if check_type(state_chain, [StateChain], raise_exception=0):
            self._state_chain = state_chain
        else:
            raise MissingStateChain()

        self._enable_log()

        for f in session_dir.iterdir():
            self.load_session(f)

    def _reset(self):
        """For unit test only."""
        self._all_session_id = []
        self._session_data = {}

    def _enable_log(self):
        log_file = Path(self._session_dir.parent, LOG_FOLDER, '_{}_{}.txt'.format(
            os.environ['username'],
            time.strftime('%Y-%m-%d')
        ))
        _vcs_logger.setup(log_file, Path(__file__).stem)

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
        check_type(session_file, [str, Path])

        session_file = Path(session_file)
        if session_file.parent != self._session_dir:
            raise InvalidSession()
        sess = Session(session_file)
        if not sess.load():
            raise InvalidSession()
        if sess.session_id not in self._session_data:
            self._session_data[sess.session_id] = sess
        if sess.session_id not in self._all_session_id:
            self._all_session_id.append(sess.session_id)

    def new_session(self, session_id):
        """
        Args:
            session_id (str):
        Raises:
            ClashingSession:
        Returns:
            Session:
        """
        check_type(session_id, [str])

        if session_id in self._session_data:
            raise ClashingSession()

        session_file = self._session_dir.joinpath(session_id)
        sess = Session(session_file)
        sess.sync_from_state_chain(self._state_chain)
        if sess.session_id not in self._session_data:
            self._session_data[sess.session_id] = sess
        if session_id not in self._all_session_id:
            self._all_session_id.append(session_id)
        return sess

    def update_session(self, session_id):
        """
        Args:
            session_id (str):
        """
        check_type(session_id, [str])

        if session_id not in self._session_data:
            self.new_session(session_id)
        else:
            sess = self._session_data[session_id]
            sess.sync_from_state_chain(self._state_chain)

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
        check_type(session_id, [str])
        check_type(revision, [int, type(None)])
        check_type(relative_path, [str, Path, type(None)])

        if session_id not in self._session_data:
            raise SessionNotFound()
        sess = self._session_data[session_id]
        return sess.detail_file_version(revision, relative_path)

    def latest_revision(self, session_id):
        """Return 0 if `session_id` does not exist

        Args:
            session_id (str):
        Raises:
            SessionNotFound:
        Returns:
            int:
        """
        if session_id not in self._session_data:
            return 0

        return self._session_data[session_id].latest_revision

    def all_revision(self, session_id):
        """
        Args:
            session_id (str):
        Raises:
            SessionNotFound:
        Returns:
            list of int:
        """
        if session_id not in self._session_data:
            raise SessionNotFound()

        return self._session_data[session_id].all_revision

    def get_session(self, session_id):
        """
        Args:
            session_id (str):
        Raises:
            SessionNotFound:
        Returns:
            Session:
        """
        check_type(session_id, [str])

        if session_id not in self._session_data:
            raise SessionNotFound()

        return self._session_data[session_id]
