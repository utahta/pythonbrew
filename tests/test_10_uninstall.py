from tests import TESTPY_VERSION

def test_uninstall():
    from pythonbrew.commands.uninstall import UninstallCommand
    c = UninstallCommand()
    c.run_command(None, [TESTPY_VERSION])
