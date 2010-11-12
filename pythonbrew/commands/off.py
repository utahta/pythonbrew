from pythonbrew.basecommand import Command
from pythonbrew.util import off

class OffCommand(Command):
    name = "off"
    usage = "%prog"
    summary = "Disable pythonbrew"
    
    def run_command(self, options, args):
        off()

OffCommand()
