from _setup_test import *
VersioningInterface = vcs_interface.VersioningInterface
RemoteVersioning = vcs_interface.RemoteVersioning
LocalVersioning = vcs_interface.LocalVersioning


class TestVersioningInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestVersioningInterface, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_workspace_deep_dir = self.output_vcs_dir.joinpath(
            WORKSPACE['FOLDER']
        )
        self.output_repo_deep_dir = self.output_vcs_dir.joinpath(
            REPO['FOLDER']
        )
        self.workspace_files = [
            'medRes/asset.ma',
            'medRes/asset.rig.ma',
            'medRes/old/asset.ma',
            'medRes/textures/tex_1.tif',
            'medRes/textures/tex_2_new_name.tif',
            'medRes/textures/tex_3_new_name.tif',
            'medRes/textures/tex_4.tif',
            'proxyRes/asset.ma',
            'proxyRes/asset.rig.ma',
        ]

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        vi = VersioningInterface(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            repo_dir=TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            session_id='review',
            init_workspace=1,
            init_repo=1
        )
        self.assertEqual(vi.workspace.deep_dir, self.output_workspace_deep_dir)
        self.assertEqual(vi.repo.deep_dir, self.output_repo_deep_dir)
        self.assertTrue(vi.workspace.deep_dir.exists())
        self.assertTrue(vi.repo.deep_dir.exists())

    def test_properties(self):
        vi = VersioningInterface(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            repo_dir=TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            session_id='review',
            init_workspace=1,
            init_repo=1
        )
        self.assertIs(vi.repo, vi._repo)
        self.assertIs(vi.workspace, vi._workspace)

    def test_operations(self):

        # Test commit() on "review" session
        vi = VersioningInterface(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            repo_dir=TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            session_id='review',
            init_workspace=1,
            init_repo=1
        )
        vi.commit(['review'], data={}, add_only=0, fast_forward=0)
        self.assertIs(vi.workspace.revision, 1)
        vi.commit(['review', 'publish'], data={}, add_only=0, fast_forward=0)
        self.assertIs(vi.workspace.revision, 2)

        # Test detail_file_version() on "publish" session
        vi = VersioningInterface(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            repo_dir=TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            session_id='publish',
            init_workspace=0,
            init_repo=0
        )
        self.assertIs(vi.workspace.revision, 1)
        self.assertEqual(vi.latest_revision('review'), 2)
        self.assertEqual(vi.latest_revision('publish'), 1)
        self.assertEqual(vi.all_revision('review'), [1, 2])
        self.assertEqual(vi.all_revision('publish'), [1])
        self.assertEqual(set(vi.all_session()), set(['review', 'publish']))

        file_versions = vi.detail_file_version('publish', 1)
        self.assertGreater(len(file_versions), 0)
        for k in file_versions:
            self.assertEqual(file_versions[k], 1)

        # Test checkout()
        cleanup_output_workspace_dir
        vi.checkout('review', 2)
        for f in self.workspace_files:
            self.assertIn(f, vi.workspace.workspace_hash)


class TestLocalVersioning(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLocalVersioning, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_workspace_deep_dir = self.output_vcs_dir.joinpath(
            WORKSPACE['FOLDER']
        )
        self.output_repo_deep_dir = self.output_vcs_dir.joinpath(
            REPO['FOLDER']
        )

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        vi = LocalVersioning(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            session_id='review'
        )
        self.assertEqual(vi.workspace.deep_dir, self.output_workspace_deep_dir)
        self.assertEqual(vi.repo.deep_dir, self.output_repo_deep_dir)
        self.assertTrue(vi.workspace.deep_dir.exists())
        self.assertTrue(vi.repo.deep_dir.exists())


class TestRemoteVersioning(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRemoteVersioning, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_remove_vcs_dir = Path(
            TEST_OUTPUT_DATA_REMOTE_REPO_DIR,
            VCS_FOLDER
        )

        self.output_workspace_deep_dir = self.output_vcs_dir.joinpath(
            WORKSPACE['FOLDER']
        )
        self.output_remote_repo_deep_dir = self.output_remove_vcs_dir.joinpath(
            REPO['FOLDER']
        )

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        vi = RemoteVersioning(
            workspace_dir=TEST_OUTPUT_DATA_WORKSPACE_DIR,
            repo_dir=TEST_OUTPUT_DATA_REMOTE_REPO_DIR,
            session_id='review'
        )
        self.assertEqual(vi.workspace.deep_dir, self.output_workspace_deep_dir)
        self.assertEqual(vi.repo.deep_dir, self.output_remote_repo_deep_dir)
        self.assertTrue(vi.workspace.deep_dir.exists())
        self.assertTrue(vi.repo.deep_dir.exists())


@log_test(__file__)
def run():
    set_global_log_level(5)
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
