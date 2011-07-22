import os
import re
from pythonbrew.basecommand import Command
from pythonbrew.define import PYTHON_VERSION_URL, LATEST_VERSIONS_OF_PYTHON,\
    PATH_PYTHONS
from pythonbrew.util import Package, get_using_python_pkgname,\
    get_using_python_path
from pythonbrew.log import logger

class ListCommand(Command):
    name = "list"
    usage = "%prog [VERSION]"
    summary = "List the installed all pythons"
    
    def __init__(self):
        super(ListCommand, self).__init__()
        self.parser.add_option(
            '-a', '--all-versions',
            dest='all_versions',
            action='store_true',
            default=False,
            help='Show the all python versions.'
        )
        self.parser.add_option(
            '-k', '--known',
            dest='known',
            action='store_true',
            default=False,
            help='List the available latest python versions.'
        )
    
    def run_command(self, options, args):
        if options.known:
            self.available_install(options, args)
        else:
            self.installed(options, args)
    
    def installed(self, options, args):
        logger.info('# installed pythons')
        cur = get_using_python_pkgname()
        for d in sorted(os.listdir(PATH_PYTHONS)):
            if cur and cur == d:
                logger.info('%s (*)' % d)
            else:
                logger.info('%s' % d)
        if not cur:
            logger.info('%s (*)' % get_using_python_path())
    
    def available_install(self, options, args):
        logger.info('# available install pythons')
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
                logger.info("Python version not found. `%s`" % pkg.name)
        else:
            for pkgname in self._get_packages_name(options):
                logger.info("%s" % pkgname)
    
    def _get_packages_name(self, options):
        return ["Python-%s" % version for version in sorted(PYTHON_VERSION_URL.keys()) 
                if(options.all_versions or (not options.all_versions and version in LATEST_VERSIONS_OF_PYTHON))]

ListCommand()
