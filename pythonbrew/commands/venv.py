import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS, PATH_HOME_ETC_VENV,\
    PATH_ETC, VIRTUALENV_DLSITE, PATH_DISTS, VIRTUALENV_CLONE_DLSITE
from pythonbrew.util import Package, \
    is_installed, get_installed_pythons_pkgname, get_using_python_pkgname,\
    untar_file, Subprocess, rm_r
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader

class VenvCommand(Command):
    name = "venv"
    usage = "%prog [create|use|delete|list|clone|rename|print_activate] [project]"
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
            "-g", "--system-site-packages",
            dest="system_site_packages",
            action='store_true',
            default=False,
            help="Give access to the global site-packages dir to the virtual environment.",
        )
        self._venv_dir = os.path.join(PATH_ETC, 'virtualenv')
        self._venv = os.path.join(self._venv_dir, 'virtualenv.py')
        self._venv_clone_dir = os.path.join(PATH_ETC, 'virtualenv-clone')
        self._venv_clone = os.path.join(self._venv_clone_dir, 'clonevirtualenv.py')
        self._clear()

    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        cmd = args[0]
        if not cmd in ('init', 'create', 'delete', 'use', 'list', 'clone', 'rename', 'print_activate'):
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
            pkgname = get_using_python_pkgname()

        self._pkgname = pkgname
        if self._pkgname:
            self._target_py = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')
            self._workon_home = os.path.join(PATH_VENVS, pkgname)
            self._py = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')

        # is already installed virtualenv?
        if not os.path.exists(self._venv) or not os.path.exists(self._venv_clone):
            self.run_command_init()

        # Create a shell script
        self.__getattribute__('run_command_%s' % cmd)(options, args)

    def run_command_init(self):
        if os.path.exists(self._venv):
            logger.info('Remove virtualenv. (%s)' % self._venv_dir)
            rm_r(self._venv_dir)
        if os.path.exists(self._venv_clone):
            logger.info('Remove virtualenv-clone. (%s)' % self._venv_clone_dir)
            rm_r(self._venv_clone_dir)
        if not os.access(PATH_DISTS, os.W_OK):
            logger.error("Can not initialize venv command: Permission denied.")
            sys.exit(1)
        d = Downloader()
        download_file = os.path.join(PATH_DISTS, 'virtualenv.tar.gz')
        d.download('virtualenv.tar.gz', VIRTUALENV_DLSITE, download_file)
        logger.info('Extracting virtualenv into %s' % self._venv_dir)
        untar_file(download_file, self._venv_dir)
        download_file = os.path.join(PATH_DISTS, 'virtualenv-clone.tar.gz')
        d.download('virtualenv-clone.tar.gz', VIRTUALENV_CLONE_DLSITE, download_file)
        logger.info('Extracting virtualenv-clone into %s' % self._venv_clone_dir)
        untar_file(download_file, self._venv_clone_dir)

    def run_command_create(self, options, args):
        if not os.access(PATH_VENVS, os.W_OK):
            logger.error("Can not create a virtual environment in %s.\nPermission denied." % PATH_VENVS)
            sys.exit(1)
        if not self._pkgname:
            logger.error("Unknown python version: ( 'pythonbrew venv create <project> -p VERSION' )")
            sys.exit(1)

        virtualenv_options = []
        if options.system_site_packages:
            virtualenv_options.append('--system-site-packages')

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
        if not self._pkgname:
            logger.error("Unknown python version: ( 'pythonbrew venv delete <project> -p VERSION' )")
            sys.exit(1)

        for arg in args[1:]:
            target_dir = os.path.join(self._workon_home, arg)
            if not os.path.isdir(target_dir):
                logger.error('%s does not exist.' % target_dir)
            else:
                if not os.access(target_dir, os.W_OK):
                    logger.error("Can not delete %s.\nPermission denied." % target_dir)
                    continue
                logger.info('Deleting `%s` environment in %s' % (arg, self._workon_home))
                # make command
                rm_r(target_dir)

    def run_command_use(self, options, args):
        if len(args) < 2:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv use <project>' )")
            sys.exit(1)

        workon_home = None
        activate = None
        if self._pkgname:
            workon_home = self._workon_home
            activate = os.path.join(workon_home, args[1], 'bin', 'activate')
        else:
            for pkgname in get_installed_pythons_pkgname():
                workon_home = os.path.join(PATH_VENVS, pkgname)
                if os.path.isdir(workon_home):
                    if len([d for d in os.listdir(workon_home) if d == args[1]]) > 0:
                        activate = os.path.join(workon_home, args[1], 'bin', 'activate')
                        break
        if not activate or not os.path.exists(activate):
            logger.error('`%s` environment does not exist. Try `pythonbrew venv create %s`.' % (args[1], args[1]))
            sys.exit(1)

        self._write("""\
echo '# Using `%(arg)s` environment (found in %(workon_home)s)'
echo '# To leave an environment, simply run `deactivate`'
source '%(activate)s'
""" % {'arg': args[1], 'workon_home': workon_home, 'activate': activate})

    def run_command_list(self, options, args):
        if options.python:
            pkgname = Package(options.python).name
            workon_home = os.path.join(PATH_VENVS, pkgname)
            if pkgname == self._pkgname:
                logger.log("%s (*)" % pkgname)
            else:
                logger.log("%s" % pkgname)
            if os.path.isdir(workon_home):
                for d in sorted(os.listdir(workon_home)):
                    if os.path.isdir(os.path.join(workon_home, d)):
                        logger.log("  %s" % d)
        else:
            for pkgname in get_installed_pythons_pkgname():
                workon_home = os.path.join(PATH_VENVS, pkgname)
                if os.path.isdir(workon_home):
                    dirs = os.listdir(workon_home)
                    if len(dirs) > 0:
                        if pkgname == self._pkgname:
                            logger.log("%s (*)" % pkgname)
                        else:
                            logger.log("%s" % pkgname)
                        for d in sorted(dirs):
                            if os.path.isdir(os.path.join(workon_home, d)):
                                logger.log("  %s" % d)

    def run_command_clone(self, options, args):
        if len(args) < 3:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv clone <source> <target>' )")
            sys.exit(1)
        if not os.access(PATH_VENVS, os.W_OK):
            logger.error("Can not clone a virtual environment in %s.\nPermission denied." % PATH_VENVS)
            sys.exit(1)
        if not self._pkgname:
            logger.error("Unknown python version: ( 'pythonbrew venv clone <source> <target> -p VERSION' )")
            sys.exit(1)

        source, target = args[1], args[2]
        source_dir = os.path.join(self._workon_home, source)
        target_dir = os.path.join(self._workon_home, target)

        if not os.path.isdir(source_dir):
            logger.error('%s does not exist.' % source_dir)
            sys.exit(1)

        if os.path.isdir(target_dir):
            logger.error('Can not overwrite %s.' % target_dir)
            sys.exit(1)

        logger.info("Cloning `%s` environment into `%s` on %s" % (source, target, self._workon_home))

        # Copies source to target
        cmd = [self._py, self._venv_clone, source_dir, target_dir]
        s = Subprocess()
        s.call(cmd)

    def run_command_rename(self, options, args):
        if len(args) < 3:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv rename <source> <target>' )")
            sys.exit(1)
        if not os.access(PATH_VENVS, os.W_OK):
            logger.error("Can not rename a virtual environment in %s.\nPermission denied." % PATH_VENVS)
            sys.exit(1)
        if not self._pkgname:
            logger.error("Unknown python version: ( 'pythonbrew venv rename <source> <target> -p VERSION' )")
            sys.exit(1)

        logger.info("Rename `%s` environment to `%s` on %s" % (args[1], args[2], self._workon_home))

        source, target = args[1], args[2]
        self.run_command_clone(options, ['clone', source, target])
        self.run_command_delete(options, ['delete', source])

    def run_command_print_activate(self, options, args):
        if len(args) < 2:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv print_activate <project>' )")
            sys.exit(1)
        if not self._pkgname:
            logger.error("Unknown python version: ( 'pythonbrew venv print_activate <project> -p VERSION' )")
            sys.exit(1)

        activate = os.path.join(self._workon_home, args[1], 'bin', 'activate')
        if not os.path.exists(activate):
            logger.error('`%s` environment already does not exist. Try `pythonbrew venv create %s`.' % (args[1], args[1]))
            sys.exit(1)

        logger.log(activate)

    def _clear(self):
        self._write("")

    def _write(self, src):
        fp = open(PATH_HOME_ETC_VENV, 'w')
        fp.write(src)
        fp.close()

VenvCommand()
