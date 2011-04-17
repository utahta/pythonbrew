from pythonbrew.basecommand import Command
from pythonbrew.log import logger
from pythonbrew.installer.pythoninstaller import PythonInstaller,\
    PythonInstallerMacOSX
from pythonbrew.util import is_macosx_snowleopard
from pythonbrew.exceptions import UnknownVersionException,\
    AlreadyInstalledException, NotSupportedVersionException

class InstallCommand(Command):
    name = "install"
    usage = "%prog [OPTIONS] VERSION"
    summary = "Build and install the given version of python"
    
    def __init__(self):
        super(InstallCommand, self).__init__()
        self.parser.add_option(
            "-f", "--force",
            dest="force",
            action="store_true",
            default=False,
            help="Force install of python.(skip make test)"
        )
        self.parser.add_option(
            "-C", "--configure",
            dest="configure",
            default="",
            metavar="CONFIGURE_OPTIONS",
            help="Options passed directly to configure."
        )
        self.parser.add_option(
            "-n", "--no-setuptools",
            dest="no_setuptools",
            action="store_true",
            default=False,
            help="Skip install of setuptools."
        )
        self.parser.add_option(
            "--as",
            dest="alias",
            default=None,
            help="Install a python under an alias."
        )
        self.parser.add_option(
            '-j', "--jobs",
            dest="jobs",
            type='int',
            default=0,
            help="Enable parallel make."
        )
    
    def run_command(self, options, args):
        if args:
            # Install pythons
            for arg in args:
                try:
                    if is_macosx_snowleopard():
                        p = PythonInstallerMacOSX(arg, options)
                    else:
                        p = PythonInstaller(arg, options)
                    p.install()
                except UnknownVersionException:
                    continue
                except AlreadyInstalledException:
                    continue
                except NotSupportedVersionException:
                    continue
        else:
            logger.info("Unknown python version.")
    
InstallCommand()
