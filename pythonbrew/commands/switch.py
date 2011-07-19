import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import Package, set_current_path, is_installed
from pythonbrew.log import logger

class SwitchCommand(Command):
    name = "switch"
    usage = "%prog VERSION"
    summary = "Permanently use the specified python as default"
    
    def run_command(self, options, args):
        if not args:
            logger.info("Unrecognized command line argument: argument not found.")
            sys.exit(1)
        pkg = Package(args[0])
        pkgname = pkg.name
        if not is_installed(pkgname):
            logger.info("`%s` is not installed." % pkgname)
            sys.exit(1)
        pkgbin = os.path.join(PATH_PYTHONS,pkgname,'bin')
        
        set_current_path('%s:%s' % (PATH_BIN, pkgbin))
        
        logger.info("Switched to %s" % pkgname)

SwitchCommand()
