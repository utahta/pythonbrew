import sys
from pythonbrew.basecommand import Command
from pythonbrew.installer.pythoninstaller import PythonInstaller,\
    PythonInstallerMacOSX
from pythonbrew.util import is_macosx

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
            help="Force installation of python."
        )
        self.parser.add_option(
            "-t", "--test",
            dest="test",
            action="store_true",
            default=False,
            help="Running `make test`."
        )
        self.parser.add_option(
            "-v", "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Display log information on the console."
        )
        self.parser.add_option(
            "-C", "--configure",
            dest="configure",
            default="",
            metavar="CONFIGURE_OPTIONS",
            help="Options passed directly to configure."
        )
        self.parser.add_option(
            "--no-setuptools",
            dest="no_setuptools",
            action="store_true",
            default=False,
            help="Skip installation of setuptools."
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
        self.parser.add_option(
            "--framework",
            dest="framework",
            action="store_true",
            default=False,
            help="Build (MacOSX|Darwin) framework."
        )
        self.parser.add_option(
            "--universal",
            dest="universal",
            action="store_true",
            default=False,
            help="Build for both 32 & 64 bit Intel."
        )
        self.parser.add_option(
            "--static",
            dest="static",
            action="store_true",
            default=False,
            help="Build static libraries."
        )

    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        # installing python
        for arg in args:
            try:
                if is_macosx():
                    p = PythonInstallerMacOSX(arg, options)
                else:
                    p = PythonInstaller(arg, options)
                p.install()
            except:
                continue

InstallCommand()
