from tests import TESTPY_VERSION

def test_use():
    from pythonbrew.commands.use import UseCommand
    c = UseCommand()
    c.run_command(None, [TESTPY_VERSION])
