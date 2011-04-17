import os
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import Package, symlink, unlink

class SymlinkCommand(Command):
    name = "symlink"
    usage = "%prog"
    summary = "Create/Remove a symbolic link"
    
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
            "-b", "--bin",
            dest="bin",
            action="append",
            default=[],
            help="Create a symbolic link to the specified script name in bin directory."
        )
    
    def run_command(self, options, args):
        pythons = self._get_pythons(options.pythons)
        for pkgname in pythons:
            if options.remove:
                for bin in os.listdir(PATH_BIN):
                    path = os.path.join(PATH_BIN, bin)
                    if os.path.islink(path):
                        unlink(path)
            else:
                self._symlink('python', 'py', pkgname)
                for bin in options.bin:
                    self._symlink(bin, bin, pkgname)
                    
    def _symlink(self, srcbin, dstbin, pkgname):
        """Create the symlink
        """
        version = Package(pkgname).version
        src = os.path.join(PATH_PYTHONS, pkgname, 'bin', srcbin)
        dst = os.path.join(PATH_BIN, '%s%s' % (dstbin, version))
        symlink(src, dst)
    
    def _get_pythons(self, _pythons):
        """Get the installed python versions. 
        """
        pythons = [Package(p).name for p in _pythons]
        return [d for d in sorted(os.listdir(PATH_PYTHONS)) 
                if not pythons or d in pythons]

SymlinkCommand()
