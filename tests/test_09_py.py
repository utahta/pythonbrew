from tests import TESTPY_FILE

class PyOptions(object):
    pythons = []
    verbose = False

def test_py():
    from pythonbrew.commands.py import PyCommand
    c = PyCommand()
    c.run_command(PyOptions(), [TESTPY_FILE])
