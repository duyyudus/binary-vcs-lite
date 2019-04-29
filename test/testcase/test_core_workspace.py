from _setup_test import *


class TestCoreWorkspace(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreWorkspace, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_workspace_init(self):
        rp = repo.Repo(TEST_OUTPUT_DATA_WORKSPACE_DIR, init=1)
        ws = workspace.Workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR, rp, init=1)

        self.assertEqual(
            util.load_json(ws._metadata_path)[WORKSPACE['REPO_RECORD_KEY']][rp.repo_id][WORKSPACE['PATH_KEY']],
            str(rp.repo_dir)
        )


if __name__ == '__main__':
    testcase_classes = [
        TestCoreWorkspace,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
    print('')
    print('SUCCEED: {}'.format(__file__))
    print('')
    print('')
