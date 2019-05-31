from _setup_test import *
Repo = repo.Repo


class TestRepo(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRepo, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_repo_deep_dir = self.output_vcs_dir.joinpath(
            REPO['FOLDER']
        )
        self.output_session_dir = self.output_repo_dir.joinpath(
            SESSION['FOLDER']
        )
        self.output_state_dir = self.output_repo_dir.joinpath(
            STATE['FOLDER']
        )
        self.output_blob_dir = self.output_repo_dir.joinpath(
            BLOB['FOLDER']
        )

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)

        self.assertTrue(check_type(rp.repo_id, [str]))

        self.assertEqual(rp.repo_dir, TEST_OUTPUT_DATA_LOCAL_REPO_DIR)
        self.assertEqual(rp.deep_dir, self.output_repo_deep_dir)
        self.assertEqual(rp._session_dir, self.output_session_dir)
        self.assertEqual(rp._state_dir, self.output_state_dir)
        self.assertEqual(rp._blob_dir, self.output_blob_dir)

        self.assertTrue(self.output_repo_deep_dir.exists())
        self.assertTrue(self.output_session_dir.exists())
        self.assertTrue(self.output_state_dir.exists())
        self.assertTrue(self.output_blob_dir.exists())

        self.assertEqual(rp._session_manager.session_dir, self.output_session_dir)
        self.assertEqual(rp._state_chain.state_dir, self.output_state_dir)
        self.assertEqual(rp._blob.blob_dir, self.output_blob_dir)

        try:
            Repo('not/exists/dir', init=0)
        except Exception as e:
            self.assertTrue(check_type(e, [repo.RepoNotFound]))

    def test_properties(self):
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)
        self.assertIs(rp.repo_dir, rp._repo_dir)
        self.assertIs(rp.deep_dir, rp._deep_dir)
        self.assertIs(rp.repo_id, rp._repo_id)


@log_test(__file__)
def run():
    testcase_classes = [
        TestRepo,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
