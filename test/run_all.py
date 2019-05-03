import sys
from pathlib2 import Path

if __name__ == '__main__':
    TESTCASE_DIR = Path(__file__).resolve().parent.joinpath('testcase')
    sys.path.append(str(TESTCASE_DIR))

    for p in TESTCASE_DIR.iterdir():
        if p.name.startswith('test') and p.name.endswith('.py'):
            if sys.version_info[0] == 3:
                import importlib.util
                spec = importlib.util.spec_from_file_location(p.name, str(p))
                testcase = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(testcase)
                testcase.run()
            else:
                import imp
                testcase = imp.load_source(p.name, str(p))
                testcase.run()
