import hashlib
from .util import *


class WorkspaceHash(dict):
    """
    A dict with structure::

        {
            file_id: {
                "hash": sha1_digest,
                "relative_path": str,
                "absolute_path": str
            },            
        }

        `file_id` is just `relative_path` in POSIX format
        `absolute_path` depend on workspace location

    """

    def __init__(self):
        super(WorkspaceHash, self).__init__()

    def hash_to_path(self, hash_value):
        for file_id in self:
            if hash_value == self[file_id]['hash']:
                return self[file_id]['relative_path']


def _hash_sha(filepath, buff_size=65536):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        data = f.read(buff_size)
        while len(data) > 0:
            sha.update(data)
            data = f.read(buff_size)
    return sha.hexdigest()


def hash_file(filepath):
    return _hash_sha(filepath)


def hash_str(input_str):
    sha = hashlib.sha1()
    sha.update(input_str.encode('ascii'))
    return sha.hexdigest()


# @_time_measure
def hash_workspace(workspace_dir,
                   include_pattern=config.CFG_DICT['INCLUDE_PATTERN'],
                   exclude_pattern=config.CFG_DICT['EXCLUDE_PATTERN'],
                   verbose=0):
    """Scan input working directory and return `WorkspaceHash` data.

    Args:
        workspace_dir (str or Path): Path to working directory
        include_pattern (list of str): Glob pattern for globbing files in `workspace_dir`
            Must be defined relatively from `workspace_dir`
        exclude_pattern (list of str): Regex pattern for filtering out files in `workspace_dir`
            It will override `include_pattern`

    Returns:
        common.hashing.WorkspaceHash:

    """

    # Need this in case None is passed into pattern value
    include_pattern = include_pattern if include_pattern else config.CFG_DICT['INCLUDE_PATTERN']
    exclude_pattern = exclude_pattern if exclude_pattern else config.CFG_DICT['EXCLUDE_PATTERN']

    workspace_hash = WorkspaceHash()
    workspace_dir = Path(workspace_dir)
    all_paths = []
    for pattern in include_pattern:
        all_paths.extend(workspace_dir.glob(pattern))

    if verbose:
        print('Hash digest info:')
    for p in all_paths:
        if match_regex_pattern(str(p), exclude_pattern):
            continue
        try:
            rel_path = p.relative_to(workspace_dir)
            hash_data = hash_file(str(p))
            if verbose:
                print('{}: {}'.format(str(p), hash_data))
            workspace_hash[rel_path.as_posix()] = {
                'hash': hash_data,
                'relative_path': str(rel_path),
                'absolute_path': str(p)
            }
        except:
            if verbose:
                print('Skipped: {}'.format(str(p)))
    return workspace_hash
