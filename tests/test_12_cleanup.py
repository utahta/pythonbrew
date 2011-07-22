def test_clean():
    from pythonbrew.commands.cleanup import CleanupCommand
    c = CleanupCommand()
    c.run_command(None, None)
