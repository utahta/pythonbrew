from tests import PYTHONBREW_ROOT
import os

TESTPY_FILE = os.path.join(PYTHONBREW_ROOT, 'etc', 'testfile.py')

class PyOptions(object):
    pythons = []
    verbose = False
    bin = "python"
    options = ""

def _create_pyfile():
    fp = open(TESTPY_FILE, 'w')
    fp.write("print('test')")
    fp.close()

def test_py():
    from pythonbrew.commands.py import PyCommand
    _create_pyfile()
    
    c = PyCommand()
    c.run_command(PyOptions(), [TESTPY_FILE])
