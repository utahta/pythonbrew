from pvm.basecommand import Command
from pvm.define import VERSION
from pvm.log import logger

class VersionCommand(Command):
    name = "version"
    usage = "%prog"
    summary = "Show version"
    
    def run_command(self, options, args):
        logger.log(VERSION)

VersionCommand()
