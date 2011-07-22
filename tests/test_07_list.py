class ListOptions(object):
    all_versions = False
    known = False

def test_list():
    from pythonbrew.commands.list import ListCommand
    c = ListCommand()
    c.run_command(ListOptions(), None)
