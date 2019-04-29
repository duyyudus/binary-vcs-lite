import sys
import os
import shutil
import unittest
from pprint import pprint
from pathlib2 import Path

# Append parent directory of `binary_vcs_lite` package
sys.path.append(str(Path(__file__).parent.parent.parent))

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

TEST_ROOT = Path(__file__).parent.parent
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

if __name__ == '__main__':
    create_workspace_dir()