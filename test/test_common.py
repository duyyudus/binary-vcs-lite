import sys
import unittest
from pprint import pprint
from pathlib2 import Path

sys.path.append(str(Path(__file__).parent.parent))
from common import hashing
from common import util

TEST_DATA_WORKDIR = Path(__file__).parent.joinpath('data', 'last')
TEST_CONCURRENT_COPY_SOURCE = Path(r'D:\temp\binary-vcs-lite-test-data\batch_copy\data')
TEST_CONCURRENT_COPY_TARGET = Path(r'D:\temp\binary-vcs-lite-test-data\batch_copy\cloned_data')


class TestHashing(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHashing, self).__init__(*args, **kwargs)

    def test_hash_workdir(self):

        ret = hashing.hash_workdir(
            TEST_DATA_WORKDIR,
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
        pprint(ret)


class TestUtil(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtil, self).__init__(*args, **kwargs)

    def test_batch_copy(self):
        path_pair = []
        for p in TEST_CONCURRENT_COPY_SOURCE.iterdir():
            path_pair.append(
                (str(p), TEST_CONCURRENT_COPY_TARGET.joinpath(p.name))
            )

        util.batch_copy(path_pair)

if __name__ == '__main__':
    case = 0
    if case == 0:
        hashing_testcase = unittest.TestLoader().loadTestsFromTestCase(TestHashing)
        unittest.TextTestRunner(verbosity=2).run(hashing_testcase)
    elif case == 1:
        util_testcase = unittest.TestLoader().loadTestsFromTestCase(TestUtil)
        unittest.TextTestRunner(verbosity=2).run(util_testcase)
