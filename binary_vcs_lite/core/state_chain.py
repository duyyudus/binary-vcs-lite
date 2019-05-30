from binary_vcs_lite.common.util import *
from .state import State


class InvalidState(VcsLiteError):
    """State file is neither valid nor exist."""


class InvalidRepoState(VcsLiteError):
    """There is no `state` folder in `.repo` folder."""


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
        new_state(workspace_hash, session_list, data)
        compare_state(s1, s2)

    """

    def __init__(self, state_dir):
        """
        Args:
            state_dir (str|Path): A folder store state files
        Raises:
            InvalidRepoState:
        """

        super(StateChain, self).__init__()

    def _reset(self):
        """For unit test only."""
        self._all_state_id = []
        self._state_data = {}

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
        pass

    def load_state(self, state_file):
        """
        Args:
            state_file (str|Path)
        Raises:
            InvalidState:
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
