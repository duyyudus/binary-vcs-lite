import functools
import time
import re
import shutil
from pathlib2 import Path
from pprint import pprint
from . import config

CFG_DICT = config.CFG_DICT
LOG_PREFIX = CFG_DICT['LOG_PREFIX']


def _time_measure(func):
    """Measure running time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print('Running time of {}() : {} seconds'.format(func.__name__, str(time.time() - st)))
        return ret
    return wrapper


def log_info(*args):
    _log_indent = 0
    message = ''.join(args)
    indent_str = ''.join([' ' for i in range(_log_indent * 4)])
    print('{} - {}'.format(LOG_PREFIX, indent_str + message))


def match_regex_pattern(input_str, patterns):
    for p in patterns:
        if re.findall(p, input_str):
            return 1


def copy_file(source, target, verbose=0):
    if not Path(target).parent.exists():
        Path(target).parent.mkdir(parents=1)
    if not Path(target).exists():
        shutil.copyfile(str(source), str(target))
        if verbose:
            log_info('Copied: {}'.format(target))


def batch_copy(path_pair, verbose=0):
    """
    Params
    ------
    path_pair : list
        List of 2-tuple of str, [(source, target),...]
    """

    for source, target in path_pair:
        copy_file(source, target, verbose=verbose)
