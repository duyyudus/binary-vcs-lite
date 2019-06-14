from _setup_test import *
SessionManager = session_manager.SessionManager
StateChain = state_chain.StateChain


class TestSessionManager(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSessionManager, self).__init__(*args, **kwargs)
        self.sample_session_dir = Path(
            TEST_SAMPLE_DATA_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            SESSION['FOLDER']
        )
        self.output_session_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            SESSION['FOLDER']
        )
        self.sample_state_dir = Path(
            TEST_SAMPLE_DATA_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            STATE['FOLDER']
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
        sc = StateChain(self.sample_state_dir)
        sm = SessionManager(self.sample_session_dir, sc)

        self.assertIs(sm.session_dir, sm._session_dir)
        self.assertIs(sm.all_session_id, sm._all_session_id)
        self.assertIs(sm.session_data, sm._session_data)

    def test_init(self):
        sc = StateChain(self.sample_state_dir)
        sm = SessionManager(self.sample_session_dir, sc)
        self.assertEqual(sm.session_dir, self.sample_session_dir)

        all_session_id = ['review', 'publish']
        for session_id in all_session_id:
            self.assertIn(session_id, sm.all_session_id)
            self.assertEqual(sm.session_data[session_id].session_id, session_id)

        try:
            sm = SessionManager('/not/exists/dir', sc)
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.InvalidRepoSession, InvalidPath]))
        try:
            sm = SessionManager(self.sample_session_dir, None)
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.MissingStateChain]))

    def test_load_session(self):
        session_id = 'review'
        session_file = self.sample_session_dir.joinpath(session_id)

        sc = StateChain(self.sample_state_dir)
        sm = SessionManager(self.sample_session_dir, sc)
        sm._reset()

        sm.load_session(session_file)
        self.assertIn(session_id, sm.all_session_id)
        self.assertEqual(sm.session_data[session_id].session_id, session_id)

        try:
            sm.load_session('not/under/same/session_dir/session')
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.InvalidSession, PathMustBeAbsolute]))

    def test_new_session(self):
        sc = StateChain(self.output_state_dir)
        sm = SessionManager(self.output_session_dir, sc)
        sm._reset()

        session_id = 'review'
        sm.new_session(session_id)
        self.assertEqual(sm.session_data[session_id].session_id, session_id)
        self.assertGreater(len(sm.session_data[session_id].revision_data), 0)

        try:
            sm.new_session(session_id)
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.ClashingSession]))

    def test_update_session(self):
        sc = StateChain(self.output_state_dir)
        sm = SessionManager(self.output_session_dir, sc)
        sm._reset()

        all_session_id = ['review', 'publish']
        for session_id in all_session_id:
            sm.update_session(session_id)
            self.assertEqual(sm.session_data[session_id].session_id, session_id)
            self.assertGreater(len(sm.session_data[session_id].revision_data), 0)

    def test_detail_file_version(self):
        sc = StateChain(self.sample_state_dir)
        sm = SessionManager(self.sample_session_dir, sc)

        session_id = 'review'
        revision = 6
        real_diff = sm.detail_file_version(session_id, revision)
        valid_diff = sm.session_data[session_id].detail_file_version(revision)
        self.assertEqual(real_diff, valid_diff)

        try:
            sm.detail_file_version('wip', 1)
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.SessionNotFound]))

    def test_get_session(self):
        sc = StateChain(self.sample_state_dir)
        sm = SessionManager(self.sample_session_dir, sc)

        sess = sm.get_session('review')
        self.assertEqual(sess.session_id, 'review')

        try:
            sm.get_session('delivery')
        except Exception as e:
            self.assertTrue(check_type(e, [session_manager.SessionNotFound]))


@log_test(__file__)
def run():
    set_global_log_level(5)
    testcase_classes = [
        TestSessionManager,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
