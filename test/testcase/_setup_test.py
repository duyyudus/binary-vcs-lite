import sys
import os
import shutil
import unittest
from pprint import pprint
from pathlib2 import Path

_cur_file = Path(__file__).resolve()
# Append parent directory of `binary_vcs_lite` package
sys.path.append(str(_cur_file.parent.parent.parent))

# Append parent directory of `tree_util_lite` package
# There must be a Git repo `tree-util-lite` in the same folder with `binary-vcs-lite` repo
sys.path.append(str(_cur_file.parent.parent.parent.parent.joinpath('tree-util-lite')))

from binary_vcs_lite.common import (
    config,
    util,
    hashing
)

from binary_vcs_lite.common.util import *

from binary_vcs_lite.core import (
    repo,
    workspace,
    state,
    blob,
    session
)

from binary_vcs_lite import vcs_interface

TEST_ROOT = Path(__file__).resolve().parent.parent
TEST_SAMPLE_DATA_WORKSPACE_DIR = str(TEST_ROOT.joinpath('sample_data', 'last'))
TEST_OUTPUT_DATA = str(TEST_ROOT.joinpath('output_data'))
TEST_OUTPUT_DATA_WORKSPACE_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('last'))
TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('remote_last'))


def cleanup_output_data():
    if Path(TEST_OUTPUT_DATA).exists():
        shutil.rmtree(TEST_OUTPUT_DATA)


def create_workspace_dir():
    for p in Path(TEST_SAMPLE_DATA_WORKSPACE_DIR).iterdir():
        if p.name == '.vcs_lite':
            continue
        target = Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, p.name)
        if not target.exists():
            shutil.copytree(str(p), str(target))


def cleanup_workspace_dir():
    for p in Path(TEST_OUTPUT_DATA_WORKSPACE_DIR).iterdir():
        if not p.name == config.CFG_DICT['VCS_FOLDER']:
            shutil.rmtree(str(p))


def start_log_test(testcase_path):
    message = '[START TEST] :: {}'.format(testcase_path)
    exe = 'Python interpreter: {}'.format(sys.executable)
    print('')
    print('#' * len(message))
    print('#' * len(message))
    print(message)
    print(exe)
    print('')


def end_log_test(testcase_path):
    message = '[END TEST] :: {}'.format(testcase_path)
    exe = 'Python interpreter: {}'.format(sys.executable)
    print('')
    print(exe)
    print(message)
    print('#' * len(message))
    print('#' * len(message))
    print('')


def log_test(testcase_path):
    def _log_test(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            switch_log_vcs(0)
            start_log_test(testcase_path)
            func(*args, **kwargs)
            end_log_test(testcase_path)
        return wrapper
    return _log_test


if __name__ == '__main__':
    pass
