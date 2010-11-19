import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import off, symlink, Package
from pythonbrew.log import logger

class SwitchCommand(Command):
    name = "switch"
    usage = "%prog VERSION"
    summary = "Switch to the given version"
    
    def run_command(self, options, args):
        if not args:
            logger.info("Unrecognized command line argument: argument not found.")
            sys.exit(1)
        pkg = Package(args[0])
        pkgname = pkg.name
        pkgdir = os.path.join(PATH_PYTHONS, pkgname)
        if not os.path.isdir(pkgdir):
            logger.info("`%s` is not installed." % pkgname)
            sys.exit(1)
        self._switch_dir(pkgdir)
        logger.info("Switched to %s" % pkgname)
    
    def _switch_dir(self, pkgdir):
        off()
        symlink(pkgdir, "%s/current" % PATH_PYTHONS)
        
        # I want better code...
        current_bin = os.path.join(PATH_PYTHONS,'current','bin')
        if not os.path.isfile(os.path.join(current_bin,"python")):
            if os.path.isfile(os.path.join(current_bin,"python3")):
                symlink(os.path.realpath("%s/python3" % current_bin), os.path.join(PATH_BIN,"python"))
            elif os.path.isfile(os.path.join(current_bin,"python3.0")):
                symlink(os.path.realpath("%s/python3.0" % current_bin), os.path.join(PATH_BIN,"python"))

SwitchCommand()
