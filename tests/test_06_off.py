def test_off():
    from pythonbrew.commands.off import OffCommand
    c = OffCommand()
    c.run_command(None, None)
