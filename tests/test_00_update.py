class UpdateOptions(object):
    master = False
    develop = False
    config = False
    force = False

def test_update():
    from pythonbrew.commands.update import UpdateCommand
    c = UpdateCommand()
    c.run_command(UpdateOptions(), None)
    