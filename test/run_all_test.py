import subprocess
import os
from pathlib2 import Path

if os.name == 'posix':
    PYTHON3_PATH = '/usr/bin/python3'
    PYTHON2_PATH = '/usr/bin/python2'
elif os.name == 'nt':
    PYTHON3_PATH = r'C:\Python3.7.0\python.exe'
    PYTHON2_PATH = r'C:\Python2.7.11\python.exe'

TESTCASE_DIR = Path(__file__).parent.joinpath('testcase')

for p in TESTCASE_DIR.iterdir():
    if p.name.startswith('test') and p.name.endswith('.py'):
        subprocess.call([PYTHON3_PATH, str(p)])

for p in TESTCASE_DIR.iterdir():
    if p.name.startswith('test') and p.name.endswith('.py'):
        subprocess.call([PYTHON2_PATH, str(p)])
