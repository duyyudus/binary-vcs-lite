from _setup_test import *


class TestBlob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBlob, self).__init__(*args, **kwargs)

    def setUp(self):
        create_output_workspace_dir()
        blob_dir = Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['FOLDER'], BLOB['FOLDER'])
        blob_dir.mkdir(parents=1, exist_ok=1)

    def tearDown(self):
        cleanup_output_data()

    def test_store_blob(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['FOLDER'], BLOB['FOLDER'])
        )
        results = b.store(workspace_hash)

        self.assertGreater(len(results), 0)
        for p in results:
            self.assertTrue(Path(p).exists())

    def test_extract_blob(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        b = blob.Blob(
            blob_dir=Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['FOLDER'], BLOB['FOLDER'])
        )
        b.store(workspace_hash)
        cleanup_output_workspace_dir()

        results = b.extract(workspace_hash)

        self.assertGreater(len(results), 0)
        for p in results:
            self.assertTrue(Path(p).exists())


@log_test(__file__)
def run():
    set_global_log_level(5)
    testcase_classes = [
        TestBlob,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
