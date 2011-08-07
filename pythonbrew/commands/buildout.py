import os
import sys
import subprocess
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, BOOTSTRAP_DLSITE
from pythonbrew.util import Package, get_using_python_pkgname, Link, is_installed
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader

class BuildoutCommand(Command):
    name = "buildout"
    usage = "%prog"
    summary = "Runs the buildout with specified or current using python"
    
    def __init__(self):
        super(BuildoutCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="python",
            default=None,
            help="Use the specified version of python.",
            metavar='VERSION'
        )
    
    def run_command(self, options, args):
        if options.python:
            pkgname = Package(options.python).name
        else:
            pkgname = get_using_python_pkgname()
        if not is_installed(pkgname):
            logger.error('`%s` is not installed.' % pkgname)
            sys.exit(1)
        logger.info('Using %s' % pkgname)
        
        # build a path
        python = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')
        
        # Download bootstrap.py
        download_url = BOOTSTRAP_DLSITE
        filename = Link(download_url).filename
        bootstrap = os.path.join(os.getcwd(), filename) # fetching into current directory
        try:
            d = Downloader()
            d.download(filename, download_url, bootstrap)
        except:
            e = sys.exc_info()[1]
            logger.error("%s" % (e))
            sys.exit(1)

        # call bootstrap.py
        if subprocess.call([python, bootstrap, '-d']):
            logger.error('Failed to bootstrap.')
            sys.exit(1)

        # call buildout
        subprocess.call(['./bin/buildout'])

BuildoutCommand()
