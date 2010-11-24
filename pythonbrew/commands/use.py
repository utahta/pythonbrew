import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import Package, write_temp
from pythonbrew.log import logger

class UseCommand(Command):
    name = "use"
    usage = "%prog VERSION"
    summary = "Using the given version of python"
    
    def run_command(self, options, args):
        if not args:
            logger.info("Unrecognized command line argument: argument not found.")
            sys.exit(1)
        pkg = Package(args[0])
        pkgname = pkg.name
        pkgdir = os.path.join(PATH_PYTHONS, pkgname)
        if not os.path.isdir(pkgdir):
            logger.info("`%s` is not installed." % pkgname)
            sys.exit(1)
        pkgbin = os.path.join(pkgdir,'bin')
        
        write_temp('%s:%s' % (PATH_BIN, pkgbin))
        
        logger.info("Using `%s`" % pkgname)

UseCommand()
