import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.util import off, rm_r, Package, get_current_python_path
from pythonbrew.log import logger

class UninstallCommand(Command):
    name = "uninstall"
    usage = "%prog VERSION"
    summary = "Uninstall the given version of python"
    
    def run_command(self, options, args):
        if args:
            pkg = Package(args[0])
            pkgname = pkg.name
            pkgpath = os.path.join(PATH_PYTHONS, pkgname)
            if not os.path.isdir(pkgpath):
                logger.info("`%s` is not installed." % pkgname)
                sys.exit(1)
            if get_current_python_path() == os.path.join(pkgpath,'bin','python'):
                off()
            rm_r(pkgpath)
        else:
            self.parser.print_help()

UninstallCommand()
