from _setup_test import *


class TestHashing(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHashing, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_hash_workspace_dir(self):
        log_info()
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
        for k in workspace_hash:
            self.assertTrue(
                Path(workspace_hash[k][WORKSPACE['ABSOLUTE_PATH_KEY']]).exists()
            )
        return workspace_hash

    def test_hash_to_path(self):
        log_info()
        workspace_hash = self.test_hash_workspace_dir()
        for v in workspace_hash.values():
            relative_path = workspace_hash.hash_to_path(v['hash'])
            self.assertEqual(relative_path, v[WORKSPACE['RELATIVE_PATH_KEY']])


class TestUtil(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtil, self).__init__(*args, **kwargs)

    def tearDown(self):
        cleanup_output_data()

    def test_batch_copy(self):
        log_info()
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
        log_info()
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


@log_test(__file__)
def run():
    testcase_classes = [
        TestHashing,
        TestUtil
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
