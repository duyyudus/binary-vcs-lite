from setup_test import *


class TestCoreRepo(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreRepo, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_repo_attr(self):
        print()
        new_repo = repo.Repo(TEST_OUTPUT_DATA_WORKSPACE_DIR, init=1)
        self.assertEqual(new_repo.repo_dir, Path(TEST_OUTPUT_DATA_WORKSPACE_DIR))
        self.assertEqual(
            new_repo.deep_dir,
            Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['REPO_FOLDER'])
        )
        self.assertEqual(
            new_repo.repo_id,
            hashing.hash_str(Path(TEST_OUTPUT_DATA_WORKSPACE_DIR, VCS_FOLDER, REPO['REPO_FOLDER']).as_posix())
        )


if __name__ == '__main__':
    testcase_classes = [
        TestCoreRepo,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
