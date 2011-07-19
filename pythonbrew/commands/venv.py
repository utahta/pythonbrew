import os
import sys
import subprocess
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, BOOTSTRAP_DLSITE, PATH_DISTS
from pythonbrew.util import Package, get_current_use_pkgname, Link
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader

class VenvCommand(Command):
    name = "venv"
    usage = "%prog [create|use|delete|list] [project]"
    summary = "Create isolated python environments"
    
    def __init__(self):
        super(VenvCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="python",
            default=None,
            help="Use the specified version of python.",
            metavar='VERSION'
        )
    
    def run_command(self, options, args):
        if not args:
            logger.error('Unrecognized command line argument: argument not found.')
            sys.exit(1)            
        cmd = args[0]
        if not cmd in ('create', 'use', 'delete', 'list'):
            logger.error('%s command not found.' % cmd)
            sys.exit(1)
        
        # Decide which version of python to use.
        if options.python:
            pkgname = Package(options.python).name
        else:
            pkgname = get_current_use_pkgname()
        logger.info('Using %s' % pkgname)
        
        if cmd == 'create':
            self._create(args[1:])
        elif cmd == 'use':
            self._use(args[1])
        elif cmd == 'delete':
            self._delete(args[1:])
        elif cmd == 'list':
            self._list()
        
        # Download bootstrap.py
#        download_url = BOOTSTRAP_DLSITE
#        filename = Link(download_url).filename
#        bootstrap = os.path.join(PATH_DISTS, filename)
#        try:
#            d = Downloader()
#            d.download(filename, download_url, bootstrap)
#        except:
#            logger.error("Failed to download. `%s`" % download_url)
#            sys.exit(1)
#
#        # Using bootstrap.py
#        if subprocess.call([python, bootstrap, '-d']):
#            logger.error('Failed to bootstrap.')
#            sys.exit(1)
#
#        # Using buildout
#        subprocess.call(['./bin/buildout'])
        
    def _create(self, projects):
        """Create python environment"""
        for proj in projects:
            print proj
            
    def _use(self, project):
        print project
        
    def _delete(self, projects):
        for proj in projects:
            print proj
        
    def _list(self):
        print 'list'

VenvCommand()
