from _setup_test import *


class TestUtil(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtil, self).__init__(*args, **kwargs)

    def tearDown(self):
        cleanup_output_data()

    def test_batch_copy(self):
        path_pair = []
        workspace_dir = Path(TEST_SAMPLE_DATA_WORKSPACE_DIR)
        for p in workspace_dir.rglob('*.ma'):
            source = str(p)
            target = Path(TEST_OUTPUT_DATA).joinpath(p.name)
            path_pair.append(
                (source, target)
            )

        results = util.batch_copy(path_pair, VcsLogger())
        for r in results:
            self.assertTrue(Path(r).exists())

    def test_json_util(self):
        data = {'test': 1}
        json_path = Path(TEST_OUTPUT_DATA, 'test_json')
        util.save_json(data, json_path, VcsLogger())
        loaded_data = util.load_json(json_path, VcsLogger())
        self.assertTrue('test' in loaded_data)
        self.assertTrue(loaded_data['test'])

        invalid_json = Path(TEST_OUTPUT_DATA, 'test_invalid_json')
        loaded_data = util.load_json(invalid_json, VcsLogger())
        self.assertTrue('test' not in loaded_data)
        self.assertTrue(not loaded_data)


@log_test(__file__)
def run():
    set_global_log_level(4)
    testcase_classes = [
        TestUtil
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
