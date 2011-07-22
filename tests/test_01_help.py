def test_help():
    from pythonbrew.commands.help import HelpCommand
    c = HelpCommand()
    c.run_command(None, None)
