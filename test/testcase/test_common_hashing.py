from _setup_test import *


class TestWorkspaceHash(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWorkspaceHash, self).__init__(*args, **kwargs)

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def init_workspace_hash(self):
        log_info()
        workspace_hash = hashing.hash_workspace(
            TEST_OUTPUT_DATA_WORKSPACE_DIR,
            file_pattern={
                'INCLUDE': [
                    '**/*',
                    # '*/*.ma',
                    # '*/asset.ma',
                    # '*/asset.rig.ma',
                    # '*/*/*.tif',
                    # '*/*/*.png'
                ],
                'EXCLUDE': [
                    VCS_FOLDER,
                    # '.jpg$',
                    # '.tx$'
                ]
            }
        )

        return workspace_hash

    def test_hash_to_path(self):
        log_info()
        workspace_hash = self.init_workspace_hash()

        self.assertGreater(len(workspace_hash.values()), 0)
        for v in workspace_hash.values():
            relative_path = workspace_hash.hash_to_path(v[WORKSPACE_HASH['HASH_KEY']])
            self.assertEqual(relative_path, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])

    def test_set_workspace_dir(self):
        log_info()
        workspace_hash = self.init_workspace_hash()
        workspace_dir = 'new/workspace/dir'
        workspace_hash.set_workspace_dir(workspace_dir)

        self.assertGreater(len(workspace_hash.values()), 0)
        for v in workspace_hash.values():
            valid_abs_path = Path(workspace_dir, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])
            real_abs_path = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            self.assertEqual(valid_abs_path.as_posix(), real_abs_path.as_posix())


@log_test(__file__)
def run():
    testcase_classes = [
        TestWorkspaceHash,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
