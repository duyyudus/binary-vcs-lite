import hashlib
import time
import re
from pathlib2 import Path
from pprint import pprint
from . import util


def hash_sha(filepath, buff_size=65536):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        data = f.read(buff_size)
        while len(data) > 0:
            sha.update(data)
            data = f.read(buff_size)
    return sha.hexdigest()


@util._time_measure
def hash_workdir(workdir, include_pattern, exclude_pattern, verbose=0):
    """
    Params
    ------
    workdir : str
        Path to working directory
    include_pattern : list of str
        Glob pattern for globbing files in `workdir`
        Must be defined relatively from `workdir`
    exclude_pattern : list of str
        Regex pattern for filtering out files in `workdir`
        It will override `include_pattern`

    Returns
    -------
    dict
        {
            relative_file_path_1: {
                "hash": sha1_digest,
                "absolute_path": str,
                "relative_path": str
            },
            relative_file_path_2: {
                "hash": sha1_digest,
                "absolute_path": str,
                "relative_path": str
            },
            ...
        }
    """

    ret = {}
    workdir = Path(workdir)
    all_paths = []
    for pattern in include_pattern:
        all_paths.extend(workdir.glob(pattern))

    if verbose:
        print('Hash digest info:')
    for p in all_paths:
        if util.match_regex_pattern(str(p), exclude_pattern):
            continue
        try:
            rel_path = p.relative_to(workdir)
            hash_data = hash_sha(str(p))
            if verbose:
                print('{}: {}'.format(str(p), hash_data))
            ret[rel_path.as_posix()] = {
                'hash': hash_data,
                'absolute_path': str(p),
                'relative_path': str(rel_path),
            }
        except:
            if verbose:
                print('Skipped: {}'.format(str(p)))
    return ret
