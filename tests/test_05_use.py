from tests import TESTPY_VERSION

def test_use():
    from pythonbrew.commands.use import UseCommand
    for py_version in TESTPY_VERSION:
        c = UseCommand()
        c.run_command(None, [py_version])
