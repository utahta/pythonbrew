import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.util import off, rm_r, Package
from pythonbrew.log import logger

class UninstallCommand(Command):
    name = "uninstall"
    usage = "%prog VERSION"
    summary = "Uninstall the given version of python"
    
    def run_command(self, options, args):
        if args:
            pkg = Package(args[0])
            pkgname = pkg.name
            pkgpath = "%s/%s" % (PATH_PYTHONS, pkgname)
            if not os.path.isdir(pkgpath):
                logger.info("`%s` is not installed." % pkgname)
                sys.exit(1)
            if os.path.islink("%s/current" % PATH_PYTHONS):
                curpath = os.path.realpath("%s/current" % PATH_PYTHONS)
                if pkgpath == curpath:
                    off()
            rm_r(pkgpath)
        else:
            self.parser.print_help()

UninstallCommand()
