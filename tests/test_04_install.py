from tests import TESTPY_VERSION

class InstallOptions(object):
    force = True
    configure = ""
    no_setuptools = False
    alias = None
    jobs = 2

def test_install():
    from pythonbrew.commands.install import InstallCommand
    py_version = TESTPY_VERSION.pop(0)
    c = InstallCommand()
    c.run_command(InstallOptions(), [py_version]) # pybrew install -f -j2 2.4.6
    c.run_command(InstallOptions(), TESTPY_VERSION) # pybrew install -f -j2 2.5.6 2.6.6 3.2

