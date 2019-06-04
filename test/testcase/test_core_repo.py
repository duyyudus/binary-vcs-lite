from _setup_test import *
Repo = repo.Repo


class TestRepo(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRepo, self).__init__(*args, **kwargs)
        self.output_vcs_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER
        )
        self.output_repo_deep_dir = self.output_vcs_dir.joinpath(
            REPO['FOLDER']
        )
        self.output_session_dir = self.output_repo_dir.joinpath(
            SESSION['FOLDER']
        )
        self.output_state_dir = self.output_repo_dir.joinpath(
            STATE['FOLDER']
        )
        self.output_blob_dir = self.output_repo_dir.joinpath(
            BLOB['FOLDER']
        )

    def setUp(self):
        create_output_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        log_info()
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)

        self.assertTrue(check_type(rp.repo_id, [str]))

        self.assertEqual(str(rp.repo_dir), TEST_OUTPUT_DATA_LOCAL_REPO_DIR)
        self.assertEqual(rp.deep_dir, self.output_repo_deep_dir)
        self.assertEqual(rp._session_dir, self.output_session_dir)
        self.assertEqual(rp._state_dir, self.output_state_dir)
        self.assertEqual(rp._blob_dir, self.output_blob_dir)

        self.assertTrue(self.output_repo_deep_dir.exists())
        self.assertTrue(self.output_session_dir.exists())
        self.assertTrue(self.output_state_dir.exists())
        self.assertTrue(self.output_blob_dir.exists())

        self.assertEqual(rp._session_manager.session_dir, self.output_session_dir)
        self.assertEqual(rp._state_chain.state_dir, self.output_state_dir)
        self.assertEqual(rp._blob.blob_dir, self.output_blob_dir)

        repo_metadata = load_json(rp._metadata_path)
        repo_id = repo_metadata[REPO['METADATA']['REPO_ID_KEY']]
        self.assertEqual(rp.repo_id, repo_id)

        try:
            Repo('not/exists/dir', init=0)
        except Exception as e:
            self.assertTrue(check_type(e, [repo.RepoNotFound]))

    def test_properties(self):
        log_info()
        rp = Repo(TEST_OUTPUT_DATA_LOCAL_REPO_DIR, init=1)
        self.assertIs(rp.repo_dir, rp._repo_dir)
        self.assertIs(rp.deep_dir, rp._deep_dir)
        self.assertIs(rp.repo_id, rp._repo_id)

    def test_operations(self):
        log_info()
        sample_workspace_list_dir = Path(TEST_SAMPLE_DATA_WORKSPACE_DIR).parent
        current_workspace_dir = Path(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        workspace_list = [1, 2, 3, 4, 5, 6, 7]

        shutil.rmtree(str(current_workspace_dir))

        rp = Repo(current_workspace_dir, init=1)

        # Run state_in()
        for v in workspace_list:
            sample_workspace_dir = sample_workspace_list_dir.joinpath(str(v))
            sample_wh = hashing.hash_workspace(sample_workspace_dir)
            rp.state_in(
                sample_wh,
                session_list=['review', 'publish'] if v in [5, 7] else ['review'],
                data={},
                current_session_id='review',
                current_revision=v,
                add_only=1 if v == 5 else 0
            )

        # Test state_out()
        for v in workspace_list:
            shutil.rmtree(str(current_workspace_dir))

            current_wh = hashing.hash_workspace(current_workspace_dir)
            rp.state_out(current_wh, 'review', v, overwrite=1)

            sample_workspace_dir = sample_workspace_list_dir.joinpath(v)
            sample_wh = hashing.hash_workspace(sample_workspace_dir)
            current_wh = hashing.hash_workspace(current_workspace_dir)

            # Start checking if `sample_wh` and `current_wh` are equal
            #

            # add only case
            tex1_hash = sample_workspace_list_dir.joinpath('4', 'medRes', 'textures', 'tex_1.tif')
            tex2_hash = sample_workspace_list_dir.joinpath('4', 'medRes', 'textures', 'tex_2.tif')

            if v == 5:
                sample_wh['medRes/textures/tex_1.tif'] = {
                    WORKSPACE_HASH['HASH_KEY']: hashing.hash_file(str(tex1_hash)),
                    WORKSPACE_HASH['RELATIVE_PATH_KEY']: 'medRes/textures/tex_1.tif'
                }
                sample_wh['medRes/textures/tex_2.tif'] = {
                    WORKSPACE_HASH['HASH_KEY']: hashing.hash_file(str(tex2_hash)),
                    WORKSPACE_HASH['RELATIVE_PATH_KEY']: 'medRes/textures/tex_2.tif'
                }
            self.assertEqual(len(list(sample_wh)), len(list(current_wh)))
            for k in sample_wh:
                self.assertIn(k, current_wh)
                self.assertEqual(
                    sample_wh[k][WORKSPACE_HASH['HASH_KEY']],
                    current_wh[k][WORKSPACE_HASH['HASH_KEY']]
                )

        # Test latest_revision()
        self.assertEqual(rp.latest_revision('review'), workspace_list[-1])

        # Test all_revision()
        self.assertEqual(rp.all_revision('review'), workspace_list)

        # Test all_session()
        self.assertEqual(rp.all_session(), set(['review', 'publish']))

        # Test detail_file_version()
        valid_review_session = load_json(sample_workspace_list_dir.joinpath('_valid_review_session.json'))
        valid_publish_session = load_json(sample_workspace_list_dir.joinpath('_valid_publish_session.json'))

        # Session "review" with latest version 7
        self.assertEqual(
            rp.detail_file_version('review'),
            valid_review_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']]['7']
        )
        # Session "review" with version 3
        self.assertEqual(
            rp.detail_file_version('review', 3),
            valid_review_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']]['3']
        )
        # Session "publish" with version 2
        self.assertEqual(
            rp.detail_file_version('publish', 2),
            valid_publish_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']]['2']
        )


@log_test(__file__)
def run():
    testcase_classes = [
        TestRepo,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
