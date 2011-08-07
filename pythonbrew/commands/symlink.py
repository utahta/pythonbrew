import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN, PATH_VENVS
from pythonbrew.util import Package, symlink, unlink, get_using_python_pkgname,\
    is_installed
from pythonbrew.log import logger

class SymlinkCommand(Command):
    name = "symlink"
    usage = "%prog [OPTIONS] [SCRIPT]"
    summary = "Create/Remove a symbolic link on your $PATH"
    
    def __init__(self):
        super(SymlinkCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="pythons",
            action="append",
            default=[],
            help="Use the specified python version.",
            metavar='VERSION'
        )
        self.parser.add_option(
            "-r", "--remove",
            dest="remove",
            action="store_true",
            default=False,
            help="Remove the all symbolic link."
        )
        self.parser.add_option(
            "-d", "--default",
            dest="default",
            default=None,
            help="Use as default the specified python version."
        )
        self.parser.add_option(
            "-v", "--venv",
            dest="venv",
            default=None,
            help="Use the virtual environment python."
        )
    
    def run_command(self, options, args):
        if options.default:
            # create only one instance as default of an application.
            pythons = self._get_pythons([options.default])
            for pkgname in pythons:
                if args:
                    bin = args[0]
                    self._symlink(bin, bin, pkgname)
                else:
                    self._symlink('python', 'py', pkgname)
        elif options.venv:
            if options.pythons:
                pkgname = Package(options.pythons[0]).name
            else:
                pkgname = get_using_python_pkgname()
            if not is_installed(pkgname):
                logger.error('`%s` is not installed.')
                sys.exit(1)
            
            venv_pkgdir = os.path.join(PATH_VENVS, pkgname)
            venv_dir = os.path.join(venv_pkgdir, options.venv)
            if not os.path.isdir(venv_dir):
                logger.error("`%s` environment was not found in %s." % (options.venv, venv_pkgdir))
                sys.exit(1)
            pkg = Package(pkgname)
            if args:
                bin = args[0]
                dstbin = '%s%s-%s' % (bin, pkg.version, options.venv)
                self._symlink(bin, dstbin, pkgname)
            else:
                dstbin = 'py%s-%s' % (pkg.version, options.venv)
                self._symlink('python', dstbin, pkgname)
        else:
            pythons = self._get_pythons(options.pythons)
            for pkgname in pythons:
                if options.remove:
                    # remove symlinks
                    for bin in os.listdir(PATH_BIN):
                        path = os.path.join(PATH_BIN, bin)
                        if os.path.islink(path):
                            unlink(path)
                else:
                    # create symlinks
                    if args:
                        bin = args[0]
                        self._symlink_version_suffix(bin, bin, pkgname)
                    else:
                        self._symlink_version_suffix('python', 'py', pkgname)
                    
    def _symlink_version_suffix(self, srcbin, dstbin, pkgname):
        """Create a symlink. add version suffix.
        """
        version = Package(pkgname).version
        dstbin = '%s%s' % (dstbin, version)
        self._symlink(srcbin, dstbin, pkgname)
    
    def _symlink(self, srcbin, dstbin, pkgname):
        """Create a symlink.
        """
        src = os.path.join(PATH_PYTHONS, pkgname, 'bin', srcbin)
        dst = os.path.join(PATH_BIN, dstbin)
        if os.path.isfile(src):
            symlink(src, dst)
        else:
            logger.error("%s was not found in your path." % src)
    
    def _get_pythons(self, _pythons):
        """Get the installed python versions list.
        """
        pythons = [Package(p).name for p in _pythons]
        return [d for d in sorted(os.listdir(PATH_PYTHONS)) 
                if not pythons or d in pythons]

SymlinkCommand()
