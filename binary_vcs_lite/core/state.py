from binary_vcs_lite.common.util import *
from tree_util_lite.core.tree import Tree


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
        self._state_file = Path(state_file)

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
        pass

    def set_next(self, target_state):
        """
        Args:
            target_state (State):
        """
        pass

    def update(self, workspace_hash, session_list, data, save=True):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_list (list of str):
            data (dict):
            save (bool, True by default):
        """
        pass

    def save(self):
        pass

    def load(self):
        pass
