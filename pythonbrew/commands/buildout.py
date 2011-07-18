import os
import sys
import subprocess
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, BOOTSTRAP_DLSITE, PATH_DISTS
from pythonbrew.util import Package, get_current_python_path, Link
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader

class BuildoutCommand(Command):
    name = "buildout"
    usage = "%prog"
    summary = "Runs the buildout against specified or currently use python"
    
    def __init__(self):
        super(BuildoutCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="python",
            default=None,
            help="Use the specified version of python.",
            metavar='VERSION'
        )
        self.parser.disable_interspersed_args()
    
    def run_command(self, options, args):
        if options.python:
            python = Package(options.python).name
            python = os.path.join(PATH_PYTHONS, python, 'bin', 'python')
            if not os.path.isfile(python):
                logger.info('%s is not installed.' % options.python)
                sys.exit(1)
        else:
            python = get_current_python_path()
        logger.info('Using %s' % python)
        
        # Download bootstrap.py
        download_url = BOOTSTRAP_DLSITE
        filename = Link(download_url).filename
        bootstrap = os.path.join(PATH_DISTS, filename)
        try:
            d = Downloader()
            d.download(filename, download_url, bootstrap)
        except:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)

        # Using bootstrap.py
        if subprocess.call([python, bootstrap, '-d']):
            logger.error('Failed to bootstrap.')
            sys.exit(1)

        # Using buildout
        subprocess.call(['./bin/buildout'])

BuildoutCommand()
