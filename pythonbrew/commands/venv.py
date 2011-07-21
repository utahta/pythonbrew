import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS, PATH_ETC_VENV
from pythonbrew.util import Subprocess, Package,\
    is_installed, get_installed_pythons_pkgname, get_using_python_pkgname
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
        self.parser.add_option(
            "-a", "--all",
            dest="all",
            action='store_true',
            default=False,
            help="Show the all python environments.",
            metavar='VERSION'
        )
        self.template_env = """export VIRTUALENVWRAPPER_PYTHON=%(venv_py)s
export VIRTUALENVWRAPPER_VIRTUALENV=%(venv_venv)s
export WORKON_HOME=%(workon_home)s
export VIRTUALENVWRAPPER_HOOK_DIR=%(workon_home)s
export VIRTUALENVWRAPPER_LOG_DIR=%(workon_home)s
source %(venv_sh)s
"""
    
    def run_command(self, options, args):
        if not args:
            logger.error('Unrecognized command line argument: ( see: \'pythonbrew help venv\' )')
            sys.exit(1)
        cmd = args[0]
        if not cmd in ('create', 'delete', 'use', 'list'):
            logger.error('Unrecognized command line argument: ( see: \'pythonbrew help venv\' )')
            sys.exit(1)
        
        # find python2
        venv_pkgname = None
        for pkgname in reversed(get_installed_pythons_pkgname()):
            # virtualenvwrapper require Python2
            venv_pkgver = Package(pkgname).version
            if venv_pkgver >= '2.4' and venv_pkgver < '3':
                venv_pkgname = pkgname
                break
        if not venv_pkgname:
            logger.error('Can not create virtual environment before installing a python2.  Try \'pythonbrew install <python2.4 - 2.7>\'.')
            sys.exit(1)
        venv_dir = os.path.join(PATH_PYTHONS, venv_pkgname)
        venv_bin = os.path.join(venv_dir, 'bin')
        
        # target python interpreter
        if options.python:
            pkgname = Package(options.python).name
            if not is_installed(pkgname):
                logger.error('%s is not installed.' % pkgname)
                sys.exit(1)
        else:
            pkgname = get_using_python_pkgname()
            if not pkgname:
                logger.error('Can not use venv command before using a python.  Try \'pythonbrew switch <some python>\'.')
                sys.exit(1)
        self._pkgname = pkgname
        self._target_py = os.path.join(PATH_PYTHONS, pkgname, 'bin', 'python')
        self._workon_home = os.path.join(PATH_VENVS, pkgname)
        self._venv_py = os.path.join(venv_bin, 'python')
        self._venv_venv = os.path.join(venv_bin, 'virtualenv')
        self._venv_sh = os.path.join(venv_bin, 'virtualenvwrapper.sh')
        
        # has virtualenv & virtualenvwrapper?
        if not self._venv_venv or not self._venv_sh:
            logger.info('Installing virtualenv into %s' % venv_dir)
            s = Subprocess(verbose=True)
            s.shell('%s %s %s' % (os.path.join(venv_bin,'pip'), 'install', 'virtualenvwrapper'))
        
        # Create a shell script
        try:
            self.__getattribute__('run_command_%s' % cmd)(options, args)
        except:
            logger.error('`%s` command not found.' % cmd)
            sys.exit(1)
    
    def run_command_create(self, options, args):
        output = [self.template_env % {'venv_py': self._venv_py,
                                       'venv_venv': self._venv_venv,
                                       'workon_home': self._workon_home,
                                       'venv_sh': self._venv_sh}]
        for arg in args[1:]:
            output.append("""echo '# Create `%(arg)s` environment into %(workon_home)s'
mkvirtualenv -p '%(target_py)s' '%(arg)s'
""" % {'arg': arg,
       'workon_home': self._workon_home,
       'target_py': self._target_py})
        self._write(''.join(output))
        
    def run_command_delete(self, options, args):
        output = [self.template_env % {'venv_py': self._venv_py, 
                                       'venv_venv': self._venv_venv,
                                       'workon_home': self._workon_home,
                                       'venv_sh': self._venv_sh}]
        for arg in args[1:]:
            output.append("""echo '# Delete `%(arg)s` environment in %(workon_home)s'
rmvirtualenv '%(arg)s'
""" % {'arg': arg,
       'workon_home': self._workon_home})
        self._write(''.join(output))
    
    def run_command_use(self, options, args):
        if len(args) < 2:
            logger.error("Unrecognized command line argument: ( 'pythonbrew venv use <project>' )")
            sys.exit(1)
        template = self.template_env + """echo '# Using `%(arg)s` environment (found in %(workon_home)s)'
echo '# To leave an environment, simply run `deactivate`'
workon '%(arg)s'
"""
        self._write(template % {'venv_py': self._venv_py, 
                                'venv_venv': self._venv_venv,
                                'workon_home': self._workon_home,
                                'venv_sh': self._venv_sh,
                                'arg': args[1]})
    
    def run_command_list(self, options, args):
        template = self.template_env + """echo '# virtualenv for %(pkgname)s (found in %(workon_home)s)'
workon
"""
        if options.all:
            output = []
            for pkgname in get_installed_pythons_pkgname():
                workon_home = os.path.join(PATH_VENVS, pkgname)
                output.append(template % {'venv_py': self._venv_py,
                                          'venv_venv': self._venv_venv,
                                          'workon_home': workon_home,
                                          'venv_sh': self._venv_sh,
                                          'pkgname': pkgname})
            self._write(''.join(output))
        else:
            self._write(template % {'venv_py': self._venv_py, 
                                    'venv_venv': self._venv_venv,
                                    'workon_home': self._workon_home,
                                    'venv_sh': self._venv_sh,
                                    'pkgname': self._pkgname})
    
    def _write(self, src):
        fp = open(PATH_ETC_VENV, 'w')
        fp.write(src)
        fp.close()
    
VenvCommand()
