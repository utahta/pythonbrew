from pythonbrew.basecommand import Command
from pythonbrew.log import logger

class CleanCommand(Command):
    name = "clean"
    usage = "%prog"
    summary = "Remove stale source folders and archives"
    
    def run_command(self, options, args):
        logger.info('\nDEPRECATION WARNING: `pythonbrew clean` has been renamed. Please run `pythonbrew cleanup` instead.\n')
        
CleanCommand()
