import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS, PATH_HOME_ETC_VENV,\
    PATH_ETC, VIRTUALENV_DLSITE, PATH_DISTS
from pythonbrew.util import Package, \
    is_installed, get_installed_pythons_pkgname, get_using_python_pkgname,\
    untar_file, Subprocess, rm_r
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader

class VenvCommand(Command):
    name = "venv"
    usage = "%prog [create|use|delete|list|rename|print_activate] [project]"
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
        if not cmd in ('init', 'create', 'delete', 'use', 'list', 'rename', 'print_activate'):
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
            logger.error("Can not initialize venv command: Permission denied.")
            sys.exit(1)
        d = Downloader()
        download_file = os.path.join(PATH_DISTS, 'virtualenv.tar.gz')
        d.download('virtualenv.tar.gz', VIRTUALENV_DLSITE, download_file)
        logger.info('Extracting virtualenv into %s' % self._venv_dir)
        untar_file(download_file, self._venv_dir)
    
    def run_command_rename(self, options, args):
        if len(args) < 3:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv rename <source> <target>' )")
            sys.exit(1)
            
        if not os.access(PATH_VENVS, os.W_OK):
            logger.error("Can not rename a virtual environment in %s.\nPermission denied." % PATH_VENVS)
            sys.exit(1)
        
        source_dir = os.path.join(self._workon_home, args[1])
        target_dir = os.path.join(self._workon_home, args[2])
        
        if not os.path.isdir(source_dir):
            logger.error('%s does not exist.' % source_dir)
            
        if os.path.isdir(target_dir):
            logger.error('Can not overwrite %s.' % target_dir)
            
        os.rename(source_dir, target_dir)
    
    def run_command_create(self, options, args):
        if not os.access(PATH_VENVS, os.W_OK):
            logger.error("Can not create a virtual environment in %s.\nPermission denied." % PATH_VENVS)
            sys.exit(1)

        virtualenv_options = []
        if options.no_site_packages:
            virtualenv_options.append('--no-site-packages')
        
        for arg in args[1:]:
            target_dir = os.path.join(self._workon_home, arg)
            logger.info("Creating `%s` environment into %s" % (arg, self._workon_home))
            # make command
            cmd = [self._py, self._venv, '-p', self._target_py]
            cmd.extend(virtualenv_options)
            cmd.append(target_dir)
            # create environment
            s = Subprocess(verbose=True)
            s.call(cmd)
        
    def run_command_delete(self, options, args):
        for arg in args[1:]:
            target_dir = os.path.join(self._workon_home, arg)
            if not os.path.isdir(target_dir):
                logger.error('%s already does not exist.' % target_dir)
            else:
                if not os.access(target_dir, os.W_OK):
                    logger.error("Can not delete %s.\nPermission denied." % target_dir)
                    continue
                logger.info('Deleting `%s` environment in %s' % (arg, self._workon_home))
                # make command
                rm_r(target_dir)
                
    def run_command_print_activate(self, options, args):
        if len(args) < 2:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv print_activate <project>' )")
            sys.exit(1)
        
        activate = os.path.join(self._workon_home, args[1], 'bin', 'activate')
        if not os.path.exists(activate):
            logger.error('`%s` environment already does not exist. Try `pythonbrew venv create %s`.' % (args[1], args[1]))
            sys.exit(1)
            
        logger.log(activate)
            
    
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
                        if os.path.isdir(os.path.join(workon_home, d)):
                            logger.log(d)
        else:
            logger.log("# virtualenv for %(pkgname)s (found in %(workon_home)s)" % {'pkgname': self._pkgname, 'workon_home': self._workon_home})
            if os.path.isdir(self._workon_home):
                for d in sorted(os.listdir(self._workon_home)):
                    if os.path.isdir(os.path.join(self._workon_home, d)):
                        logger.log(d)
    
    def _write(self, src):
        fp = open(PATH_HOME_ETC_VENV, 'w')
        fp.write(src)
        fp.close()
    
VenvCommand()
