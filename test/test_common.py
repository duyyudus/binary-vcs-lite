from setup_test import *


class TestHashing(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHashing, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_hash_workspace_dir(self):
        print()
        workspace_hash = hashing.hash_workspace(
            TEST_OUTPUT_DATA_WORKSPACE_DIR,
            include_pattern=[
                '**/*',
                # '*/*.ma',
                # '*/asset.ma',
                # '*/asset.rig.ma',
                # '*/*/*.tif',
                # '*/*/*.png'
            ],
            exclude_pattern=[
                # '.jpg$',
                # '.tx$'
            ]
        )
        # pprint(workspace_hash)
        return workspace_hash

    def test_hash_to_path(self):
        print()
        workspace_hash = self.test_hash_workspace_dir()
        for v in workspace_hash.values():
            print(v)
            relative_path = workspace_hash.hash_to_path(v['hash'])
            self.assertEqual(relative_path, v['relative_path'])


class TestUtil(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtil, self).__init__(*args, **kwargs)

    def tearDown(self):
        cleanup_output_data()

    def test_batch_copy(self):
        print()
        path_pair = []
        workspace_dir = Path(TEST_SAMPLE_DATA_WORKSPACE_DIR)
        for p in workspace_dir.rglob('*.ma'):
            source = str(p)
            target = Path(TEST_OUTPUT_DATA).joinpath(p.name)
            path_pair.append(
                (source, target)
            )

        results = util.batch_copy(path_pair, verbose=1)
        for r in results:
            self.assertTrue(Path(r).exists())

    def test_util_json(self):
        print()
        data = {'test': 1}
        json_path = Path(TEST_OUTPUT_DATA, 'test_json')
        util.save_json(data, json_path, verbose=1)
        loaded_data = util.load_json(json_path, verbose=1)
        self.assertTrue('test' in loaded_data)
        self.assertTrue(loaded_data['test'])

        invalid_json = Path(TEST_OUTPUT_DATA, 'test_invalid_json')
        loaded_data = util.load_json(invalid_json, verbose=1)
        self.assertTrue('test' not in loaded_data)
        self.assertTrue(not loaded_data)

if __name__ == '__main__':
    testcase_classes = [
        TestHashing,
        TestUtil
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)
