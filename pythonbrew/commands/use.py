import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_HOME_ETC_TEMP
from pythonbrew.util import Package
from pythonbrew.log import logger

class UseCommand(Command):
    name = "use"
    usage = "%prog VERSION"
    summary = "Use the specified python in current shell"
    
    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        pkg = Package(args[0])
        pkgname = pkg.name
        pkgdir = os.path.join(PATH_PYTHONS, pkgname)
        if not os.path.isdir(pkgdir):
            logger.error("`%s` is not installed." % pkgname)
            sys.exit(1)
        pkgbin = os.path.join(pkgdir,'bin')
        
        self._set_temp(pkgbin)
        
        logger.info("Using `%s`" % pkgname)

    def _set_temp(self, path):
        fp = open(PATH_HOME_ETC_TEMP, 'w')
        fp.write('PATH_PYTHONBREW_TEMP="%s"\n' % (path))
        fp.close()

UseCommand()
