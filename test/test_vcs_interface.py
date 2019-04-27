import sys
import unittest
from pprint import pprint
from pathlib2 import Path

import setup_test
from common import config
import vcs_interface

_CFG_DICT = config.CFG_DICT
VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

TEST_OUTPUT_DATA_WORKSPACE_DIR = setup_test.TEST_OUTPUT_DATA_WORKSPACE_DIR
TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR = setup_test.TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR


class TestVcsInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestVcsInterface, self).__init__(*args, **kwargs)

    def setUp(self):
        setup_test.create_workspace_dir()

    def tearDown(self):
        setup_test.cleanup_output_data()

    def test_local_working(self):
        work = vcs_interface.LocalWorking(TEST_OUTPUT_DATA_WORKSPACE_DIR, init=1)
        self.assertTrue(work._repo.deep_dir.exists())
        self.assertTrue(work._workspace.deep_dir.exists())

    def test_remote_working(self):
        work = vcs_interface.RemoteWorking(
            TEST_OUTPUT_DATA_WORKSPACE_DIR,
            TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR,
            init=1
        )
        self.assertTrue(work._repo.deep_dir.exists())
        self.assertTrue(work._workspace.deep_dir.exists())

if __name__ == '__main__':
    testcase_classes = [
        TestVcsInterface,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
