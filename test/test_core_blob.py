import sys
import unittest
from pprint import pprint
from pathlib2 import Path

import setup_test
from common import config, hashing
from core import blob

_CFG_DICT = config.CFG_DICT
VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

TEST_OUTPUT_DATA_WORKSPACE_DIR = setup_test.TEST_OUTPUT_DATA_WORKSPACE_DIR


class TestCoreBlob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreBlob, self).__init__(*args, **kwargs)

    def setUp(self):
        setup_test.create_workspace_dir()

    def tearDown(self):
        setup_test.cleanup_output_data()

    def test_store_blob(self):
        print()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO_FOLDER, BLOB_FOLDER)
        )
        results = b.store_blob(workspace_hash, verbose=1)
        for p in results:
            self.assertTrue(Path(p).exists())

    def test_extract_blob(self):
        print()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO_FOLDER, BLOB_FOLDER)
        )
        b.store_blob(workspace_hash)
        setup_test.cleanup_workspace_dir()

        results = b.extract_blob(workspace_hash, verbose=1)
        for p in results:
            self.assertTrue(Path(p).exists())

if __name__ == '__main__':
    testcase_classes = [
        TestCoreBlob,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
