from tests import TESTPY_FILE

class PyOptions(object):
    pythons = []
    verbose = False

def _create_pyfile():
    fp = open(TESTPY_FILE, 'w')
    fp.write("print 'test'")
    fp.close()

def test_py():
    from pythonbrew.commands.py import PyCommand
    _create_pyfile()
    
    c = PyCommand()
    c.run_command(PyOptions(), [TESTPY_FILE])
