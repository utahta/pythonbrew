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
            help="Force installation of a Python."
        )
        self.parser.add_option(
            "-C", "--configure",
            dest="configure",
            default="",
            metavar="CONFIGURE_OPTIONS",
            help="Custom configure options."
        )
        self.parser.add_option(
            "-n", "--no-setuptools",
            dest="no_setuptools",
            action="store_true",
            default=False,
            help="Skip installation of setuptools."
        )
    
    def run_command(self, options, args):
        if args:
            # Install Python
            PythonInstaller(args[0], options).install()
        else:
            logger.info("Unknown python version.")
    
InstallCommand()
