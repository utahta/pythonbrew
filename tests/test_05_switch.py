from tests import TESTPY_VERSION

def test_switch():
    from pythonbrew.commands.switch import SwitchCommand
    for py_version in TESTPY_VERSION:
        c = SwitchCommand()
        c.run_command(None, [py_version])
