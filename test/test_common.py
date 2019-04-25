import sys
import unittest
from pprint import pprint
from pathlib2 import Path

sys.path.append(str(Path(__file__).parent.parent))
from common import hashing

TEST_DATA_WORKDIR = Path(__file__).parent.joinpath('data', 'last')


class TestHashing(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHashing, self).__init__(*args, **kwargs)

    def test_hash_workdir(self):

        ret = hashing.hash_workdir(
            TEST_DATA_WORKDIR,
            include_pattern=[
                # '**/*',
                '*/*.ma',
                # '*/zippy.ma',
                # '*/zippy.rig.ma',
                '*/*/*.tif',
                '*/*/*.png'
            ],
            exclude_pattern=[
                # '.jpg$',
                # '.tx$'
            ]
        )
        pprint(ret)


if __name__ == '__main__':
    hashing_testcase = unittest.TestLoader().loadTestsFromTestCase(TestHashing)
    unittest.TextTestRunner(verbosity=2).run(hashing_testcase)
