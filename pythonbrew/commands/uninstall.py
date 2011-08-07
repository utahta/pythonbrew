import os
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN, PATH_VENVS
from pythonbrew.util import off, rm_r, Package, get_using_python_pkgname, unlink,\
    is_installed
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
                venvpath = os.path.join(PATH_VENVS, pkgname)
                if not is_installed(pkgname):
                    logger.error("`%s` is not installed." % pkgname)
                    continue
                if get_using_python_pkgname() == pkgname:
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
                rm_r(venvpath)
        else:
            self.parser.print_help()

UninstallCommand()
