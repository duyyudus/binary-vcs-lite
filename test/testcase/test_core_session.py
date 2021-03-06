from _setup_test import *
Session = session.Session
StateChain = state_chain.StateChain


class TestSession(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSession, self).__init__(*args, **kwargs)
        self.sample_session_file = Path(
            TEST_SAMPLE_DATA_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            SESSION['FOLDER'],
            'review'
        )
        self.output_session_file = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            SESSION['FOLDER'],
            'review'
        )
        self.output_state_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            STATE['FOLDER']
        )

    def setUp(self):
        create_output_repo_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_properties(self):
        sess = Session(self.sample_session_file)
        self.assertIs(sess.session_id, sess._session_id)
        self.assertIs(sess.session_file, sess._session_file)
        self.assertIs(sess.revision_data, sess._revision_data)
        self.assertEqual(
            sess.all_revision,
            sorted([int(rev) for rev in sess.revision_data])
        )
        self.assertEqual(sess.latest_revision, sess.all_revision[-1])

    def test_init(self):
        sess = Session(self.sample_session_file)
        self.assertEqual(sess.session_id, self.sample_session_file.name)
        self.assertEqual(sess.session_file, self.sample_session_file)
        self.assertGreater(len(sess.revision_data), 0)
        self.assertGreater(len(sess._detail_version_data), 0)

    def test_sync_from_state_chain_and_save(self):
        if self.output_session_file.exists():
            os.remove(str(self.output_session_file))

        state_chain = StateChain(self.output_state_dir)
        sess = Session(self.output_session_file)

        # save() is called in sync_from_state_chain()
        sess.sync_from_state_chain(state_chain)

        valid_session = load_json(self.sample_session_file, VcsLogger())

        # Test sync_from_state_chain()
        valid_revision_data = valid_session[SESSION['CONTENT']['REVISION_KEY']]
        for rev in valid_revision_data:
            self.assertIn(int(rev), sess.all_revision)
            self.assertIn(rev, sess.revision_data)
            self.assertEqual(valid_revision_data[rev], sess.revision_data[rev])

        valid_detail_version_data = valid_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']]
        real_detail_version_data = sess._detail_version_data
        for rev in valid_detail_version_data:
            self.assertEqual(valid_detail_version_data[rev], real_detail_version_data[rev])

        # Test save()
        real_session = load_json(self.output_session_file, VcsLogger())
        self.assertEqual(valid_session, real_session)

    def test_load(self):
        valid_session = load_json(self.sample_session_file, VcsLogger())

        # load() is called in __init__()
        sess = Session(self.sample_session_file)

        self.assertEqual(
            valid_session[SESSION['CONTENT']['REVISION_KEY']],
            sess.revision_data
        )
        self.assertEqual(
            valid_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']],
            sess._detail_version_data
        )

    def test_detail_file_version(self):
        valid_session = load_json(self.sample_session_file, VcsLogger())
        valid_revision_data = valid_session[SESSION['CONTENT']['REVISION_KEY']]
        valid_detail_version_data = valid_session[SESSION['CONTENT']['DETAIL_VERSION_KEY']]
        sess = Session(self.sample_session_file)

        for rev in valid_revision_data:
            self.assertEqual(
                sess.detail_file_version(int(rev)),
                valid_detail_version_data[rev]
            )

        for p in valid_detail_version_data['1']:
            print(p)
            self.assertEqual(
                sess.detail_file_version(1, relative_path=p),
                {p: valid_detail_version_data['1'][p]}
            )

        try:
            sess.detail_file_version(7)
        except Exception as e:
            self.assertTrue(check_type(e, [session.RevisionNotFound]))


@log_test(__file__)
def run():
    set_global_log_level(5)
    testcase_classes = [
        TestSession,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
