import re
from pythonbrew.basecommand import Command
from pythonbrew.define import PYTHON_PACKAGE_URL
from pythonbrew.util import Package
from pythonbrew.log import logger

class ListCommand(Command):
    name = "list"
    usage = "%prog [VERSION]"
    summary = "List the available install version of python"
    
    def run_command(self, options, args):
        if args:
            pkg = Package(args[0])
            _re = re.compile(r"%s" % pkg.name)
            pkgs = []
            for pkgname in self._get_packages_name():
                if _re.match(pkgname):
                    pkgs.append(pkgname)
            if pkgs:
                logger.info("Pythons:")
                for pkgname in pkgs:
                    logger.info("  %s" % pkgname)
            else:
                print "Package not found. `%s`" % pkg.name
        else:
            logger.info("Pythons:")
            for pkgname in self._get_packages_name():
                logger.info("  %s" % pkgname)
    
    def _get_packages_name(self):
        return ["Python-%s" % version for version in sorted(PYTHON_PACKAGE_URL.keys())]

ListCommand()
