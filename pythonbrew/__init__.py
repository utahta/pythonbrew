import sys
from pythonbrew.basecommand import command_dict, load_all_commands
from pythonbrew.baseparser import parser
from pythonbrew.log import logger

def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help'] # as default
    
    load_all_commands()
    command = args[0].lower()
    if command not in command_dict:
        if command == 'clean':
            # note: for some time
            logger.info('\nDEPRECATION WARNING: `pythonbrew clean` has been renamed. Please run `pythonbrew cleanup` instead.\n')
            return
        parser.error("Unknown command: `%s`" % command)
        return
    command = command_dict[command]
    command.run(args[1:])
