from _setup_test import *
Workspace = workspace.Workspace
Repo = repo.Repo


class TestWorkspace(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWorkspace, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_workspace_deep_dir = self.output_vcs_dir.joinpath(
            WORKSPACE['FOLDER']
        )
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

    def test_init(self):
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)
        ws = Workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR, rp, 'review', init=1)

        self.assertEqual(str(ws.workspace_dir), TEST_OUTPUT_DATA_WORKSPACE_DIR)
        self.assertEqual(ws.deep_dir, self.output_workspace_deep_dir)
        self.assertTrue(self.output_workspace_deep_dir.exists())
        self.assertEqual(ws.session_id, 'review')
        self.assertEqual(ws.revision, 0)
        self.assertEqual(ws.file_pattern['INCLUDE'], DEFAULT_FILE_PATTERN['INCLUDE'])
        self.assertEqual(ws.file_pattern['EXCLUDE'], DEFAULT_FILE_PATTERN['EXCLUDE'])

    def test_properties(self):
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)
        ws = Workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR, rp, 'review', init=1)
        self.assertIs(ws.file_pattern, ws._file_pattern)
        self.assertIs(ws.workspace_dir, ws._workspace_dir)
        self.assertIs(ws.deep_dir, ws._deep_dir)
        self.assertIs(ws.session_id, ws._session_id)
        self.assertIs(ws.revision, ws._revision)

        for f in self.workspace_files:
            self.assertIn(f, ws.workspace_hash)

    def test_operations(self):
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)

        # Test commit() on "review" session
        ws = Workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR, rp, 'review', init=1)
        ws.commit(['review'], data={}, add_only=0, fast_forward=0)
        self.assertIs(ws.revision, 1)
        ws.commit(['review', 'publish'], data={}, add_only=0, fast_forward=0)
        self.assertIs(ws.revision, 2)

        # Test detail_file_version() on "publish" session
        ws = Workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR, rp, 'publish', init=0)
        self.assertIs(ws.revision, 1)
        self.assertEqual(ws.latest_revision('review'), 2)
        self.assertEqual(ws.latest_revision('publish'), 1)
        self.assertEqual(ws.all_revision('review'), [1, 2])
        self.assertEqual(ws.all_revision('publish'), [1])
        self.assertEqual(set(ws.all_session()), set(['review', 'publish']))

        file_versions = ws.detail_file_version('publish', 1)
        self.assertGreater(len(file_versions), 0)
        for k in file_versions:
            self.assertEqual(file_versions[k], 1)

        # Test checkout()
        cleanup_output_workspace_dir()
        ws.checkout('review', 2)
        for f in self.workspace_files:
            self.assertIn(f, ws.workspace_hash)


@log_test(__file__)
def run():
    set_global_log_level(5)
    testcase_classes = [
        TestWorkspace,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
