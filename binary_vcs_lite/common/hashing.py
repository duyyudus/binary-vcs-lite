import hashlib
from .util import *


class WorkspaceHash(dict):
    """
    A dict with structure::

        {
            file_id: {
                hash_key: sha1_digest,
                relative_path_key: str,
                absolute_path_key: str
            },
        }

        Key-value of `file_id` is paired-value of `relative_path_key` in POSIX format
        Paired-value of `absolute_path_key` depend on workspace location

    """

    def __init__(self):
        super(WorkspaceHash, self).__init__()

    def hash_to_path(self, hash_value):
        for file_id in self:
            if hash_value == self[file_id][WORKSPACE['HASH_KEY']]:
                return self[file_id][WORKSPACE['RELATIVE_PATH_KEY']]


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
        log_info('Hash digest info:')
    for p in all_paths:
        if match_regex_pattern(str(p), exclude_pattern):
            continue
        try:
            rel_path = p.relative_to(workspace_dir)
            hash_data = hash_file(str(p))
            if verbose:
                log_info('{}: {}'.format(str(p), hash_data))
            workspace_hash[rel_path.as_posix()] = {
                WORKSPACE['HASH_KEY']: hash_data,
                WORKSPACE['RELATIVE_PATH_KEY']: str(rel_path),
                WORKSPACE['ABSOLUTE_PATH_KEY']: str(p)
            }
        except Exception as e:
            if verbose:
                log_info('Skipped: {}'.format(str(p)))
                log_info('----Error: {}'.format(e))
    return workspace_hash
