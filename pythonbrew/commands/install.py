from pythonbrew.basecommand import Command
from pythonbrew.log import logger
from pythonbrew.installer import PythonInstaller

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
    
    def run_command(self, options, args):
        if args:
            # Install Python
            PythonInstaller(args[0], options).install()
        else:
            logger.info("Unknown python version.")
    
InstallCommand()
