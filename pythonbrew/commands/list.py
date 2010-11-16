import re
from pythonbrew.basecommand import Command
from pythonbrew.define import PYTHON_VERSION_URL, LATEST_VERSIONS_OF_PYTHON
from pythonbrew.util import Package
from pythonbrew.log import logger

class ListCommand(Command):
    name = "list"
    usage = "%prog [VERSION]"
    summary = "List the available install version of python"

    def __init__(self):
        super(ListCommand, self).__init__()
        self.parser.add_option(
            "--all-versions",
            dest="all_versions",
            action="store_true",
            default=False,
            help="All versions of Python are visible."
        )
    
    def run_command(self, options, args):
        if args:
            pkg = Package(args[0])
            _re = re.compile(r"%s" % pkg.name)
            pkgs = []
            for pkgname in self._get_packages_name(options):
                if _re.match(pkgname):
                    pkgs.append(pkgname)
            if pkgs:
                for pkgname in pkgs:
                    logger.info("%s" % pkgname)
            else:
                print "Python version not found. `%s`" % pkg.name
        else:
            for pkgname in self._get_packages_name(options):
                logger.info("%s" % pkgname)
    
    def _get_packages_name(self, options):
        return ["Python-%s" % version for version in sorted(PYTHON_VERSION_URL.keys()) 
                if(options.all_versions or (not options.all_versions and version in LATEST_VERSIONS_OF_PYTHON))]

ListCommand()
