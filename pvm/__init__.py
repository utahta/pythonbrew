import sys
import os
from pvm.basecommand import command_dict, load_all_commands
from pvm.baseparser import parser
from pvm.log import logger
from pvm.define import PATH_HOME_ETC
from pvm.util import makedirs

def init_home():
    if not os.path.isdir(PATH_HOME_ETC):
        makedirs(PATH_HOME_ETC)

def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help'] # as default
    
    init_home()
    load_all_commands()
    command = args[0].lower()
    if command not in command_dict:
        parser.error("Unknown command: `%s`" % command)
        return
    command = command_dict[command]
    command.run(args[1:])
