def test_version():
    from pythonbrew.commands.version import VersionCommand
    c = VersionCommand()
    c.run_command(None, None)
