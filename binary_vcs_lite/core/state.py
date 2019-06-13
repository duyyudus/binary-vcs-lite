from binary_vcs_lite.common.util import *
from binary_vcs_lite.common.hashing import WorkspaceHash
from binary_vcs_lite.common import hashing
from tree_util_lite.core.tree import Tree

_vcs_logger = VcsLogger()
log_info = _vcs_logger.log_info
log_debug = _vcs_logger.log_debug
log_error = _vcs_logger.log_error


class StateTree(Tree):
    """A tree represent for file hierarchy state.
    Must be initialized from `WorkspaceHash` instance.
    """

    def __init__(self, workspace_hash):
        """
        Args:
            workspace_hash (WorkspaceHash):
        """
        super(StateTree, self).__init__('state_tree', 'state_root')
        self.build_tree(workspace_hash.ls_path_with_hash())


class State(object):
    """A single State

    Attributes:
        _state_id (str):
        _state_file (Path):
        _state_tree (StateTree):
        _timestamp (str):
        _session_list (list of str):
        _data (dict):
        _previous (State):
        _next (State):

    Properties:
        state_id (str):
        state_file (Path):
        state_tree (StateTree):
        timestamp (str):
        session_list (list of str):
        data (dict):
        previous (State):
        next (State):

    Methods:
        set_previous(state)
        set_next(state)
        update(workspace_hash, session_list, data, save=True)
        save()
        load()

    """

    def __init__(self, state_file):
        """
        Args:
            state_file (str|Path): JSON file which store state data

        """

        super(State, self).__init__()
        check_type(state_file, [str, Path])

        state_file = Path(state_file)

        self._state_file = state_file
        self._state_id = self._state_file.name
        self._state_tree = None
        self._timestamp = str(int(time.time()))
        self._session_list = []
        self._data = {}
        self._previous = None
        self._next = None

        self._enable_log()

        if self._state_file.exists():
            self.load()

    def _enable_log(self):
        log_file = Path(self._state_file.parent.parent, LOG_FOLDER, '_{}_{}.txt'.format(
            os.environ['username'],
            time.strftime('%Y-%m-%d')
        ))
        _vcs_logger.setup(log_file, Path(__file__).stem)

    @property
    def state_id(self):
        """str: """
        return self._state_id

    @property
    def state_file(self):
        """Path: """
        return self._state_file

    @property
    def state_tree(self):
        """StateTree: """
        return self._state_tree

    @property
    def timestamp(self):
        """str: """
        return self._timestamp

    @property
    def session_list(self):
        """list of str: """
        return self._session_list

    @property
    def data(self):
        """dict: """
        return self._data

    @property
    def previous(self):
        """State: """
        return self._previous

    @property
    def next(self):
        """State: """
        return self._next

    def set_previous(self, target_state):
        """
        Args:
            target_state (State):
        """
        check_type(target_state, [State])
        self._previous = target_state
        if not target_state.next:
            target_state.set_next(self)

    def set_next(self, target_state):
        """
        Args:
            target_state (State):
        """
        check_type(target_state, [State])
        self._next = target_state
        if not target_state.previous:
            target_state.set_previous(self)

    def update(self, workspace_hash, session_list, data, save=True):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_list (list of str):
            data (dict):
            save (bool, True by default):
        """
        check_type(workspace_hash, [WorkspaceHash])
        check_type(session_list, [list])
        check_type(data, [dict])

        self._state_tree = StateTree(workspace_hash)
        self._timestamp = str(int(time.time()))
        self._session_list = session_list
        self._data = data
        if save:
            self.save()

    def save(self):
        """Save state attributes to state file.

        Returns:
            bool:
        """
        file_key = STATE['CONTENT']['FILE_KEY']
        timestamp_key = STATE['CONTENT']['TIMESTAMP_KEY']
        session_list_key = STATE['CONTENT']['SESSION_LIST_KEY']
        data_key = STATE['CONTENT']['DATA_KEY']

        data = {
            file_key: self._state_tree.ls_all_leaves(relative=1),
            timestamp_key: self._timestamp,
            session_list_key: self._session_list,
            data_key: self._data
        }
        save_json(data, self._state_file, _vcs_logger)
        return True

    def load(self):
        """Load state attributes to state file.

        Returns:
            bool:
        """
        file_key = STATE['CONTENT']['FILE_KEY']
        timestamp_key = STATE['CONTENT']['TIMESTAMP_KEY']
        session_list_key = STATE['CONTENT']['SESSION_LIST_KEY']
        data_key = STATE['CONTENT']['DATA_KEY']

        data = load_json(self._state_file, _vcs_logger)
        workspace_hash = hashing.workspace_hash_from_paths(data[file_key])

        self._state_tree = StateTree(workspace_hash)
        self._timestamp = data[timestamp_key]
        self._session_list = data[session_list_key]
        self._data = data[data_key]
        return True

    def to_workspace_hash(self):
        """Create a new `WorkspaceHash` instance from `self._state_tree`.

        Returns:
            WorkspaceHash:
        """
        paths_with_hash = self._state_tree.ls_all_leaves(relative=1)
        return hashing.workspace_hash_from_paths(paths_with_hash)
