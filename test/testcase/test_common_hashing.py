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
            vcs_logger=VcsLogger()
        )

        return workspace_hash

    def test_init(self):
        workspace_hash = self.init_workspace_hash()

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            abs_path = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            self.assertTrue(abs_path.exists())

        for f in self.workspace_files:
            self.assertIn(f, workspace_hash)

    def test_hash_to_path(self):
        workspace_hash = self.init_workspace_hash()

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            relative_path = workspace_hash.hash_to_path(v[WORKSPACE_HASH['HASH_KEY']])
            self.assertEqual(relative_path, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])

    def test_set_workspace_dir(self):
        workspace_hash = self.init_workspace_hash()
        workspace_dir = 'new/workspace/dir'
        workspace_hash.set_workspace_dir(workspace_dir)

        self.assertGreater(len(workspace_hash), 0)
        for v in workspace_hash.values():
            valid_abs_path = Path(workspace_dir, v[WORKSPACE_HASH['RELATIVE_PATH_KEY']])
            real_abs_path = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            self.assertEqual(valid_abs_path.as_posix(), real_abs_path.as_posix())

    def test_workspace_hash_from_path(self):
        paths = [
            'some/path1/_dx_hash1',
            'some/path2/_dx_hash2',
        ]
        ws = hashing.workspace_hash_from_paths(paths)
        valid_data = {
            'some/path1': 'hash1',
            'some/path2': 'hash2',
        }
        for k in ws:
            ws_hash = ws[k][WORKSPACE_HASH['HASH_KEY']]
            self.assertEqual(valid_data[k], ws_hash)


@log_test(__file__)
def run():
    set_global_log_level(5)
    testcase_classes = [
        TestWorkspaceHash,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
