import sys
import os
import shutil
import unittest
from pprint import pprint
from pathlib2 import Path

_cur_file = Path(__file__).resolve()
# Append parent directory of `binary_vcs_lite` package
sys.path.append(str(_cur_file.parent.parent.parent))
sys.path.append(str(_cur_file.parent.parent.parent.parent))


# Append parent directory of `tree_util_lite` package
# There must be a Git repo `tree-util-lite` in the same folder with `binary-vcs-lite` repo
sys.path.append(str(_cur_file.parent.parent.parent.parent.joinpath('tree-util-lite')))

from binary_vcs_lite.common.util import *
from binary_vcs_lite.common.config import *

from binary_vcs_lite.common import (
    config,
    util,
    hashing
)

from binary_vcs_lite.core import (
    workspace,
    repo,
    blob,
    state_chain,
    state,
    session_manager,
    session
)

from binary_vcs_lite import vcs_interface

TEST_ROOT = _cur_file.parent.parent
TEST_SAMPLE_DATA_WORKSPACE_DIR = str(TEST_ROOT.joinpath('sample_data_workspace', 'last'))
TEST_SAMPLE_DATA_REPO_DIR = str(TEST_ROOT.joinpath('sample_data_repo', 'last'))

TEST_OUTPUT_DATA = str(TEST_ROOT.joinpath('output_data'))
TEST_OUTPUT_DATA_WORKSPACE_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('last'))
TEST_OUTPUT_DATA_LOCAL_REPO_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('last'))
TEST_OUTPUT_DATA_REMOTE_REPO_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('remote_last'))


def create_output_workspace_dir():
    """Copy from sample workspace dir to output folder."""
    for p in Path(TEST_SAMPLE_DATA_WORKSPACE_DIR).iterdir():
        if p.name == VCS_FOLDER:
            continue
        target = Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, p.name)
        if not target.exists():
            shutil.copytree(str(p), str(target))


def create_output_repo_dir(local=1):
    """Copy from sample repo dir to output folder."""
    for p in Path(TEST_SAMPLE_DATA_REPO_DIR).iterdir():
        target = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR if local else TEST_OUTPUT_DATA_REMOTE_REPO_DIR,
            p.name
        )
        if not target.exists():
            shutil.copytree(str(p), str(target))


def cleanup_output_data():
    logging.shutdown()
    if Path(TEST_OUTPUT_DATA).exists():
        shutil.rmtree(TEST_OUTPUT_DATA)


def cleanup_output_workspace_dir():
    """Clean output workspace dir."""
    logging.shutdown()
    for p in Path(TEST_OUTPUT_DATA_WORKSPACE_DIR).iterdir():
        if p.name != VCS_FOLDER:
            shutil.rmtree(str(p))


def cleanup_output_repo_dir():
    """Clean output repo dir."""
    logging.shutdown()
    for p in Path(TEST_OUTPUT_DATA_LOCAL_REPO_DIR).iterdir():
        if p.name == VCS_FOLDER:
            shutil.rmtree(str(p))
    for p in Path(TEST_OUTPUT_DATA_REMOTE_REPO_DIR).iterdir():
        if p.name == VCS_FOLDER:
            shutil.rmtree(str(p))


def copy_dir(source, target):
    """Remove existing files/folders before copying."""

    source = Path(source)
    if not source.exists():
        return 0
    target = Path(target)
    if not target.exists():
        target.mkdir(parents=1)
    for s in source.iterdir():
        t = target.joinpath(s.name)
        if t.exists():
            if t.is_dir():
                shutil.rmtree(str(t))
            else:
                os.remove(str(t))

        if s.is_dir():
            shutil.copytree(str(s), str(t))
        else:
            shutil.copyfile(str(s), str(t))


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
            set_global_log_level(0)
            start_log_test(testcase_path)
            func(*args, **kwargs)
            end_log_test(testcase_path)
        return wrapper
    return _log_test


if __name__ == '__main__':
    pass
