from tests import TESTPY_VERSION

def test_uninstall():
    from pythonbrew.commands.uninstall import UninstallCommand
    for py_version in TESTPY_VERSION:
        c = UninstallCommand()
        c.run_command(None, [py_version])
