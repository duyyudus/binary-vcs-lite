from _setup_test import *


class TestStateChain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStateChain, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()


@log_test(__file__)
def run():
    testcase_classes = [
        TestStateChain,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
