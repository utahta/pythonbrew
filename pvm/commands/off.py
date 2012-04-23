from pvm.basecommand import Command
from pvm.util import off

class OffCommand(Command):
    name = "off"
    usage = "%prog"
    summary = "Disable pvm"
    
    def run_command(self, options, args):
        off()

OffCommand()
