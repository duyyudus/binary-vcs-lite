from _setup_test import *


class TestCoreState(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreState, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_state_tree(self):
        log_info()
        t = state.StateTree('state_tree', 'last')
        proxy, med = t.root.add_children('proxyRes', 'medRes')
        asset, asset_rig, tex_folder = med.add_children('asset.ma', 'asset.rig.ma', 'textures')
        tex_folder.add_children('tex_1.tif', 'tex_2_new.tif', 'tex_3_new.tif')
        t.render_tree()


@log_test(__file__)
def run():
    testcase_classes = [
        TestCoreState,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
