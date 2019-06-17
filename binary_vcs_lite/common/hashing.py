import hashlib
from .util import *
from .config import *
from tree_util_lite.core import tree


class WorkspaceHash(dict):
    """An instance of this class represent for a specific workspace,
    "workspace" means a set of file and their hash digest.

    Once instantiated, it cannot modify itself to represent for another workspace.
    Although it can point to different workspace parent directories,
    but the set of files-and-hashes is kept intact.

    A dict with structure::

        {
            file_id: {
                HASH_KEY: sha1_digest,
                RELATIVE_PATH_KEY: str,
                ABSOLUTE_PATH_KEY: str
            },
        }

        Key-value of `file_id` is paired-value of `relative_path_key` in POSIX format
        Paired-value of `absolute_path_key` depend on workspace location

    Attributes:
        _workspace_dir (Path):

    Properties:
        workspace_dir (Path):

    Methods:
        set_workspace_dir(target_dir)
        update_abs_path()
        hash_to_path(hash_value)
        ls_path_with_hash()
    """

    def __init__(self, workspace_dir):
        """
        Args:
            workspace_dir (str|Path): Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`
        """
        super(WorkspaceHash, self).__init__()
        self._workspace_dir = workspace_dir
        if workspace_dir:
            self.update_abs_path()

    @property
    def workspace_dir(self):
        return self._workspace_dir

    def set_workspace_dir(self, target_dir):
        """
        Args:
            target_dir (str|Path):
        """
        check_type(target_dir, [str, Path])

        self._workspace_dir = target_dir
        if target_dir:
            self.update_abs_path()

    def update_abs_path(self):
        """Update absolute path using `self._workspace_dir`"""

        for f in self:
            abs_path = Path(self._workspace_dir, self[f][WORKSPACE_HASH['RELATIVE_PATH_KEY']])
            self[f][WORKSPACE_HASH['ABSOLUTE_PATH_KEY']] = abs_path.as_posix()

    def hash_to_path(self, hash_value):
        """
        Args:
            hash_value (str):

        Returns:
            str:
        """
        check_type(hash_value, [str])

        for file_id in self:
            if hash_value == self[file_id][WORKSPACE_HASH['HASH_KEY']]:
                return self[file_id][WORKSPACE_HASH['RELATIVE_PATH_KEY']]

    def ls_path_with_hash(self):
        """Return a list of path with data as suffix

        Example:
            [
                'path/to/file1/_dx_000001',
                'path/to/file2/_dx_000002',
                ...
            ]

        Returns:
            list of str
        """
        ret = []
        for k in self:
            p = tree.path_with_data(k, self[k][WORKSPACE_HASH['HASH_KEY']])
            ret.append(p)
        return ret


def _hash_sha(filepath, buff_size=65536):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        data = f.read(buff_size)
        while len(data) > 0:
            sha.update(data)
            data = f.read(buff_size)
    return sha.hexdigest()


def hash_file(filepath):
    """
    Args:
        filepath (str|Path):
    Returns:
        str:
    """
    check_type(filepath, [str, Path])
    return _hash_sha(str(filepath))


def hash_str(input_str):
    """
    Args:
        input_str (str):
    Returns:
        str:
    """
    check_type(input_str, [str])
    sha = hashlib.sha1()
    sha.update(input_str.encode('ascii'))
    return sha.hexdigest()


# @_time_measure
def hash_workspace(workspace_dir,
                   file_pattern=DEFAULT_FILE_PATTERN,
                   vcs_logger=VcsLogger()):
    """Scan input working directory and return `WorkspaceHash` data.

    This is the only way to create a new `WorkspaceHash` instance.

    Args:
        workspace_dir (str|Path): Path to working directory
        file_pattern (dict): contain INCLUDE and EXCLUDE pattern
            INCLUDE
                Glob pattern for globbing files in `workspace_dir`
                Must be defined relatively from `workspace_dir`
            EXCLUDE
                Regex pattern for filtering out files in `workspace_dir`
                It will override `include_pattern`

    Returns:
        common.hashing.WorkspaceHash:

    """
    check_type(workspace_dir, [str, Path])
    check_type(file_pattern, [dict])

    vcs_logger.log_info('Hashing workspace: {}'.format(str(workspace_dir)))

    # Need this in case None is passed into pattern value
    include_pattern = file_pattern['INCLUDE'] if file_pattern else DEFAULT_FILE_PATTERN['INCLUDE']
    exclude_pattern = file_pattern['EXCLUDE'] if file_pattern else DEFAULT_FILE_PATTERN['EXCLUDE']

    vcs_logger.log_debug('Include Pattern ::')
    vcs_logger.log_debug(include_pattern)
    vcs_logger.log_debug('Exclude Pattern ::')
    vcs_logger.log_debug(exclude_pattern)

    workspace_dir = Path(workspace_dir)
    workspace_hash = WorkspaceHash(workspace_dir)
    all_paths = []
    for pattern in include_pattern:
        all_paths.extend(workspace_dir.glob(pattern))

    vcs_logger.log_debug('Hash digest info:')
    for p in all_paths:
        if match_regex_pattern(str(p), exclude_pattern):
            vcs_logger.log_debug('Skipped excluded file: {}'.format(str(p)))
            continue
        if Path(p).is_dir():
            continue
        try:
            rel_path = p.relative_to(workspace_dir)
            hash_data = hash_file(p)
            vcs_logger.log_debug('{}: {}'.format(str(p), hash_data))

            workspace_hash[rel_path.as_posix()] = {
                WORKSPACE_HASH['HASH_KEY']: hash_data,
                WORKSPACE_HASH['RELATIVE_PATH_KEY']: str(rel_path)
            }
        except Exception as e:
            vcs_logger.log_error('Skipped hashing file: {}'.format(str(p)))
            vcs_logger.log_error('----Error: {}'.format(e))

    workspace_hash.set_workspace_dir(workspace_dir)
    vcs_logger.log_info('Hashing completed')
    return workspace_hash


def workspace_hash_from_paths(paths):
    """Create instance of `WorkspaceHash` from a list of file paths and their hashes

    Args:
        paths (list of str): paths with data as suffix
    Returns:
        WorkspaceHash:
    """
    check_type(paths, [list])

    ws = WorkspaceHash(None)
    for p in paths:
        p, d = tree.separate_path_data(p)
        ws[p] = {
            WORKSPACE_HASH['HASH_KEY']: d,
            WORKSPACE_HASH['RELATIVE_PATH_KEY']: p
        }
    return ws
