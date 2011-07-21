class VenvOptions(object):
    python = '2.6.6'
    all = False

def test_venv():
    from pythonbrew.commands.venv import VenvCommand
    c = VenvCommand()
    c.run_command(VenvOptions(), ['create', 'aaa'])
    c.run_command(VenvOptions(), ['list'])
    c.run_command(VenvOptions(), ['use', 'aaa'])
    c.run_command(VenvOptions(), ['delete', 'aaa'])
