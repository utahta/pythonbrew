import os
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_BUILD, PATH_DISTS
from pythonbrew.util import rm_r

class CleanCommand(Command):
    name = "clean"
    usage = "%prog"
    summary = "Remove stale source folders and archives"
    
    def run_command(self, options, args):
        self._clean(PATH_BUILD)
        self._clean(PATH_DISTS)
        
    def _clean(self, root):
        for dir in os.listdir(root):
            rm_r(os.path.join(root, dir))

CleanCommand()
