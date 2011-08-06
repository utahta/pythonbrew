import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS, PATH_HOME_ETC_VENV,\
    PATH_ETC, VIRTUALENV_DLSITE, PATH_DISTS
from pythonbrew.util import Package, \
    is_installed, get_installed_pythons_pkgname, get_using_python_pkgname,\
    untar_file
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
        self.parser.add_option(
            "-a", "--all",
            dest="all",
            action='store_true',
            default=False,
            help="Show the all python environments.",
        )
        self.parser.add_option(
            "-n", "--no-site-packages",
            dest="no_site_packages",
            action='store_true',
            default=False,
            help="Don't give access to the global site-packages dir to the virtual environment.",
        )
        self._venv_dir = os.path.join(PATH_ETC, 'virtualenv')
        self._venv = os.path.join(self._venv_dir, 'virtualenv.py')
        
    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        cmd = args[0]
        if not cmd in ('init', 'create', 'delete', 'use', 'list'):
            self.parser.print_help()
            sys.exit(1)
        
        # initialize?
        if cmd == 'init':
            self.run_command_init()
            return
        
        # target python interpreter
        if options.python:
            pkgname = Package(options.python).name
            if not is_installed(pkgname):
                logger.error('%s is not installed.' % pkgname)
                sys.exit(1)
        else:
            # check using python under pythonbrew
            pkgname = get_using_python_pkgname()
            if not pkgname:
                logger.error('Can not use venv command before switching a python.  Try \'pythonbrew switch <version of python>\'.')
                sys.exit(1)
        self._pkgname = pkgname
        self._target_py = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')
        self._workon_home = os.path.join(PATH_VENVS, pkgname)
        self._py = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')
        
        # is already installed virtualenv?
        if not os.path.exists(self._venv):
            self.run_command_init()
        
        # Create a shell script
        self.__getattribute__('run_command_%s' % cmd)(options, args)
    
    def run_command_init(self):
        if os.path.exists(self._venv):
            logger.info('venv command is already initialized.')
            return
        if not os.access(PATH_DISTS, os.W_OK):
            logger.error("Can not write to %s: Permission denied." % PATH_DISTS)
            sys.exit(1)
        d = Downloader()
        download_file = os.path.join(PATH_DISTS, 'virtualenv.tar.gz')
        d.download('virtualenv.tar.gz', VIRTUALENV_DLSITE, download_file)
        logger.info('Extracting virtualenv into %s' % self._venv_dir)
        untar_file(download_file, self._venv_dir)
    
    def run_command_create(self, options, args):
        virtualenv_options = ''
        if options.no_site_packages:
            virtualenv_options += '--no-site-packages'
        
        print 'in create'
        output = []
        for arg in args[1:]:
            target_dir = os.path.join(self._workon_home, arg)
            output.append("""\
echo '# Create `%(arg)s` environment into %(workon_home)s'
%(py)s %(venv)s -p '%(target_py)s' %(options)s '%(target_dir)s'
""" % {'arg': arg, 'workon_home': self._workon_home, 'py': self._py, 'venv': self._venv, 'target_py': self._target_py, 'options': virtualenv_options, 'target_dir': target_dir})
        self._write(''.join(output))
        
    def run_command_delete(self, options, args):
        output = []
        for arg in args[1:]:
            target_dir = os.path.join(self._workon_home, arg)
            if not os.path.isdir(target_dir):
                logger.error('%s already does not exist.' % target_dir)
            else:
                output.append("""\
echo '# Delete `%(arg)s` environment in %(workon_home)s'
rm -rf '%(target_dir)s'
""" % {'arg': arg, 'workon_home': self._workon_home, 'target_dir': target_dir})
        if output:
            self._write(''.join(output))
    
    def run_command_use(self, options, args):
        if len(args) < 2:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv use <project>' )")
            sys.exit(1)
        
        activate = os.path.join(self._workon_home, args[1], 'bin', 'activate')
        if not os.path.exists(activate):
            logger.error('`%s` environment already does not exist. Try `pythonbrew venv create %s`.' % (args[1], args[1]))
            sys.exit(1)
        
        self._write("""\
echo '# Using `%(arg)s` environment (found in %(workon_home)s)'
echo '# To leave an environment, simply run `deactivate`'
source '%(activate)s'
""" % {'arg': args[1], 'workon_home': self._workon_home, 'activate': activate})
        
    def run_command_list(self, options, args):
        if options.all:
            for pkgname in get_installed_pythons_pkgname():
                workon_home = os.path.join(PATH_VENVS, pkgname)
                logger.log("# virtualenv for %(pkgname)s (found in %(workon_home)s)" % {'pkgname': pkgname, 'workon_home': workon_home})
                if os.path.isdir(workon_home):
                    for d in sorted(os.listdir(workon_home)):
                        logger.log(d)
        else:
            logger.log("# virtualenv for %(pkgname)s (found in %(workon_home)s)" % {'pkgname': self._pkgname, 'workon_home': self._workon_home})
            if os.path.isdir(self._workon_home):
                for d in sorted(os.listdir(self._workon_home)):
                    logger.log(d)
    
    def _write(self, src):
        fp = open(PATH_HOME_ETC_VENV, 'w')
        fp.write(src)
        fp.close()
    
VenvCommand()
