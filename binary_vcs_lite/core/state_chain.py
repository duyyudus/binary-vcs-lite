from tree_util_lite.core import diff_engine
from tree_util_lite.diff_interpreter import binary_vcs_diff

from binary_vcs_lite.common.util import *
from binary_vcs_lite.common.hashing import WorkspaceHash
from .state import State

_vcs_logger = VcsLogger()
log_info = _vcs_logger.log_info
log_debug = _vcs_logger.log_debug
log_error = _vcs_logger.log_error


class StateNotFound(VcsLiteError):
    """State not found."""

    def __init__(self, message='', vcs_logger=None):
        super(StateNotFound, self).__init__(message, vcs_logger)


class InvalidState(VcsLiteError):
    """State file is neither valid nor exist."""

    def __init__(self, message='', vcs_logger=None):
        super(InvalidState, self).__init__(message, vcs_logger)


class InvalidRepoState(VcsLiteError):
    """There is no `state` folder in `.repo` folder."""

    def __init__(self, message='', vcs_logger=None):
        super(InvalidRepoState, self).__init__(message, vcs_logger)


class StateChain(object):
    """Chain of states.

    Attributes:
        _state_dir (Path):
        _all_state_id (list of str):
        _state_data (dict of State):

    Properties:
        state_dir (Path):
        all_state_id (list of str):
        state_data (dict of State):
        last_state (State):

    Methods:
        load_state(state_file)
        new_state(workspace_hash, session_list, data, save=True)
        compare_state(s1, s2)
        get_state(state_id)

    """

    def __init__(self, state_dir):
        """
        Args:
            state_dir (str|Path): A folder store state files
        Raises:
            InvalidRepoState:
        """

        super(StateChain, self).__init__()
        check_type(state_dir, [str, Path])

        state_dir = Path(state_dir)
        check_path(state_dir)

        self._state_dir = state_dir
        self._all_state_id = []
        self._state_data = {}

        if not state_dir.exists():
            raise InvalidRepoState('InvalidRepoState: {}'.format(state_dir.as_posix()), _vcs_logger)

        self._enable_log()

        for f in state_dir.iterdir():
            self.load_state(f)

        self._sort_state_id()

        log_info('Initialized state chain')
        log_debug('All state IDs:')
        log_debug(self._all_state_id)

    def _reset(self):
        """For unit test only."""
        self._all_state_id = []
        self._state_data = {}

    def _enable_log(self):
        log_file = Path(self._state_dir.parent, LOG_FOLDER, '_{}_{}.txt'.format(
            os.environ['username'],
            time.strftime('%Y-%m-%d')
        ))
        _vcs_logger.setup(log_file, Path(__file__).stem)

    def _sort_state_id(self):
        sorted_ids = sorted([int(i[1:]) for i in self._all_state_id])
        self._all_state_id = ['s' + str(i) for i in sorted_ids]

    @property
    def state_dir(self):
        """Path: """
        return self._state_dir

    @property
    def all_state_id(self):
        """list of str: """
        return self._all_state_id

    @property
    def state_data(self):
        """dict of State: """
        return self._state_data

    @property
    def last_state(self):
        """State: """
        if not self.all_state_id:
            return None
        return self._state_data[self.all_state_id[-1]]

    def load_state(self, state_file):
        """
        Args:
            state_file (str|Path):
        Raises:
            InvalidState:
        """
        check_type(state_file, [str, Path])

        state_file = Path(state_file)
        if state_file.parent != self._state_dir:
            raise InvalidState('InvalidState: {}'.format(state_file.as_posix()), _vcs_logger)

        s = State(state_file)
        if not s.load():
            raise InvalidState('InvalidState: {}'.format(state_file.as_posix()), _vcs_logger)

        if self.last_state:
            self.last_state.set_next(s)

        if s.state_id not in self._state_data:
            self._state_data[s.state_id] = s
        if s.state_id not in self._all_state_id:
            self._all_state_id.append(s.state_id)

    def new_state(self, workspace_hash, session_list, data, save=True):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_list (list of str):
            data (dict):
            save (bool, True by default):

        Returns:
            State:
        """
        check_type(workspace_hash, [WorkspaceHash])
        check_type(session_list, [list])
        check_type(data, [dict])

        if self.all_state_id:
            state_id = 's' + str(int(self.all_state_id[-1][1:]) + 1)
        else:
            state_id = 's0'
        state_file = self._state_dir.joinpath(state_id)
        s = State(state_file)
        s.update(workspace_hash, session_list, data, save)

        if self.last_state:
            self.last_state.set_next(s)

        if s.state_id not in self._state_data:
            self._state_data[s.state_id] = s
        if s.state_id not in self._all_state_id:
            self._all_state_id.append(s.state_id)
        return s

    def compare_state(self, s1, s2, return_path):
        """
        Args:
            s1 (State):
            s2 (State):
            return_path (bool): return diff data as paths or `tree_util_lite.core.tree.Node`

        Returns:
            dict: diff data in below format, all paths are in relative format ( without root )
                {
                    'added': list,  # Added
                    'deleted': list,  # Deleted
                    'renamed': dict,  # Renamed: same parent, different label, same hash
                    'unchanged': list,  # Unchanged: same parent, same label, same hash
                    'modified': list,  # Modified: same parent, same label, different hash
                    'moved': dict,  # Moved: different parent, same label, same hash
                    'copied': dict,  # Copied: any node share hash with some node in `unchanged`
                }

        """
        check_type(s1, [State])
        check_type(s2, [State])

        differ = diff_engine.DiffEngine(s1.state_tree, s2.state_tree)
        differ.compute_edit_sequence(show_matrix=0, show_edit=0)
        diff_data = differ.postprocess_edit_sequence(return_path=0, show_diff=0)
        return binary_vcs_diff.interpret(diff_data, return_path=return_path, show_diff=0)

    def get_state(self, state_id):
        """
        Args:
            state_id (str):
        Returns:
            State:
        """
        check_type(state_id, [str])

        if state_id not in self._state_data:
            raise StateNotFound('StateNotFound: {}'.format(state_id), _vcs_logger)

        return self._state_data[state_id]
