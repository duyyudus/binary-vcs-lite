from pathlib2 import Path
from common import util

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class IsNotFolder(Exception):
    """Raise in case operation run in a non-folder Node."""

    def __init__(self, node_path):
        super(IsNotFolder, self).__init__()
        log_info('"{}" is not a folder Node'.format(node_path))


class InvalidBehavior(Exception):
    """Invalid behavior on Node."""


class SameNode(Exception):
    """Two name point to the same node."""


class InvalidNode(Exception):
    """Invalid Node."""


class Node(object):
    """
    Represent for a file/folder

    Attributes
    ----------
    node_name : str
    node_path : Path
    file_hash : str
    parent : core.state.Node
    childs : list of core.state.Node
        Not exists if Node is file

    """

    def __init__(self, node_name, file_hash=None, parent=None, verbose=0):
        """
        Params
        ------
        node_name : str
        file_hash : str
            Set to None make it a folder node
        parent : core.state.Node

        """

        super(Node, self).__init__()
        self.node_name = node_name
        self.file_hash = file_hash
        self.parent = parent
        self._verbose = verbose

        if not self.is_file:
            self.childs = []

        self.set_parent(parent)

    def _validate_node(self, node):
        if node == self:
            raise SameNode()
        elif node == None:
            return 0
        elif type(node) != Node:
            raise InvalidNode()
        else:
            return 1

    def set_parent(self, parent):
        if not self._validate_node(parent):
            return 0

        if self.parent != parent:
            # Remove `self` from current parent childs
            cur_parent = self.parent
            if self in cur_parent.childs:
                cur_parent.childs.remove(self)

        if parent.is_file:
            raise IsNotFolder(parent.node_path)
        self.parent = parent
        if self._verbose:
            log_info('"{}" set "{}" as parent'.format(
                self.node_path,
                parent.node_path
            ))

        if self not in parent.childs:
            parent.add_child(self)
        return 1

    def add_child(self, child):
        if not self._validate_node(child):
            return 0

        if self.is_file:
            raise IsNotFolder(self.node_path)
        self.childs.append(child)
        if self._verbose:
            log_info('"{}" added "{}" as child'.format(
                self.node_path,
                child.node_path
            ))

        if child.parent != self:
            child.set_parent(self)
        return 1

    @property
    def is_file(self):
        return 1 if self.file_hash else 0

    @property
    def child_count(self):
        return len(self.childs) if not self.is_file else None

    @property
    def node_path(self):
        cur_parent = self.parent
        parts = [self.node_name]
        while cur_parent:
            parts.insert(0, cur_parent.node_name)
            cur_parent = cur_parent.parent
        return Path(*parts)


class State(object):
    """A single State"""

    def __init__(self, state_file):
        """
        Params
        ------
        state_file : str or Path
            JSON file which store state data

        """

        super(State, self).__init__()
        self.state_file = Path(state_file)

    def from_workspace_hash(self, workspace_hash):
        """
        Params
        ------
        workspace_hash : common.hashing.WorkspaceHash

        """

        pass


class StateChain(object):
    """
    Chain of states.

    """

    def __init__(self, state_dir):
        """
        Params
        ------
        state_dir : str or Path
            A folder store state data
        """

        super(StateChain, self).__init__()
        self.state_dir = Path(state_dir)
