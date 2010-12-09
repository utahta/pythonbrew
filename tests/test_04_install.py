from tests import TESTPY_VERSION

class InstallOptions(object):
    force = True
    configure = ""
    no_setuptools = False

def test_install():
    from pythonbrew.commands.install import InstallCommand
    c = InstallCommand()
    c.run_command(InstallOptions(), [TESTPY_VERSION])
