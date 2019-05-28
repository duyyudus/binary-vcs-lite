from _setup_test import *
State = state.State


class TestState(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestState, self).__init__(*args, **kwargs)
        self.test_state_file = Path(
            TEST_OUTPUT_DATA_WORKSPACE_DIR,
            VCS_FOLDER,
            REPO['FOLDER'],
            STATE['FOLDER'],
            's0'
        )

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_update(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        s0 = State(self.test_state_file)
        s0.update(
            workspace_hash,
            ['review'],
            {'message': 'test_state'}
        )

        for v in workspace_hash.values():
            relative_path = v[WORKSPACE_HASH['RELATIVE_PATH_KEY']]
            hash_value = v[WORKSPACE_HASH['HASH_KEY']]
            n = s0.state_tree.search(relative_path)
            self.assertGreater(len(n), 0)
            self.assertEqual(n[0].data, hash_value)

        self.assertTrue(s0.timestamp is not None)
        self.assertGreater(len(s0.session_list), 0)
        self.assertGreater(len(s0.data.values()), 0)

    def test_set_next(self):
        s0 = State('path/to/s0')
        s1 = State('path/to/s1')
        s0.set_next(s1)
        self.assertEqual(s0.next, s1)
        self.assertEqual(s1.previous, s0)

    def test_set_previous(self):
        s0 = State('path/to/s0')
        s1 = State('path/to/s1')
        s1.set_previous(s0)
        self.assertEqual(s0.next, s1)
        self.assertEqual(s1.previous, s0)

    def test_save(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        s0 = State(self.test_state_file)
        s0.update(
            workspace_hash,
            ['review'],
            {'message': 'test_state'}
        )
        s0.save()

        valid_data = load_json(self.test_state_file)
        self.assertEqual(
            valid_data[STATE['CONTENT']['TIMESTAMP_KEY']],
            s0.timestamp
        )
        self.assertEqual(
            valid_data[STATE['CONTENT']['SESSION_LIST_KEY']],
            s0.session_list
        )
        self.assertEqual(
            valid_data[STATE['CONTENT']['DATA_KEY']],
            s0.data
        )

        self.assertGreater(len(valid_data[STATE['CONTENT']['FILE_KEY']]), 0)
        for f in valid_data[STATE['CONTENT']['FILE_KEY']]:
            n = s0.state_tree.search(Path(f).parent.as_posix())
            self.assertGreater(len(n), 0)

    def test_load(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        s0 = State(self.test_state_file)
        s0.update(
            workspace_hash,
            ['review'],
            {'message': 'test_state'}
        )
        s0.save()

        s0 = State(self.test_state_file)
        s0.load()

        valid_data = load_json(self.test_state_file)
        self.assertEqual(
            valid_data[STATE['CONTENT']['TIMESTAMP_KEY']],
            s0.timestamp
        )
        self.assertEqual(
            valid_data[STATE['CONTENT']['SESSION_LIST_KEY']],
            s0.session_list
        )
        self.assertEqual(
            valid_data[STATE['CONTENT']['DATA_KEY']],
            s0.data
        )

        self.assertGreater(len(valid_data[STATE['CONTENT']['FILE_KEY']]), 0)
        for f in valid_data[STATE['CONTENT']['FILE_KEY']]:
            n = s0.state_tree.search(Path(f).parent.as_posix())
            self.assertGreater(len(n), 0)


class TestStateTree(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStateTree, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_init(self):
        workspace_hash = hashing.hash_workspace(TEST_OUTPUT_DATA_WORKSPACE_DIR)
        state_tree = state.StateTree(workspace_hash)
        for v in workspace_hash.values():
            relative_path = v[WORKSPACE_HASH['RELATIVE_PATH_KEY']]
            hash_value = v[WORKSPACE_HASH['HASH_KEY']]
            n = state_tree.search(relative_path)
            self.assertGreater(len(n), 0)
            self.assertEqual(n[0].data, hash_value)


@log_test(__file__)
def run():
    testcase_classes = [
        TestState,
        TestStateTree
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
