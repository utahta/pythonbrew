import os
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_BIN
from pythonbrew.util import Package, symlink, unlink

class SymlinkCommand(Command):
    name = "symlink"
    usage = "%prog"
    summary = "Create/Remove a symbolic link to python"
    
    def __init__(self):
        super(SymlinkCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="pythons",
            action="append",
            default=[],
            help="Using specified python versions."
        )
        self.parser.add_option(
            "-r", "--remove",
            dest="remove",
            action="store_true",
            default=False,
            help="Remove a symbolic link."
        )
    
    def run_command(self, options, args):
        pythons = self._get_pythons(options.pythons)
        for python in pythons:
            version = Package(python).version
            src = os.path.join(PATH_PYTHONS, python, 'bin', 'python')
            dst = os.path.join(PATH_BIN, 'py%s' % (version))
            if options.remove:
                unlink(dst)
            else:
                symlink(src, dst)
    
    def _get_pythons(self, _pythons):
        pythons = [Package(p).name for p in _pythons]
        return [d for d in sorted(os.listdir(PATH_PYTHONS)) 
                if not pythons or d in pythons]

SymlinkCommand()
