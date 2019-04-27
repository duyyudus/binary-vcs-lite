import sys
import os
import shutil
import unittest
from pprint import pprint
from pathlib2 import Path
sys.path.append(str(Path(__file__).parent.parent))

from common import config

TEST_SAMPLE_DATA_WORKSPACE_DIR = str(Path(__file__).parent.joinpath('sample_data', 'last'))
TEST_OUTPUT_DATA = str(Path(__file__).parent.joinpath('output_data'))
TEST_OUTPUT_DATA_WORKSPACE_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('last'))
TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR = str(Path(TEST_OUTPUT_DATA).joinpath('remote_last'))


def cleanup_output_data():
    if Path(TEST_OUTPUT_DATA).exists():
        shutil.rmtree(TEST_OUTPUT_DATA)


def create_workspace_dir():
    for p in Path(TEST_SAMPLE_DATA_WORKSPACE_DIR).iterdir():
        target = Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, p.name)
        if not target.exists():
            shutil.copytree(str(p), str(target))


def cleanup_workspace_dir():
    for p in Path(TEST_OUTPUT_DATA_WORKSPACE_DIR).iterdir():
        if not p.name == config.CFG_DICT['VCS_FOLDER']:
            shutil.rmtree(str(p))
