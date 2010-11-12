import os
import sys
import re
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
            logger.error("Unrecognized command line argument: argument not found.")
            sys.exit(1)
        pkg = Package(args[0])
        pkgname = pkg.name
        pkgdir = "%s/%s" % (PATH_PYTHONS, pkgname)
        if not os.path.isdir(pkgdir):
            logger.error("`%s` is not installed." % pkgname)
            sys.exit(1)
        self._switch_dir(pkgdir)
        logger.info("Switched to %s" % pkgname)
    
    def _switch_dir(self, pkgdir):
        off()
        symlink(pkgdir, "%s/current" % PATH_PYTHONS)
        for root, dirs, files in os.walk("%s/current/bin/" % PATH_PYTHONS):
            for f in files:
                symlink("%s%s" % (root, f), "%s/%s" % (PATH_BIN, f))
            break
        # I want better code
        if not os.path.isfile("%s/python" % PATH_BIN):
            if os.path.isfile("%s/python3" % PATH_BIN):
                symlink(os.path.realpath("%s/python3" % PATH_BIN), "%s/python" % PATH_BIN)
            elif os.path.isfile("%s/python3.0" % PATH_BIN):
                symlink(os.path.realpath("%s/python3.0" % PATH_BIN), "%s/python" % PATH_BIN)

SwitchCommand()
