from _setup_test import *
StateChain = state_chain.StateChain


class TestStateChain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStateChain, self).__init__(*args, **kwargs)
        self.output_state_dir = Path(
            TEST_OUTPUT_DATA_LOCAL_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            STATE['FOLDER']
        )
        self.sample_state_dir = Path(
            TEST_SAMPLE_DATA_REPO_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            STATE['FOLDER']
        )

    def setUp(self):
        create_output_repo_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_properties(self):
        log_info()
        sc = StateChain(self.sample_state_dir)

        self.assertIs(sc.state_dir, sc._state_dir)
        self.assertIs(sc.all_state_id, sc._all_state_id)
        self.assertIs(sc.state_data, sc._state_data)
        self.assertIs(sc.last_state, sc.state_data[sc.all_state_id[-1]])

    def test_init(self):
        log_info()
        sc = StateChain(self.sample_state_dir)
        self.assertEqual(sc.state_dir, self.sample_state_dir)

        all_state_id = ['s0', 's1', 's2', 's3', 's4', 's5']
        self.assertEqual(sc.all_state_id, all_state_id)
        for i in all_state_id:
            self.assertEqual(sc.state_data[i].state_id, i)

        try:
            sc = StateChain('not/exists/dir')
        except Exception as e:
            self.assertTrue(check_type(e, [state_chain.InvalidRepoState]))

    def test_load_state(self):
        log_info()
        s0_file = self.sample_state_dir.joinpath('s0')
        s1_file = self.sample_state_dir.joinpath('s1')

        sc = StateChain(self.sample_state_dir)
        sc._reset()

        sc.load_state(s0_file)
        self.assertIs(sc.last_state.state_id, 's0')
        sc.load_state(s1_file)
        self.assertIs(sc.last_state.state_id, 's1')
        self.assertIs(sc.state_data['s0'].next, sc.state_data['s1'])
        self.assertIs(sc.state_data['s1'].previous, sc.state_data['s0'])

        try:
            sc.load_state('not/under/same/state_dir/state')
        except Exception as e:
            self.assertTrue(check_type(e, [state_chain.InvalidState]))

    def test_new_state(self):
        log_info()
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        sc = StateChain(self.output_state_dir)
        new_state = sc.new_state(
            workspace_hash,
            ['review'],
            {'message': 'new_state'}
        )

        for v in workspace_hash.values():
            relative_path = v[WORKSPACE_HASH['RELATIVE_PATH_KEY']]
            hash_value = v[WORKSPACE_HASH['HASH_KEY']]
            n = new_state.state_tree.search(relative_path)
            self.assertGreater(len(n), 0)
            self.assertEqual(n[0].data, hash_value)

        self.assertEqual(new_state.state_id, 's6')
        self.assertTrue(check_type(new_state.timestamp, [str]))
        self.assertGreater(len(new_state.session_list), 0)
        self.assertGreater(len(new_state.data.values()), 0)

        self.assertTrue(new_state.state_file.exists())
        os.remove(str(new_state.state_file))


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
