from tests import TESTPY_VERSION

def test_switch():
    from pythonbrew.commands.switch import SwitchCommand
    c = SwitchCommand()
    c.run_command(None, [TESTPY_VERSION])
