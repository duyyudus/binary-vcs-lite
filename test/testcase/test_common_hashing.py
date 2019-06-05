from _setup_test import *


class TestWorkspaceHash(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWorkspaceHash, self).__init__(*args, **kwargs)
        self.workspace_files = [
            'medRes/asset.ma',
            'medRes/asset.rig.ma',
            'medRes/old/asset.ma',
            'medRes/textures/tex_1.tif',
            'medRes/textures/tex_2_new_name.tif',
            'medRes/textures/tex_2_new_name.tif',
            'medRes/textures/tex_4.tif',
            'proxyRes/asset.ma',
            'proxyRes/asset.rig.ma',
        ]

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
            },
            verbose=1
        )

        return workspace_hash

    def test_init(self):
        log_info()
        workspace_hash = self.init_workspace_hash()

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            abs_path = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            self.assertTrue(abs_path.exists())

        for f in self.workspace_files:
            self.assertIn(f, workspace_hash)

    def test_hash_to_path(self):
        log_info()
        workspace_hash = self.init_workspace_hash()

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            relative_path = workspace_hash.hash_to_path(v[WORKSPACE_HASH['HASH_KEY']])
            self.assertEqual(relative_path, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])

    def test_set_workspace_dir(self):
        log_info()
        workspace_hash = self.init_workspace_hash()
        workspace_dir = 'new/workspace/dir'
        workspace_hash.set_workspace_dir(workspace_dir)

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            valid_abs_path = Path(workspace_dir, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])
            real_abs_path = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            self.assertEqual(valid_abs_path.as_posix(), real_abs_path.as_posix())


@log_test(__file__)
def run():
    switch_log_vcs(0)
    testcase_classes = [
        TestWorkspaceHash,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
