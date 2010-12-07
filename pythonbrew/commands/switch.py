import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN, PATH_ETC_CURRENT
from pythonbrew.util import Package
from pythonbrew.log import logger

class SwitchCommand(Command):
    name = "switch"
    usage = "%prog VERSION"
    summary = "Switch to the given version of python"
    
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
        
        self._set_current('%s:%s' % (PATH_BIN, pkgbin))
        
        logger.info("Switched to %s" % pkgname)
        
    def _set_current(self, path):
        fp = open(PATH_ETC_CURRENT, 'w')
        fp.write('PATH_PYTHONBREW="%s"\n' % (path))
        fp.close()


SwitchCommand()
