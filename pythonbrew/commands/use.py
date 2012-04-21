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
        pkglib = os.path.join(pkgdir,'lib')

        self._set_temp(pkgbin, pkglib)

        logger.info("Using `%s`" % pkgname)

    def _set_temp(self, bin_path, lib_path):
        fp = open(PATH_HOME_ETC_TEMP, 'w')
        fp.write('deactivate &> /dev/null\nPATH_PYTHONBREW_TEMP="%s"\nPATH_PYTHONBREW_TEMP_LIB="%s"\n' % (bin_path, lib_path))
        fp.close()

UseCommand()
