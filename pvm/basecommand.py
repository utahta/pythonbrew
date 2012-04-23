import os
import sys
import re
from optparse import OptionParser
from pvm import commands

command_dict = {}

class Command(object):
    name = None
    usage = None
    summary = ""
    
    def __init__(self):
        self.parser = OptionParser(usage=self.usage,
                                   prog='%s %s' % ("pvm", self.name))
        command_dict[self.name] = self
        
    def run(self, args):
        options, args = self.parser.parse_args(args)
        self.run_command(options, args)

def load_command(name):
    full_name = 'pvm.commands.%s' % name
    if full_name in sys.modules:
        return
    try:
        __import__(full_name)
    except ImportError:
        pass

def load_all_commands():
    for name in command_names():
        load_command(name)

def command_names():
    return [path[:-3] for path in os.listdir(commands.__path__[0]) if not re.match("(__init__\.py$|.*\.pyc$)", path)]
