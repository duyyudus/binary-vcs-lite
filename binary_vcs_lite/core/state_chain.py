from binary_vcs_lite.common.util import *
from .state import State


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

    """

    def __init__(self, state_dir):
        """
        Args:
            state_dir (str|Path): A folder store state files
        """

        super(StateChain, self).__init__()

    @property
    def state_dir(self):
        return self._state_dir

    @property
    def all_state_id(self):
        return self._all_state_id

    @property
    def state_data(self):
        return self._state_data

    @property
    def last_state(self):
        """State: """
        pass

    def load_state(self, state_file):
        """
        Args:
            state_file (Path)
        """
        pass

    def new_state(self, workspace_hash, session_list, data):
        """
        Args:
            workspace_hash (WorkspaceHash):
            session_list (list of str):
            data (dict):

        Returns:
            State:
        """
        pass

    def compare_state(self, s1, s2):
        """
        Args:
            s1 (State):
            s2 (State):

        Returns:
            dict: diff data
        """
        pass
