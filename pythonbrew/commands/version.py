from pythonbrew.basecommand import Command
from pythonbrew.define import VERSION
from pythonbrew.log import logger

class VersionCommand(Command):
    name = "version"
    usage = "%prog"
    summary = "Show version"
    
    def run_command(self, options, args):
        logger.log(VERSION)

VersionCommand()
