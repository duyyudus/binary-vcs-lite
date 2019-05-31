from _setup_test import *


class TestVersioningInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestVersioningInterface, self).__init__(*args, **kwargs)

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()


class TestLocalVersioning(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLocalVersioning, self).__init__(*args, **kwargs)

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()


class TestRemoteVersioning(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRemoteVersioning, self).__init__(*args, **kwargs)

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()


@log_test(__file__)
def run():
    testcase_classes = [
        TestVersioningInterface,
        TestLocalVersioning,
        TestRemoteVersioning
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
