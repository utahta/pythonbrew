import sys
from pythonbrew.basecommand import command_dict, load_all_commands
from pythonbrew.baseparser import parser

def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help'] # as default
    
    load_all_commands()
    command = args[0].lower()
    if command not in command_dict:
        parser.error("Unknown command: `%s`" % command)
        return
    command = command_dict[command]
    command.run(args)
