import functools
import time
import re
import shutil
from pathlib2 import Path
from pprint import pprint
from . import config

CFG_DICT = config.CFG_DICT


def _time_measure(func):
    """Measure running time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print('Running time of {}() : {} seconds'.format(func.__name__, str(time.time() - st)))
        return ret
    return wrapper


def match_regex_pattern(input_str, patterns):
    for p in patterns:
        if re.findall(p, input_str):
            return 1


def copy_file(source, target):
    if not Path(target).parent.exists():
        Path(target).parent.mkdir(parents=1)
    shutil.copyfile(str(source), str(target))


def batch_copy(path_pair):
    for source, target in path_pair:
        copy_file(source, target)
