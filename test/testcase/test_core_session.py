from _setup_test import *


class TestCoreSession(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreSession, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()


if __name__ == '__main__':
    testcase_classes = [
        TestCoreSession,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
    print('')
    print('SUCCEED: {}'.format(__file__))
    print('')
    print('')
