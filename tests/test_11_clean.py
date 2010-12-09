def test_clean():
    from pythonbrew.commands.clean import CleanCommand
    c = CleanCommand()
    c.run_command(None, None)
