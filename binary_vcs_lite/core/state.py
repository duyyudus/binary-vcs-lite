from binary_vcs_lite.common.util import *


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
    """Represent for a file/folder.

    Attributes:
        _node_name (str):
        _file_hash (str):
        _parent (core.state.Node):
        _childs (list of core.state.Node): Not exists if Node is file

    Properties:
        node_name (str):
        node_path (Path):
        file_hash (str):
        parent (core.state.Node):
        childs (list of core.state.Node):
        is_file (bool):
        child_count (int):

    """

    def __init__(self, node_name, file_hash=None, parent=None, verbose=0):
        """
        Args:
            node_name (str):
            file_hash (str): Set to None make it a folder node
            parent (core.state.Node):

        """

        super(Node, self).__init__()
        self._node_name = node_name
        self._file_hash = file_hash
        self._parent = parent
        self._verbose = verbose

        if not self.is_file:
            self._childs = []

        self.set_parent(parent)

    @property
    def node_name(self):
        """str: """
        return self._node_name

    @property
    def file_hash(self):
        """str: """
        return self._file_hash

    @property
    def parent(self):
        """core.state.Node: """
        return self._parent

    @property
    def childs(self):
        """list of core.state.Node: """
        return [] if self.is_file else self._childs

    @property
    def is_file(self):
        """bool: """
        return 1 if self._file_hash else 0

    @property
    def child_count(self):
        """int: """
        return len(self._childs) if not self.is_file else None

    @property
    def node_path(self):
        """Path: """
        cur_parent = self._parent
        parts = [self._node_name]
        while cur_parent:
            parts.insert(0, cur_parent.node_name)
            cur_parent = cur_parent.parent
        return Path(*parts)

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

        if self._parent != parent:
            # Remove `self` from current parent childs
            cur_parent = self._parent
            if self in cur_parent.childs:
                cur_parent.childs.remove(self)

        if parent.is_file:
            raise IsNotFolder(parent.node_path)
        self._parent = parent
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
        self._childs.append(child)
        if self._verbose:
            log_info('"{}" added "{}" as child'.format(
                self.node_path,
                child.node_path
            ))

        if child.parent != self:
            child.set_parent(self)
        return 1


class StateTree(object):
    """
    A tree of Node objects.

    Internal attributes
        _tree_name (str):
        _root (core.state.Node):

    Exposed properties
        tree_name (str):
        root (core.state.Node):

    """

    def __init__(self, tree_name):
        """
        Args:
            tree_name (str):

        """

        super(StateTree, self).__init__()
        self._tree_name = tree_name
        self._root = Node('{}_root'.format(tree_name))

    @property
    def tree_name(self):
        """str: """
        return self._tree_name

    @property
    def root(self):
        """core.state.Node: """
        return self._root

    def add_sub_tree(self, sub_path):
        """
        Args:
            sub_path (str): path of sub tree to be appended under `self._root`
        """
        pass


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
