from _setup_test import *


class TestBlob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBlob, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_store_blob(self):
        log_info()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['FOLDER'], BLOB['FOLDER'])
        )
        results = b.store_blob(workspace_hash, verbose=1)

        self.assertGreater(len(results), 0)
        for p in results:
            self.assertTrue(Path(p).exists())

    def test_extract_blob(self):
        log_info()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['FOLDER'], BLOB['FOLDER'])
        )
        b.store_blob(workspace_hash)
        cleanup_workspace_dir()

        results = b.extract_blob(workspace_hash, verbose=1)

        self.assertGreater(len(results), 0)
        for p in results:
            self.assertTrue(Path(p).exists())


@log_test(__file__)
def run():
    testcase_classes = [
        TestBlob,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
