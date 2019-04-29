from _setup_test import *


class TestVcsInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestVcsInterface, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_local_working(self):
        log_info()
        work = vcs_interface.LocalWorking(TEST_OUTPUT_DATA_WORKSPACE_DIR, init=1)
        self.assertTrue(work._repo.deep_dir.exists())
        self.assertTrue(work._workspace.deep_dir.exists())

    def test_remote_working(self):
        log_info()
        work = vcs_interface.RemoteWorking(
            TEST_OUTPUT_DATA_WORKSPACE_DIR,
            TEST_OUTPUT_DATA_REMOTE_WORKSPACE_DIR,
            init=1
        )
        self.assertTrue(work._repo.deep_dir.exists())
        self.assertTrue(work._workspace.deep_dir.exists())


@log_test(__file__)
def run():
    testcase_classes = [
        TestVcsInterface,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
