import os
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import off, rm_r, Package, get_current_python_path, unlink
from pythonbrew.log import logger

class UninstallCommand(Command):
    name = "uninstall"
    usage = "%prog VERSION"
    summary = "Uninstall the given version of python"
    
    def run_command(self, options, args):
        if args:
            # Uninstall pythons
            for arg in args:
                pkg = Package(arg)
                pkgname = pkg.name
                pkgpath = os.path.join(PATH_PYTHONS, pkgname)
                if not os.path.isdir(pkgpath):
                    logger.info("`%s` is not installed." % pkgname)
                    continue
                if get_current_python_path() == os.path.join(pkgpath,'bin','python'):
                    off()
                for d in os.listdir(PATH_BIN):
                    # remove symlink
                    path = os.path.join(PATH_BIN, d)
                    if os.path.islink(path):
                        basename = os.path.basename(os.path.realpath(path))
                        tgtpath = os.path.join(pkgpath, 'bin', basename)
                        if os.path.isfile(tgtpath) and os.path.samefile(path, tgtpath):
                            unlink(path)
                rm_r(pkgpath)
        else:
            self.parser.print_help()

UninstallCommand()
