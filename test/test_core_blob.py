import sys
import unittest
from pprint import pprint
from pathlib2 import Path

sys.path.append(str(Path(__file__).parent.parent))
from core import blob

TEST_DATA_WORKDIR = Path(__file__).parent.joinpath('data', 'last')


class TestCoreBlob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreBlob, self).__init__(*args, **kwargs)

    def test_store_blob(self):
        b = blob.Blob(TEST_DATA_WORKDIR, TEST_DATA_WORKDIR)
        b.store_blob(verbose=1)


if __name__ == '__main__':
    case = 0
    if case == 0:
        blob_testcase = unittest.TestLoader().loadTestsFromTestCase(TestCoreBlob)
        unittest.TextTestRunner(verbosity=2).run(blob_testcase)
