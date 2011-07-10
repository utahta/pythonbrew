from pythonbrew.basecommand import Command, command_dict
from pythonbrew.baseparser import parser
from pythonbrew.log import logger

class HelpCommand(Command):
    name = "help"
    usage = "%prog [COMMAND]"
    summary = "Show available commands"
    
    def run_command(self, options, args):
        if args:
            command = args[0]
            if command not in command_dict:
                parser.error("Unknown command: `%s`" % command)
                return
            command = command_dict[command]
            command.parser.print_help()
            return
        parser.print_help()
        logger.info("\nCommands available:")
        commands = [command_dict[key] for key in sorted(command_dict.keys())]
        for command in commands:
            logger.info("  %s: %s" % (command.name, command.summary))
        logger.info("\nFurther Instructions:")
        logger.info("  https://github.com/utahta/pythonbrew")

HelpCommand()
