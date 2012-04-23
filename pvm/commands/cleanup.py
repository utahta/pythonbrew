import os
from pvm.basecommand import Command
from pvm.define import PATH_BUILD, PATH_DISTS
from pvm.util import rm_r

class CleanupCommand(Command):
    name = "cleanup"
    usage = "%prog"
    summary = "Remove stale source folders and archives"
    
    def run_command(self, options, args):
        self._cleanup(PATH_BUILD)
        self._cleanup(PATH_DISTS)
        
    def _cleanup(self, root):
        for dir in os.listdir(root):
            rm_r(os.path.join(root, dir))

CleanupCommand()
