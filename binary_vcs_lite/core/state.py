from binary_vcs_lite.common.util import *
from tree_util_lite.core.tree import Tree


class IsNotFolder(VcsLiteError):
    """Raise in case operation run in a non-folder Node."""


class StateTree(Tree):
    """
    A tree represent for file hierarchy state.

    Attributes:
        _tree_name (str):
        _root (tree_util_lite.core.tree.Node):

    Properties:
        tree_name (str):
        root (tree_util_lite.core.tree.Node):

    """

    def __init__(self, tree_name, root_name):
        """
        Args:
            tree_name (str):
            root_name (str):

        """

        super(StateTree, self).__init__(tree_name, root_name)


class State(object):
    """A single State"""

    def __init__(self, state_file):
        """
        Args:
            state_file (str or Path): JSON file which store state data

        """

        super(State, self).__init__()
        self._state_file = Path(state_file)

    def from_workspace_hash(self, workspace_hash):
        """
        Args:
            workspace_hash (common.hashing.WorkspaceHash):

        """

        pass


class StateChain(object):
    """
    Chain of states.

    """

    def __init__(self, state_dir):
        """
        Args:
            state_dir (str or Path): A folder store state data
        """

        super(StateChain, self).__init__()
        self._state_dir = Path(state_dir)

    @property
    def state_dir(self):
        """Path: """
        return self._state_dir

    @property
    def latest_state(self):
        """str: """
        return '0x00000000000000000000000000000000000000'
