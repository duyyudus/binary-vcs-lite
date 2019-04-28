from setup_test import *


class TestCoreBlob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreBlob, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_store_blob(self):
        print()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['REPO_FOLDER'], REPO['BLOB_FOLDER'])
        )
        results = b.store_blob(workspace_hash, verbose=1)
        for p in results:
            self.assertTrue(Path(p).exists())

    def test_extract_blob(self):
        print()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['REPO_FOLDER'], REPO['BLOB_FOLDER'])
        )
        b.store_blob(workspace_hash)
        cleanup_workspace_dir()

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
