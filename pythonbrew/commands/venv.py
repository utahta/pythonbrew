import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS, PATH_ETC_VENV
from pythonbrew.util import get_using_python_pkgname, Subprocess, Package,\
    is_installed
from pythonbrew.log import logger

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
            logger.error('Unrecognized command line argument: ( see: \'pythonbrew help venv\' )')
            sys.exit(1)
        cmd = args[0]
        if not cmd in ('create', 'use', 'delete', 'list'):
            logger.error('Unrecognized command line argument: ( see: \'pythonbrew help venv\' )')
            sys.exit(1)
        
        if options.python:
            pkgname = Package(options.python).name
            if not is_installed(pkgname):
                logger.error('%s is not installed.' % pkgname)
                sys.exit(1)
        else:
            pkgname = get_using_python_pkgname()
            if not pkgname:
                logger.error('Can not create virtual environment before using a python.  Try \'pythonbrew install <some python>\'.')
                sys.exit(1)
        pkg_dir = os.path.join(PATH_PYTHONS, pkgname)
        pkg_bin_dir = os.path.join(pkg_dir, 'bin')
        
        self._pkg_bin_dir = pkg_bin_dir
        self._venv_dir = os.path.join(PATH_VENVS, pkgname)
        
        # has virtualenv & virtualenvwrapper?
        if(not os.path.exists(os.path.join(pkg_bin_dir, 'virtualenvwrapper.sh')) or 
           not os.path.exists(os.path.join(pkg_bin_dir, 'virtualenv'))):
            logger.info('Installing virtualenv into %s' % pkg_dir)
            s = Subprocess(verbose=True)
            s.shell('%s %s %s' % (os.path.join(pkg_bin_dir,'pip'), 'install', 'virtualenvwrapper'))
        
        # Initialize virtualenv
        self._init()
        
        # check
        if cmd == 'use':
            if len(args) < 2:
                logger.error("Unrecognized command line argument: ( 'pythonbrew venv use <project>' )")
                sys.exit(1)
        elif cmd == 'list':
            logger.info('# virtualenv for %s (found in %s)' % (pkgname, self._venv_dir))
    
    def _init(self):
        fp = open(PATH_ETC_VENV, 'w')
        fp.write("VIRTUALENVWRAPPER_PYTHON=%s\n" % os.path.join(self._pkg_bin_dir, 'python'))
        fp.write("WORKON_HOME=%s" % self._venv_dir)
        fp.close()

VenvCommand()
